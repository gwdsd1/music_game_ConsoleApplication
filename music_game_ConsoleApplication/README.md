# Console Rhythm Game 6L - 使用说明

## 功能特性

✨ **双模式游戏**
- 随机模式：自动生成音符，难度逐渐增加
- 曲谱模式：加载自定义曲谱和音乐文件

🎵 **音乐支持**
- 支持 MP3, WAV, WMA 等格式
- 实时音乐播放
- 音符与音乐同步

📝 **曲谱系统**
- 简单的文本格式曲谱（.chart）
- 支持自定义 BPM 和音乐偏移
- 轻松创建和编辑曲谱

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

创建必要的文件夹：
```
music_game_ConsoleApplication/
├── charts/          # 存放曲谱文件
│   └── example.chart
├── music/           # 存放音乐文件
│   └── song.mp3
└── music_game_ConsoleApplication.exe
```

### 3. 运行游戏

双击运行 `music_game_ConsoleApplication.exe`

## 游戏模式

### 模式1：随机模式

- 自动生成随机音符
- 难度随分数增加
- 适合练习和休闲娱乐

启动游戏后选择 `1`

### 模式2：曲谱模式

- 加载自定义曲谱
- 可选择播放音乐
- 体验完整的音乐游戏

启动游戏后：
1. 选择 `2`
2. 输入曲谱文件路径（如：`charts/example.chart`）
3. 选择是否加载音乐（Y/N）
4. 如果选择Y，输入音乐文件路径（如：`music/song.mp3`）

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

### 快速示例

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

## 文件结构

```
music_game_ConsoleApplication/
├── music_game_ConsoleApplication.cpp   # 主程序
├── ChartLoader.h                       # 曲谱加载器
├── MusicPlayer.h                       # 音乐播放器
├── CHART_GUIDE.md                      # 曲谱制作指南
├── README.md                           # 本文件
├── charts/                             # 曲谱文件夹
│   └── example.chart                   # 示例曲谱
└── music/                              # 音乐文件夹
    └── (你的音乐文件)
```

## 系统要求

- **操作系统**: Windows 10 或更高版本
- **终端**: 支持 ANSI 转义序列的终端
  - Windows Terminal（推荐）
  - 新版 CMD
  - PowerShell
- **音频格式**: MP3, WAV, WMA 等

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

## 进阶使用

### 自定义游戏参数

编辑 `Game` 结构体中的参数：

```cpp
int perfectWindow = 0;  // Perfect 判定窗口
int goodWindow = 1;      // Good 判定窗口
double speedRowsPerSec = 15.0;  // 下落速度
```

### 添加更多轨道

修改 `lanes` 变量和 `laneKeys` 数组

### 自定义键位

修改 `laneKeys` 数组：
```cpp
array<char, 6> laneKeys = { 'A','S','D','J','K','L' };
```

## 技巧和建议

1. **新手练习**
   - 先玩随机模式熟悉操作
   - 从慢速曲谱开始（BPM 80-100）

2. **提高准确度**
   - 注意观察判定反馈
   - 保持稳定的节奏感
   - 多练习连击

3. **制作曲谱**
   - 先听熟音乐
   - 使用节拍器确定BPM
   - 从简单模式开始
   - 多次测试调整

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目仅供学习使用。

## 更新日志

### v2.0
- ✨ 添加曲谱模式
- 🎵 添加音乐播放支持
- 📊 改进统计显示
- 🎨 优化视觉效果

### v1.0
- 🎮 基础游戏功能
- 🎯 判定系统
- 🏆 分数和连击系统
