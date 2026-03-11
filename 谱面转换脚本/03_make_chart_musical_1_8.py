import numpy as np
import random

SONG_NAME = "n-buna_because_summer_will_end"
BPM = "120"      # 注释字段，不影响你的 time-based chart
OFFSET = 0.0
OUT = "n-buna_because_summer_will_end_vocal_first_1-8.chart"

# 只用 1-4（偏四轨）
ALLOW_SPICE = False
SPICE_LANES = [0, 5]
SPICE_PROB = 0.03

# 鼓点“填空”距离阈值：离人声太近就不加鼓点，避免打断旋律
DRUM_FILL_MIN_DIST = 0.16

# 最终控密度（局部允许密）
MIN_GAP_NORMAL = 0.11
MIN_GAP_DENSE = 0.085
DENSE_TRIGGER = 0.165
DENSE_WINDOW = 5.5

RANDOM_SEED = 7

def read_times(path):
    xs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                xs.append(float(s))
    return np.array(sorted(xs), dtype=np.float64)

def build_grid_1_8(beat_times):
    grid = []
    for i in range(len(beat_times) - 1):
        b0 = beat_times[i]
        b1 = beat_times[i + 1]
        grid.append(b0)
        grid.append((b0 + b1) / 2.0)  # 1/8 midpoint
    grid.append(beat_times[-1])
    grid = np.unique(np.round(np.array(grid, dtype=np.float64), 6))
    return np.sort(grid)

def quantize(times, grid):
    idx = np.searchsorted(grid, times)
    out = []
    for t, j in zip(times, idx):
        cands = []
        if j > 0:
            cands.append(grid[j - 1])
        if j < len(grid):
            cands.append(grid[min(j, len(grid) - 1)])
        q = min(cands, key=lambda g: abs(g - t))
        out.append(q)
    out = np.unique(np.round(np.array(out, dtype=np.float64), 6))
    return np.sort(out)

def dynamic_thin(times):
    out = []
    last_keep = None
    prev_raw = None
    dense_until = -1e9

    for t in times:
        if prev_raw is not None and (t - prev_raw) < DENSE_TRIGGER:
            dense_until = max(dense_until, t + DENSE_WINDOW)
        prev_raw = t

        dense = (t <= dense_until)
        min_gap = MIN_GAP_DENSE if dense else MIN_GAP_NORMAL

        if last_keep is None or (t - last_keep) >= min_gap:
            out.append(t)
            last_keep = t

    return np.array(out, dtype=np.float64)

def merge_vocal_first(qv, qd, min_dist):
    """
    保留人声 qv；鼓点 qd 只在离最近人声足够远时加入。
    """
    merged = list(qv)
    for t in qd:
        j = np.searchsorted(qv, t)
        d = 1e9
        if j > 0:
            d = min(d, abs(t - qv[j - 1]))
        if j < len(qv):
            d = min(d, abs(t - qv[min(j, len(qv) - 1)]))
        if d >= min_dist:
            merged.append(t)
    merged = np.unique(np.round(np.array(merged, dtype=np.float64), 6))
    return np.sort(merged)

def assign_lanes_by_phrases(times):
    """
    简单“分句”走位：相邻时间差小的一串当一句，句内阶梯回摆，句间重置。
    """
    if len(times) == 0:
        return []

    phrase_gap = 0.35  # 超过这个间隔认为换一句（可调）
    patterns = [
        [2, 3, 4, 3, 2, 1, 2, 3],  # 回摆
        [2, 3, 2, 3, 4, 3, 2, 1],  # 更像“说唱/连音”
    ]

    out = []
    pat = patterns[0]
    step = 0
    prev_t = times[0]
    prev_lane = None

    for t in times:
        if (t - prev_t) > phrase_gap:
            # 新的一句：重置 pattern 和 step
            step = 0
            pat = patterns[(patterns.index(pat) + 1) % len(patterns)]
            prev_lane = None

        lane = pat[step % len(pat)]
        if prev_lane == lane:
            lane = 3 if lane == 2 else 2

        out.append((t, lane))
        prev_lane = lane
        prev_t = t
        step += 1

    return out

def main():
    random.seed(RANDOM_SEED)

    beats = read_times("beats.txt")
    drums = read_times("drum_events.txt")
    vocals = read_times("vocal_events.txt")

    grid = build_grid_1_8(beats)
    qd = quantize(drums, grid)
    qv = quantize(vocals, grid)

    merged = merge_vocal_first(qv, qd, DRUM_FILL_MIN_DIST)
    merged = dynamic_thin(merged)

    notes = assign_lanes_by_phrases(merged)

    lines = []
    lines.append(f"# Song: {SONG_NAME}")
    lines.append(f"# BPM: {BPM}")
    lines.append(f"# Offset: {OFFSET}")
    lines.append("")
    lines.append("# Format: time(seconds), lane(0-5)")
    lines.append("# Lanes: 0=S, 1=D, 2=F, 3=J, 4=K, 5=L")
    lines.append("")
    for t, lane in notes:
        if ALLOW_SPICE and (random.random() < SPICE_PROB):
            lane = random.choice(SPICE_LANES)
        lines.append(f"{t:.6f}, {lane}")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("grid points:", len(grid))
    print("vocal (quantized):", len(qv))
    print("drum (quantized):", len(qd))
    print("merged notes:", len(merged))
    print("wrote:", OUT)

if __name__ == "__main__":
    main()