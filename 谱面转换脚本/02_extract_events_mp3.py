import os
import sys
import numpy as np
import librosa

# ---- 基于脚本位置定位根目录（避免工作目录不同导致找不到文件）----
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR  # 你的脚本就在项目根目录时这样写就行

# ====== 改这里：你的分离输出目录名（非常关键）======
SONG_SUBDIR = "n-buna_because_summer_will_end"  # 改成 separated\htdemucs\ 下真实子目录名
# ====================================================

SONG_DIR = os.path.join(PROJECT_ROOT, "separated", "htdemucs", SONG_SUBDIR)
DRUMS = os.path.join(SONG_DIR, "drums.mp3")
VOCALS = os.path.join(SONG_DIR, "vocals.mp3")

HOP = 512

DRUM_DELTA = 0.10
DRUM_WAIT = 3
DRUM_MIN_GAP = 0.12

VOCAL_DELTA = 0.10
VOCAL_WAIT = 2
VOCAL_MIN_GAP = 0.12

def die(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)

def check_exists(path: str):
    if not os.path.exists(path):
        die(
            "File not found:\n"
            f"  {path}\n\n"
            "Fix:\n"
            "  1) Check the demucs output folder name under separated\\htdemucs\\\n"
            "  2) Set SONG_SUBDIR in this script to that folder name.\n"
        )

def unique_round(x, nd=6):
    return np.unique(np.round(np.asarray(x, dtype=np.float64), nd))

def thin_min_gap(times, min_gap):
    times = np.sort(times)
    out = []
    last = -1e9
    for t in times:
        if t - last >= min_gap:
            out.append(t)
            last = t
    return np.array(out, dtype=np.float64)

def extract_onsets_basic(path, delta, wait):
    y, sr = librosa.load(path, sr=None, mono=True)
    frames = librosa.onset.onset_detect(
        y=y, sr=sr, hop_length=HOP,
        backtrack=True, units="frames",
        delta=delta, wait=wait
    )
    times = librosa.frames_to_time(frames, sr=sr, hop_length=HOP)
    return unique_round(times, 6), y, sr

def extract_vocal_onsets(path, delta, wait):
    y, sr = librosa.load(path, sr=None, mono=True)

    # 1) 预加重，突出辅音/音节起音
    y = librosa.effects.preemphasis(y, coef=0.97)

    # 2) Mel 频谱（去低频残留，聚焦人声清晰区域）
    S = librosa.feature.melspectrogram(
        y=y, sr=sr,
        n_fft=2048, hop_length=HOP,
        n_mels=128, fmin=120, fmax=8000
    )
    oenv = librosa.onset.onset_strength(
        S=librosa.power_to_db(S, ref=np.max),
        sr=sr, hop_length=HOP,
        aggregate=np.median
    )

    frames = librosa.onset.onset_detect(
        onset_envelope=oenv,
        sr=sr, hop_length=HOP,
        backtrack=True, units="frames",
        delta=delta, wait=wait
    )
    times = librosa.frames_to_time(frames, sr=sr, hop_length=HOP)
    times = unique_round(times, 6)
    return times, y, sr

def to_scalar_tempo(tempo):
    if tempo is None:
        return float("nan")
    if np.isscalar(tempo):
        return float(tempo)
    arr = np.asarray(tempo).reshape(-1)
    return float(arr[0]) if arr.size else float("nan")

def extract_beats_fill_from_zero(y, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP)
    beat_times = unique_round(beat_times, 6)
    tempo = to_scalar_tempo(tempo)

    # 补齐从 0 开始的 beat grid（避免前面空谱）
    if beat_times.size >= 2:
        period = float(np.median(np.diff(beat_times)))
    else:
        period = 60.0 / tempo if np.isfinite(tempo) and tempo > 0 else 0.5

    if beat_times.size > 0 and beat_times[0] > 1.0:
        fill = np.arange(0.0, float(beat_times[0]), period, dtype=np.float64)
        beat_times = unique_round(np.concatenate([fill, beat_times]), 6)

    return tempo, beat_times

def write_times(path, times):
    with open(os.path.join(PROJECT_ROOT, path), "w", encoding="utf-8") as f:
        for t in times:
            f.write(f"{t:.6f}\n")

def main():
    print("Python:", sys.version.split()[0])
    print("SONG_DIR:", SONG_DIR)

    check_exists(DRUMS)
    check_exists(VOCALS)

    # 鼓 onsets（基础骨架）
    drum_onsets, y_d, sr_d = extract_onsets_basic(DRUMS, DRUM_DELTA, DRUM_WAIT)
    drum_onsets = thin_min_gap(drum_onsets, DRUM_MIN_GAP)

    # 人声 onsets（更贴音节）
    vocal_onsets, y_v, sr_v = extract_vocal_onsets(VOCALS, VOCAL_DELTA, VOCAL_WAIT)
    vocal_onsets = thin_min_gap(vocal_onsets, VOCAL_MIN_GAP)

    tempo, beats = extract_beats_fill_from_zero(y_d, sr_d)

    write_times("drum_events.txt", drum_onsets)
    write_times("vocal_events.txt", vocal_onsets)
    write_times("beats.txt", beats)

    print("Estimated tempo (rough):", tempo)
    print("Drum events:", len(drum_onsets))
    print("Vocal events:", len(vocal_onsets))
    print("Beats:", len(beats))
    print("Wrote drum_events.txt vocal_events.txt beats.txt")

if __name__ == "__main__":
    main()