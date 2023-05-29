import multiprocessing
import subprocess
import os
import shutil

#初始化A.txt和B.txt
with open('A.txt', 'w') as file:
	file.write('0')

with open('B.txt', 'w') as file:
	file.write('0')

#初始化A和B文件夹
# 删除A
dir_to_delete = 'A'
if os.path.exists(dir_to_delete):
	shutil.rmtree(dir_to_delete)

# 创建A
dir_to_create = 'A'
os.makedirs(dir_to_create, exist_ok=True)

# 删除B
dir_to_delete = 'B'
if os.path.exists(dir_to_delete):
	shutil.rmtree(dir_to_delete)

# 创建B
dir_to_create = 'B'
os.makedirs(dir_to_create, exist_ok=True)

#启动
def run_script(script_name):
	subprocess.run(['python', script_name])
if __name__ == "__main__":
	# 创建三个进程
	process1 = multiprocessing.Process(target=run_script, args=('GPTxm1.py',))
	process2 = multiprocessing.Process(target=run_script, args=('ly.py',))
	process3 = multiprocessing.Process(target=run_script, args=('auj.py',))

	# 启动三个进程
	process1.start()
	process2.start()
	process3.start()

	# 等待三个进程完成
	process1.join()
	process2.join()
	process3.join()

