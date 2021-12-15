import matplotlib.pyplot as plt
import numpy as np
import cv2
import pickle

# pattern_path = './Pattern'
# pattern_all = np.zeros((12,12,3,12))
# for k in range(1,13):
#     pattern_all[:,:,:,k-1] = cv2.imread(pattern_path+'/'+str(k)+'.png')
#
# print(np.shape(pattern_all))
# f = open('pattern.pickle','wb')
# pickle.dump(pattern_all,f)
# f.close()

def PatternRecognizing(img):
    f = open('pattern.pickle', 'rb')
    pattern_all = pickle.load(f)
    f.close()

    img_center = img[3:15, 4:16, :]
    if np.std(img_center) < 40:
        temp = np.mean(img[:3, :, :], axis=(0, 1, 2)) + np.mean(img[:, :3, :], axis=(0, 1, 2))
        if temp > 380:
            return -1
        else:
            return 0
    else:
        min_diff = np.zeros((12, 1))
        for i in range(12):
            min_diff_temp = 1000000000
            for x1 in range(np.size(img, 0) - 11):
                for x2 in range(np.size(img, 1) - 11):
                    temp_diff = np.abs(img[x1:(12 + x1), x2:(12 + x2), :] - pattern_all[:, :, :, i])
                    temp_diff = temp_diff.sum(axis=(0, 1, 2))
                    if temp_diff < min_diff_temp:
                        min_diff_temp = temp_diff
            min_diff[i] = min_diff_temp
        min_idx = np.argmin(min_diff)
        return min_idx + 1

if __name__ == '__main__':
    img = cv2.imread("screenshot.jpg")
    width_block = 30
    height_block = 16
    x_left = 12
    x_right = 493
    y_left = 55
    y_right = 312

    size_img = 12

    x = np.linspace(x_left, x_right, width_block + 1)
    y = np.linspace(y_left, y_right, height_block + 1)

    mine_field = np.zeros((height_block, width_block))
    log = []

    for k in range(len(x) - 1):
        for j in range(len(y) - 1):
            temp = img[round(y[j])-1:round(y[j + 1]), round(x[k])-1:round(x[k + 1]), :]
            # cv2.imshow('1',temp)
            # cv2.waitKey(100)
            # cv2.destroyAllWindows()
            # temp = np.reshape(temp, (1, size_img * size_img * 3))
            img_center = temp[3:15, 4:16, :]
            if np.std(img_center) < 40:
                temp_sum = np.mean(temp[:3, :, :], axis=(0, 1, 2)) + np.mean(temp[:, :3, :], axis=(0, 1, 2))
                log.append(temp_sum)

            # mine_field[j, k] = PatternRecognizing(temp)
    print(len(log))
    plt.plot(log,'x')
    plt.show()