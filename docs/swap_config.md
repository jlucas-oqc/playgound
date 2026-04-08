# Linux Memory Tuning for Large Test Workloads

This document lays out a recommended swap configuration for Linux development machines, optimized for large memory
workloads like parallel test suites. The goal is to prevent OOM kills and severe slowdowns by using zram (compressed RAM
swap) as the primary swap mechanism, with optional disk swap as a fallback.

Using the 16GB baseline given here, the Qat pytest suite run at 4-way parallelism with a reasonable set of applications
(IDE, broswer with 4-5 tabs, slack etc.) can use over 24GB of memory completes successfully without OOM kills and with
only moderate swap usage. Without these tunings, the same workload frequently caused full system lockups.

The configuration is designed to be adaptable to larger RAM sizes (32GB/48GB/64GB) with simple adjustments.

It combines:

- `zram` — fast compressed swap in RAM
- disk swap — optional final fallback (mainly useful on lower-memory systems)
- kernel tuning — smoother behaviour under memory pressure

> **Note:** the commands given below use a 16GB baseline. Use
> [Scaling to larger memory systems](#scaling-to-larger-memory-systems) for 32GB/48GB/64GB values.

16GB baseline:

```mermaid
flowchart LR
    subgraph RAM16[Physical RAM: 16GB total]
        SYS16[System working memory<br/>apps + cache]
        Z16["12GB zram<br/>(uses up to ~4.8GB RAM)"]
    end

    SYS16 -. memory pressure .-> Z16
    Z16 -->|zram full| D16[swap.img on disk<br/>24GB fallback]
```

32GB example:

```mermaid
flowchart LR
    subgraph RAM32[Physical RAM: 32GB total]
        SYS32[System working memory<br/>apps + cache]
        Z32["24GB zram<br/>(uses up to ~9.6GB RAM)"]
    end

    SYS32 -. memory pressure .-> Z32
    Z32 -->|zram full| D32[swap.img on disk<br/>16GB fallback]
```

______________________________________________________________________

## Enable zram (compressed RAM swap)

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

Verify zram is active (and higher priority than disk swap, if present):

```bash
zramctl
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
```

Expected: if `/swap.img` is present, the zram entry has a higher `PRIO` value.

______________________________________________________________________

## Configure file-backed disk swap

Commands below use the 16GB baseline (`24G`); change `fallocate -l` for other sizes, or skip this section for `0G`.

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

## Kernel VM tuning

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

Based on practical QAT runs on 16GB/32GB, then extrapolated for larger RAM sizes. Validate with `zramctl` and `free`
under load.

### 1) Recommended settings

| RAM size | zram `PERCENT` | zram logical cap (approx) | Disk swap (`/swap.img`) | `vm.dirty_background_ratio` | `vm.dirty_ratio` |
| -------- | -------------- | ------------------------- | ----------------------- | --------------------------- | ---------------- |
| 16 GB    | 75             | ~12.0 GB                  | 24 GB                   | 5                           | 15               |
| 32 GB    | 75             | ~24.0 GB                  | 16 GB                   | 4                           | 12               |
| 48 GB    | 60             | ~28.8 GB                  | 0 GB                    | 3                           | 10               |
| 64 GB    | 50             | ~32.0 GB                  | 0 GB                    | 3                           | 10               |

All other settings (`ALGO=zstd`, `PRIORITY=100`, `vm.swappiness=30`, `vm.vfs_cache_pressure=50`,
`vm.overcommit_memory=1`) remain the same regardless of RAM size.

### 2) Expected behavior at high pressure (zram near cap)

Assumptions:

- zram compression ratio: `2.5:1`
- Expected zram RAM used ~= zram logical cap / 2.5
- Expected native RAM used ~= physical RAM - expected zram RAM used
- Logical memory resident in RAM ~= zram logical cap + expected native RAM used
- Approx total logical memory ~= zram logical cap + expected native RAM used + disk swap

| RAM size | Expected native RAM used | Expected zram RAM used | Logical memory resident in RAM | Approx total logical memory |
| -------- | ------------------------ | ---------------------- | ------------------------------ | --------------------------- |
| 16 GB    | ~11.2 GB                 | ~4.8 GB                | ~23.2 GB                       | ~47.2 GB                    |
| 32 GB    | ~22.4 GB                 | ~9.6 GB                | ~46.4 GB                       | ~62.4 GB                    |
| 48 GB    | ~36.5 GB                 | ~11.5 GB               | ~65.3 GB                       | ~65.3 GB                    |
| 64 GB    | ~51.2 GB                 | ~12.8 GB               | ~83.2 GB                       | ~83.2 GB                    |

Logical caps from `PERCENT` are approximate; validate expected behavior on your workload with `zramctl` under load.

______________________________________________________________________

## Notes

- Some swap usage is normal — do not treat swap activity as a problem
- Slightly increased CPU usage is expected from zram compression
- Tuned for **developer workloads**, not latency-critical or production systems
