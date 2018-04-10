
def split_player_test(str):
    name = 'We游戏机器人'
    players = str.split('@')
    print(players)
    players.pop(0)
    new_players = []
    """
    str1 = '\u2005'
    str1 = str1.encode('utf-8')
    str2 = '　'
    str2 = str2.encode('utf-8')
    """
    for player in players:
        # print(player)
        player = player.strip()
        # player = player.replace('\u2005', '')
        # player = player.replace('　', '')
        player = player.strip('\u2005')
        player = player.strip('　')
        if player == '我':
            new_players.append(name)
        else:
            new_players.append(player)
    print(new_players)
    print()

def str_test():
    str = '猜拳，邀请，@郭子\u2005 @我'
    split_player_test(str)

    str = '猜拳，邀请，@郭子\u2005 @司马云信\u2005'
    split_player_test(str)

if __name__ == "__main__":
    str_test()
