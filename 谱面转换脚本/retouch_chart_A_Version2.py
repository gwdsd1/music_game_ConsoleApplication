import re

INPUT = "yorushika_paddle.chart"
OUTPUT = "yorushika_paddle_comfy_A.chart"

# A风格（鼓点为主、稳定踩点）推荐
MIN_GAP = 0.12  # seconds: 0.11~0.13 自己试
MAIN_LANES = [1, 2, 3, 4]  # D F J K only

time_lane_re = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*,\s*([0-5])\s*$")

def parse(lines):
    header = []
    notes = []
    seen_note = False
    for line in lines:
        m = time_lane_re.match(line)
        if m:
            seen_note = True
            notes.append((float(m.group(1)), int(m.group(2))))
        else:
            if not seen_note:
                header.append(line.rstrip("\n"))
    return header, notes

def thin(notes, min_gap):
    notes.sort(key=lambda x: x[0])
    out = []
    last_t = -1e9
    for t, lane in notes:
        if t - last_t >= min_gap:
            out.append((t, lane))
            last_t = t
    return out

def choose_lane(prev_lane, desired_lane):
    # 把 desired_lane 映射到 1-4 的“目标轨”
    if desired_lane not in MAIN_LANES:
        # 若原来是 0/5 等，尽量落在 prev 附近
        target = prev_lane if prev_lane in MAIN_LANES else 2
    else:
        target = desired_lane

    # 评分：更贴 target、更贴 prev（相邻移动）、避免重复
    best = None
    for ln in MAIN_LANES:
        score = 0.0
        score += abs(ln - target) * 1.0
        if prev_lane in MAIN_LANES:
            score += abs(ln - prev_lane) * 0.6  # 更强调相邻移动
        if ln == prev_lane:
            score += 2.0  # 强力避免同轨连打
        cand = (score, ln)
        if best is None or cand < best:
            best = cand
    return best[1]

def remap(notes):
    out = []
    prev_lane = None
    for t, lane in notes:
        nl = choose_lane(prev_lane, lane)
        out.append((t, nl))
        prev_lane = nl
    return out

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header, notes = parse(lines)
    notes0 = len(notes)

    notes = thin(notes, MIN_GAP)
    notes = remap(notes)

    out = []
    out.extend(header)
    out.append(f"# Retouched style=A (drum-focused, steady), MIN_GAP={MIN_GAP:.3f}s, lanes=1-4 only")
    out.append("")
    for t, lane in notes:
        out.append(f"{t:.6f}, {lane}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print("input notes:", notes0)
    print("output notes:", len(notes))
    print("wrote:", OUTPUT)

if __name__ == "__main__":
    main()