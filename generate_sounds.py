import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), '../frontend/assets')
os.makedirs(ASSET_DIR, exist_ok=True)

RATE = 44100

def save_wav_to_mp3(wav_path, mp3_path):
    sound = AudioSegment.from_wav(wav_path)
    sound.export(mp3_path, format="mp3")
    os.remove(wav_path)

def gen_beep(filename, freq=800, duration=0.12, volume=0.5):
    t = np.linspace(0, duration, int(RATE * duration), False)
    tone = np.sin(freq * 2 * np.pi * t) * volume
    audio = np.int16(tone * 32767)
    wav_path = os.path.join(ASSET_DIR, filename + '.wav')
    mp3_path = os.path.join(ASSET_DIR, filename + '.mp3')
    write(wav_path, RATE, audio)
    save_wav_to_mp3(wav_path, mp3_path)

# reveal: 短促哔声
# flag: 低频短促哔声
# explosion: 爆炸噪音
# victory: 上升音阶

def gen_reveal():
    gen_beep('reveal', freq=1200, duration=0.09, volume=0.4)

def gen_flag():
    gen_beep('flag', freq=400, duration=0.11, volume=0.5)

def gen_explosion():
    duration = 0.25
    t = np.linspace(0, duration, int(RATE * duration), False)
    noise = np.random.uniform(-1, 1, t.shape) * np.exp(-8*t) * 0.7
    audio = np.int16(noise * 32767)
    wav_path = os.path.join(ASSET_DIR, 'explosion.wav')
    mp3_path = os.path.join(ASSET_DIR, 'explosion.mp3')
    write(wav_path, RATE, audio)
    save_wav_to_mp3(wav_path, mp3_path)

def gen_victory():
    # 上升三音阶
    freqs = [660, 880, 1046]
    result = np.array([], dtype=np.float32)
    for f in freqs:
        t = np.linspace(0, 0.11, int(RATE * 0.11), False)
        tone = np.sin(f * 2 * np.pi * t) * 0.5
        result = np.concatenate([result, tone])
    audio = np.int16(result * 32767)
    wav_path = os.path.join(ASSET_DIR, 'victory.wav')
    mp3_path = os.path.join(ASSET_DIR, 'victory.mp3')
    write(wav_path, RATE, audio)
    save_wav_to_mp3(wav_path, mp3_path)

if __name__ == '__main__':
    gen_reveal()
    gen_flag()
    gen_explosion()
    gen_victory()
    print('音效已生成到 frontend/assets/') 