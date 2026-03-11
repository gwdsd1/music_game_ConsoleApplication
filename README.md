# Console Rhythm Game 6L - 使用说明

## 功能特性

✨ **三模式游戏**
- 随机模式：自动生成音符，难度逐渐增加
- 曲谱模式：加载自定义曲谱和音乐文件
- 关卡模式：内置 4 首预设关卡，即选即玩

🎵 **音乐支持**
- 支持 MP3, WAV, WMA 等格式
- 基于 Windows MCI 的实时音乐播放
- 音符与音乐同步，音乐播放结束后自动结算

📝 **曲谱系统**
- 简单的文本格式曲谱（.chart）
- 支持自定义 BPM 和音乐偏移
- 手动创建或使用 Python 脚本自动生成曲谱

🤖 **Python 自动谱面生成**
- 使用 Demucs (htdemucs) 进行音源分离（鼓、人声、贝斯、其他）
- 使用 librosa 进行鼓点 onset 检测、人声 onset 检测、节拍追踪
- 自动量化到 1/8 拍网格，人声优先合并鼓点
- 智能分轨分配与密度控制

🎮 **游戏特性**
- 6轨道设计（S D F | J K L）
- Perfect/Good/Miss 判定系统
- 实时反馈和分数统计
- 连击系统
- 彩色终端界面

## 快速开始

### 1. 编译项目

使用 Visual Studio 打开项目并编译，或使用命令行：

```bash
cd music_game_ConsoleApplication
# 使用 MSBuild
msbuild music_game_ConsoleApplication.vcxproj
```

### 2. 准备文件

项目结构：
```
music_game_ConsoleApplication/
├── charts/                              # 曲谱文件夹
│   ├── yorushika_paddle.chart
│   ├── zutomayo_justice.chart
│   ├── r-906_manimani.chart
│   ├── n-buna_because_summer_will_end.chart
│   └── example.chart
├── music/                               # 音乐文件夹
│   ├── yorushika_paddle.mp3
│   ├── zutomayo_justice.mp3
│   ├── r-906_manimani.mp3
│   └── n-buna_because_summer_will_end.mp3
└── music_game_ConsoleApplication.exe
```

### 3. 运行游戏

双击运行 `music_game_ConsoleApplication.exe`

## 游戏模式

### 模式1：随机模式 (Random Mode)

- 自动生成随机音符
- 难度随分数增加
- 适合练习和休闲娱乐

启动游戏后选择 `1`

### 模式2：曲谱模式 (Chart Mode)

- 加载自定义曲谱
- 可选择播放音乐
- 体验完整的音乐游戏

启动游戏后：
1. 选择 `2`
2. 输入曲谱文件路径（如：`charts/example.chart`）
3. 选择是否加载音乐（Y/N）
4. 如果选择Y，输入音乐文件路径（如：`music/song.mp3`）

### 模式3：关卡模式 (Stage Mode) 🌟

- 内置 4 首预设关卡，自动加载曲谱与音乐
- 音乐播放结束后自动结算成绩

启动游戏后：
1. 选择 `3`
2. 从关卡列表中选择编号

**内置关卡列表：**

| 关卡 | 歌手 | 曲名 |
|:----:|:----:|:----:|
| 1 | Yorushika | Paddle |
| 2 | ZUTOMAYO | Justice |
| 3 | r-906 | manimani |
| 4 | n-buna | because summer will end |

## 操作说明

### 按键对应

```
左手区域:          右手区域:
   S  D  F           J  K  L
   ↓  ↓  ↓           ↓  ↓  ↓
  [|][|][|]         [|][|][|]
   轨道0-2            轨道3-5
```

### 游戏中操作

- **S/D/F/J/K/L** - 按对应轨道
- **Q** - 退出游戏

### 判定说明

- **PERFECT** - 完美时机（±0行）➜ +10分
- **GOOD** - 良好时机（±1行）➜ +5分
- **MISS** - 错过音符 ➜ -2生命，连击中断

## 曲谱制作

详见 [CHART_GUIDE.md](CHART_GUIDE.md)

### 手动创建

创建 `charts/my_song.chart`：

```
# Song: My First Chart
# BPM: 120
# Offset: 0.0

# Format: time(seconds), lane(0-5)
1.0, 0
1.5, 1
2.0, 2
2.5, 3
3.0, 4
3.5, 5
```

### Python 自动生成曲谱（谱面转换脚本）

项目附带一套 Python 脚本，可以从任意 MP3 音乐文件自动识别节拍和音符事件，生成 `.chart` 曲谱。

#### 环境准备

```bash
cd 谱面转换脚本
python -m venv venv
venv\Scripts\activate
pip install librosa numpy demucs
```

#### 流程概览

```
MP3 音乐文件
    │
    ▼
┌─────────────────────────────────┐
│ Step 1: Demucs 音源分离          │
│   demucs -n htdemucs song.mp3   │
│   → separated/htdemucs/song/    │
│     ├── drums.mp3               │
│     ├── vocals.mp3              │
│     ├── bass.mp3                │
│     └── other.mp3               │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Step 2: 提取音符事件             │
│   02_extract_events_mp3.py      │
│   → drum_events.txt             │
│   → vocal_events.txt            │
│   → beats.txt                   │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Step 3: 生成 .chart 曲谱        │
│   03_make_chart_musical_1_8.py  │
│   → song_name.chart             │
└─────────────────────────────────┘
```

#### 详细步骤

**Step 1：使用 Demucs 分离音源**

```bash
demucs -n htdemucs your_song.mp3
```

分离结果保存在 `separated/htdemucs/<song_name>/` 下，包含 `drums.mp3`、`vocals.mp3` 等。

**Step 2：提取鼓点/人声 onset 和节拍**

编辑 `02_extract_events_mp3.py`，将 `SONG_SUBDIR` 改为你的歌曲目录名：

```python
SONG_SUBDIR = "your_song_name"  # separated/htdemucs/ 下的子目录名
```

运行：

```bash
python 02_extract_events_mp3.py
```

脚本功能：
- 从 `drums.mp3` 提取鼓点 onset → `drum_events.txt`
- 从 `vocals.mp3` 使用 Mel 频谱 + 预加重提取人声 onset → `vocal_events.txt`
- 使用 `librosa.beat.beat_track` 追踪节拍 → `beats.txt`

**Step 3：合并并生成 .chart 曲谱**

编辑 `03_make_chart_musical_1_8.py`，设置歌曲信息：

```python
SONG_NAME = "your_song_name"
OUT = "your_song_name.chart"
```

运行：

```bash
python 03_make_chart_musical_1_8.py
```

脚本功能：
- 将人声/鼓点 onset 量化到 1/8 拍网格
- 人声优先，鼓点填空（距人声过近的鼓点自动跳过）
- 智能密度控制（普通段/密集段自动切换）
- 按"分句"模式分配轨道（回摆走位，避免同轨连打）

生成的 `.chart` 文件放入 `charts/` 目录，对应 MP3 放入 `music/` 目录即可使用。

#### 辅助脚本

| 脚本 | 功能 |
|:-----|:-----|
| `extract_onsets.py` | 从原始 MP3 直接提取 onset（简易版，不分离音源） |
| `times_to_chart_Version2.py` | 将 onset 时间列表转为 .chart（偏四轨分配） |
| `retouch_chart_A_Version2.py` | 曲谱润色 A 风格：鼓点为主，稳定踩点，限 1-4 轨 |
| `retouch_chart_B_Version2.py` | 曲谱润色 B 风格：动态密度，密集段/普通段自动切换 |
| `chart_maker.py` | 交互式手动输入曲谱 / 模式快速生成曲谱 |

## 文件结构

```
music_game_ConsoleApplication/
├── music_game_ConsoleApplication.cpp   # 主程序（C++）
├── ChartLoader.h                       # 曲谱加载器
├── MusicPlayer.h                       # 音乐播放器（MCI）
├── chart_maker.py                      # 交互式曲谱制作工具
├── CHART_GUIDE.md                      # 曲谱制作指南
├── README.md                           # 本文件
├── charts/                             # 曲谱文件夹
│   ├── yorushika_paddle.chart          # 关卡1 曲谱
│   ├── zutomayo_justice.chart          # 关卡2 曲谱
│   ├── r-906_manimani.chart            # 关卡3 曲谱
│   ├── n-buna_because_summer_will_end.chart  # 关卡4 曲谱
│   └── example.chart                   # 示例曲谱
├── music/                              # 音乐文件夹
│   ├── yorushika_paddle.mp3
│   ├── zutomayo_justice.mp3
│   ├── r-906_manimani.mp3
│   └── n-buna_because_summer_will_end.mp3
└── 谱面转换脚本/                        # Python 自动谱面生成工具
    ├── 02_extract_events_mp3.py        # 提取鼓点/人声 onset 和节拍
    ├── 03_make_chart_musical_1_8.py    # 合成 .chart（1/8 拍量化）
    ├── extract_onsets.py               # 简易 onset 提取
    ├── times_to_chart_Version2.py      # 时间列表转 .chart
    ├── retouch_chart_A_Version2.py     # 曲谱润色 A 风格
    └── retouch_chart_B_Version2.py     # 曲谱润色 B 风格
```

## 系统要求

- **操作系统**: Windows 10 或更高版本
- **终端**: 支持 ANSI 转义序列的终端
  - Windows Terminal（推荐）
  - 新版 CMD
  - PowerShell
- **音频格式**: MP3, WAV, WMA 等
- **Python 谱面生成**（可选）:
  - Python 3.8+
  - librosa, numpy, demucs

## 故障排除

### 问题：音符与音乐不同步

**解决方案**: 调整曲谱文件中的 `Offset` 值
- 音符太早 → 增加 Offset（如：0.0 → 0.1）
- 音符太晚 → 减少 Offset（如：0.0 → -0.1）

### 问题：无法加载音乐文件

**解决方案**:
1. 确认文件路径正确
2. 确认文件格式支持（MP3/WAV）
3. 尝试转换为 WAV 格式

### 问题：颜色显示不正常

**解决方案**:
- 使用 Windows Terminal
- 或升级到 Windows 10 1909 或更高版本

### 问题：曲谱加载失败

**解决方案**:
1. 检查文件格式是否正确
2. 确认时间值递增排列
3. 确认轨道号在 0-5 范围内

### 问题：Python 脚本找不到分离后的音频

**解决方案**:
1. 确认已运行 `demucs -n htdemucs your_song.mp3`
2. 检查 `separated/htdemucs/` 下是否有对应子目录
3. 修改脚本中的 `SONG_SUBDIR` 为正确的目录名

## 进阶使用

### 自定义游戏参数

编辑 `Game` 结构体中的参数：

```cpp
int perfectWindow = 0;  // Perfect 判定窗口
int goodWindow = 1;      // Good 判定窗口
double speedRowsPerSec = 15.0;  // 下落速度
```

### 添加新关卡

在 `music_game_ConsoleApplication.cpp` 中的 `stages` 向量添加新条目：

```cpp
static const std::vector<Stage> stages = {
    // ... 现有关卡 ...
    { "5", "Artist", "Song Name", "charts/your_chart.chart", "music/your_song.mp3" },
};
```

然后将对应的 `.chart` 文件和 `.mp3` 文件分别放入 `charts/` 和 `music/` 目录。

### 自定义键位

修改 `laneKeys` 数组：
```cpp
array<char, 6> laneKeys = { 'A','S','D','J','K','L' };
```

## 技巧和建议

1. **新手练习**
   - 先玩随机模式熟悉操作
   - 从关卡模式中选择节奏较慢的歌曲开始

2. **提高准确度**
   - 注意观察判定反馈
   - 保持稳定的节奏感
   - 多练习连击

3. **制作曲谱**
   - 推荐使用 Python 脚本自动生成初版曲谱
   - 用润色脚本（retouch_chart）调整手感
   - 多次测试调整 Offset 和密度参数

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目仅供学习使用。

## 更新日志

### v3.0
- 🎮 新增关卡模式（Stage Mode），内置 4 首预设关卡
- 🤖 新增 Python 自动谱面生成工具链（Demucs + librosa）
- 🎵 游戏结束改为音乐播放完毕后自动结算
- 📝 新增曲谱润色脚本（A/B 风格）

### v2.0
- ✨ 添加曲谱模式
- 🎵 添加音乐播放支持
- 📊 改进统计显示
- 🎨 优化视觉效果

### v1.0
- 🎮 基础游戏功能
- 🎯 判定系统
- 🏆 分数和连击系统
