# This code is for deal the error of label.
# 1, To merge two label which are created by different people.

import xlrd
import os
import numpy as np
import time
from multiprocessing import Pool
import logging
import shutil as st
import cv2
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='{:s}_address_label.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

class AddressLabel(object):
    def __init__(self):
        self.final_path = "D:/pycharm_project/temp/92_276_a03/final_label/"
        self.root_path = "D:/pycharm_project/temp/92_276_a03/original_label/"
        self.judge_path = "D:/pycharm_project/temp/92_276_a03/judge_label/"
        self.action_chinese_name = {'戴眼镜', '脱帽', '敬礼', '梳头', '向前扔东西', '自拍', '读书', '签字', '打字', '打电话',
                                    '捡东西', '看手表', '咳嗽', '喝水', '吃东西', '抽烟', '擦汗', '修眉', '玩手机', '散步',
                                    '转身', '快速走', '慢跑', '快速跑', '跳绳', '原地跳两下', '趴下', '跌倒', '后仰躺下',
                                    '痛苦的蜷缩成一团', '拔剑', '射箭', '拔枪', '打棒球', '篮球运球', '投篮', '篮球控球',
                                    '乒乓球颠球', '乒乓球发球', '乒乓球正手拉球', '乒乓球反手接球', '羽毛球颠球', '羽毛球发球',
                                    '羽毛球扣杀', '羽毛球跨步接球', '吉他扫弦', '民谣指弹', '吹竹笛', '吹口琴', '拿话筒唱歌',
                                    '吹竖笛', '弹钢琴', '篮球运球攻防', '篮球空中传球', '足球传球', '握手', '击掌', '交接东西',
                                    '干杯', '拥抱', '摔跤', '格斗', '蛙跳', '用剑决斗', '丢垃圾', '打喷嚏', '打哈欠'}
        self.temp_path = "D:/pycharm_project/temp/"
        self.temp_file = "test_label.txt"
        pass
    def read_txt(self, path):
        label_content = []
        with open(path) as lf:
            for line in lf.readlines():
                label_line = line.strip("\n").split(",")
                label_content.append(label_line)
                pass
            pass
        return label_content
        pass
    def read_excel(self):
        wb = xlrd.open_workbook(filename=self.temp_path + self.temp_file)
        print(wb.sheet_names())  # get all sheet names
        sheet1 = wb.sheet_by_index(0)  # get the sheet by index
        # sheet2 = wb.sheet_by_name('Sheet1')  # get the sheet by name
        print(sheet1)
        print(sheet1.name, sheet1.nrows, sheet1.ncols)
        rows = sheet1.row_values(0)  # get row content
        cols = sheet1.col_values(0)  # get cul content
        print(rows)
        print(cols)
        print(sheet1.cell(1, 0).value)  # three ways to get the contents of the table
        print(sheet1.cell_value(0, 0))
        print(sheet1.row(0)[0].value)
        pass
    def generate_list(self):
        original_path = self.root_path
        path_list = []
        file_list = os.listdir(original_path)
        for i, ICount in enumerate(file_list):
            path_list.append(original_path + ICount)
            pass
        return path_list, file_list
        pass
    def merge2labels(self):
        label_list  = self.generate_list()
        for i, IContent in enumerate(label_list[1]):
            original_label = self.read_txt(self.root_path + IContent)
            judge_label = self.read_txt(self.judge_path + IContent)
            if len(original_label) == len(judge_label):
                # TODO
                #  final_label = ""
                pass
            else:
                print("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                logger.info("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                pass
            pass
        pass

    pass

if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    my_task = AddressLabel()
    # label_content = my_task.read_txt(my_task.temp_path + my_task.temp_file)
    # print(np.array(label_content)[:, 3], '\n', len(label_content))
    # np.savetxt('test.txt', np.array(label_content), delimiter=',', fmt='%s')
    # label_list = my_task.generate_list()
    # print(label_list[1])

    # processing by pool map
    # p = Pool(8)

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass
