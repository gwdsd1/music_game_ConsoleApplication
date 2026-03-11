#!/usr/bin/env python3
"""
简易曲谱制作工具
用于辅助创建 .chart 文件
"""

import sys
import os

def create_chart_interactive():
    """交互式创建曲谱"""
    print("=" * 50)
    print("Console Rhythm Game - Chart Creator")
    print("=" * 50)
    print()
    
    # 获取歌曲信息
    title = input("Song Title: ").strip()
    if not title:
        title = "Untitled"
    
    bpm_str = input("BPM (default 120): ").strip()
    bpm = float(bpm_str) if bpm_str else 120.0
    
    offset_str = input("Offset in seconds (default 0.0): ").strip()
    offset = float(offset_str) if offset_str else 0.0
    
    # 计算每拍时间
    beat_duration = 60.0 / bpm
    print(f"\nEach beat = {beat_duration:.3f} seconds")
    print(f"Each half beat = {beat_duration/2:.3f} seconds")
    print(f"Each quarter beat = {beat_duration/4:.3f} seconds")
    print()
    
    # 输入音符
    notes = []
    print("Enter notes (format: time lane, or beat.subdivision lane)")
    print("Lanes: 0=S, 1=D, 2=F, 3=J, 4=K, 5=L")
    print("Examples:")
    print("  1.0 0      -> time 1.0s, lane S")
    print("  b1 0       -> beat 1, lane S")
    print("  b1.5 2     -> beat 1.5 (half beat), lane F")
    print("Type 'done' to finish\n")
    
    while True:
        line = input("Note> ").strip()
        
        if line.lower() == 'done':
            break
        
        if not line:
            continue
        
        try:
            parts = line.split()
            if len(parts) != 2:
                print("  Error: Need 2 values (time lane)")
                continue
            
            time_str, lane_str = parts
            lane = int(lane_str)
            
            if lane < 0 or lane > 5:
                print("  Error: Lane must be 0-5")
                continue
            
            # 解析时间（支持 beat 格式）
            if time_str.startswith('b'):
                beat_num = float(time_str[1:])
                time = beat_num * beat_duration
                print(f"  Beat {beat_num} -> {time:.3f}s")
            else:
                time = float(time_str)
            
            notes.append((time, lane))
            print(f"  Added: {time:.3f}s, lane {lane}")
            
        except ValueError as e:
            print(f"  Error: {e}")
    
    if not notes:
        print("\nNo notes added. Exiting.")
        return
    
    # 排序
    notes.sort()
    
    # 保存
    output_file = input("\nOutput filename (e.g., my_song.chart): ").strip()
    if not output_file:
        output_file = "output.chart"
    
    if not output_file.endswith('.chart'):
        output_file += '.chart'
    
    # 确保 charts 目录存在
    os.makedirs('charts', exist_ok=True)
    output_path = os.path.join('charts', output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Song: {title}\n")
        f.write(f"# BPM: {bpm}\n")
        f.write(f"# Offset: {offset}\n")
        f.write("\n")
        f.write("# Format: time(seconds), lane(0-5)\n")
        f.write("# Lanes: 0=S, 1=D, 2=F, 3=J, 4=K, 5=L\n")
        f.write("\n")
        
        for time, lane in notes:
            f.write(f"{time:.3f}, {lane}\n")
    
    print(f"\n✓ Chart saved to: {output_path}")
    print(f"  Total notes: {len(notes)}")
    print(f"  Duration: {notes[-1][0]:.1f}s")


def convert_simple_pattern():
    """根据模式快速生成曲谱"""
    print("=" * 50)
    print("Pattern Generator")
    print("=" * 50)
    print()
    
    title = input("Song Title: ").strip() or "Pattern"
    bpm = float(input("BPM (default 120): ").strip() or "120")
    
    beat_duration = 60.0 / bpm
    
    print("\nPattern Types:")
    print("  1. Single notes (one per beat)")
    print("  2. Alternating (left-right)")
    print("  3. Roll (0->5)")
    print("  4. Chord progression")
    
    pattern_type = input("\nSelect pattern (1-4): ").strip()
    
    start_beat = float(input("Start beat: ").strip() or "1")
    num_notes = int(input("Number of notes/groups: ").strip() or "8")
    
    notes = []
    
    if pattern_type == "1":
        # 单音符
        lane = int(input("Lane (0-5): ").strip() or "0")
        for i in range(num_notes):
            time = (start_beat + i) * beat_duration
            notes.append((time, lane))
    
    elif pattern_type == "2":
        # 左右交替
        left_lane = 0
        right_lane = 5
        for i in range(num_notes):
            time = (start_beat + i * 0.5) * beat_duration
            lane = left_lane if i % 2 == 0 else right_lane
            notes.append((time, lane))
    
    elif pattern_type == "3":
        # 滚动
        for i in range(num_notes):
            time = (start_beat + i * 0.25) * beat_duration
            lane = i % 6
            notes.append((time, lane))
    
    elif pattern_type == "4":
        # 和弦
        for i in range(num_notes):
            time = (start_beat + i) * beat_duration
            # 三音和弦
            notes.append((time, 0))
            notes.append((time, 2))
            notes.append((time, 4))
    
    # 保存
    output_file = input("\nOutput filename: ").strip() or "pattern.chart"
    if not output_file.endswith('.chart'):
        output_file += '.chart'
    
    os.makedirs('charts', exist_ok=True)
    output_path = os.path.join('charts', output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Song: {title}\n")
        f.write(f"# BPM: {bpm}\n")
        f.write(f"# Offset: 0.0\n\n")
        
        for time, lane in sorted(notes):
            f.write(f"{time:.3f}, {lane}\n")
    
    print(f"\n✓ Pattern saved to: {output_path}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'pattern':
        convert_simple_pattern()
    else:
        create_chart_interactive()


if __name__ == "__main__":
    main()
