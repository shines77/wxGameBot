
import threading, time

class ScheduleThread(threading.Thread):
    """
    @summary: 初始化对象。
    @param threadName: 线程名称。
    """
    def __init__(self, thread_name):
        # 注意：一定要显式的调用父类的初始化函数。
    super(ScheduleThread, self).__init__(name = thread_name)

    """
    计划任务线程
    """
    def run(self):
        global schedule_time
        global bot
        global stat
        while 1:
            time.sleep(300)
            cur_hour = time.strftime("%H", time.localtime())
            print("cur:{}\tschedule:{}".format(cur_hour, schedule_time))
            if cur_hour == schedule_time:
                continue
            elif cur_hour == '09':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ""
                    index = 1
                    for rank in stat[group.name]['rank']:
                        # print("{}: {} {}".format(index, rank['name'], rank['time']))
                        msg_text += "{}: {} {}\n".format(index, rank['name'], rank['time'])
                        index += 1
                    if msg_text:
                        msg_text = "排行日报\n起床排行榜：\n" + msg_text
                        group.send(msg_text)
            elif cur_hour == '20':
                for group in bot.groups():
                    print(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ""
                    index = 1
                    count = stat[group.name]['count']
                    for name in sorted(count, key=lambda x: count[x], reverse=True):
                        # print("{}: {} {}".format(index, rank['name'], rank['time']))
                        msg_text += "{}: {} 发言了 {} 次\n".format(index, name, count[name])
                        index += 1
                    if msg_text:
                        msg_text = "排行日报\n发言排行榜：\n" + msg_text
                        group.send(msg_text)
            elif cur_hour == '00':
                stat = dict()
                with open('stat.json', 'w') as fh:
                    fh.write('')
            schedule_time = cur_hour
