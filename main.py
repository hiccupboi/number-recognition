from functools import reduce
from PIL import Image
import numpy as np
from collections import Counter
from matplotlib import style, pyplot as plt

style.use("ggplot")


def create_examples():
    number_array_examples = open('numArEx.txt', 'a')
    numbers_we_have = range(1, 10)
    for each_num in numbers_we_have:
        for further_num in numbers_we_have:
            print(str(each_num) + '.' + str(further_num))
            img_file_path = 'images/numbers/' + str(each_num) + '.' + str(further_num) + '.png'
            ei = Image.open(img_file_path)
            eiar = np.array(ei)
            eiarl = str(eiar.tolist())
            print(eiarl)
            line_to_write = str(each_num) + '::' + eiarl + '\n'
            number_array_examples.write(line_to_write)


def threshold(image_array):
    balance_array = []
    new_array = image_array
    for each_row in image_array:
        for each_pix in each_row:
            avg_num = reduce(lambda x, y: x + y, each_pix[:3]) / len(each_pix[:3])
            balance_array.append(avg_num)
    balance = reduce(lambda x, y: x + y, balance_array) / len(balance_array)
    for each_row in new_array:
        for each_pix in each_row:
            if reduce(lambda x, y: x + y, each_pix[:3]) / len(each_pix[:3]) > balance:
                each_pix[0] = 255
                each_pix[1] = 255
                each_pix[2] = 255
                each_pix[3] = 255
            else:
                each_pix[0] = 0
                each_pix[1] = 0
                each_pix[2] = 0
                each_pix[3] = 255
    return new_array


def what_is_this_number(file_path):
    matched_array = []
    load_examples = open('numArEx.txt', 'r').read()
    load_examples = load_examples.split('\n')

    i = Image.open(file_path)
    iar = np.array(i)
    iarl = iar.tolist()

    in_question = str(iarl)

    for each_example in load_examples:
        try:
            split_example = each_example.split('::')
            current_num = split_example[0]
            current_ar = split_example[1]

            each_pix_example = current_ar.split('],')
            each_pix_in_question = in_question.split('],')

            x = 0

            while x < len(each_pix_example):
                if each_pix_example[x] == each_pix_in_question[x]:
                    matched_array.append(int(current_num))

                x += 1
        except Exception as e:
            print(str(e))

    x = Counter(matched_array)
    print(x)
    graphX = []
    graphY = []

    ylimi = 0

    for each_thing in x:
        graphX.append(each_thing)
        graphY.append(x[each_thing])
        ylimi = x[each_thing]

    fig = plt.figure()
    ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4, 4), (1, 0), rowspan=3, colspan=4)

    ax1.imshow(iar)
    ax2.bar(graphX, graphY, align='center')
    plt.ylim(400)

    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)

    plt.show()


what_is_this_number('images/test.png')
