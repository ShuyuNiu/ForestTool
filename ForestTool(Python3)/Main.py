# coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/forestTool'
import time
import HttpReq
from User import User
from datetime import datetime, timedelta
import sys
import platform
from dateutil.parser import parse
import csv

# 是否是Windows
os_is_windows = platform.system() == 'Windows'

# 种植成功时间
global plant_succ_time
plant_succ_time = datetime.now()

tree_type_str = "请选择植物类型【1.开花的树 2.树屋 3.鸟巢 4.柠檬树 5.三兄弟 6.树丛 7.章鱼 8.樱花 9.椰子树 10.猫咪 11.一株很大的草 12.中国松 13.仙人掌球 14.南瓜 15.稻草人 16.圣诞树 17.中国新年竹 18.蘑菇 19.仙人掌 20.银杏 21.紫藤 22.西瓜 23.竹子 24.糖果树 25.向日葵 26.玫瑰 27.枫树 28.面包树 29.大王花 30.香蕉 31.新年竹 32.地球樹 33.康乃馨 34.頻果樹 35.星空樹 36.咕咕鐘 37.月亮樹 38.彩虹花 39.幽靈草 40.藍色橡樹 41.橡樹 42.粉紅色橡樹 43.黃色橡樹 44.紫色橡樹 45.銀柳 46.小藍花 47.星星珊瑚 48.巧克力草莓蛋糕 49.櫻桃起司蛋糕 50.提拉米蘇 51.抹茶紅豆蛋糕 52.檸檬蛋糕 53.黑森林蛋糕 54.藍莓蛋糕 55.草莓戚風蛋糕 56.蛋糕樹 57.狗狗樹 58.熊童子 59.煙火樹 60.獨角獸樹 61.太空樹 62.仙樹 63.楊柳 64.幸運草 65.森林之心 66.六週年蛋糕樹 67.水之心 68.聖代樹 69.情人樹 70.梨子樹屋 71.女巫魔菇】，无论是否已购买都可以种植，超出數字的植物有兴趣可以自行测试: "


# 程序入口
def main():
    print(u'欢迎使用ForestTool')
    try:
        with open('user_login.txt', 'r') as f:
            user_login_list = f.readlines()
            if len(user_login_list) == 2:
                s_account = user_login_list[0].strip('\n')
                s_pwd = user_login_list[1].strip('\n')
                login_input = {'account': s_account, 'pwd': s_pwd}
            else:
                login_input = get_login()
    except IOError:
        login_input = get_login()
    login(login_input)


# 根据系统获取raw_input中文编码结果
def gbk_encode(str):
    if os_is_windows:
        return str.decode('utf-8').encode('gbk')
    else:
        return str


# 获取用户输入的账号和密码
def get_login():
    account = input('请输入您的账号:')
    pwd = input('请输入您的密码:')
    return {'account': account, 'pwd': pwd}


# 获取批量植树功能的用户选择信息
def get_add_time():
    add_time = input('请输入专注时间（分钟）: ')
    tree_type = input(tree_type_str)
    note = input('请输入此任务备注: ')
    add_count = input('请输入批量植树数量: ')
    return {'add_time': add_time, 'tree_type': tree_type, 'note': note, 'add_count': add_count}


# 获取刷金币功能的用户选择信息
def get_coin_task():
    add_time = input('请输入每棵树种植时间（分钟）【5-120分钟，每5分钟一阶段，每增加1阶段多1金币，第一阶段2金币】: ')
    tree_type = input(tree_type_str)
    note = input('请输入此任务备注: ')
    return {'add_time': add_time, 'tree_type': tree_type, 'note': note}


# 获取刷金币功能的用户选择信息
def get_dis_add():
    start_time = input('请输入开始时间（格式：\'2019-01-01/11:11:11\'）: ')
    end_time = input('请输入结束时间（格式：\'2019-01-01/11:11:11\'）: ')
    tree_type = input(tree_type_str)
    note = input('请输入此任务备注: ')
    return {'start_time': start_time, 'end_time': end_time, 'tree_type': tree_type, 'note': note}


def get_minutes_tree():
    start_time = input('请输入开始时间（格式：\'2019-01-01/11:11:11\'）: ')
    minutes = input('持續分鐘數（整數）：')
    tree_type = input(tree_type_str)
    note = input('请输入此任务备注: ')
    return {'start_time': start_time, 'minutes': minutes, 'tree_type': tree_type, 'note': note}


def get_csv_file():
    print('支援的csv內容：start_time（開始時間，2019-01-01/11:11:11）、minutes（分鐘數）、tree_type（樹的種類）、note（備註）')
    print('tree_type 為：', tree_type_str)
    file_name = input('請輸入csv檔案路徑: ')
    csvfile = open(file_name, newline='')
    rows = csv.DictReader(csvfile)
    return rows


# 获取用户选择菜单的信息
def get_mode():
    mode_input = input('请选择您要进行的操作: 1.自动刷金币 2.批量植树 3.根据时间区间植树 4.使用其他账号登录 5.根據分鐘數種樹 6.使用csv檔批量種樹 7.退出ForestTool: ')
    return mode_input


# 前往菜单
def to_menu(user):
    while(True):
        mode_input = get_mode()
        funcs = {
            '1': lambda user: add_coin_task(user),
            '2': lambda user: add_time(user),
            '3': lambda user: add_dis_time(user),
            '4': lambda user: login(get_login()),
            '5': lambda user: add_minutes_tree(user),
            '6': lambda user: csv_minutes_tree(user),
            '7': lambda user: exit(0),
        }
        func = funcs.get(mode_input)
        if func:
            func(user)
        else:
            print(u'您的输入不合法，请输入选择！！')


# 用户登录
def login(login_input):
    post_json = {
        'session': {
            'email': login_input['account'],
            'password': login_input['pwd'],
        },
        'seekruid': ''

    }
    print(u'正在登录，请稍后...')
    res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/sessions', {}, post_json, '', 'POST')
    if 'remember_token' in res:
        user = User(res['user_name'], res['user_id'], res['remember_token'])
        print(u'登录成功！！欢迎您，' + res['user_name'])
        try:
            with open('user_login.txt', 'w') as f:
                f.write(login_input['account'] + '\n')
                f.write(login_input['pwd'] + '\n')
        except IOError:
            print(u'IO异常，无法保存账号密码')
        to_menu(user)

    else:
        print(u'登录失败，账号或密码错误，请重新输入！！')
        login(get_login())


# 批量植树功能
def add_time(user):
    add_time_input = get_add_time()
    add_time_data = int(add_time_input['add_time'])
    tree_type = int(add_time_input['tree_type'])
    print(u'正在执行，请稍后...')
    note = add_time_input['note']
    add_count = int(add_time_input['add_count'])
    curr_count = 0
    while curr_count < add_count:
        curr_count = curr_count + 1
        add_per_time(add_time_data, note, tree_type, user, curr_count, '', '')
        time.sleep(1)
    to_menu(user)


# 种植一棵树
def add_per_time(add_time_data, note, tree_type, user, per_add_count, start_time, end_time):
    time_now = datetime.now()
    time_now = time_now - timedelta(hours=8)
    time_pass = time_now - timedelta(minutes=add_time_data)
    if len(start_time):
        s_start_time = start_time
    else:
        s_start_time = time_pass.isoformat()
    if len(end_time):
        s_end_time = end_time
    else:
        s_end_time = time_now.isoformat()
    post_json = {
        "plant": {
            "end_time": s_end_time,
            "longitude": 0,
            "note": note,
            "is_success": 1,
            "room_id": 0,
            "die_reason": '',
            "tag": 0,
            "latitude": 0,
            "has_left": 0,
            "start_time": s_start_time,
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
    post_res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/plants', {}, post_json, user.remember_token, 'POST')
    if 'id' not in post_res:
        print(u'植树失败！！返回信息：' + post_res)
    else:
        HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/plants/updated_plants?seekruid=' + str(user.user_id) + '&update_since=' + time_now.isoformat() + '/', {}, '', user.remember_token, 'GET')
        now_time = datetime.now()
        print(u'【%s】第%d棵树种植成功！！' % (now_time.strftime("%Y-%m-%d %H:%M:%S"), per_add_count))
        global plant_succ_time
        plant_succ_time = now_time


# 刷金币功能
def add_coin_task(user):
    get_coin_input = get_coin_task()
    add_time = int(get_coin_input['add_time'])
    tree_type = get_coin_input['tree_type']
    note = get_coin_input['note']
    get_res = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/users/' + str(user.user_id) + '/coin?seekruid=' + str(user.user_id), {}, '', user.remember_token, 'GET')

    if 'coin' in get_res:
        print(u'您当前金币数：' + str(get_res['coin']))
        print(u'开始自动刷金币，每%d分钟植一棵树...' % add_time)
    total_time = 0
    curr_count = 1
    while True:
        if curr_count == 1 or (not total_time == 0 and total_time % (add_time * 60) == 0):
            add_per_time(add_time, note, tree_type, user, curr_count, '', '')
            curr_count = curr_count + 1
            get_res_sub = HttpReq.send_req('https://c88fef96.forestapp.cc/api/v1/users/' + str(user.user_id) + '/coin?seekruid=' + str(user.user_id), {}, '', user.remember_token, 'GET')
            print(u'您当前金币数：' + str(get_res_sub['coin']) + u'(赚得金币数：' + str(get_res_sub['coin'] - get_res['coin']) + ')')
        global plant_succ_time
        total_time = int((datetime.now() - plant_succ_time).total_seconds())
        if not total_time == add_time * 60:
            sys.stdout.write('\r' + u'距离下一棵树种植时间 :' + str(add_time * 60 - total_time).zfill(len(str(add_time * 60))),)
            sys.stdout.flush()
        if total_time == add_time * 60:
            print('')
        time.sleep(1)


# 根据时间区间种植树
def add_dis_time(user):
    get_dis_input = get_dis_add()
    start_time = parse(get_dis_input['start_time'])
    end_time = parse(get_dis_input['end_time'])
    tree_type = get_dis_input['tree_type']
    note = get_dis_input['note']
    s_start_time = start_time
    s_start_time = s_start_time - timedelta(hours=8)
    end_time = end_time - timedelta(hours=8)
    curr_count = 0
    while True:
        curr_count = curr_count + 1
        add_per_time(10, note, tree_type, user, curr_count, s_start_time.isoformat(), (s_start_time + timedelta(minutes=10)).isoformat())
        s_start_time = s_start_time + timedelta(minutes=10, seconds=1)
        print('下一棵树对应需求时间：' + (s_start_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"))
        if int((end_time - s_start_time).total_seconds()) < 10:
            print(u'执行完毕！！')
            break


# 根據分鐘數種樹
def add_minutes_tree(user):
    get_input = get_minutes_tree()
    per_minutes_tree(user, get_input)
    print(u'执行完毕！！')


# 使用csv檔種樹
def csv_minutes_tree(user):
    rows = get_csv_file()
    for row in rows:
        per_minutes_tree(user, row)
    print(u'执行完毕！！')


# 每天的分鐘種樹
def per_minutes_tree(user, get_input):
    utc_start_time = parse(get_input['start_time']) - timedelta(hours=8)
    minutes = int(get_input['minutes'])
    tree_type = get_input['tree_type']
    note = get_input.get('note', '')
    curr_count = 0
    while minutes > 0:
        curr_count += 1
        real_minutes = min(minutes, 120)
        # 避免下棵樹在 130 < m < 120, m - 120 = 9~1
        if 120 < minutes < 130:
            real_minutes -= 10
        end_time = utc_start_time + timedelta(minutes=real_minutes)
        add_per_time(real_minutes, note, tree_type, user, curr_count, utc_start_time.isoformat(), end_time.isoformat())
        # 下次種植用
        utc_start_time = end_time + timedelta(seconds=1)
        minutes -= real_minutes
        # 顯示改回 UTC+8
        print('下一棵树对应需求时间：' + (utc_start_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)


main()
