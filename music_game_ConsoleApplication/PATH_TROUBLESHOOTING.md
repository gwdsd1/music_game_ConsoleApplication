# 路径输入问题诊断指南

## 问题现象
选择模式2后，粘贴路径显示"Failed to load chart!"

## 常见原因与解决方案

### ✅ 解决方案 1：使用正斜杠

**错误输入**（Windows 复制的路径）：
```
charts\example.chart
D:\music_game\charts\example.chart
```

**正确输入**：
```
charts/example.chart
D:/music_game/charts/example.chart
```

**现在程序会自动转换**，但建议使用正斜杠

---

### ✅ 解决方案 2：使用相对路径

如果你的可执行文件在：
```
D:\港大\课程\y1s2\COMP2113\music_game_ConsoleApplication\
```

曲谱文件应该在：
```
D:\港大\课程\y1s2\COMP2113\music_game_ConsoleApplication\charts\example.chart
```

**输入**：
```
charts/example.chart
```

---

### ✅ 解决方案 3：检查文件是否存在

**验证步骤**：

1. 打开资源管理器
2. 找到你的项目文件夹
3. 确认存在 `charts` 文件夹
4. 确认里面有 `example.chart` 文件

**如果没有，创建它**：
```
mkdir charts
notepad charts/example.chart
```

复制以下内容：
```
# Song: Example Chart
# BPM: 120
# Offset: 0.0

1.0, 0
1.5, 5
2.0, 2
2.5, 3
3.0, 1
3.5, 4
```

---

### ✅ 解决方案 4：避免中文路径

**问题路径**：
```
D:/港大/课程/COMP2113/charts/example.chart
```

**建议**：
1. 将整个项目移到无中文路径，如：
```
C:/Projects/music_game/
```

2. 或者使用绝对路径并用英文文件夹：
```
D:/HKU/Courses/COMP2113/music_game_ConsoleApplication/charts/example.chart
```

---

### ✅ 解决方案 5：使用完整路径测试

**步骤**：
1. 在资源管理器中找到 `example.chart`
2. 按住 Shift + 右键
3. 选择"复制为路径"
4. 粘贴到程序中
5. **手动将所有 `\` 改为 `/`**

**示例**：
```
复制的：  "D:\music_game\charts\example.chart"
修改为：   D:/music_game/charts/example.chart
```

---

## 快速测试方法

### 方法 1：从项目根目录运行

1. 打开 CMD 或 PowerShell
2. 切换到项目目录：
```cmd
cd D:\港大\课程\y1s2\COMP2113\music_game_ConsoleApplication
```

3. 运行程序：
```cmd
x64\Debug\music_game_ConsoleApplication.exe
```

4. 输入相对路径：
```
charts/example.chart
```

### 方法 2：使用 Python 工具创建测试文件

```bash
python chart_maker.py pattern
# 选择模式 1
# 输入简单设置
# 生成 test.chart
```

然后测试：
```
charts/test.chart
```

---

## 程序改进说明

✅ **现在程序会自动**：
1. 移除路径首尾空格
2. 将反斜杠 `\` 转换为正斜杠 `/`
3. 显示详细错误信息
4. 显示加载的文件信息

✅ **错误提示更详细**：
```
✗ Failed to load chart!
  Possible reasons:
  - File does not exist
  - Invalid file format
  - Path contains special characters

  Tips:
  - Use forward slashes: charts/example.chart
  - Use relative path from executable location
  - Avoid paths with spaces or non-ASCII characters
```

---

## 完整示例

### 场景：首次运行游戏

**文件结构**：
```
music_game_ConsoleApplication/
├── music_game_ConsoleApplication.exe  ← 在这里运行
├── charts/
│   └── example.chart                  ← 你的曲谱
└── music/
    └── song.mp3                        ← 你的音乐
```

**运行步骤**：
```
1. 双击运行 music_game_ConsoleApplication.exe
2. 选择: 2
3. 输入: charts/example.chart           ← 注意用正斜杠
4. 显示: ✓ Chart loaded: Example Chart
5. 选择: Y (加载音乐)
6. 输入: music/song.mp3
7. 开始游戏！
```

---

## 仍然失败？

### Debug 步骤

1. **确认工作目录**
   
   在主函数开始添加：
   ```cpp
   char cwd[1024];
   getcwd(cwd, sizeof(cwd));
   std::cout << "Working directory: " << cwd << std::endl;
   ```

2. **测试文件是否存在**
   
   ```cmd
   dir charts\example.chart
   ```

3. **使用绝对路径测试**
   
   找到文件的完整路径，用正斜杠输入

4. **检查文件编码**
   
   确保 `.chart` 文件是 UTF-8 或 ANSI 编码

5. **查看曲谱文件内容**
   
   打开 `charts/example.chart`，确认格式正确：
   ```
   # Song: ...
   # BPM: ...
   # Offset: ...
   
   时间, 轨道
   ```

---

## 联系方式

如果问题仍未解决，请提供：
1. 完整的错误消息
2. 你输入的路径
3. 文件确实存在的证明（截图）
4. 工作目录路径

---

## 快速参考

| 问题 | 解决方案 |
|------|---------|
| 反斜杠路径 | 改用正斜杠 `/` |
| 中文路径 | 移到英文路径 |
| 找不到文件 | 用绝对路径测试 |
| 空格问题 | 程序自动处理 |
| 编码问题 | 用 UTF-8 保存 |

---

✅ **现在重新编译并运行程序，路径处理已经改进！**
