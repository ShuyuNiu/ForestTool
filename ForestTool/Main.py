#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/forestTool'
import json
import time
import HttpReq
from User import User
from datetime import datetime,timedelta
import sched
import sys
import os
import platform

#是否是Windows
os_is_windows = platform.system() == 'Windows'

#程序入口
def main():
	print(u'欢迎使用ForestTool')
	try:
	    with open('user_login.txt', 'r') as f:
	    	user_login_list = f.readlines()
	    	if len(user_login_list) == 2:
	    		s_account = user_login_list[0].strip('\n')
	    		s_pwd = user_login_list[1].strip('\n')
	    		login_input = {'account':s_account,'pwd':s_pwd}
	    	else:
	    		login_input = get_login()
	except IOError:
	    login_input = get_login()
	login(login_input)

#根据系统获取raw_input中文编码结果
def gbk_encode(str):
	if os_is_windows:
		return str.decode('utf-8').encode('gbk')
	else:
		return str

#获取用户输入的账号和密码
def get_login():
	account = raw_input(gbk_encode('请输入您的账号: ')).decode(sys.stdin.encoding)
	pwd = raw_input(gbk_encode('请输入您的密码: ')).decode(sys.stdin.encoding)
	return {'account':account,'pwd':pwd}

#获取批量植树功能的用户选择信息
def get_add_time():
	add_time = raw_input(gbk_encode('请输入专注时间（分钟）: '))
	tree_type = raw_input(gbk_encode('请选择植物类型【1.开花的树 2.树屋 3.鸟巢 4.柠檬树 5.三兄弟 6.树丛 7.章鱼 8.樱花 9.椰子树 10.猫咪 11.一株很大的草 12.中国松 13.仙人掌球 14.南瓜 15.稻草人 16.圣诞树 17.中国新年竹 18.蘑菇 19.仙人掌 20.银杏 21.紫藤 22.西瓜 23.竹子 24.糖果树 25.向日葵 26.玫瑰 27.枫树 28.面包树 29.大王花 30.香蕉】，无论是否已购买都可以种植，超出30的植物有兴趣可以自行测试: ')).decode(sys.stdin.encoding)
	note = raw_input(gbk_encode('请输入此任务备注: ')).decode(sys.stdin.encoding)
	add_count = raw_input(gbk_encode('请输入批量植树数量: ')).decode(sys.stdin.encoding)
	return {'add_time':add_time,'tree_type':tree_type,'note':note,'add_count':add_count}

#获取刷金币功能的用户选择信息
def get_coin_task():
	add_time = raw_input(gbk_encode('请输入每棵树种植时间（分钟）【5-120分钟，每5分钟一阶段，每增加1阶段多1金币，第一阶段2金币】: ')).decode(sys.stdin.encoding)
	tree_type = raw_input(gbk_encode('请选择植物类型【1.开花的树 2.树屋 3.鸟巢 4.柠檬树 5.三兄弟 6.树丛 7.章鱼 8.樱花 9.椰子树 10.猫咪 11.一株很大的草 12.中国松 13.仙人掌球 14.南瓜 15.稻草人 16.圣诞树 17.中国新年竹 18.蘑菇 19.仙人掌 20.银杏 21.紫藤 22.西瓜 23.竹子 24.糖果树 25.向日葵 26.玫瑰 27.枫树 28.面包树 29.大王花 30.香蕉】，无论是否已购买都可以种植，超出30的植物有兴趣可以自行测试: ')).decode(sys.stdin.encoding)
	note = raw_input(gbk_encode('请输入此任务备注: ')).decode(sys.stdin.encoding)
	return {'add_time':add_time,'tree_type':tree_type,'note':note}

#获取用户选择菜单的信息
def get_mode():
	mode_input = raw_input(gbk_encode('请选择您要进行的操作: 1.自动刷金币 2.批量植树 3.使用其他账号登录 4.退出ForestTool: ')).decode(sys.stdin.encoding)
	return mode_input

#前往菜单
def to_menu(user):
	while(True):
	   		mode_input = get_mode()
	   		if mode_input == '1':
	   			add_coin_task(user)
	   			break
	   		elif mode_input == '2':
	   			add_time(user)
	   			break
	   		elif mode_input == '3':
	   			login(get_login())
	   			break
	   		elif mode_input == '4':
	   			exit(0)
	   			break
	   		else:
	   			print(u'您的输入不合法，请输入选择！！')

#用户登录
def login(login_input):
	post_json = {
	'session':{
		'email':login_input['account'],
		'password':login_input['pwd'],
		},
		'seekruid':''

	}
	print(u'正在登录，请稍后...')
   	res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/sessions',{},post_json,'','POST')
   	if res.has_key('remember_token'):
   		user = User(res['user_name'],res['user_id'],res['remember_token'])
   		print (u'登录成功！！欢迎您，'+ res['user_name'])
   		try:
	   		with open('user_login.txt', 'w') as f:
	   			f.write(login_input['account']+'\n')
	   			f.write(login_input['pwd']+'\n')
	   	except IOError:
	   		print(u'IO异常，无法保存账号密码')
   		to_menu(user)

   	else:
   		print(u'登录失败，账号或密码错误，请重新输入！！')
   		login(get_login())

#批量植树功能
def add_time(user):
	add_time_input = get_add_time()
	add_time_data = int(add_time_input['add_time'])
	tree_type = int(add_time_input['tree_type'])
	print(u'正在执行，请稍后...')
	note = add_time_input['note']
	add_count = int(add_time_input['add_count'])
	curr_count = 0
	while curr_count<add_count:
		curr_count = curr_count+1
		add_per_time(add_time_data,note,tree_type,user,curr_count)
		time.sleep(1)
	to_menu(user)
			
#种植一棵树	
def add_per_time(add_time_data,note,tree_type,user,per_add_count):
	time_now = datetime.now()
	time_now = time_now - timedelta(hours = 8)
	time_pass = time_now - timedelta(minutes = add_time_data) 
	post_json = {
		"plant": {
			"end_time": time_now.isoformat(),
			"longitude": 0,
			"note": note,
			"is_success": 1,
			"room_id": 0,
			"die_reason": '',
			"tag": 0,
			"latitude": 0,
			"has_left": 0,
			"start_time": time_pass.isoformat(),
			"trees": [{
				"phase": 4,
				"theme": 0,
				"is_dead": 0,
				"position": -1,
				"tree_type": tree_type
			}]
		},
		"seekruid": str(user.user_id)
	}
	print(u'植树中，请稍后...')
	post_res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/plants',{},post_json,user.remember_token,'POST')
	if not post_res.has_key('id'):
		print(u'植树失败！！返回信息：'+post_res)
	else:
		get_res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/plants/updated_plants?seekruid='+ str(user.user_id)+'&update_since='+time_now.isoformat()+'/',{},'',user.remember_token,'GET')
		now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print(u'【%s】第%d棵树种植成功！！'%(now_time,1))
		
#刷金币功能
def add_coin_task(user):
	get_coin_input = get_coin_task()
	add_time = int(get_coin_input['add_time'])
	tree_type = get_coin_input['tree_type']
	note = get_coin_input['note']
	get_res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/users/'+str(user.user_id)+'/coin?seekruid='+ str(user.user_id),{},'',user.remember_token,'GET')

	if get_res.has_key('coin'):
		print(u'您当前金币数：'+str(get_res['coin']))
		print(u'开始自动刷金币，每%d分钟植一棵树...'%add_time)
	total_time = 0
	curr_count = 1
	while True:
		if total_time == 0 or total_time % (add_time * 60) == 0:
		    add_per_time(add_time,note,tree_type,user,curr_count)
		    curr_count = curr_count+1
		    get_res_sub = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/users/'+str(user.user_id)+'/coin?seekruid='+ str(user.user_id),{},'',user.remember_token,'GET')
		    print(u'您当前金币数：'+str(get_res_sub['coin'])+u'(赚得金币数：'+str(get_res_sub['coin']-get_res['coin'])+')')
		total_time = total_time+1
		if total_time == add_time * 60:
			total_time = 0
		if not total_time == 0:
			sys.stdout.write('\r'+u'距离下一棵树种植时间 :' + str(add_time * 60 - total_time).zfill(len(str(add_time * 60))),) 
        	sys.stdout.flush()
			#print('距离下一棵树种植时间 :'+str(600 - total_time),)
			#print('\r')
		if total_time == 0:
			print('')
	   	time.sleep(1)

main()

