#
# Reference:
#
# 一个简单有趣的微信聊天机器人
# https://zhujia.info/2017/06/26/MakeAWechatBot/
#
import threading, time

# 导入模块
from wxpy import *
# from .scheduler import ScheduleThread

schedule_time = ""
stat = {}

# 初始化机器人，扫码登陆
bot = Bot()

def tuling_auto_reply(msg):
    return "reply: " + msg

@bot.register([Friend, Group])
def auto_reply_friend(msg):
    """
    消息自动回复
    """
    print(msg)
    # print("group = " + msg.chat.name)
    # print("name = " + msg.member.name)
    # print("msg.text = " + msg.text)

    if isinstance(msg.chat, Group):
        group = msg.chat.name
        name = msg.member.name
        if group in stat:
            if name in stat[group]['count']:
                stat[group]['count'][name] += 1
            else:
                stat[group]['count'][name] = 1
            flag = True
            for rank in stat[group]['rank']:
                if name == rank['name']:
                    flag = False
                    break
            if flag:
                stat[group]['rank'].append({'name': name, 'time': time.strftime("%H:%M:%S", time.localtime())})
        else:
            stat[group] = {"count": {name: 1}, 'rank': [{'name': name, 'time': time.strftime("%H:%M:%S", time.localtime())}, ]}
        if msg.text == "发言排行榜":
            gs = bot.groups().search(group)
            g = ensure_one(gs)
            if not stat[g.name]:
                return
            msg_text = ""
            index = 1
            count = stat[g.name]['count']
            for name in sorted(count, key=lambda x: count[x], reverse=True):
                # print("{}: {} {}".format(index, rank['name'], rank['time']))
                msg_text += "{}: {} 发言了 {} 次\n".format(index, name, count[name])
                index += 1
            if msg_text:
                msg_text = "发言排行榜：\n" + msg_text
                g.send(msg_text)
        elif msg.text == "起床排行榜":
            gs = bot.groups().search(group)
            g = ensure_one(gs)
            if not stat[g.name]:
                return
            msg_text = ""
            index = 1
            for rank in stat[g.name]['rank']:
                # print("{}: {} {}".format(index, rank['name'], rank['time']))
                msg_text += "{}: {} {}\n".format(index, rank['name'], rank['time'])
                index += 1
            if msg_text:
                msg_text = "起床排行榜：\n" + msg_text
                g.send(msg_text)
        else:
            g.send(msg.text)
        with open('stat.json', 'w') as fh:
            fh.write(json.dumps(stat))
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

def stopThread():
    global stopEvent
    global scheduleThread
    print("[Info] stopThread(), waiting for ...")
    stopEvent.set()
    scheduleThread.join()
    print("[Info] scheduleThread is stopped.")

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
            time.sleep(30)
            cur_time = time.strftime("%H:%M", time.localtime())
            loop += 1
            if loop >= 2:
                loop = 0
                print("[Info] cur_time: {}, schedule_time: {}".format(cur_time, schedule_time))
            if cur_time == schedule_time:
                continue
            elif cur_time == '09:00':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ""
                    index = 1
                    for rank in stat[group.name]['rank']:
                        # print("{}: {} {}".format(index, rank['name'], rank['time']))
                        msg_text += "{}：{} {}\n".format(index, rank['name'], rank['time'])
                        index += 1
                    if msg_text:
                        msg_text = "排行日报\n起床排行榜：\n" + msg_text
                        group.send(msg_text)
            elif cur_time == '23:00':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ""
                    index = 1
                    count = stat[group.name]['count']
                    for name in sorted(count, key=lambda x: count[x], reverse=True):
                        # print("{}: {} {}".format(index, rank['name'], rank['time']))
                        msg_text += "{}：{} 发言了 {} 次\n".format(index, name, count[name])
                        index += 1
                    if msg_text:
                        msg_text = "排行日报\n发言排行榜：\n" + msg_text
                        group.send(msg_text)
            elif cur_time == '00:00':
                stat = dict()
                with open('stat.json', 'w') as fh:
                    fh.write('')
            schedule_time = cur_time

if __name__ == "__main__":
    # print("__main__ = " + __name__)
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

embed()
