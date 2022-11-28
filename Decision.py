import numpy as np
import myIO
import random
import time
import matplotlib.pyplot as plt
import scipy.optimize
import hyperparams as p


# 0: 空
# -1: 未占据
# 1-8:雷数
# 9: 旗
# 10: 雷
# 11: 命中的雷
# 12: 标错的雷
def getFieldsAround(mine_fileds, k, j):
    max_x = np.size(mine_fileds, 0) - 1
    max_y = np.size(mine_fileds, 1) - 1
    if k == 0 and j == 0:
        return [(0, 1), (1, 1), (1, 0)]
    if k == max_x and j == 0:
        return [(max_x, 1), (max_x - 1, 1), (max_x - 1, 0)]
    if k == max_x and j == max_y:
        return [(max_x - 1, max_y), (max_x - 1, max_y - 1), (max_x, max_y - 1)]
    if k == 0 and j == max_y:
        return [(1, max_y), (1, max_y - 1), (0, max_y - 1)]
    if k == 0:
        return [(0, j - 1), (1, j - 1), (1, j), (1, j + 1), (0, j + 1)]
    if k == max_x:
        return [(max_x, j - 1), (max_x - 1, j - 1), (max_x - 1, j), (max_x - 1, j + 1), (max_x, j + 1)]
    if j == 0:
        return [(k - 1, 0), (k - 1, 1), (k, 1), (k + 1, 1), (k + 1, 0)]
    if j == max_y:
        return [(k - 1, max_y), (k - 1, max_y - 1), (k, max_y - 1), (k + 1, max_y - 1), (k + 1, max_y)]

    return [(k - 1, j - 1), (k - 1, j), (k - 1, j + 1), (k, j + 1), (k + 1, j + 1), (k + 1, j), (k + 1, j - 1),
            (k, j - 1)]


def isGoodGame(mine_fields):
    if np.any(mine_fields >= 10):
        print('Boom!')
        f = open('log.txt', 'a')
        f.write('0')
        f.close()
        return False
    return True


def isComplete(mine_fields, rect):
    if not np.any(mine_fields < 0):
        print('Complete!')
        f = open('log.txt', 'a')
        f.write('1')
        f.close()
        return True
    return False


def getBlankFields(mine_fields, k, j):
    remain_mines = mine_fields[k, j]
    blank_fields = []
    mines_around = getFieldsAround(mine_fields, k, j)
    for temp_k, temp_j in mines_around:
        if mine_fields[temp_k, temp_j] == 9:
            remain_mines -= 1
        elif mine_fields[temp_k, temp_j] == -1:
            blank_fields.append((temp_k, temp_j))

    return remain_mines, blank_fields


def randomChoose(mine_fields):
    blank_fields = []
    for k in range(np.size(mine_fields,0)):
        for j in range(np.size(mine_fields,1)):
            if mine_fields[k, j] < 0:
                blank_fields.append((k, j))
    return random.choice(blank_fields)

def normal(mine_fields):
    height = np.size(mine_fields,0)
    width = np.size(mine_fields,1)
    
    blank_fields_order = np.zeros((height, width))
    blank_fields = []
    count = 0
    if p.mode == 'Beginner':
        total_bomb = 10
    elif p.mode == 'Intermediate':
        total_bomb = 40
    elif p.mode == 'Expert':
        total_bomb = 99
    for k in range(np.size(mine_fields,0)):
        for j in range(np.size(mine_fields,1)):
            if mine_fields[k, j] == -1:
                blank_fields.append((k, j))
                blank_fields_order[k, j] = count
                count += 1
            elif mine_fields[k, j] == 9:
                total_bomb -= 1
    x = np.ones((1, count))
    y = [total_bomb]
    for k in range(np.size(mine_fields,0)):
        for j in range(np.size(mine_fields,1)):
            if mine_fields[k, j] >= 1 and mine_fields[k, j] <= 8:
                mine_num = mine_fields[k, j]
                mines_around = getFieldsAround(mine_fields, k, j)
                temp_x = np.zeros((1, count))
                to_stack = False
                for temp_k, temp_j in mines_around:
                    if mine_fields[temp_k, temp_j] == -1:
                        to_stack = True
                        temp_x[0, round(blank_fields_order[temp_k, temp_j])] = 1
                    elif mine_fields[temp_k, temp_j] == 9:
                        mine_num -= 1
                if to_stack:
                    x = np.concatenate((x, temp_x), axis=0)
                    y.append(mine_num)

    output_possibility = np.matmul(np.linalg.pinv(x), y)

    ind_bomb = np.argwhere(output_possibility > 0.999)
    ind_safe = np.argwhere(output_possibility < 0.001)

    output = []
    for k in range(np.size(ind_safe)):
        temp_k, temp_j = blank_fields[round(ind_safe[k, 0])]
        output.append((temp_k, temp_j, 'left_click'))
    for k in range(np.size(ind_bomb)):
        temp_k, temp_j = blank_fields[round(ind_bomb[k, 0])]
        output.append((temp_k, temp_j, 'right_click'))
    if len(output) > 0:
        return output
    elif len(output_possibility) > 0:
        ind_minp = np.argmin(output_possibility)
        temp_k, temp_j = blank_fields[ind_minp]
        return [(temp_k, temp_j, 'left_click')]
    else:
        return []    


def deep_calcalating(mine_fields):
    height = np.size(mine_fields,0)
    width = np.size(mine_fields,1)
    
    blank_fields_order = np.zeros((height, width))
    blank_fields = []
    count = 0
    if p.mode == 'Beginner':
        total_bomb = 10
    elif p.mode == 'Intermediate':
        total_bomb = 40
    elif p.mode == 'Expert':
        total_bomb = 99
        
    for k in range(np.size(mine_fields,0)):
        for j in range(np.size(mine_fields,1)):
            if mine_fields[k, j] == -1:
                blank_fields.append((k, j))
                blank_fields_order[k, j] = count
                count += 1
            elif mine_fields[k, j] == 9:
                total_bomb -= 1
    x = np.ones((1, count))
    y = [total_bomb]
    for k in range(np.size(mine_fields,0)):
        for j in range(np.size(mine_fields,1)):
            if mine_fields[k, j] >= 1 and mine_fields[k, j] <= 8:
                mine_num = mine_fields[k, j]
                mines_around = getFieldsAround(mine_fields, k, j)
                temp_x = np.zeros((1, count))
                to_stack = False
                for temp_k, temp_j in mines_around:
                    if mine_fields[temp_k, temp_j] == -1:
                        to_stack = True
                        temp_x[0, round(blank_fields_order[temp_k, temp_j])] = 1
                    elif mine_fields[temp_k, temp_j] == 9:
                        mine_num -= 1
                if to_stack:
                    x = np.concatenate((x, temp_x), axis=0)
                    y.append(mine_num)
    y = np.reshape(np.array(y), (-1, 1))
    np.savetxt('x.csv', x, delimiter=",")
    np.savetxt('y.csv', y, delimiter=",")
    f = open('info.txt', 'w')
    f.write('1')
    f.close()

    while True:
        f = open('info.txt', 'r')
        a = f.read()
        if a == '0':
            f.close()
            break
        f.close()
    output_possibility = np.loadtxt('output.csv', delimiter=",")

    ind_bomb = np.argwhere(output_possibility > 0.999)
    ind_safe = np.argwhere(output_possibility < 0.001)
    if np.size(ind_safe) == 0:
        f = open('info.txt', 'w')
        f.write('2')
        f.close()
        while True:
            f = open('info.txt', 'r')
            a = f.read()
            if a == '0':
                f.close()
                break
            f.close()
        output_possibility = np.loadtxt('output.csv', delimiter=",")

    output = []
    for k in range(np.size(ind_safe)):
        temp_k, temp_j = blank_fields[round(ind_safe[k, 0])]
        output.append((temp_k, temp_j, 'left_click'))
    for k in range(np.size(ind_bomb)):
        temp_k, temp_j = blank_fields[round(ind_bomb[k, 0])]
        output.append((temp_k, temp_j, 'right_click'))
    if len(output) > 0:
        return output
    elif len(output_possibility) > 0:
        ind_minp = np.argmin(output_possibility)
        temp_k, temp_j = blank_fields[ind_minp]
        return [(temp_k, temp_j, 'left_click')]
    else:
        return []


def start_game(mine_fields, rect):
    y_max = np.size(mine_fields,1)-1
    x_max = np.size(mine_fields,0)-1
    if np.sum(mine_fields != -1) <= 3:
        if mine_fields[0, 0] == -1:
            myIO.click(rect, 0, 0, 'left_click')
        elif mine_fields[0, y_max] == -1:
            myIO.click(rect, 0, y_max, 'left_click')
        elif mine_fields[x_max, 0] == -1:
            myIO.click(rect, x_max, 0, 'left_click')
        else:
            myIO.click(rect, x_max, y_max, 'left_click')
        return True
    return False


def next_move(mine_fields, rect):
    if not isGoodGame(mine_fields):
        print('Failed! Click any button to restart!')
        return 0

    if isComplete(mine_fields, rect):
        return 2
    
    if start_game(mine_fields, rect):
        return 1

    # Naive Mine Sweeper
    if p.algorithm == 'naive':
        flag = False
        for k in range(np.size(mine_fields,0)):
            for j in range(np.size(mine_fields,1)):
                if mine_fields[k, j] >= 1 and mine_fields[k, j] <= 8:
                    remain_mines, blank_fields = getBlankFields(mine_fields, k, j)
                    if remain_mines == 0 and len(blank_fields) > 0:
                        for temp_k, temp_j in blank_fields:
                            myIO.click(rect, temp_k, temp_j, 'left_click')
                        flag = True
                    elif remain_mines > 0 and remain_mines == len(blank_fields):
                        for temp_k, temp_j in blank_fields:
                            myIO.click(rect, temp_k, temp_j, 'right_click')
                            mine_fields[temp_k, temp_j] = 9
                        flag = True

                    elif remain_mines > len(blank_fields):
                        print('Something must be wrong!')
                        return 0
        if flag:
            return 1
        else:
            k, j = randomChoose(mine_fields)
            myIO.click(rect, k, j, 'left_click') 
    elif p.algorithm == 'normal':
        output = normal(mine_fields)
        if len(output) == 0:
            k, j = randomChoose(mine_fields)
            myIO.click(rect, k, j, 'left_click')
        else:
            for k, j, click_type in output:
                myIO.click(rect, k, j, click_type)                        
    elif p.algorithm == 'deep':       
        output = deep_calcalating(mine_fields)
        for k, j, click_type in output:
            myIO.click(rect, k, j, click_type)

    return 1
