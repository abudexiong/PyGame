#-*- coding:utf-8 -*-
__author__ = '凯'
#import curses
from random import randrange,choice
from collections import defaultdict

actions=['Up','Left','Down','Right','Restart','Exit']
letters_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(letters_codes,actions*2))
#print letters_codes
#print actions_dict
'''在大写键开启的情况下输入wasd以及重启退出同样有效
   使用字典将值与按键一一对应'''
def get_user_action(keyboard):#阻塞 循环
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
        return actions_dict[char]
#转置矩阵 矩阵逆转
def transpose(field):
    return[list(row) for row in zip(*field)]
def invert(field):
    return [row[::-1]for row in field]

class GameField(object):
    def __init__(self,height=4.width=4,win=2048):
    self.height = height
    self.width=width
    self.win_value = 2048
    self.score = 0
    self.highscore=0
    self.reset()

    def  spawn(self):
        new_element= 4 if randrange(100)>89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range (self.height) if self.field[i][j]==0])
        self.field[i][j]=new_element

    def reset(self):
        if self.score>self.highscore:
            self.highscore=self.score
        self.score=0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move_row_left(row):
        def tighten(row):
            new_row = [i for i in row if i != 0]
            new_row +=[0 for i in range(len(row)-len(new_row))]
            return new_row

        def merge(row):
            pair = False
            new_row=[]
            for i in range(len(row)):
                if pair :
                    new_row.append(2*row[i])
                    self.score+=2*row[i]
                    pair = False
                else:
                    if i+1<len(row) and row[i] == row[i+1]:
                        pair = True
                        new_row.append(0)
                    else:
                        new_row.append(row[i])
            assert len(new_row)==len(row)
            return new_row
        return tighten(merge(tighten(row)))

    def move(self,direction):
        def move_row_left(row):

            move = {}
            move['Left']=lambda field:[move_row_left(row) for row in field]
            move['Right']=lambda field:invert(move['Left'](invert(field)))
            move['Up']=lambda field:transpose(move['Left'](transpose(field)))
            move['Down']=lambda field:transpose(move['Right'](transpose(field)))

            if direction in move:
                if self.move_is_possible(direction):
                    self.field=move[direction](self.field)
                    self.spawn()
                    return True
                else:
                    return False

    def is_win(self):
        return any(any(i>=self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return  not any(self.move_is_possible(move) for move in actions)

    def move_is_possible(self,direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] ==0 and row[i+1] !=0:
                    return True
                if row[i] !=0 and row[i+1] ==row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row)-1))
        check={}
        check =
def main(stdscr):
    def init():
        return 'Game'
        #重置游戏棋盘

    def not_game(state):
        responses = defaultdict(lambda :state)
        responses['Restart'],responses['Exit']='Init','Exit'
        return responses[action]

    def game():
        if action=='Restart':
            return 'Init'
        if action=='Exit':
            return 'Exit'
        if win:
            return 'Win'
        if lose:
            return 'Gameover'
        return 'Game'
    state_actions={
        'Init':init(),
        'Win':lambda :not_game('Win'),
        'Gameover':lambda :not_game('Gameover'),
        'Game':game()
    }
    state = 'Init'

    while state !='Exit':
        state = state_actions[state]()
