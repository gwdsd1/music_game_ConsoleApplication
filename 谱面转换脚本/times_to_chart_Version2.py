import math
import random

INPUT_TIMES = "onset_times.txt"   # 也可以改成 beat_times.txt
OUTPUT_CHART = "output.chart"

SONG_NAME = "yorushika_paddle"#这一部分是可以自己编辑不同曲目的
BPM = "100"          # 你不知道就先留 ?
OFFSET = 0.0       # 需要整体提前/延后时改这里，比如 -0.08 或 +0.05

# 难度/风格参数
FOUR_LANE_MAIN = [1, 2, 3, 4]  # D F J K
SPICE_LANES = [0, 5]           # 偶尔点缀 S/L
SPICE_PROB = 0.04              # 点缀概率（困难但偏四轨：建议 0~0.08）

MIN_GAP = 0.10                 # 最���间隔（秒），防止过密；困难可 0.08~0.12
ROUND_TO = 0.000001            # 6 位小数

def read_times(path):
    times = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                t = float(s)
                times.append(t)
            except ValueError:
                pass
    return sorted(times)

def dedupe_and_thin(times, min_gap):
    out = []
    last = -1e9
    for t in times:
        if t - last >= min_gap:
            out.append(t)
            last = t
    return out

def pick_lane(prev_lane, i):
    # 让手感“左右交替”一点，减少同一轨连打
    main = FOUR_LANE_MAIN[:]

    # 避免连续重复同一 lane
    if prev_lane in main and len(main) > 1:
        main.remove(prev_lane)

    # 低概率用 0/5 点缀
    if random.random() < SPICE_PROB:
        return random.choice(SPICE_LANES)

    # 简单的来回分配：在剩余 main 里选一个
    return main[i % len(main)]

def main():
    random.seed(7)  # 固定随机种子，保证可复现

    times = read_times(INPUT_TIMES)
    times = [round(t + OFFSET, 6) for t in times if t + OFFSET >= 0]
    times = dedupe_and_thin(times, MIN_GAP)

    lines = []
    lines.append(f"# Song: {SONG_NAME}")
    lines.append(f"# BPM: {BPM}")
    lines.append(f"# Offset: {OFFSET}")
    lines.append("")
    lines.append("# Format: time(seconds), lane(0-5)")
    lines.append("# Lanes: 0=S, 1=D, 2=F, 3=J, 4=K, 5=L")
    lines.append("")

    prev_lane = None
    for i, t in enumerate(times):
        lane = pick_lane(prev_lane, i)
        prev_lane = lane
        lines.append(f"{t:.6f}, {lane}")

    with open(OUTPUT_CHART, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("notes:", len(times))
    print("wrote", OUTPUT_CHART)

if __name__ == "__main__":
    main()