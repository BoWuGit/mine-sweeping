#!/usr/bin/env python3
"""
生成扫雷游戏音效的base64编码文件
"""

import base64
import wave
import struct
import math
import os

def generate_beep_sound(frequency=440, duration=0.3, sample_rate=44100, amplitude=0.3):
    """生成蜂鸣声音效"""
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        sample = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        # 添加淡入淡出效果
        if i < sample_rate * 0.05:  # 前50ms淡入
            sample *= i / (sample_rate * 0.05)
        elif i > num_samples - sample_rate * 0.05:  # 后50ms淡出
            sample *= (num_samples - i) / (sample_rate * 0.05)
        
        samples.append(int(sample * 32767))
    
    return samples

def generate_click_sound(duration=0.1, sample_rate=44100):
    """生成点击音效"""
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        # 生成短促的点击声
        if i < num_samples // 4:
            sample = 0.2 * math.sin(2 * math.pi * 800 * i / sample_rate)
        else:
            sample = 0.1 * math.sin(2 * math.pi * 600 * i / sample_rate) * math.exp(-i / (sample_rate * 0.02))
        
        samples.append(int(sample * 32767))
    
    return samples

def generate_explosion_sound(duration=0.5, sample_rate=44100):
    """生成爆炸音效"""
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        # 生成爆炸声
        t = i / sample_rate
        if t < 0.1:
            # 爆炸开始
            sample = 0.4 * math.sin(2 * math.pi * 200 * t) * math.exp(-t * 10)
        elif t < 0.3:
            # 爆炸持续
            sample = 0.2 * math.sin(2 * math.pi * 150 * t) * math.exp(-t * 5)
        else:
            # 爆炸结束
            sample = 0.1 * math.sin(2 * math.pi * 100 * t) * math.exp(-t * 3)
        
        samples.append(int(sample * 32767))
    
    return samples

def generate_victory_sound(duration=1.0, sample_rate=44100):
    """生成胜利音效"""
    num_samples = int(sample_rate * duration)
    samples = []
    
    # 胜利音效：上升的音阶
    frequencies = [523, 659, 784, 1047]  # C5, E5, G5, C6
    samples_per_note = num_samples // len(frequencies)
    
    for i in range(num_samples):
        note_index = i // samples_per_note
        if note_index >= len(frequencies):
            note_index = len(frequencies) - 1
        
        freq = frequencies[note_index]
        t = (i % samples_per_note) / sample_rate
        sample = 0.3 * math.sin(2 * math.pi * freq * t)
        
        # 添加淡入淡出
        if t < 0.1:
            sample *= t / 0.1
        elif t > 0.15:
            sample *= (0.25 - t) / 0.1
        
        samples.append(int(sample * 32767))
    
    return samples

def samples_to_wav_bytes(samples, sample_rate=44100):
    """将采样数据转换为WAV格式字节"""
    # WAV文件头
    wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        36 + len(samples) * 2,  # 文件大小
        b'WAVE',
        b'fmt ',
        16,  # fmt块大小
        1,   # PCM格式
        1,   # 单声道
        sample_rate,
        sample_rate * 2,  # 字节率
        2,   # 块对齐
        16,  # 位深度
        b'data',
        len(samples) * 2  # 数据大小
    )
    
    # 音频数据
    audio_data = struct.pack(f'<{len(samples)}h', *samples)
    
    return wav_header + audio_data

def wav_to_base64(wav_bytes):
    """将WAV字节转换为base64编码"""
    return base64.b64encode(wav_bytes).decode('utf-8')

def main():
    """生成所有音效的base64编码"""
    print("正在生成扫雷游戏音效的base64编码...")
    
    # 生成各种音效
    sounds = {
        'click': generate_click_sound(),
        'beep': generate_beep_sound(),
        'explosion': generate_explosion_sound(),
        'victory': generate_victory_sound()
    }
    
    # 转换为base64编码
    base64_sounds = {}
    for name, samples in sounds.items():
        wav_bytes = samples_to_wav_bytes(samples)
        base64_sounds[name] = wav_to_base64(wav_bytes)
        print(f"✓ 生成 {name}.wav 音效")
    
    # 创建JavaScript文件
    js_content = """// 扫雷游戏音效文件
// 这些是base64编码的WAV音效文件，可以直接在浏览器中使用

const SOUNDS = {
"""
    
    for name, base64_data in base64_sounds.items():
        js_content += f'    "{name}": "data:audio/wav;base64,{base64_data}",\n'
    
    js_content += """};

// 预加载音效
const audioElements = {};
for (const [name, dataUrl] of Object.entries(SOUNDS)) {
    const audio = new Audio(dataUrl);
    audio.preload = 'auto';
    audioElements[name] = audio;
}

// 播放音效的函数
function playSound(soundName) {
    if (audioElements[soundName]) {
        audioElements[soundName].currentTime = 0;
        audioElements[soundName].play().catch(e => console.log('音效播放失败:', e));
    }
}

// 导出音效
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SOUNDS, playSound };
}
"""
    
    # 保存JavaScript文件
    with open('sounds.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"\n✓ 已生成 sounds.js 文件")
    print(f"✓ 包含 {len(base64_sounds)} 个音效文件")
    print("\n使用方法:")
    print("1. 将 sounds.js 文件复制到前端目录")
    print("2. 在HTML中引入: <script src='sounds.js'></script>")
    print("3. 在代码中调用: playSound('click') 或 playSound('explosion')")
    
    # 显示文件大小
    file_size = os.path.getsize('sounds.js')
    print(f"\n文件大小: {file_size / 1024:.1f} KB")

if __name__ == '__main__':
    main() 