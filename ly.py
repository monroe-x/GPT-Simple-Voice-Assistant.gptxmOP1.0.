import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os  # 引入os模块
import sys

#获取当前模式信息
with open('MS.txt', 'r') as file:
	MS = file.read()
if MS == "1":
    print("模式为1，已开启ly.py")
else:
    print("模式不为1，已关闭ly.py")
    sys.exit()

fs = 48000  # 采样率
max_duration = 180  # 最大录音为3分钟
segment_length = 1  # 段长度为1秒

# 创建闭包来保持状态
def create_callback():
    buffer = []
    last_timestamp = datetime.now()
    counter = 0  # 计数器

    def callback(indata, frames, time, status):
        nonlocal buffer, last_timestamp, counter
        buffer.append(indata.copy())
        current_timestamp = datetime.now()
        elapsed = (current_timestamp - last_timestamp).total_seconds()
        if elapsed >= segment_length:
            # 录音数据
            recording = np.concatenate(buffer)
            filename = f'A{counter}.wav'
            # 修改保存位置为当前目录下的名为“A”的文件夹
            filepath = os.path.join('A', filename)  # 更新文件保存路径
            write(filepath, fs, recording)
            # 清空缓存并更新时间戳
            buffer.clear()
            last_timestamp = current_timestamp
            counter += 1  # 更新计数器

    return callback

# 文件监视器
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, stream):
        self.stream = stream

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('A.txt'):
            with open('A.txt', 'r') as f:
                content = f.read().strip()
                if content == '1':
                    self.stream.stop()

callback = create_callback()

with sd.InputStream(callback=callback, channels=2, samplerate=fs, dtype='int16') as stream:
    print('A.txt出1')
    # 设置 watchdog
    observer = Observer()
    handler = FileChangeHandler(stream)
    observer.schedule(handler, path='.', recursive=False)
    observer.start()
    try:
        while stream.active:
            pass
    except KeyboardInterrupt:
        stream.stop()
    finally:
        observer.stop()
        observer.join()
