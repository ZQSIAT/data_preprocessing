# This code is for deal the error of label.
# 1, To merge two label which are created by different people.

import xlrd
import os
import numpy as np
import time
from multiprocessing import Pool
import shutil as st
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='./log/{:s}_address_label.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class AddressLabel(object):
    """
    The class is for generating the final label with including some function for dealing label array.
    """
    def __init__(self):
        self.final_path = "D:/pycharm_project/temp/92_276_a03/final_label/"
        self.root_path = "D:/pycharm_project/temp/92_276_a03/original_label/"
        self.judge_path = "D:/pycharm_project/temp/92_276_a03/judge_label/"
        self.action_chinese_name = ['戴眼镜', '脱帽', '敬礼', '梳头', '向前扔东西', '自拍', '读书', '签字', '打字', '打电话',
                                    '捡东西', '看手表', '咳嗽', '喝水', '吃东西', '抽烟', '擦汗', '修眉', '玩手机', '散步',
                                    '转身', '快速走', '慢跑', '快速跑', '跳绳', '原地跳两下', '趴下', '跌倒', '后仰躺下',
                                    '痛苦的蜷缩成一团', '拔剑', '射箭', '拔枪', '打棒球', '篮球运球', '投篮', '篮球控球',
                                    '乒乓球颠球', '乒乓球发球', '乒乓球正手拉球', '乒乓球反手接球', '羽毛球颠球', '羽毛球发球',
                                    '羽毛球扣杀', '羽毛球跨步接球', '吉他扫弦', '民谣指弹', '吹竹笛', '吹口琴', '拿话筒唱歌',
                                    '吹竖笛', '弹钢琴', '篮球运球攻防', '篮球空中传球', '足球传球', '握手', '击掌', '交接东西',
                                    '干杯', '拥抱', '摔跤', '格斗', '蛙跳', '用剑决斗', '丢垃圾', '打喷嚏', '打哈欠']
        self.temp_path = "D:/pycharm_project/temp/"
        self.temp_file = "test_label.txt"
        pass

    @staticmethod
    def read_txt(path):
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

    def merge2labels_92_276_a03(self):
        """
        Merge the original label and judgment label for the second phase.
        """
        label_list = self.generate_list()
        for i, IContent in enumerate(label_list[1]):
            if os.path.exists(self.final_path + IContent):
                print("\"{:s}\" has done.".format(IContent))
                continue
                pass
            original_label = self.read_txt(self.root_path + IContent)
            judge_label = self.read_txt(self.judge_path + IContent)
            if len(original_label) == len(judge_label):
                # --contrast action judge--
                original_action = np.array(original_label)[:, 3]
                judge_action = np.array(judge_label)[:, 3]
                if np.where(original_action != judge_action)[0].size > 0:  # If there are inconsistencies.
                    for ii in np.where(original_action != judge_action)[0]:
                        print("{:s}, {:d}".format(IContent, ii + 1))
                        logger.info("{:s}, {:d}".format(IContent, ii + 1))
                        pass
                    pass
                else:  # If there are no inconsistencies.
                    final_label = np.array(judge_label)
                    final_label[:, [3, 4]] = final_label[:, [4, 3]]  # Swap columns 4 and 5 of the action judgment label
                    coded_list_label = self.generate_action_order(final_label, IContent)
                    # Specify the time window judgement
                    replaced_list_label = self.replace_time_windows_judgment(None, ['31', '26', '28', '25'], '1', coded_list_label)
                    # Save the final labels
                    save_name = self.final_path + IContent
                    np.savetxt(save_name, np.array(replaced_list_label), delimiter=',', fmt='%s')
                    print("\"{:s}\" has done.".format(IContent))
                    pass
                pass

            else:
                print("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                logger.info("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                continue
                pass
            break
            raise RuntimeError
            pass
        pass

    def generate_action_order(self, final_label=None, sequence=None):
        """
        Encode the Chinese description of the action with Numbers.
        :param final_label:Labels that are not action coded with a ndarray type.
        :param sequence:The name of the label file being operated on with a str type.
        :return:Action coded label data with a list type.
        """
        assert (final_label is not None) and (sequence is not None), "The input parameter cannot be empty"
        list_final_label = final_label.tolist()
        for i, i_content in enumerate(final_label):
            if i_content[0] in self.action_chinese_name:
                list_final_label[i][0] = str(self.action_chinese_name.index(i_content[0]) + 1)
                pass
            else:
                print("In sequence {:s}. \"{:s}\" This action is not in the total action list!!!".format(sequence, i_content[0]))
                logger.info("In sequence {:s}. \"{:s}\" This action is not in the total action list!!!".format(sequence, i_content[0]))
                continue
            pass
        return list_final_label
        pass

    @staticmethod
    def replace_time_windows_judgment(action_order=None, action_order_array=None, your_judgement='1', final_label=None):
        """
        Manually specify that the time window judgement for certain actions is determined to be 1 or 2.
        :param action_order:The action order that you want to replace i.e., '1'-'67'.
        :param your_judgement:Your judgement i.e., 1 or 2.
        :param action_order_array:The action order array that you want to replace i.e., ['1','4','67'].
        :param final_label:Labels that are not action coded with a list type.
        :return:Time windows judgement replaced label data with a list type.
        """
        list_final_label = final_label
        if action_order_array is None and action_order is not None and final_label is not None:
            for i, i_content in enumerate(final_label):
                if i_content[0] == action_order:
                    list_final_label[i][3] = your_judgement
                    pass
                pass
            pass
        if action_order_array is not None and action_order is None and final_label is not None:
            for i, i_content in enumerate(final_label):
                for j in action_order_array:
                    if i_content[0] == j:
                        list_final_label[i][3] = your_judgement
                        pass
                    pass
                pass
            pass
        return list_final_label
        pass
    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    my_task = AddressLabel()
    my_task.merge2labels_92_276_a03()
    # my_task.merge2labels()
    # label_content = my_task.read_txt(my_task.temp_path + my_task.temp_file)
    # original_label = my_task.read_txt(my_task.temp_path + "P001T001S003_o.txt")
    # judge_label = my_task.read_txt(my_task.temp_path + "P001T001S003_j.txt")
    # if len(original_label) == len(judge_label):
    #
    #     print(np.array(original_label)[:, 3])
    #     print(np.array(judge_label)[:, 3])
    #     original_action_determine = np.array(original_label)[:, 3]
    #     judge_action_determine = np.array(judge_label)[:, 3]
    #     contrast = original_action_determine != judge_action_determine
    #     print(np.where(contrast)[0].size > 0)
    #
    #     final_label = np.array(judge_label)
    #     # print(final_label)
    #     final_label[:, [3, 4]] = final_label[:, [4, 3]]
    #
    #     # print(final_label)
    #     list_final_label = final_label.tolist()
    #     for i, i_content in enumerate(list_final_label):
    #         # print(i, '\n', i_content)
    #         print(i_content[0])
    #         list_final_label[i][0] = str(my_task.action_chinese_name.index(i_content[0]) + 1)
    #         pass
    #     print(list_final_label)
    #
    #     np.savetxt('test.txt', np.array(list_final_label), delimiter=',', fmt='%s')
    #     # file = open('file_name.txt', 'w')
    #     # file.write(str(list_final_label))
    #     # file.close()
    #     pass
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
