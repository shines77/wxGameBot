#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Reference:
#
#     一个简单有趣的微信聊天机器人
#     https://zhujia.info/2017/06/26/MakeAWechatBot/
#
# 导入模块
from wxpy import *

import threading, time, json, re
import chardet
import sys

PY_VERSION = sys.version
PY2 = PY_VERSION < '3'

if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    import importlib
    importlib.reload(sys)

# re.split(' |\t|\v|\r|\n|\f|~|,|;|:|\?|`|!|@|#|\$|\%|\^|&|\*|\.|\/|\|\'|\"', '123,456,789')
# re.split(' |`|!|@|#|\$|\%|\^|&|\*|\?|~|,|;|:|/|\.|\'|\"|\t|\v|\r|\n|\f|\|', '123,456,789')
# re.split('，|;|。|‘|“|”', '123,456,789')
# re.split(r'[,;:~!@#\$\%\^\*\?~\.\'\"\t\v\f\r\n|]', '123,456,789')
# re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123,456,789')
# re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/，；。‘’“”？·、！　]', '123,456,789')

# msg_delimiter = '@|#|$|%|`|!|^|&|*|,|;|||/|\\|\.|\'|\"| |，|;|。|‘|“|”'
# msg_delimiter = ' |`|!|@|#|\$|\%|\^|&|\*|\?|~|,|;|:|/|\.|\'|\"|\t|\v|\r|\n|\f|\|'

# msg_delimiter = r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/，；。‘’“”？·、！　]'
msg_delimiter = ' |`|!|@|#|\$|\%|\^|&|\*|\?|~|,|;|:|/|\.|\'|\"|\t|\v|\r|\n|\f|\||，|；|。|‘|’|“|”|？|·|、|！|　'
wait_time_sec = 10

schedule_time = ""
stat = {}

# 初始化机器人，扫码登陆
bot = Bot(cache_path = False, console_qr = 1)

fingerGuessGame = None
finger_game_time = ''
finger_stop_event = threading.Event()

def str_split(str, seperators):
    result = [str]
    for seperator in seperators:
        tokens = []
        map(lambda t: tokens.extend(t.split(seperator)), result)
        # print('result is ', result)
        result = tokens
    return result

def str_length(str):
    length = len(str)
    utf8_length = len(str.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return length

class FingerGuessGame(threading.Thread):
    def __init__(self, group, friends, players, stop_event = None):
        super(FingerGuessGame, self).__init__()
        self.group = group
        self.friends = friends
        self.players = players
        self.stop_event = stop_event
        self.heart_time = 1

    def reset(self):
        self.stage = 0
        self.score = []

    def start(self):
        self.reset()

        msg_text = '“剪刀石头布” 游戏创建成功！\n\n参与的玩家是：\n\n'
        for player in self.players:
            msg_text += '　' + player + '\n'
        msg_text += '\n请以上玩家点击我的头像，私密我回复数字 66，代表开始游戏，注意不是发在当前群里，而是私密我！'
        self.group.send(msg_text)

    def terminate(self):
        self.stop()

    def stop(self):
        global fingerGuessGame
        print('[Info] Stopping FingerGuessGame thread, waiting for a while...')
        self.stop_event.set()
        if fingerGuessGame != None:
            fingerGuessGame.join()
            print('[Info] FingerGuessGame thread have stopped.')

    def run(self):
        global finger_game_time
        global bot
        loop = 0
        start_time = time.time()
        while not self.stop_event.isSet():
            time.sleep(self.heart_time)
            loop += 1
            if loop >= (300 / self.heart_time):
                loop = 0
            cur_time = time.time()
            if (cur_time - start_time) > 60 * 1000:
                start_time = time.time()

def stop_finger_guess_game():
    if fingerGuessGame != None:
        fingerGuessGame.terminate()

def create_finger_guess_game(group, players):
    global fingerGuessGame
    global bot
    # print('create_finger_guess_game(): enter ...')
    # group.send('正在创建 "剪刀石头布" 游戏……')
    if fingerGuessGame != None:
        # print('create_finger_guess_game(): fingerGuessGame != None')
        group.send('警告：\n　　一个群在同一时刻只能创建一个 “剪刀石头布” 游戏，请先结束当前游戏！')
    else:
        friends = []
        # print('create_finger_guess_game(): get friends.')
        for player in players:
            # print(player)
            friend = bot.friends().search(player)
            # print(len(friend))
            # print(friend)
            if len(friend) > 0:
                friend = ensure_one(friend)
                if friend in group:
                    friends.append(friend)
                else:
                    group.send('错误：\n　　玩家: [" + player + "] 不在当前微信群里，不能正常启动游戏！')
                    return
            else:
                group.send('错误：\n　　玩家: [" + player + "] 还未添加本游戏机器人的微信好友，受邀请的玩家必须先把我加为好友，才能进行游戏！')
                return
        if len(friends) == len(players):
            finger_stop_event.clear()
            game = FingerGuessGame(group, friends, players, finger_stop_event)
            if game != None:
                game.start()
                fingerGuessGame = game
            else:
                group.send('“剪刀石头布” 游戏创建失败！')
        else:
            group.send('错误：\n　　还有玩家还未添加本游戏机器人的微信好友！')
    
    # print('create_finger_guess_game(): leave ...')

def tuling_auto_reply(msg):
    return "reply: " + msg

def handle_group_message(msg):
    global msg_delimiter
    group_name = msg.chat.name
    member_name = msg.member.name

    if group_name in stat:
        if member_name in stat[group_name]['count']:
            stat[group_name]['count'][member_name] += 1
        else:
            stat[group_name]['count'][member_name] = 1
        flag = True
        for rank in stat[group_name]['rank']:
            if member_name == rank['name']:
                flag = False
                break
        if flag:
            stat[group_name]['rank'].append({'name': member_name, 'time': time.strftime("%H:%M:%S", time.localtime())})
    else:
        stat[group_name] = {"count": {member_name: 1}, 'rank': [{'name': member_name, 'time': time.strftime("%H:%M:%S", time.localtime())}, ]}

    group = bot.groups().search(group_name)
    if len(group) > 0:
        if len(group) > 1:
            print('Error: group_name = [{}]，与该群同名的群不止一个，一共有 {} 个。'.format(group_name, len(group)))
        group = ensure_one(group)
    else:
        print('Error: group_name = [' + group_name + ']，找不到该群。')
        return

    if msg.text == '发言排名' or msg.text == '发言排行榜':
        if not stat[group.name]:
            return
        msg_text = ""
        index = 1
        count = stat[group.name]['count']
        for name in sorted(count, key=lambda x: count[x], reverse=True):
            # print('{}: {} {}'.format(index, rank['name'], rank['time']))
            msg_text += '{}: {} 发言了 {} 次\n'.format(index, name, count[name])
            index += 1
        if msg_text:
            msg_text = msg.text + '：\n' + msg_text
            group.send(msg_text)
    elif msg.text == '起床排名' or msg.text == '起床排行榜':
        if not stat[group.name]:
            return
        msg_text = ""
        index = 1
        for rank in stat[group.name]['rank']:
            # print('{}: {} {}'.format(index, rank['name'], rank['time']))
            msg_text += '{}: {} {}\n'.format(index, rank['name'], rank['time'])
            index += 1
        if msg_text:
            msg_text = msg.text + '：\n' + msg_text
            group.send(msg_text)
    else:
        # print('msg_delimiter = " + msg_delimiter)
        tokens = re.split(msg_delimiter, msg.text)
        tokens = [t for t in tokens if t]
        # print(tokens)

        if len(tokens) >= 1:
            if tokens[0] == '猜拳':
                # 猜拳游戏
                if len(tokens) >= 2 and tokens[1] == '邀请':
                    # 邀请玩家, 格式: @玩家1, @玩家2, @玩家3, @我f
                    tmp_players = msg.text.split('@')
                    # print(tmp_players)
                    players = []
                    if len(tmp_players) >= 2:
                        tmp_players.pop(0)
                        for player in tmp_players:
                            # print(player)
                            player = player.strip()
                            player = player.strip('\u2005')
                            player = player.strip('　')
                            if player == '我':
                                players.append(member_name)
                            else:
                                players.append(player)
                    print(players)
                    if len(players) > 4:
                        group.send('抱歉，"剪刀石头布" 游戏仅支持2至4名玩家，人太多了玩不转！请重新邀请玩家。')
                    if len(players) >= 2:
                        create_finger_guess_game(group, players)
                    else:
                        group.send('抱歉，"剪刀石头布" 游戏必须两人或两人以上才行进行！请重新邀请玩家。')

        elif len(msg.text) != 0:
            print(msg.text)

def handle_friend_message(msg):
    global msg_delimiter

    name = msg.chat.name
    # print('name = ' + name)
    # print('msg.text = ' + msg.text)

    # print('msg_delimiter = ' + msg_delimiter)
    tokens = re.split(msg_delimiter, msg.text)
    tokens = [t for t in tokens if t]
    print(tokens)

@bot.register([Friend, Group])
def auto_reply_friend(msg):
    """
    消息自动回复
    """
    print(msg)
    """
    if isinstance(msg.chat, Group):
        print('group = ' + msg.chat.name)
        print('name = ' + msg.member.name)
    elif isinstance(msg.chat, Friend):
        print('name = ' + msg.chat.name)
    print('msg.text = ' + msg.text)
    """

    if isinstance(msg.chat, Group):
        # Handle group message
        handle_group_message(msg)

        with open('stat.json', 'w') as fh:
            fh.write(json.dumps(stat))
            
        if not msg.is_at:
            return
    elif isinstance(msg.chat, Friend):
        # Handle friend message
        handle_friend_message(msg)

        if not msg.is_at:
            return        

    return tuling_auto_reply(msg)

# 打印来自其他好友、群聊和公众号的消息
# @bot.register()
# def print_others(msg):
#    print(msg)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求')

def stopBot():
    bot.logout()
    time.sleep(1)
    stopThread()

def stopThread():
    global stopEvent
    global scheduleThread
    print('[Info] Stopping ScheduleThread, waiting for {} seconds...'.format(wait_time_sec))
    stopEvent.set()
    scheduleThread.join()
    print('[Info] ScheduleThread have stopped.')

class ScheduleThread(threading.Thread):
    """
    @summary: 初始化对象。
    @param thread_name: 线程名称。
    """
    def __init__(self, threadName, stopEvent = None):
        # 注意：一定要显式的调用父类的初始化函数。
        super(ScheduleThread, self).__init__(name = threadName)
        self.stopEvent = stopEvent

    """
    计划任务线程
    """
    def run(self):
        global schedule_time
        global bot
        global stat
        loop = 0
        while not self.stopEvent.isSet():
            time.sleep(wait_time_sec)
            cur_time = time.strftime('%H:%M', time.localtime())
            loop += 1
            if loop >= (300 / wait_time_sec):
                loop = 0
                print('[Info] cur_time: {}, schedule_time: {}'.format(cur_time, schedule_time))
            if cur_time == schedule_time:
                continue
            elif cur_time == '09:00':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ''
                    index = 1
                    for rank in stat[group.name]['rank']:
                        # print('{}: {} {}'.format(index, rank['name'], rank['time']))
                        msg_text += '{}：{} {}\n'.format(index, rank['name'], rank['time'])
                        index += 1
                    if msg_text:
                        msg_text = '排行日报\n起床排行榜：\n' + msg_text
                        group.send(msg_text)
            elif cur_time == '23:00':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ''
                    index = 1
                    count = stat[group.name]['count']
                    for name in sorted(count, key=lambda x: count[x], reverse=True):
                        # print('{}: {} {}'.format(index, rank['name'], rank['time']))
                        msg_text += '{}：{} 发言了 {} 次\n'.format(index, name, count[name])
                        index += 1
                    if msg_text:
                        msg_text = '排行日报\n发言排行榜：\n' + msg_text
                        group.send(msg_text)
            elif cur_time == '00:00':
                stat = dict()
                with open('stat.json', 'w') as fh:
                    fh.write('')
            schedule_time = cur_time

if __name__ == '__main__':
    # print('__main__ = ' + __name__)

    stopEvent = threading.Event()
    scheduleThread = ScheduleThread("scheduler", stopEvent)
    scheduleThread.start()

# | ① ♠ 2 | ② ♡ 3 | ③ ♠ 4 | ④ ♢ 5
# | ⑤ ♠ 7 | ⑥ ♡ 8 | ⑦ ♣ 9 | ⑧ ♢ 10

# ① ♠ 2 ② ♥ 3 ③ ♠ 4 ④ ♣ 5
# ⑤ ♠ 7 ⑥ ♡ 8 ⑦ ♠ 9 ⑧ ♢10

#　※ 空 |　※ 空 | 　※ 空 | 　※ 空
# ♠ 2 | ♥ 3 | ♣ 4 | ♦ 5
# ♠ 7 | ♥ 8 | ♣ 9 | ♦10

"""
剩余公共牌：40 张
♠ 2(4) ♥ 3(2) ♣ 4(2) ♦ 5(3)
♠ 7(1) ♥ 8(3) ♣ 9(1) ♦10(5)
请选择一堆牌，并猜下一张公共牌比它大还是小？
❤ ♥
"""

# bot.join()
embed()
