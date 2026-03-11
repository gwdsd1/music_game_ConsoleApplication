import re
import random

INPUT = "yorushika_paddle.chart"
OUTPUT = "yorushika_paddle_comfy_B.chart"

# ---------- B 风格参数（你最可能需要调这几个） ----------
# 普通段最小间隔（越大越稳）
MIN_GAP_NORMAL = 0.115

# 密集段最小间隔（越小越爽越难）
MIN_GAP_DENSE = 0.085

# 如何判定“进入密集段”：当最近的间隔小于此值时，认为是高能/旋律碎点段
DENSE_TRIGGER_GAP = 0.160

# 密集段持续多久（秒）：检测到密集后，接下来这段时间使用 MIN_GAP_DENSE
DENSE_WINDOW_SEC = 6.0

# 偏四轨：主轨
MAIN_LANES = [1, 2, 3, 4]

# 是否允许 0/5 点缀（更爽但不那么“偏四轨”）
ALLOW_SPICE = False
SPICE_LANES = [0, 5]
SPICE_PROB = 0.03   # 3% 点缀

# 为了结果可复现
RANDOM_SEED = 7
# ---------------------------------------------------------

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
    notes.sort(key=lambda x: x[0])
    return header, notes

def is_dense_mode(prev_t, t):
    if prev_t is None:
        return False
    return (t - prev_t) < DENSE_TRIGGER_GAP

def thin_dynamic(notes):
    """
    动态去抖/控密度：
    - 普通段用 MIN_GAP_NORMAL
    - 触发密集后在 DENSE_WINDOW_SEC 内用 MIN_GAP_DENSE
    """
    out = []
    last_kept_t = None
    prev_raw_t = None

    dense_until = -1e9

    for t, lane in notes:
        # 检测密集触发
        if is_dense_mode(prev_raw_t, t):
            dense_until = max(dense_until, t + DENSE_WINDOW_SEC)
        prev_raw_t = t

        min_gap = MIN_GAP_DENSE if t <= dense_until else MIN_GAP_NORMAL

        if last_kept_t is None or (t - last_kept_t) >= min_gap:
            out.append((t, lane))
            last_kept_t = t

    return out

def pick_lane_normal(prev_lane, desired_lane):
    # 普通段：稳，尽量相邻移动，少大跳，避免同轨连打
    target = desired_lane if desired_lane in MAIN_LANES else (prev_lane if prev_lane in MAIN_LANES else 2)

    best = None
    for ln in MAIN_LANES:
        score = 0.0
        score += abs(ln - target) * 1.0
        if prev_lane in MAIN_LANES:
            score += abs(ln - prev_lane) * 0.55
        if ln == prev_lane:
            score += 1.6
        cand = (score, ln)
        if best is None or cand < best:
            best = cand
    return best[1]

def pick_lane_dense(prev_lane, step_idx):
    """
    密集段：更像旋律的“阶梯/回摆”走位
    用一个循环模式生成 lane：2-3-4-3-2-1-2-3...
    """
    pattern = [2, 3, 4, 3, 2, 1, 2, 3]
    ln = pattern[step_idx % len(pattern)]
    # 避免和 prev 完全重复（如果重复就向邻轨挪）
    if prev_lane == ln:
        ln = 3 if ln == 2 else 2
    return ln

def remap(notes):
    out = []
    prev_lane = None
    prev_t = None
    dense_until = -1e9
    dense_step = 0

    for t, lane in notes:
        # dense 检测（用相邻点间隔）
        if prev_t is not None and (t - prev_t) < DENSE_TRIGGER_GAP:
            dense_until = max(dense_until, t + DENSE_WINDOW_SEC)

        dense = (t <= dense_until)

        if dense:
            new_lane = pick_lane_dense(prev_lane, dense_step)
            dense_step += 1
        else:
            dense_step = 0
            new_lane = pick_lane_normal(prev_lane, lane)

        if ALLOW_SPICE and (random.random() < SPICE_PROB) and dense:
            new_lane = random.choice(SPICE_LANES)

        out.append((t, new_lane))
        prev_lane = new_lane
        prev_t = t

    return out

def main():
    random.seed(RANDOM_SEED)

    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header, notes = parse(lines)
    in_count = len(notes)

    notes = thin_dynamic(notes)
    notes = remap(notes)

    out = []
    out.extend(header)
    out.append("# Retouched style=B (melody-follow, locally dense)")
    out.append(f"# MIN_GAP_NORMAL: {MIN_GAP_NORMAL}")
    out.append(f"# MIN_GAP_DENSE: {MIN_GAP_DENSE}")
    out.append(f"# DENSE_TRIGGER_GAP: {DENSE_TRIGGER_GAP}")
    out.append(f"# DENSE_WINDOW_SEC: {DENSE_WINDOW_SEC}")
    out.append(f"# ALLOW_SPICE: {ALLOW_SPICE} (prob={SPICE_PROB})")
    out.append("")

    for t, lane in notes:
        out.append(f"{t:.6f}, {lane}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print("input notes:", in_count)
    print("output notes:", len(notes))
    print("wrote:", OUTPUT)

if __name__ == "__main__":
    main()