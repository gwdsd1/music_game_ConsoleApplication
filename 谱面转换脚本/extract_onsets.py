import numpy as np
import librosa

AUDIO_PATH = "yorushika_paddle.mp3"

# 可调参数（决定“密度”）
HOP_LENGTH = 512
DELTA = 0.07          # 越大 -> 检测越少（更稀疏）；越小 -> 检测越多（更密）
WAIT = 3              # 防止过近重复（单位：帧）；越大 -> 更少点

def main():
    y, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)

    onset_frames = librosa.onset.onset_detect(
        y=y,
        sr=sr,
        hop_length=HOP_LENGTH,
        backtrack=True,
        units="frames",
        delta=DELTA,
        wait=WAIT,
    )

    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=HOP_LENGTH)

    # 去重 + 四舍五入到微秒级显示（你给的标签是 6 位小数）
    onset_times = np.unique(np.round(onset_times.astype(np.float64), 6))

    with open("onset_times.txt", "w", encoding="utf-8") as f:
        for t in onset_times:
            f.write(f"{t:.6f}\n")

    print("onset count:", len(onset_times))
    print("wrote onset_times.txt")

if __name__ == "__main__":
    main()