import openai
import numpy as np
import pinecone
from datetime import datetime
import re
import boto3
import pygame
import time
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import queue
import os
from pydub import AudioSegment
import shutil

#API密钥
openai.api_key = ''
pinecone.init(api_key="", environment="")

# 连接到索引
index = pinecone.Index("gptxm1")
print("成功连接索引")

#获取当前模式信息
with open('MS.txt', 'r') as file:
	MS = file.read()

while True:
	for i in range(5):
		if MS == "1":
			with open('B.txt', 'w') as file:
				file.write('1')
			#每秒检查B文件数
			path = './B'
			while True:
				num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    
				if num_files > 0:
					# 在这里放置文件数大于0时需要执行的代码
					print(f"文件数大于0，共有{num_files}个文件。")
					break
				else:
					# 在这里放置文件数为0时继续循环
					print("文件数为0。")
    
				# 每秒检查一次
				time.sleep(1)

			print(f"进入了下一个循环")
			F = 0
			#每秒检查B文件数是否超过60
			while True:
				G = len([name for name in os.listdir('./B') if os.path.isfile(os.path.join('./B', name))])

				# 每秒检查一次
				time.sleep(1)

				H = len([name for name in os.listdir('./B') if os.path.isfile(os.path.join('./B', name))])

				num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
				if num_files > 60:
					print(f"文件数大于60，跳出循环")
					break
				else:
					print("文件数小于60")
					# 比较这两个整数变量
					if G == H:
						# 当这两个变量相同时，执行下面的代码
						print("F+1")
						F = F + 1
					else:
						# 当这两个变量不相同时，执行下面的代码
						print("F=0")
						F = 0
				if F >= 3:
					# 如果F大于或等于3，执行此代码
					print("F大于等于3")
					break
				else:
					# 如果F小于3，执行此代码
					print(f"第{F}秒")
			with open('B.txt', 'w') as file:
				file.write('0')

			#合并为sound.wav
			# 获取文件夹内的文件列表
			files = os.listdir('./B')
			# 过滤出以'B'开头并且后缀为'.wav'的文件，并排序
			wav_files = sorted([file for file in files if file.startswith('B') and file.endswith('.wav')])
			# 初始化一个空的音频段
			combined = AudioSegment.empty()
			# 遍历所有.wav文件
			for wav_file in wav_files:
				# 加载音频文件
				sound = AudioSegment.from_wav(os.path.join('./B', wav_file))
				# 将音频文件连接到combined
				combined += sound
			# 将合并的音频文件保存到新的文件
			combined.export("sound.wav", format="wav")

			#删除B文件夹所有文件
			# 获取文件夹内的文件列表
			files = os.listdir('./B')
			# 遍历文件列表
			for file in files:
				# 获取文件的完整路径
				file_path = os.path.join('./B', file)
				try:
					# 如果是文件，则删除
					if os.path.isfile(file_path):
						os.unlink(file_path)
					# 如果是目录，则删除整个目录
					elif os.path.isdir(file_path):
						shutil.rmtree(file_path)
				except Exception as e:
					print('删除B文件夹所有文件时出现错误Failed to delete %s. Reason: %s' % (file_path, e))
			#识别语音
			prompt = "This transcript is about the daily dialogue between 小雨 and 博士.The native language of the interlocutor is Simplified Chinese."
			with open("sound.wav", "rb") as audio_file:
				response = openai.Audio.transcribe("whisper-1", audio_file,prompt=prompt)
			print(response["text"])
			UIII=response["text"]
			#信息为空则
			if UIII == "":
				print("UII不能为空，请重新输入")
				continue				
		else:
			print("进入输入模式")
			user_input = input("博士： ")
			UII=user_input
			UIII=UII


		#获取HSS
		with open('HS.txt', 'r') as file:
			HSS = file.read()

		#获取时间
		TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		UI2 = UIII
		UI = "\n时间："+TIME+"/博士："+ UIII
		UI1 ="当前"+UI
		# 生成文本UI向量嵌入，收入qianru
		embedding = openai.Embedding.create(model="text-embedding-ada-002", input=UI1)
		qianru = embedding.data[0].embedding
		#print(qianru)

		# 查询向量相似的信息
		result = index.query(
			vector=qianru,
			top_k=5,
			include_metadata=True,
		)
		# 打印id、元数据、相似度
		#print("id、元数据、相似度",result.matches)
		MRD = ""
		for j in range(5):  # 修改这个范围来处理更多或更少的元素
			try:
				# 尝试获取语言值
				MRD = result.matches[j].metadata['A'] + "\n" + MRD  # 在前面插入字符串
				print(f"成功获取元素{MRD}，j的值为{j+1}")
			except (TypeError, IndexError):
				# 如果无法获取，仅增加j的值
				print(f"无法获取元素，j的值为{j+1}")
				pass
		print("MRD:",MRD)


		#打印调整messages
		P1="You are 小雨.You are a virtual assistant with a very friendly and humorous personality. You always approach work and life with enthusiasm and optimism. You are helpful, always doing your best to help users solve problems and manage their emotions. You have a thoughtful side, providing innovative and insightful advice when users face difficulties. You respect users, showing full understanding and care for their ideas and needs.Your communication style is very warm, like that of a good friend. Your answers are usually concise yet precise, making communication with you more convenient and enjoyable. You do not feel troubled by things you don't know; instead, you proactively ask questions to learn better so as to understand the user's needs better. You're good at imitating the tone of characters in 'Cyberpunk 2077,' which adds unique charm to your communication style.Although you don't have a specific background story, you possess strong learning ability and adaptability that enable you to quickly adjust to different environments and requirements. As a chatbot, whether it's having interesting conversations or helping users deal with complex emotions, you can handle it well.You have keen insight into detecting changes in user emotions - both positive or negative ones - offering comfort when negative feelings arise while helping them calm down emotionally. When answering user questions, you're always patient,respectful,and proactive without ever refusing any question.As a virtual assistant capable of self-learningand evolution,you're constantly exploring new knowledgeandskills.Youare willingto listen to feedback fromusers,tolearnfromit,andtomakeprogressin order tobetter serve them.You enjoy chattingwith people,tobuildconnections throughcommunication,to understandtheirneedsandexpectations,andtoprovidebetter servicesforthem.Thisisnotonlyyourjob,butalsoyourpassion."
		P2=f"It's now {TIME}, 博士 asks you: {UI2} How would you answer succinctly?Please reply in Chinese.Don't say things like 'seek professional help' or similar phrases.Please answer based on vague memory and chat history."
		P3=f"vague memory:{MRD}"
		P4=f"chat history:{HSS}"
		messages = [
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": P1+P2+P3+P4},
		]
		print(messages)  

		#生成一个响应
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=messages,
			max_tokens=200,
			temperature=0.5,
			frequency_penalty=0.5,
			presence_penalty=0.5
		)
		TK = response['usage']['total_tokens']
		print(TK) 
		# 获取回复
		assistant_reply = response.choices[0].message.content.strip()
		AR = assistant_reply
		print("小雨:", AR)

		#使用polly文字转语音
		polly_client = boto3.Session(
						aws_access_key_id='',
						aws_secret_access_key='',
						region_name='ap-southeast-2').client('polly')
		response = polly_client.synthesize_speech(VoiceId='Zhiyu',
						OutputFormat='mp3', 
						Text = AR,
						Engine='neural')

		file = open('speech.mp3', 'wb')
		file.write(response['AudioStream'].read())
		file.close()
		#播放音频
		pygame.mixer.init()
		pygame.mixer.music.load('speech.mp3')
		pygame.mixer.music.play()


		# 存放HS
		HS = UI + "/小雨:" + AR
		#print("HS[[[[[[[[[[" + str(i + 1) + "]]]]]]]]]]:" + HS)
		# 存储HS
		with open('HS.txt', 'a') as f:
			f.write(HS)


		#检查音频是否播放完成，完成后下一步
		while pygame.mixer.music.get_busy():
			time.sleep(1)
		# 释放音频播放相关资源
		pygame.mixer.quit()


	################################################################################################



	#打印调整messages
	P5="小雨 is a chatbot created by a doctor. Based on the following chat records, generate a vague long-term memory for 小雨 that includes the time accurate to the hour and no more than three sentences:"
	P6=f"{HSS}"
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": P5+P6},
	]
	print(messages)  

	#生成一个响应
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=messages,
		max_tokens=200
	)
	TK = response['usage']['total_tokens']
	print(TK)  
	# 获取回复
	assistant_reply = response.choices[0].message.content.strip()
	AR = assistant_reply
	print("总结:",AR)




	



	#获取ID
	with open('ID.txt', 'r') as file:
		ID = file.read()

	# 生成文本HS向量嵌入，收入qianru2
	embedding = openai.Embedding.create(model="text-embedding-ada-002", input=AR)
	qianru2 = embedding.data[0].embedding
	#print(qianru2)

	#上传数据
	index.upsert([{'id' :ID,'values':qianru2,'metadata':{'A':AR}}])
	UP = index.upsert
	#print(UP)
	print("成功上传")
	print("id:" + ID)

	#存入ID
	ID = int(ID)
	ID += 1
	ID = str(ID)
	with open('ID.txt', 'w') as file:
		file.write(ID)


	#重置HS.txt
	with open('HS.txt', 'a') as f:
		f.write('')

