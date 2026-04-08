# Linux Memory Tuning for Large Test Workloads

Without tuning, Linux dev machines can suffer OOM kills, severe slowdown or desktop freezes under large memory-intensive
workloads (such as large parallel pytest suites). This guide permanently configures a machine to handle them more
gracefully.

It combines:

- `zram` — fast compressed swap in RAM
- disk swap — optional final fallback (mainly useful on lower-memory systems)
- kernel tuning — smoother behaviour under memory pressure

> **Note: all specific values in this guide (swap sizes, `PERCENT`, sysctl ratios) are tuned for a 16GB RAM machine.**
> See [Scaling to larger memory systems](#scaling-to-larger-memory-systems) at the end for suggested values for 32GB,
> 48GB, and 64GB machines.

The configuration for a 16GB RAM machine looks like this.

Note: Mermaid cannot automatically size boxes to exact memory proportions. The diagrams below show the right
relationships and approximate capacities, but they are not to scale.

```mermaid
flowchart LR
    subgraph RAM16[Physical RAM: 16GB total]
        SYS16[System working memory<br/>apps + cache]
        Z16[zram in RAM<br/>up to 12GB logical swap<br/>allocated on demand]
    end

    SYS16 -. memory pressure .-> Z16
    Z16 -->|zram full| D16[swap.img on disk<br/>24GB fallback]
```

For a 32GB RAM machine, use the same pattern with a smaller disk-swap fallback:

```mermaid
flowchart LR
    subgraph RAM32[Physical RAM: 32GB total]
        SYS32[System working memory<br/>apps + cache]
        Z32[zram in RAM<br/>up to 16GB logical swap<br/>allocated on demand]
    end

    SYS32 -. memory pressure .-> Z32
    Z32 -->|zram full| D32[swap.img on disk<br/>16GB fallback]
```

______________________________________________________________________

## Configure disk swap

Use these recommended disk swap sizes:

- **16GB RAM**: `24G` `/swap.img`
- **32GB RAM**: `16G` `/swap.img`
- **48GB RAM and above**: no disk swap (`0G`)

The commands below use the 16GB baseline (`24G`); adjust the `fallocate -l` value for other sizes, or skip this section
entirely when using `0G`.

Use `/swap.img` consistently in all commands and in `/etc/fstab`.

```bash
sudo swapoff /swap.img || true
sudo fallocate -l 24G /swap.img
sudo chmod 600 /swap.img
sudo mkswap /swap.img
sudo swapon /swap.img
```

Verify:

```bash
swapon --show
```

Ensure `/etc/fstab` contains:

```conf
/swap.img none swap sw 0 0
```

______________________________________________________________________

## Enable zram

Install:

```bash
sudo apt update
sudo apt install -y zram-tools
```

Edit config:

```bash
sudo nano /etc/default/zramswap
```

```conf
# zstd gives better compression at low CPU cost
ALGO=zstd

# Logical zram swap as a percentage of physical RAM
PERCENT=75

# Prefer zram over disk swap (higher number = higher priority)
PRIORITY=100
```

The config above is the 16GB baseline (`PERCENT=75`); for larger systems, set `PERCENT` from the scaling table.

Apply:

```bash
sudo swapoff -a
sudo systemctl restart zramswap
sudo swapon -a
```

Verify zram is active (and has higher priority if disk swap is enabled):

```bash
zramctl
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
```

Expected: if `/swap.img` is present, the zram entry has a higher `PRIO` value.

______________________________________________________________________

## Kernel tuning

Create a VM tuning `sysctl` file:

```bash
sudo nano /etc/sysctl.d/99-dev-memory.conf
```

```conf
# Prefer swap moderately early — good with fast zram-backed swap.
vm.swappiness = 30

# Keep filesystem cache longer for repeated test/build cycles.
vm.vfs_cache_pressure = 50

# Reduce large writeback bursts that cause stalls.
vm.dirty_background_ratio = 5
vm.dirty_ratio = 15

# Optimistic allocation — prevents failures in large Python workloads.
vm.overcommit_memory = 1
```

Apply:

```bash
sudo sysctl --system
```

______________________________________________________________________

## Scaling to larger memory systems

The rules of thumb used in this guide:

- **zram `PERCENT`**: set relative to physical RAM to make memory pressure explicit: `75` (16GB), `50` (32GB), `42`
  (48GB), `38` (64GB).
- Logical caps from `PERCENT` are approximate; validate expected behavior on your workload with `zramctl` under load.
- **Disk swap**: based on practical usage, use `24GB` on 16GB systems, `16GB` on 32GB systems, and `0GB` on 48GB+
  developer workstations.
- **Estimated zram compression ratio**: assume about `2.5:1` for planning (typical for mixed dev workloads; actual
  values vary by data). zram capacity is logical, but only the compressed backing consumes RAM. So the effective extra
  memory from zram is approximately `logical_zram * (1 - 1/ratio)`.
- **`vm.swappiness`**: keep at `30` for all sizes; zram is fast enough that early swapping is acceptable.
- **`vm.dirty_background_ratio` / `vm.dirty_ratio`**: scale down slightly on larger systems where writeback bursts can
  be proportionally larger.

| Setting                       | 16 GB  | 32 GB  | 48 GB  | 64 GB  |
| ----------------------------- | ------ | ------ | ------ | ------ |
| zram `PERCENT`                | 75     | 50     | 42     | 38     |
| zram logical cap              | ~12 GB | ~16 GB | ~20 GB | ~24 GB |
| Expected native RAM used\*\*  | ~11 GB | ~26 GB | ~40 GB | ~54 GB |
| Expected zram RAM used\*\*    | ~5 GB  | ~6 GB  | ~8 GB  | ~10 GB |
| Disk swap (`/swap.img`)       | 24 GB  | 16 GB  | 0 GB   | 0 GB   |
| Approx total logical memory\* | ~47 GB | ~58 GB | ~60 GB | ~78 GB |
| `vm.dirty_background_ratio`   | 5      | 4      | 3      | 3      |
| `vm.dirty_ratio`              | 15     | 12     | 10     | 10     |

All other settings (`ALGO=zstd`, `PRIORITY=100`, `vm.swappiness=30`, `vm.vfs_cache_pressure=50`,
`vm.overcommit_memory=1`) remain the same regardless of RAM size.

\* Uses an estimated zram compression ratio of `2.5:1`.

\*\* Split of physical RAM when zram is near its logical cap (`native RAM + zram RAM ~= physical RAM`).

______________________________________________________________________

## Notes

- Some swap usage is normal — do not treat swap activity as a problem
- Slightly increased CPU usage is expected from zram compression
- Tuned for **developer workloads**, not latency-critical or production systems
