import random
import numpy as np
from msvcrt import getch


class Robots():
    # ゲームの初期化
    def __init__(self):
        self.map_size = {'x': 60, 'y': 20}
        self.object = {'space': 0, 'player': 1,
                       'enemy': 2, 'captured': 3, 'scrap': 4}
        self.level = 1
        self.ADD_ENEMY = 5
        self.MAX_ENEMY = 40
        self.enemy_num = self.ADD_ENEMY
        self.enemy_prev = self.enemy_num
        self.score = 0

    #　マップの更新及びオブジェクトの配置
    def set_object(self):
        self.system_map \
        = np.full((self.map_size['x'], self.map_size['y']), self.object['space'])
        self.system_map \
        = np.reshape(self.system_map, self.map_size['x'] * self.map_size['y'])
        self.system_map[0] = self.object['player']
        self.system_map[1:self.enemy_num + 1] = self.object['enemy']
        random.shuffle(self.system_map)
        self.system_map \
        = np.reshape(self.system_map, (self.map_size['x'], self.map_size['y']))

    # マップの出力
    def print_map(self, map_name='visuality_map'):
        for y in range(self.map_size['y']):
            for x in range(self.map_size['x']):
                if map_name == 'system_map':
                    print(self.system_map[x][y], end='')
                else:
                    if self.system_map[x][y] == self.object['space']:
                        print('.', end=' ')
                    elif self.system_map[x][y] == self.object['player']:
                        print('@', end=' ')
                    elif self.system_map[x][y] == self.object['enemy']:
                        print('+', end=' ')
                    elif self.system_map[x][y] >= self.object['captured'] and self.system_map[x][y] % 2 == 1 :
                        print('☆', end=' ')
                    elif self.system_map[x][y] >= self.object['scrap'] and self.system_map[x][y] % 2 == 0:
                        print('*', end=' ')
            print()
        print(' Level:{} Score:{}\n'.format(self.level, self.score))

    # プレイヤーのコントロール
    def move_player(self):
        while True:
            control = getch().decode()
            if '0' <= control <= '9':
                break

        player_place = np.where(self.system_map == self.object['player'])
        player_x = int(player_place[0])
        player_y = int(player_place[1])
        self.system_map[player_x][player_y] = self.object['space']

        if control == '7' \
        and player_x > 0 and player_y > 0 \
        and self.system_map[player_x - 1][player_y - 1] == self.object['space']:
            self.system_map[player_x - 1][player_y - 1] \
            += self.object['player']

        elif control == '8' \
        and player_y > 0 \
        and self.system_map[player_x][player_y - 1] == self.object['space']:
            self.system_map[player_x][player_y - 1] \
            += self.object['player']

        elif control == '9' \
        and player_x < (self.map_size['x'] - 1) and player_y > 0 \
        and self.system_map[player_x + 1][player_y - 1] == self.object['space']:
            self.system_map[player_x + 1][player_y - 1] \
            += self.object['player']

        elif control == '4' \
        and player_x > 0 \
        and self.system_map[player_x - 1][player_y] == self.object['space']:
            self.system_map[player_x - 1][player_y] \
            += self.object['player']

        elif control == '6' \
        and player_x < (self.map_size['x'] - 1) \
        and self.system_map[player_x + 1][player_y] == self.object['space']:
            self.system_map[player_x + 1][player_y] \
            += self.object['player']

        elif control == '1' \
        and player_x > 0 and player_y < (self.map_size['y'] - 1) \
        and self.system_map[player_x - 1][player_y + 1] == self.object['space']:
            self.system_map[player_x - 1][player_y + 1] \
            += self.object['player']

        elif control == '2' \
        and player_y < (self.map_size['y'] - 1) \
        and self.system_map[player_x][player_y + 1] == self.object['space']:
            self.system_map[player_x][player_y + 1] \
            += self.object['player']

        elif control == '3' \
        and player_x < (self.map_size['x'] - 1) and player_y < (self.map_size['y'] - 1) \
        and self.system_map[player_x + 1][player_y + 1] == self.object['space']:
            self.system_map[player_x + 1][player_y + 1] \
            += self.object['player']

        elif control == '0':
            while True:
                x = np.random.randint(0, self.map_size['x'])
                y = np.random.randint(0, self.map_size['y'])
                if self.system_map[x][y] == self.object['space']:
                    self.system_map[x][y] += self.object['player']
                    break

        else:
            self.system_map[player_x][player_y] += self.object['player']

    # ロボットのコントロール
    def move_enemy(self):
        player_place = np.where(self.system_map == self.object['player'])
        player_x = int(player_place[0])
        player_y = int(player_place[1])
        enemy_place = np.where(self.system_map == self.object['enemy'])
        enemy_x = enemy_place[0]
        enemy_y = enemy_place[1]

        enemy_num = np.sum(self.system_map == self.object['enemy'])

        for count in range(enemy_num):
            self.system_map[enemy_x[count]][enemy_y[count]] -= self.object['enemy']

            if player_x < enemy_x[count] and player_y < enemy_y[count] \
            and enemy_x[count] > 0 and enemy_y[count] > 0 \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] - 1][enemy_y[count] - 1] \
                += self.object['enemy']

            elif player_x == enemy_x[count] and player_y < enemy_y[count] \
            and enemy_y[count] > 0 \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count]][enemy_y[count] - 1] \
                += self.object['enemy']

            elif player_x > enemy_x[count] and player_y < enemy_y[count] \
            and enemy_x[count] < (self.map_size['x'] - 1) and enemy_y[count] > 0 \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] + 1][enemy_y[count] - 1] \
                += self.object['enemy']

            elif player_x < enemy_x[count] and player_y == enemy_y[count] \
            and enemy_x[count] > 0 \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] - 1][enemy_y[count]] \
                += self.object['enemy']

            elif player_x > enemy_x[count] and player_y == enemy_y[count] \
            and enemy_x[count] < (self.map_size['x'] - 1) \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] + 1][enemy_y[count]] \
                += self.object['enemy']

            elif player_x < enemy_x[count] and player_y > enemy_y[count] \
            and enemy_x[count] > 0 and enemy_y[count] < (self.map_size['y'] - 1) \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] - 1][enemy_y[count] + 1] \
                += self.object['enemy']

            elif player_x == enemy_x[count] and player_y > enemy_y[count] \
            and enemy_y[count] < (self.map_size['y'] - 1) \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count]][enemy_y[count] + 1] \
                += self.object['enemy']

            elif player_x > enemy_x[count] and player_y > enemy_y[count] \
            and enemy_x[count] < (self.map_size['x'] - 1) and enemy_y[count] < (self.map_size['y'] - 1) \
            and self.system_map[enemy_x[count]][enemy_y[count]] == self.object['space']:
                self.system_map[enemy_x[count] + 1][enemy_y[count] + 1] \
                += self.object['enemy']

            else:
                self.system_map[enemy_x[count]][enemy_y[count]] += self.object['enemy']

    # ステージの状態の確認
    def check(self):
        if self.object['captured'] in self.system_map:
            return True
        
        elif self.object['enemy'] not in self.system_map:
            self.add_sroce()
            self.update_stage()
            return False
        
        else:
            self.add_sroce()
            return False

    # スコアの加算
    def add_sroce(self):
        enemy_num = np.sum(self.system_map == self.object['enemy'])
        self.score += (self.enemy_prev - enemy_num)
        self.enemy_prev = enemy_num

    # ステージの更新
    def update_stage(self):
        self.score += self.level * 10 + self.enemy_num
        self.level += 1
        
        if self.enemy_num >= self.MAX_ENEMY:
            self.enemy_num = self.MAX_ENEMY
        else:
            self.enemy_num += self.ADD_ENEMY
        self.enemy_prev = self.enemy_num

        self.set_object()

    
    def game_over(self):
        print('\n-----------GAME OVER-----------\n')

        while True:
            control = input('Continue? [y/n]\n  >> ')
            print()
            if control == 'y':
                return True
            elif control == 'n':
                return False
            else:
                pass