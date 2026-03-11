param(
  [string]$SongPath = "yorushika_paddle.mp3",
  [string]$Model = "htdemucs"
)

# 输出到 separated\<model>\<songname>\*.wav
demucs -n $Model "$SongPath"