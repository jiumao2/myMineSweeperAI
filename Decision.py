import numpy as np
import myMouse
import random
import time
import UpdateFrame
import matplotlib.pyplot as plt
import scipy.optimize

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
    for k in range(16):
        for j in range(30):
            if mine_fields[k, j] <= 0:
                blank_fields.append((k, j))
    return random.choice(blank_fields)


def deep_calcalating(mine_fields):
    blank_fields_order = np.zeros((16, 30))
    blank_fields = []
    count = 0
    total_bomb = 99
    for k in range(16):
        for j in range(30):
            if mine_fields[k, j] == -1:
                blank_fields.append((k, j))
                blank_fields_order[k, j] = count
                count += 1
            elif mine_fields[k, j] == 9:
                total_bomb -= 1
    x = np.ones((1, count))
    y = [total_bomb]
    for k in range(16):
        for j in range(30):
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
    f = open('info.txt','w')
    f.write('1')
    f.close()
    # # output_possibility = np.matmul(np.linalg.pinv(x), y)
    # fun = lambda t: np.linalg.norm(t)
    # cons = ()
    # print(x.shape)
    # print(y.shape)
    # x0 = 0.3 * np.ones((np.size(x, 1), 1))  # 设置初始值
    # print(x0.shape)
    # for k in range(np.size(x,1)):
    #     temp = ({'type': 'ineq', 'fun': lambda t: t[k]},)  # x>=e，即 x > 0
    #     cons = cons + temp
    # for k in range(np.size(x,0)):
    #     temp = ({'type': 'eq', 'fun': lambda t: np.matmul(x[k,:],t)-y[k,:]},)
    #     cons = cons + temp
    # print(cons)
    #
    #
    # res = scipy.optimize.minimize(fun, x0, constraints=cons)
    # print(res)
    # output_possibility = res.x
    # print(np.matmul(x[0,:],output_possibility)-y[0,:])
    # print(output_possibility)
    # output_possibility = output_possibility.reshape((-1,))
    while True:
        f = open('info.txt','r')
        a = f.read()
        if a == '0':
            f.close()
            break
        f.close()
    output_possibility = np.loadtxt('output.csv',delimiter=",")

    ind_bomb = np.argwhere(output_possibility > 0.999)
    ind_safe = np.argwhere(output_possibility < 0.001)
    if np.size(ind_safe) == 0:
        f = open('info.txt', 'w')
        f.write('2')
        f.close()
    while True:
        f = open('info.txt','r')
        a = f.read()
        if a == '0':
            f.close()
            break
        f.close()
    output_possibility = np.loadtxt('output.csv', delimiter=",")

    output = []
    for k in range(np.size(ind_safe)):
        temp_k, temp_j = blank_fields[round(ind_safe[k, 0])]
        print(temp_k, temp_j, output_possibility[round(ind_safe[k, 0])])
        output.append((temp_k, temp_j, 'left_click'))
    # for k in range(np.size(ind_bomb)):
    #     temp_k, temp_j = blank_fields[round(ind_bomb[k,0])]
    #     print(temp_k, temp_j, output_possibility[round(ind_bomb[k, 0])])
    #     output.append((temp_k, temp_j, 'right_click'))
    if len(output) > 0:
        return output
    else:
        if len(output) == 30*16:
            return [(0, 0, 'left_click')]
        ind_minp = np.argmin(output_possibility)
        temp_k, temp_j = blank_fields[ind_minp]
        print(temp_k, temp_j, output_possibility[ind_minp])
        return [(temp_k, temp_j, 'left_click')]

def start_game(mine_fields, rect):
    if np.sum(mine_fields!=-1) <= 3:
        if mine_fields[0,0]==-1:
            myMouse.click(rect,0,0,'left_click')
        elif mine_fields[0,29]==-1:
            myMouse.click(rect,0,29,'left_click')
        elif mine_fields[15,0]==-1:
            myMouse.click(rect,15,0,'left_click')
        else:
            myMouse.click(rect,15, 29,'left_click')
        return True
    return False

def next_move(mine_fields, rect):
    if not isGoodGame(mine_fields):
        print('Failed! Click any button to restart!')
        # os.system('Pause')
        return 0

    if isComplete(mine_fields, rect):
        # os.system('pause')
        myMouse.click(rect, 0, 0, 'restart')
        return 2

    # # Naive Mine Sweeper
    # flag = False
    # for k in range(16):
    #     for j in range(30):
    #         if mine_fields[k, j] >= 1 and mine_fields[k, j] <= 8:
    #             remain_mines, blank_fields = getBlankFields(mine_fields, k, j)
    #             if remain_mines == 0 and len(blank_fields) > 0:
    #                 for temp_k, temp_j in blank_fields:
    #                     myMouse.click(rect, temp_k, temp_j, 'left_click')
    #                 flag = True
    #             elif remain_mines > 0 and remain_mines == len(blank_fields):
    #                 for temp_k, temp_j in blank_fields:
    #                     myMouse.click(rect, temp_k, temp_j, 'right_click')
    #                     mine_fields[temp_k, temp_j] = 9
    #                 flag = True
    #
    #             elif remain_mines > len(blank_fields):
    #                 print('Something must be wrong!')
    #                 # os.system('Pause')
    #                 # time.sleep(3)
    #                 return 0
    #                 myMouse.click(rect, 0, 0, 'restart')
    #
    # if flag:
    #     return 1
    if start_game(mine_fields, rect):
        return 1

    output = deep_calcalating(mine_fields)
    for k, j, click_type in output:
        myMouse.click(rect, k, j, click_type)

    # rand_k, rand_j = randomChoose(mine_fields)
    # myMouse.click(rect, k, j, 'left_click')
    return 1

if __name__ == '__main__':
    hwnd = UpdateFrame.get_screenshot()
    rect = UpdateFrame.get_position(hwnd)
    mine_field = UpdateFrame.process_screenshot()
    output = deep_calcalating(mine_field)
