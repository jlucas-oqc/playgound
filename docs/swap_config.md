# Linux Memory Tuning for Large Test Workloads

Without tuning, Linux dev machines can suffer OOM kills, severe slowdown or desktop freezes under large memory-intensive
workloads (such as large parallel pytest suites). This guide permanently configures a machine to handle them more
gracefully.

It combines:

- `zram` — fast compressed swap in RAM
- disk swap — large fallback safety net
- kernel tuning — smoother behaviour under memory pressure

Assuming a 16GB RAM machine, the configuration looks like this:

```mermaid
flowchart LR
    A[RAM\n16GB physical memory] -->|pressure builds| B[zram\ncompressed swap in RAM\nup to 12GB capacity\ndynamically sized]
    B -->|zram capacity reached| C[swap.img\ndisk swap\n24GB fallback]
```

______________________________________________________________________

## Configure disk swap

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

# Capacity headroom — not pre-allocated, only used under pressure
PERCENT=75

# Prefer zram over disk swap (higher number = higher priority)
PRIORITY=100
```

Apply:

```bash
sudo swapoff -a
sudo systemctl restart zramswap
sudo swapon -a
```

Verify zram is active and has higher priority than disk swap:

```bash
zramctl
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
```

Expected: the zram entry has a higher `PRIO` value than `/swap.img`.

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

## Notes

- Some swap usage is normal — do not treat swap activity as a problem
- Slightly increased CPU usage is expected from zram compression
- Tuned for **developer workloads**, not latency-critical or production systems
