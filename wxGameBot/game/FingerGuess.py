#!/usr/bin/python
# coding: utf-8

from enum import unique, Enum, IntEnum
import threading, time, json, re
import traceback

from ..utils.globalvar import GlobalVar
from ..utils.exception import display_exception

globalvar = GlobalVar()
console = globalvar.get_var("console")

@unique
class FingerType(IntEnum):
    Unknown = -1
    Rock = 0
    Scissors = 1
    Paper = 2

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
    global console
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
    global console
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
