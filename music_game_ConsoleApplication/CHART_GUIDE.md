# 曲谱制作指南

## 曲谱文件格式

曲谱文件是简单的文本文件（.chart），格式如下：

```
# Song: 歌曲名称
# BPM: 节拍速度（例如：120）
# Offset: 音乐偏移时间（秒，例如：0.0）

# Format: time(seconds), lane(0-5)
# Lanes: 0=S, 1=D, 2=F, 3=J, 4=K, 5=L

时间, 轨道号
1.0, 0
1.5, 5
2.0, 2
```

## 制作方法

### 方法1：手动制作

1. **准备音乐文件**
   - 支持 MP3, WAV 等格式
   - 放在 `music/` 文件夹中

2. **创建曲谱文件**
   - 在 `charts/` 文件夹中创建 `.chart` 文件
   - 使用文本编辑器编辑

3. **确定BPM**
   - 使用在线BPM检测工具
   - 或使用音乐软件（Audacity等）

4. **标记音符**
   - 听音乐，记录每个需要按键的时间点
   - 格式：`时间(秒), 轨道(0-5)`
   - 例如：`1.5, 2` 表示在1.5秒时，F键（轨道2）

### 方法2：使用音乐编辑软件

1. **使用 Audacity**
   - 打开音乐文件
   - 使用标签功能（Ctrl+B）标记节拍
   - 导出标签为文本
   - 转换为 .chart 格式

2. **使用 osu! Editor**
   - 创建 osu! beatmap
   - 导出时间轴信息
   - 转换为 .chart 格式

## 示例曲谱

### 简单示例（4/4拍，BPM=120）

```chart
# Song: Simple Test
# BPM: 120
# Offset: 0.0

# 每拍0.5秒（120 BPM = 2拍/秒）
# 第1-4拍：单音符
0.5, 0
1.0, 1
1.5, 2
2.0, 3

# 第5-8拍：快速序列
2.5, 4
2.75, 5
3.0, 0
3.25, 1
3.5, 2
3.75, 3

# 第9-12拍：和弦
4.0, 0
4.0, 2
4.0, 4
5.0, 1
5.0, 3
5.0, 5
```

### 复杂示例（交替、滚动）

```chart
# Song: Advanced Pattern
# BPM: 140
# Offset: 0.0

# 左右交替（每0.25秒）
1.0, 0
1.25, 5
1.5, 0
1.75, 5
2.0, 0
2.25, 5

# 从左到右滚动
3.0, 0
3.1, 1
3.2, 2
3.3, 3
3.4, 4
3.5, 5

# 三连音
4.0, 2
4.167, 2
4.333, 2
```

## 轨道对应关系

```
轨道号  |  按键  |  位置
--------|--------|----------
   0    |   S    |  左手1
   1    |   D    |  左手2
   2    |   F    |  左手3
   3    |   J    |  右手1
   4    |   K    |  右手2
   5    |   L    |  右手3
```

## 制作技巧

1. **节奏对齐**
   - 先确定准确的BPM
   - 使用节拍器辅助
   - 每4拍或8拍一组

2. **难度设计**
   - 简单：单音符，慢节奏（0.5秒间隔）
   - 中等：快速单音符，简单和弦（0.25秒）
   - 困难：复杂模式，多个和弦（0.125秒）

3. **测试**
   - 多次播放测试
   - 调整 Offset 直到音符与音乐同步
   - 请其他人试玩

## 工具推荐

- **BPM检测**: https://www.beatsperminuteonline.com/
- **音频编辑**: Audacity (免费)
- **节拍器**: https://www.metronomeonline.com/
- **时间计算器**: Excel/Google Sheets

## 转换脚本示例（Python）

```python
# 将 Audacity 标签转换为 .chart 格式
def convert_audacity_to_chart(labels_file, output_file, lane=0):
    with open(labels_file, 'r') as f:
        lines = f.readlines()
    
    with open(output_file, 'w') as f:
        f.write("# Song: Converted Chart\n")
        f.write("# BPM: 120\n")
        f.write("# Offset: 0.0\n\n")
        
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) >= 1:
                time = parts[0]
                f.write(f"{time}, {lane}\n")
```

## 常见问题

**Q: 音符和音乐不同步怎么办？**
A: 调整 Offset 值，正值让音符提前，负值让音符延后

**Q: 如何创建和弦（同时多个音符）？**
A: 使用相同的时间值，不同的轨道号

**Q: 支持什么音乐格式？**
A: Windows MCI 支持 MP3, WAV, WMA 等常见格式

**Q: 如何测试曲谱？**
A: 运行游戏，选择模式2，输入曲谱路径
