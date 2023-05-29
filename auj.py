from pydub import AudioSegment
import numpy as np
import os
import time
import shutil
import sys

#获取当前模式信息
with open('MS.txt', 'r') as file:
	MS = file.read()
if MS == "1":
    # 这里写你想运行的代码
    print("模式为1，已开启auj.py")
    # 其他代码...
else:
    print("模式不为1，已关闭auj.py")
    sys.exit()

#每0.5秒检测A文件夹中是否有新文件产生
# 指定需要监控的文件夹
directory = './A'
# 获取初始的文件列表
initial_files = set(os.listdir(directory))
while True:
    while True:
        time.sleep(0.5)
        current_files = set(os.listdir(directory))
        # 判断是否有新的文件产生
        new_files = current_files - initial_files
        if new_files:
            # 更新文件列表
            initial_files = current_files
            print("新文件已产生: ", new_files)
            # 判断B.txt内容是否为'1'
            with open('B.txt', 'r') as file:
                content = file.read().strip()  # strip()方法用来去掉字符串前后的空格或换行符
            if content == '1':
                print("B.txt为1，检查分贝")
                break
            else:
                print("B.txt不为1，删除文件，继续检查新文件")
                for file in new_files:
                    WAV = file
                    # 删除文件
                    file_path = os.path.join('./A', WAV)
                    try:
                        os.remove(file_path)
                        print(f" '{WAV}'已删除.")
                    except FileNotFoundError:
                        print(f"'{WAV}' 删除时出现错误")

    for file in new_files:
        WAV = file
        print("正在读取的文件名: ", WAV)

        # 读取音频文件
        audio = AudioSegment.from_file(os.path.join(directory, file))

        # 获取音频信号的样本
        samples = np.array(audio.get_array_of_samples())
    
        # 如果音频是立体声，将样本转化为二维数组
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))

        # 计算音频信号的最大振幅
        peak_amplitude = np.max(np.abs(samples))

        # 计算最大分贝值
        peak_db = 20 * np.log10(peak_amplitude)

        # 将结果存入变量UII
        UII = peak_db

        # 打印结果值以及它的类型
        print("分贝值：", UII)
        
        # 根据UII的值执行不同的操作
        if UII > 70:
            # UII大于70时执行的代码
            print("分贝值大于70，执行相关操作")
            # 移动文件
            src_path = os.path.join('./A', WAV)
            dst_path = os.path.join('./B', WAV)
            try:
                shutil.move(src_path, dst_path)
                print(f" '{WAV}'已经移动到B")
            except FileNotFoundError:
                print(f" '{WAV}'移动时出错")
            # 重命名
            A = WAV
            A1 = './B/' + A
            B = A.replace('A', 'B', 1)
            B1 = './B/' + B
            try:
                os.rename(A1, B1)
                print(f"文件已成功重命名为: {B1}")
            except OSError as e:
                print(f"重命名时发生错误 {e}")
        else:
            print("分贝值小于或等于70，执行删除")
            # 删除文件
            file_path = os.path.join('./A', WAV)
            try:
                os.remove(file_path)
                print(f" '{WAV}'已删除.")
            except FileNotFoundError:
                print(f"'{WAV}' 删除时出现错误")


