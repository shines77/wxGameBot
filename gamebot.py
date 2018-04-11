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
from enum import unique, Enum, IntEnum

import threading, time, json, re
import chardet
import sys, math
import traceback

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
wait_time_sec = 5

schedule_time = ""
stat = {}

# 初始化机器人，扫码登陆
bot = Bot(cache_path = False, console_qr = 1)

# 0: None, 1: FingerGuessGame, 2: PokerGuessGame
current_game = 0

# FingerGuessGame
fingerGuessGame = None
finger_game_time = ''
finger_stop_event = threading.Event()

@unique
class LogType(IntEnum):
    OFF = 0
    DEFAULT = 1
    INFO = 2
    WARNING = 3
    VERBO = 4
    TRACE = 5
    DEBUG = 6
    ERROR = 7
    FATAL = 8
    CRITICAL = 9
    ALL = 10

class Console:
    def __init__(self, level = LogType.WARNING):
        self.level = level

    def join_text(self, log_type, *args):
        text = log_type
        i = 0
        for (arg,) in args:
            i += 1
            if i < len(args):
                text += str(arg) + ' '
            else:
                text += str(arg)
        return text

    def print(self, *args):
        if self.level.value >= LogType.DEFAULT.value:
            text = self.join_text('', args)
            print(text)

    def log(self, *args):
        if self.level.value >= LogType.DEFAULT.value:
            text = self.join_text("[Default] ", args)
            print(text)

    def info(self, *args):
        if self.level.value >= LogType.INFO.value:
            text = self.join_text("[Info] ", args)
            print(text)

    def warn(self, *args):
        if self.level.value >= LogType.WARNING.value:
            text = self.join_text("[Warning] ", args)
            print(text)

    def verbo(self, *args):
        if self.level.value >= LogType.VERBO.value:
            text = self.join_text("[Verbo] ", args)
            print(text)

    def trace(self, *args):
        if self.level.value >= LogType.TRACE.value:
            text = self.join_text("[Trace] ", args)
            print(text)

    def debug(self, *args):
        if self.level.value >= LogType.DEBUG.value:
            text = self.join_text("[Debug] ", args)
            print(text)

    def error(self, *args):
        if self.level.value >= LogType.ERROR.value:
            text = self.join_text("[Error] ", args)
            print(text)

    def fatal(self, *args):
        if self.level.value >= LogType.FATAL.value:
            text = self.join_text("[Fatal] ", args)
            print(text)

    def critical(self, *args):
        if self.level.value >= LogType.CRITICAL.value:
            text = self.join_text("[Critical] ", args)
            print(text)

    def nothing(self, *args):
        if self.level.value > LogType.ALL.value:
            text = self.join_text("[nothing] ", args)
            print(text)

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

def display_exception(err):
    global console
    console.warn('=============================================================')
    # console.warn('str(Exception):        ', str(Exception))
    console.warn('str(err):              ', str(err))
    console.warn('repr(err):             ', repr(err))
    console.warn('traceback.print_exc(): ', traceback.print_exc())
    console.warn('traceback.format_exc():\n%s' % traceback.format_exc())
    console.warn('=============================================================')

def send_group_msg(group, msg_text):
    global console
    if group != None:
        group.send(msg_text)
    msg_text = msg_text.replace('\n', '')
    console.info(msg_text)

@unique
class FingerType(IntEnum):
    Unknown = -1
    Rock = 0
    Scissors = 1
    Paper = 2

@unique
class WinnerType(IntEnum):
    Unknown = -1
    Rock = 0
    Scissors = 1
    Paper = 2
    Deuce1 = 3
    Deuce3 = 4
    Error0 = 5
    Error2 = 6
    Error = 7

def get_finger_value(finger_type):
    if finger_type == FingerType.Rock:
        return 0
    elif finger_type == FingerType.Scissors:
        return 1
    elif finger_type == FingerType.Paper:
        return 2
    else:
        return -1

def get_winner_value(winner_type):
    if winner_type == WinnerType.Rock:
        return 0
    elif winner_type == WinnerType.Scissors:
        return 1
    elif winner_type == WinnerType.Paper:
        return 2
    elif winner_type == WinnerType.Deuce1:
        return 3
    elif winner_type == WinnerType.Deuce3:
        return 4
    elif winner_type == WinnerType.Error0:
        return 5
    elif winner_type == WinnerType.Error2:
        return 6
    elif winner_type == WinnerType.Error:
        return 7
    else:
        return -1

# '👊', '✌', '👋', '✋'
def get_finger_emote(finger_type):
    if finger_type == FingerType.Rock:
        return '[拳头]'
    elif finger_type == FingerType.Scissors:
        return '[胜利]'
    elif finger_type == FingerType.Paper:
        return '👋'
    else:
        return '[疑问]'

def get_finger_short_name(finger_type):
    if finger_type == FingerType.Rock:
        return '石头'
    elif finger_type == FingerType.Scissors:
        return '剪刀'
    elif finger_type == FingerType.Paper:
        return '布'
    else:
        return '未知'

def get_finger_name(finger_type):
    try:
        if finger_type == FingerType.Rock:
            return '[拳头] (石头)'
        elif finger_type == FingerType.Scissors:
            return '[胜利] (剪刀)'
        elif finger_type == FingerType.Paper:
            return '[OK] (布)'
        else:
            return '[疑问] (未知)'
    except Exception as err:
        display_exception(err)            

class FingerGuessGame(threading.Thread):
    def __init__(self, group, friends, players, stop_event = None):
        super(FingerGuessGame, self).__init__()
        self.group = group
        self.friends = friends
        self.players = players
        self.total_players = len(players)
        self.stop_event = stop_event

        self.heart_time = 1
        self.reset()

    def reset(self):
        self.playing = False
        self.running = False
        self.stage = 0
        self.max_stage = 7
        self.results = {}
        self.scores = {}
        for player in self.players:
            self.scores[player] = { 'win': 0, 'lose': 0, 'deuce': 0, 'error': 0 }

    def is_playing(self):
        return self.playing

    def is_running(self):
        return self.running

    def is_valid_player(self, name):
        for player in self.players:
            if name == player:
                return True
        return False

    def make_player_msg(self, player_name, winner_type):
        global console
        console.trace("make_player_msg(): enter.")
        msg_text = ''
        console.info(self.results)
        try:
            msg_out = '第{}轮: '.format(self.stage + 1)
            i = 0
            for player in self.players:
                if player in self.results:
                    msg_out += get_finger_emote(self.results[player])
                else:
                    msg_out += '[衰]'
                if player == player_name:
                    msg_out += ' *'
                i += 1
                if i < len(self.players):
                    msg_out += ' vs '

            if (player_name in self.results):
                if (get_winner_value(winner_type) >= 0 and get_winner_value(winner_type) <= 2) \
                    and (get_winner_value(winner_type) == get_finger_value(self.results[player_name])):
                    msg_text = '你赢了!'
                elif (get_winner_value(winner_type) >= 0 and get_winner_value(winner_type) <= 2) \
                    and (get_winner_value(winner_type) != get_finger_value(self.results[player_name])):
                    msg_text = '你输了!'
                else:
                    if winner_type == WinnerType.Deuce1:
                        msg_text = '平局!'
                    elif winner_type == WinnerType.Deuce3:
                        msg_text = '平局!'
                    elif (winner_type == WinnerType.Error) \
                        or (winner_type == WinnerType.Error0) \
                        or (winner_type == WinnerType.Error2):
                        msg_text = '未知错误! (Error：' + str(winner_type.value) + ')'
                    elif winner_type == WinnerType.Unknown:
                        msg_text = '未知错误! [Unknown]'
                    else:
                        msg_text = '其他错误! (Error：' + str(winner_type.value) + ')'
            else:
                msg_text = '错误：你不在游戏列表中! (Error：' + str(winner_type.value) + ')'

        except Exception as err:
            display_exception(err)
        console.trace("make_player_msg(): leave.")
        return (msg_out + ' , ' + msg_text)

    def make_group_msg(self, winner_type, msg_text):
        global console
        console.trace("make_group_msg(): enter.")
        try:
            winner_list = []
            msg_out = '第{}轮: '.format(self.stage + 1)
            i = 0
            for player in self.players:
                i += 1
                if player in self.results:
                    msg_out += get_finger_emote(self.results[player])
                    if (get_winner_value(winner_type) >= 0 and get_winner_value(winner_type) <= 2) \
                        and (get_winner_value(winner_type) == get_finger_value(self.results[player])):
                        if len(self.players) < 4:
                            winner_list.append('[{}]'.format(player))
                        else:
                            winner_list.append('[{}][{}]'.format(i, player))
                else:
                    msg_out += '[衰]'
                if i < len(self.players):
                    msg_out += ' vs '

            msg_text = ''
            if (winner_type == WinnerType.Rock) \
                or (winner_type == WinnerType.Scissors) \
                or (winner_type == WinnerType.Paper):
                winner_str = ''
                i = 0
                for winner in winner_list:
                    winner_str += winner
                    i += 1
                    if i < len(winner_list):
                        winner_str += ', '
                msg_text = winner_str + ' 赢!'
            else:
                if winner_type == WinnerType.Deuce1:
                    msg_text = '平局!'
                elif winner_type == WinnerType.Deuce3:
                    msg_text = '平局!'
                elif (winner_type == WinnerType.Error) \
                    or (winner_type == WinnerType.Error0) \
                    or (winner_type == WinnerType.Error2):
                    msg_text = '未知错误! (Error：' + str(winner_type.value) + ')'
                elif winner_type == WinnerType.Unknown:
                    msg_text = '未知错误! [Unknown]'
                else:
                    msg_text = '其他错误! (Error：' + str(winner_type.value) + ')'

        except Exception as err:
            display_exception(err)
        console.trace("make_group_msg(): leave.")
        return (msg_out + ' , ' + msg_text)

    def send_group_msg(self, msg_text):
        global console
        console.trace("send_group_msg(): enter.")
        try:
            self.group.send(msg_text)
            msg_text = msg_text.replace('\n', '')
            console.info(msg_text)
        except Exception as err:
            display_exception(err)
        console.trace("send_group_msg(): leave.")

    def send_msg(self, winner_type, msg_text):
        global console
        console.trace("FingerGuessGame::send_msg(): enter.")
        try:
            for friend in self.friends:
                player_name = friend.name
                console.trace("send_msg(): player_name = " + player_name)
                player_msg = self.make_player_msg(player_name, winner_type)
                friend.send(player_msg)
            group_msg = self.make_group_msg(winner_type, msg_text)
            if self.group != None:
                self.group.send(group_msg)
            # group_msg = group_msg.replace('\n', '')
            console.info(group_msg)
        except Exception as err:
            display_exception(err)
        console.trace("FingerGuessGame::send_msg(): leave.")

    def counter_winlose(self, winner_type):
        global console
        console.trace("counter_winlose(): enter.")
        winner_value = get_winner_value(winner_type)
        try:
            if (winner_type == WinnerType.Rock) \
                or (winner_type == WinnerType.Scissors) \
                or (winner_type == WinnerType.Paper):
                for player in self.players:
                    if player in self.results:
                        if winner_value == get_finger_value(self.results[player]):
                            if ('win' in self.scores[player]):
                                self.scores[player]['win'] += 1
                            else:
                                self.scores[player]['win'] = 1
                        else:
                            if ('lose' in self.scores[player]):
                                self.scores[player]['lose'] += 1
                            else:
                                self.scores[player]['lose'] = 1
            else:
                if winner_type == WinnerType.Deuce1 or winner_type == WinnerType.Deuce3:
                    for player in self.players:
                        if player in self.results:
                            if ('deuce' in self.scores[player]):
                                self.scores[player]['deuce'] += 1
                            else:
                                self.scores[player]['deuce'] = 1
                else:
                    for player in self.players:
                        if player in self.results:                    
                            if ('error' in self.scores[player]):
                                self.scores[player]['error'] += 1
                            else:
                                self.scores[player]['error'] = 1

        except Exception as err:
            display_exception(err)

        console.trace("counter_winlose(): leave.")
    
    def display_summary(self):
        max_wins = math.floor((self.max_stage + 1) / 2)
        msg_text = '胜负统计：({}盘{}胜)\n\n'.format(self.max_stage, max_wins)

        i = 0
        for player in self.scores:
            win = 0
            lose = 0
            deuce = 0
            error = 0            
            if 'win' in self.scores[player]:
                win = self.scores[player]['win']
            if 'lose' in self.scores[player]:
                lose = self.scores[player]['lose']
            if 'deuce' in self.scores[player]:
                deuce = self.scores[player]['deuce']
            if 'error' in self.scores[player]:
                error = self.scores[player]['error']
            win_rate = math.floor((win * 1000.0) / (win + deuce + lose + error)) / 10.0
            msg_text += '[0{}] [{}]：\n胜：{}，平：{}，负：{}，胜率：{}%\n' \
                .format(i + 1, player, win, deuce, lose, win_rate)
            i += 1
            if i < len(self.scores):
                msg_text += '\n'

        for friend in self.friends:
            friend.send(msg_text)        

        self.group.send(msg_text)
        console.info(msg_text)

    def is_gameover(self):
        b_gameover = False
        max_wins = math.floor((self.max_stage + 1) / 2)
        for player in self.scores:
            if 'win' in self.scores[player]:
                if self.scores[player]['win'] >= max_wins:
                    b_gameover = True
                    break

        if b_gameover:
            self.display_summary()
            self.stop()

        return b_gameover

    def start(self):
        global console
        console.trace("FingerGuessGame::start(): enter.")
        try:
            if not self.is_playing():
                self.reset()
                self.playing = True

                msg_text = '“石头剪刀布” 游戏创建成功！\n\n参与的玩家是：\n\n'
                i = 1
                for player in self.players:
                    msg_text += ' [0{}] [{}] \n'.format(i, player)
                    i += 1
                msg_text += '\n请以上玩家私密我，回复数字 66，表示确认。'
                self.send_group_msg(msg_text)
            else:
                self.send_group_msg('错误：\n游戏已经在进行中！')
        except Exception as err:
            display_exception(err)
        console.trace("FingerGuessGame::start(): leave.")

    def terminate(self):
        self.stop()

    def stop(self):
        global console
        global fingerGuessGame
        console.trace("FingerGuessGame::stop(): enter.")
        try:
            if self.is_playing():
                console.info('Stopping FingerGuessGame thread, waiting for...')
                self.stop_event.set()
                if fingerGuessGame != None:
                    if self.is_running():
                        fingerGuessGame.join()
                    console.info('FingerGuessGame thread have stopped.')
                    self.running = False
                self.playing = False
        except Exception as err:
            display_exception(err)
        console.trace("FingerGuessGame::stop(): leave.")

    def play(self, name, finger_type):
        global console
        console.trace('FingerGuessGame::play(): enter.')
        try:
            console.info('play(): name = {}, finger_type = {}'.format(name, finger_type))
            if self.is_playing():
                if self.is_valid_player(name):
                    # console.trace('[Info]: is a valid player.')
                    self.results[name] = finger_type
                    # console.trace("self.results = ")
                    # console.trace(self.results)
                    if len(self.results) == self.total_players:
                        self.judge()
                        self.results.clear()
                        self.stage += 1
                # else:
                    # console.trace('[Error]: is a invalid player.')
            else:
                # self.send_group_msg('错误：\n游戏没有开始！')
                console.info('错误：\n游戏没有开始！')
        except Exception as err:
            display_exception(err)
        console.trace('FingerGuessGame::play(): leave.')

    def judge(self):
        # 判断输赢
        global console
        console.trace('FingerGuessGame::judge(): enter.')
        try:
            # console.info(self.results)

            finger_info = {}
            for name, finger_type in self.results.items():
                if not finger_info.get(finger_type):
                    finger_info[finger_type] = []
                finger_info[finger_type].append(name)
            console.info(finger_info)

            winner_type = WinnerType.Unknown

            if len(finger_info) == 3:
                winner_type = WinnerType.Deuce3
                self.send_msg(winner_type, '没人输也没人赢，平局！')
            elif len(finger_info) == 1:
                winner_type = WinnerType.Deuce1
                if finger_info.get(FingerType.Rock):
                    self.send_msg(winner_type, '大家出的都是 [拳头] (石头)，平局！')
                elif finger_info.get(FingerType.Scissors):
                    self.send_msg(winner_type, '大家出的都是 [胜利] (剪刀)，平局！')
                elif finger_info.get(FingerType.Paper):
                    self.send_msg(winner_type, '大家出的都是 [OK] (布)，平局！')
                else:
                    self.send_msg(winner_type, '大家出的都是一样的拳，且是未知类型，平局！')
            elif len(finger_info) == 0:
                winner_type = WinnerType.Error0
                self.send_msg(winner_type, '错误：\n抱歉，没有人出拳！')
            elif len(finger_info) == 2:
                """
                fingers = []
                for finger in finger_info.keys():
                    fingers.append(finger)
                console.info(fingers)
                if (fingers[0] == FingerType.Rock and fingers[1] == FingerType.Scissors) \
                    or (fingers[0] == FingerType.Scissors and fingers[1] == FingerType.Rock):
                    winner_type = WinnerType.Rock
                    self.send_msg(winner_type, '出 [拳头] (石头) 的玩家获胜！')
                elif (fingers[0] == FingerType.Rock and fingers[1] == FingerType.Paper) \
                    or (fingers[0] == FingerType.Paper and fingers[1] == FingerType.Rock):
                    winner_type = WinnerType.Paper
                    self.send_msg(winner_type, '出 [OK] (布) 的玩家获胜！')
                elif (fingers[0] == FingerType.Scissors and fingers[1] == FingerType.Paper) \
                    or (fingers[0] == FingerType.Paper and fingers[1] == FingerType.Scissors):
                    winner_type = WinnerType.Scissors
                    self.send_msg(winner_type, '出 [胜利] (剪刀) 的玩家获胜！')
                else:
                    winner_type = WinnerType.Error2
                    self.send_msg(winner_type, '错误：\n未知错误！')
                """
                if finger_info.get(FingerType.Rock):
                    if finger_info.get(FingerType.Scissors):
                        winner_type = WinnerType.Rock
                        self.send_msg(winner_type, '出 [拳头] (石头) 的玩家获胜！')
                    elif finger_info.get(FingerType.Paper):
                        winner_type = WinnerType.Paper
                        self.send_msg(winner_type, '出 [OK] (布) 的玩家获胜！')
                elif finger_info.get(FingerType.Scissors):
                    if finger_info.get(FingerType.Paper):
                        winner_type = WinnerType.Scissors
                        self.send_msg(winner_type, '出 [胜利] (剪刀) 的玩家获胜！')
                    else:
                        winner_type = WinnerType.Scissors
                        self.send_msg(winner_type, '错误：\n只有出 [胜利] (剪刀) 的玩家，且存在未知类型的出拳！')
                elif finger_info.get(FingerType.Paper):
                    winner_type = WinnerType.Paper
                    self.send_msg(winner_type, '错误：\n只有出 [OK] (布) 的玩家，且存在未知类型的出拳！')
                else:
                    winner_type = WinnerType.Error2
                    self.send_msg(winner_type, '错误：\n未知错误！')
            else:
                winner_type = WinnerType.Error
                self.send_msg(winner_type, '错误：\n出拳类型超过 3 种！')
            
            self.counter_winlose(winner_type)
            self.is_gameover()

        except Exception as err:
            display_exception(err)

        console.trace('FingerGuessGame::judge(): leave.')

    def run(self):
        global console
        global finger_game_time
        global bot
        loop = 0
        start_time = time.time()
        self.running = True
        while not self.stop_event.isSet():
            time.sleep(self.heart_time)
            loop += 1
            if loop >= (300 / self.heart_time):
                loop = 0
            cur_time = time.time()
            if (cur_time - start_time) > 60 * 1000:
                start_time = time.time()

def stop_finger_guess_game():
    global current_game
    global fingerGuessGame
    if current_game == 1 and fingerGuessGame != None:
        fingerGuessGame.terminate()
        current_game = 0
        fingerGuessGame = None

def create_finger_guess_game(group, players):
    global console
    global current_game
    global fingerGuessGame
    global bot
    console.trace('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    console.trace('create_finger_guess_game(): enter.')
    try:
        if current_game != 0:
            if current_game == 1:
                send_group_msg(group, '警告：\n　　一个群在同一时刻只能创建一个 “石头剪刀布” 游戏，请先结束当前游戏！')
            else:
                send_group_msg(group, '警告：\n　　一个群在同一时刻只能创建一个游戏，请先结束当前游戏！')
            return
        # send_group_msg(group, '正在创建 "石头剪刀布" 游戏……')
        if fingerGuessGame != None:
            # console.trace('create_finger_guess_game(): fingerGuessGame != None')
            send_group_msg(group, '警告：\n　　一个群在同一时刻只能创建一个 “石头剪刀布” 游戏，请先结束当前游戏！')
        else:
            friends = []
            # console.trace('create_finger_guess_game(): get friends.')
            for player in players:
                # console.info(player)
                friend = bot.friends().search(player)
                # console.info(len(friend))
                # console.info(friend)
                if len(friend) > 0:
                    friend = ensure_one(friend)
                    if friend in group:
                        friends.append(friend)
                    else:
                        send_group_msg(group, '错误：\n　　玩家: [" + player + "] 不在当前微信群里，不能正常启动游戏！')
                        return
                else:
                    send_group_msg(group, '错误：\n　　玩家: [" + player + "] 还未添加本游戏机器人的微信好友，受邀请的玩家必须先把我加为好友，才能进行游戏！')
                    return
            if len(friends) == len(players):
                finger_stop_event.clear()
                game = FingerGuessGame(group, friends, players, finger_stop_event)
                if game != None:
                    game.start()
                    current_game = 1
                    fingerGuessGame = game
                else:
                    send_group_msg(group, '“石头剪刀布” 游戏创建失败！')
            else:
                send_group_msg(group, '错误：\n　　还有玩家还未添加本游戏机器人的微信好友！')
    except Exception as err:
        display_exception(err)

    console.trace('create_finger_guess_game(): leave.')
    console.trace('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

def tuling_auto_reply(msg):
    return "reply: " + msg

def handle_group_message(msg):
    global console
    global msg_delimiter

    try:
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
                console.error('Error: group_name = [{}]，与该群同名的群不止一个，一共有 {} 个。'.format(group_name, len(group)))
            group = ensure_one(group)
        else:
            console.error('Error: group_name = [' + group_name + ']，找不到该群。')
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
            # console.info('msg_delimiter = " + msg_delimiter)
            tokens = re.split(msg_delimiter, msg.text)
            tokens = [t for t in tokens if t]
            # console.info(tokens)

            if len(tokens) >= 1:
                if tokens[0] == '猜拳':
                    # 猜拳游戏
                    if len(tokens) >= 2 and tokens[1] == '邀请':
                        # 邀请玩家, 格式: @玩家1, @玩家2, @玩家3, @我f
                        tmp_players = msg.text.split('@')
                        # console.info(tmp_players)
                        players = []
                        if len(tmp_players) >= 2:
                            tmp_players.pop(0)
                            for player in tmp_players:
                                # console.info(player)
                                player = player.strip()
                                player = player.strip('\u2005')
                                player = player.strip('　')
                                if player == '我':
                                    players.append(member_name)
                                else:
                                    players.append(player)
                        console.info(players)
                        if len(players) > 4:
                            send_group_msg(group, '抱歉，"石头剪刀布" 游戏仅支持2至4名玩家，人太多了不好玩！请减少邀请的玩家数。')
                        if len(players) >= 2:
                            create_finger_guess_game(group, players)
                        else:
                            send_group_msg(group, '抱歉，"石头剪刀布" 游戏必须两人或两人以上才行进行！请重新邀请玩家。')
            elif len(msg.text) != 0:
                console.info(msg.text)

    except Exception as err:
        display_exception(err)

def play_finger_guess_game(name, action):
    global console
    global current_game
    global fingerGuessGame
    console.info('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    console.trace("play_finger_guess_game(): enter.")

    try:
        if fingerGuessGame != None:
            if fingerGuessGame.is_playing():
                action = action.strip()
                action = action.strip('　')
                console.trace("play_finger_guess_game(): action = " + action)
                if action == '石头' or action == '[拳头]':
                    fingerGuessGame.play(name, FingerType.Rock)
                elif action == '剪刀' or action == '[胜利]':
                    fingerGuessGame.play(name, FingerType.Scissors)
                elif action == '布' or action == '[OK]':
                    fingerGuessGame.play(name, FingerType.Paper)
    except Exception as err:
        display_exception(err)

    console.trace("play_finger_guess_game(): leave.")
    console.info('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

def handle_friend_message(msg):
    global console
    global msg_delimiter
    global current_game
    global fingerGuessGame
    global bot

    try:
        name = msg.chat.name
        # console.trace('name = ' + name)
        # console.trace('msg.text = ' + msg.text)

        # console.trace('msg_delimiter = ' + msg_delimiter)
        tokens = re.split(msg_delimiter, msg.text)
        tokens = [t for t in tokens if t]
        # console.trace(tokens)

        if current_game == 1 and fingerGuessGame != None:
            # 游戏：石头剪刀布
            if len(tokens) >= 1:
                play_finger_guess_game(name, tokens[0])
            else:
                play_finger_guess_game(name, msg.text)
        else:
            console.info(tokens)
    except Exception as err:
        display_exception(err)

@bot.register([Friend, Group])
def auto_reply_friend(msg):
    """
    消息自动回复
    """
    global console

    try:
        console.info(msg)
        """
        if isinstance(msg.chat, Group):
            console.info('group = ' + msg.chat.name)
            console.info('name = ' + msg.member.name)
        elif isinstance(msg.chat, Friend):
            console.info('name = ' + msg.chat.name)
        console.info('msg.text = ' + msg.text)
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

    except Exception as err:
        display_exception(err)

    return tuling_auto_reply(msg)

# 打印来自其他好友、群聊和公众号的消息
# @bot.register()
# def print_others(msg):
#    console.info(msg)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求。[我是机器人]')

def stop():
    global console
    global bot
    try:
        bot.logout()
        time.sleep(1)
        stop_finger_guess_game()
        stopThread()
    except Exception as err:
        display_exception(err)

def stopThread():
    global console
    global stopEvent
    global scheduleThread
    try:
        console.info('Stopping ScheduleThread, waiting for {} seconds...'.format(wait_time_sec))
        stopEvent.set()
        scheduleThread.join()
        console.info('ScheduleThread have stopped.')
    except Exception as err:
        display_exception(err)

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
        global console
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
                console.info('cur_time: {}, schedule_time: {}'.format(cur_time, schedule_time))
            if cur_time == schedule_time:
                continue
            elif cur_time == '09:00':
                for group in bot.groups():
                    console.info(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ''
                    index = 1
                    for rank in stat[group.name]['rank']:
                        # console.info('{}: {} {}'.format(index, rank['name'], rank['time']))
                        msg_text += '{}：{} {}\n'.format(index, rank['name'], rank['time'])
                        index += 1
                    if msg_text:
                        msg_text = '排行日报\n起床排行榜：\n' + msg_text
                        group.send(msg_text)
            elif cur_time == '23:00':
                for group in bot.groups():
                    console.info(group.name)
                    if not stat[group.name]:
                        continue
                    msg_text = ''
                    index = 1
                    count = stat[group.name]['count']
                    for name in sorted(count, key=lambda x: count[x], reverse=True):
                        # console.info('{}: {} {}'.format(index, rank['name'], rank['time']))
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

    console = Console(LogType.WARNING)

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
