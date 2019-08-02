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
import json


class AddressLabel(object):
    """
    The class is for generating the final label with including some function for dealing label array.
    """
    def __init__(self):
        self.dst_name = "DataSet2"
        self.parameters = [['original_action', 'original', 3, 1], ['original_action', 'original', 3, 2],
                           ['judge_action', 'judge', 3, 2], ['judge_time_windows', 'judge', 4, 2],
                           ['judge_time_windows', 'judge', 4, None], ['final_action_judge', 4],
                           ['final_time_windows_judge', 3]]
        self.present_parameter = self.parameters[6]

        self.json_name = self.present_parameter[0]  # judge_action judge_time_windows original_action
        self.final_path = "Z:/DATASET_BACKUP/LABEL/new_label/{:s}/final_label/".format(self.dst_name)
        self.root_path = "Z:/DATASET_BACKUP/LABEL/new_label/{:s}/现在输出标签/".format(self.dst_name)
        self.judge_path = "Z:/DATASET_BACKUP/LABEL/new_label/{:s}/判断后的输出标签/".format(self.dst_name)
        self.log_path = "Z:/DATASET_BACKUP/LABEL/new_label/{:s}/log/".format(self.dst_name)
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
        self.action_error = {"Total": 0}
        self.temp_store_path = self.log_path + "{:s}-{:s}_error.json".format(self.dst_name, self.json_name)

        self.final_label_path = "Z:/DATASET_BACKUP/LABEL/new_label/final_label_all/"
        self.src_video_path = "Z:/publish_data/{:s}/RGB_HIKVISION_CAPTURE/".format(self.dst_name)
        self.dst_video_path = "Z:/publish_data/{:s}/temp_error_trimmed_video/".format(self.dst_name)
        self.file_model = "O{:03d}P{:03d}C{:03d}T{:03d}S{:03d}A{:03d}.{:s}"
        self.file_suffixes = "mp4"
        self.names_alphabet = ["cairuilin", "caojunhai", "changhongguang", "changming", "changxiangxu", "chengjiawen",
                               "chenhongxu", "chenhongyu", "chenjialing", "chenjiangtao", "chenjiaxing", "chenjinbao",
                               "chenliaoran", "chenming", "chenmingting", "chenpeng", "chentianxiao", "chenwenjie",
                               "chenxianger", "chenyanxia", "chenyipeng", "chenyizhu", "chenyongcai", "chenyongfa",
                               "chenyongkang", "chenyu", "chenzejia", "chenzhuo", "dengjun", "dengliucheng", "dongyijing",
                               "dutao", "duxiaomeng", "fangyue", "fanjilei", "fanxiaoyuan", "fuchenjie", "gaochunbo",
                               "gaoyiqian", "geminghui", "gongliang", "gongyue", "guhaoying", "guoda", "guojunguang",
                               "guoqiong", "hanbo", "hannana", "haojingxuan", "haoluoying", "hejiawen", "hejiemin",
                               "huangchi", "huanghaiyan", "huangjianan", "huangshuxian", "huangweicong", "huangweijuan",
                               "huangxiaoqin", "huangxiaoye", "huangxuanli", "huangzihang", "hujing", "huxinyan",
                               "huyueyan", "huzeming", "jiangjie", "jiangwenyao", "jiangzhiming", "jinxiaowan", "jishujian",
                               "kangping", "laiqiqi", "laixinjie", "laiyingru", "liangxiaosi", "lianroumin", "lianshengxiong",
                               "libingbing", "lichuanfu", "lihongjian", "lijiamin", "lijianyao", "limeng", "limin", "limingzhao",
                               "limuyou", "linchuang", "linjiaming", "linjiaqi", "linjiawei", "linjiaxin", "linlanfang",
                               "linshiyi", "linyanfei", "linyue", "liqiang", "liqianying", "lisinan", "liuanqi", "liuboyi",
                               "liuchangdong", "liucheng", "liujia", "liujianeng", "liujinmeng", "liuxinwen", "liuxusheng",
                               "liuyaqi", "liuyuan", "liuyuxiang", "liuzhao", "liwen", "lixiaokai", "lixingxing", "lixueyi",
                               "liyang", "liyiling", "liyongshun", "liyuqin", "lizeshun", "lizhangjian", "lizhitao",
                               "lizihao", "longshixiao", "luchengzhi", "luchunxian", "lukaijie", "luojiangliu", "luojianming",
                               "luokaiqian", "luowei", "lvdan", "lvjingya", "maijinhui", "majiake", "mayizhen", "moningkai",
                               "musainan", "niebeina", "nijiangpeng", "niuyuan", "ouyangpei", "pangwenjun", "panjiadong",
                               "penglingxiu", "pengsongqiao", "pengxiaobin", "qianyinqiu", "qiujinyue", "quyangyang",
                               "renjiao", "renpei", "rongchuyu", "ruanpanpan", "shangpeihan", "shangtianyu", "shenguibao",
                               "shujun", "sunshijie", "sunyuyao", "suoya", "sushuiqing", "suzhilong", "tanghuan",
                               "tangjunzhi", "tangshi", "tangwenjie", "tantiancheng", "tanyuanqi", "taoxiudian",
                               "tianfangbi", "tianyanling", "tujiali", "wangbaoliang", "wangchao", "wangjing", "wangjuan",
                               "wangkewei", "wangsi", "wangxingyong", "wangxinnian", "wangxiufang", "wangying",
                               "wangzhicheng", "wanqiao", "weiliyang", "wengsifan", "wuhaisi", "wuhaitao", "wuhongzhen",
                               "wutong", "wuweixuan", "wuxudong", "xiaminghui", "xianglei", "xiangli", "xiaofen",
                               "xiaozhuo", "xiegang", "xiele", "xiezhuolin", "xiongguangyang", "xiongwei", "xubingqi",
                               "xujiangyao", "xujiaohao", "xujiayang", "xujinshuang", "xuliang", "xupei", "xuxiao", "xuyue",
                               "yanghan", "yangkai", "yangkaibo", "yangruohan", "yangweijie", "yangwensi", "yangyuanyuan",
                               "yangzhaonan", "yangzhiguang", "yanyubai", "yaoyufeng", "yejiexia", "yinli", "yuandawei",
                               "yujunyi", "yurongjian", "zanjianhuan", "zengning", "zhangbaowen", "zhangbensong",
                               "zhangge", "zhanghang", "zhangjin", "zhangjunjie", "zhangkuiqing", "zhangna", "zhangshenghai",
                               "zhangxiangnan", "zhangxiaohan", "zhangxinyu", "zhangyan", "zhangyingkui", "zhangzongxin",
                               "zhanjiaxuan", "zhaofeng", "zhaohaoda", "zhaoqingsong", "zhaoshilin", "zhaotaoling",
                               "zhaowengui", "zhaoyuliang", "zhaozhicheng", "zhengdanna", "zhenglimeng", "zhengshaoxuan",
                               "zhengzegeng", "zhengzhicheng", "zhongkaiyu", "zhongxinyu", "zhongyankun", "zhoulibing",
                               "zhoulikai", "zhouqiuming", "zhouweixiao", "zhouxianhang", "zhuangyingzhen", "zhujiayi",
                               "zhujingxian", "zhulei", "zhurongxiang", "zhuyaping", "zhuzhenkun", "zhuzhenye"]
        self.names_time = ['zhuyaping', 'chenyipeng', 'sunshijie', 'haoluoying', 'lihongjian', 'fanxiaoyuan', 'guojunguang',
                           'tianyanling', 'liqiang', 'shenguibao', 'linchuang', 'liuyuxiang', 'haojingxuan', 'liuyuan',
                           'zhangshenghai', 'xiaozhuo', 'huangshuxian', 'huanghaiyan', 'linyanfei', 'zhaotaoling',
                           'liujinmeng', 'lianroumin', 'chenjinbao', 'huangweijuan', 'lukaijie', 'zhongkaiyu', 'wangchao',
                           'huangchi', 'maijinhui', 'lianshengxiong', 'linyue', 'zhulei', 'hujing', 'zhoulibing',
                           'liujianeng', 'zhengshaoxuan', 'tanyuanqi', 'laixinjie', 'yangruohan', 'zhangyingkui', 'liwen',
                           'lijiamin', 'zhengzegeng', 'luowei', 'chenjialing', 'guhaoying', 'wuhongzhen', 'linjiawei',
                           'laiyingru', 'lisinan', 'zhoulikai', 'yangweijie', 'renpei', 'gongliang', 'weiliyang',
                           'zhengzhicheng', 'xiezhuolin', 'zhangkuiqing', 'tangwenjie', 'huangxiaoqin', 'panjiadong',
                           'lvdan', 'wangxinnian', 'laiqiqi', 'zhenglimeng', 'liangxiaosi', 'linjiaqi', 'chenjiaxing',
                           'shangtianyu', 'pengxiaobin', 'ruanpanpan', 'guoqiong', 'sushuiqing', 'huangzihang',
                           'huangxiaoye', 'gongyue', 'tianfangbi', 'wangjing', 'wuxudong', 'xiaofen', 'chenhongyu',
                           'suzhilong', 'dengliucheng', 'gaochunbo', 'fuchenjie', 'caojunhai', 'zhongxinyu',
                           'ouyangpei', 'jinxiaowan', 'geminghui', 'zhanjiaxuan', 'luokaiqian', 'pengsongqiao',
                           'huzeming', 'zhuangyingzhen', 'limeng', 'yinli', 'quyangyang', 'musainan', 'shujun',
                           'zhengdanna', 'yanghan', 'yangzhiguang', 'zhanghang', 'nijiangpeng', 'liyang', 'zhongyankun',
                           'chenzhuo', 'chenyu', 'luojianming', 'chenpeng', 'xubingqi', 'qiujinyue', 'zhangyan',
                           'changxiangxu', 'zhujingxian', 'hanbo', 'zhurongxiang', 'changming', 'xiongguangyang',
                           'wangxingyong', 'xiangli', 'linshiyi', 'gaoyiqian', 'mayizhen', 'liucheng', 'wuhaitao',
                           'changhongguang', 'limin', 'tanghuan', 'xiegang', 'yanyubai', 'zhangjunjie', 'wangbaoliang',
                           'zhangbensong', 'jiangwenyao', 'wangkewei', 'liuanqi', 'zhangxiaohan', 'chenyizhu',
                           'majiake', 'yujunyi', 'jiangjie', 'zhuzhenkun', 'chenyongfa', 'chenyongcai', 'yangkai',
                           'liujia', 'chengjiawen', 'lvjingya', 'liqianying', 'yejiexia', 'qianyinqiu', 'wangjuan',
                           'taoxiudian', 'chenhongxu', 'sunyuyao', 'kangping', 'wangxiufang', 'liuxinwen',
                           'linlanfang', 'wengsifan', 'lichuanfu', 'liuchangdong', 'dutao', 'zhangge', 'xiaminghui',
                           'zhaoqingsong', 'shangpeihan', 'zhangjin', 'hejiemin', 'zhangxiangnan', 'lizhitao',
                           'longshixiao', 'luchunxian', 'tangjunzhi', 'zhuzhenye', 'chenxianger', 'chenyongkang',
                           'wutong', 'lizihao', 'zanjianhuan', 'tantiancheng', 'xujiangyao', 'fanjilei', 'duxiaomeng',
                           'wangying', 'huxinyan', 'zhouxianhang', 'guoda', 'suoya', 'huangxuanli', 'wanqiao', 'yangwensi',
                           'liuboyi', 'chentianxiao', 'limuyou', 'jiangzhiming', 'lixingxing', 'fangyue', 'xianglei',
                           'yurongjian', 'liyuqin', 'zengning', 'chenjiangtao', 'lizeshun', 'zhangxinyu', 'yangyuanyuan',
                           'moningkai', 'tujiali', 'rongchuyu', 'zhouweixiao', 'yangzhaonan', 'cairuilin',
                           'dongyijing', 'zhangbaowen', 'lixueyi', 'liuxusheng', 'luchengzhi', 'jishujian', 'zhaoshilin',
                           'wangsi', 'zhujiayi', 'zhangna', 'yangkaibo', 'huangjianan', 'liyiling', 'chenming',
                           'liuyaqi', 'penglingxiu', 'wuhaisi', 'liuzhao', 'dengjun', 'chenyanxia', 'xuliang', 'zhaofeng',
                           'luojiangliu', 'xuyue', 'lixiaokai', 'huangweicong', 'lizhangjian', 'xiele', 'lijianyao',
                           'libingbing', 'limingzhao', 'wuweixuan', 'niuyuan', 'liyongshun', 'xupei', 'hejiawen',
                           'zhaoyuliang', 'zhangzongxin', 'tangshi', 'niebeina', 'chenliaoran', 'chenwenjie', 'xiongwei',
                           'zhouqiuming', 'zhaowengui', 'zhaozhicheng', 'yuandawei', 'wangzhicheng', 'yaoyufeng',
                           'zhaohaoda', 'pangwenjun', 'xujinshuang', 'huyueyan', 'linjiaxin', 'chenzejia', 'linjiaming',
                           'chenmingting', 'xujiayang', 'xujiaohao', 'hannana', 'xuxiao', 'renjiao']
        self.operation1_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[0:76]]
        self.phase1_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[0:91]]
        pass

    def my_eliminate_task(self):
        label_ls = os.listdir(self.final_label_path)
        label_ls_1 = []
        label_ls_2 = []
        for i_t in label_ls:
            if int(i_t[1:4]) in self.phase1_people_number:
                label_ls_1.append(i_t)
                pass
            else:
                label_ls_2.append(i_t)
                pass
            pass
        label_ls_present = label_ls_1
        if self.dst_name is "DataSet2":
            label_ls_present = label_ls_2
            pass
        label_ls_present.sort()
        for i_label in label_ls_present:
            i_label_path = self.final_label_path + i_label
            label = self.read_txt(i_label_path)
            self.eliminate_error_action_video(label, i_label)
            # break
            pass
        pass

    def eliminate_error_action_video(self, label, file_name=None):
        """
        Eliminate the error video from the trimmed action video
        :param label: Reading list from label file.
        :param file_name: Label file name.
        :return: No return.
        """
        if len(np.array(label).shape) is 2:
            t_judge = np.array(label)[:, 3]
            a_judge = np.array(label)[:, 4]
            t_judge_error = np.where(t_judge == '2')[0]
            a_judge_error = np.where(a_judge == '2')[0]
            u_judge = list(set(t_judge_error).union(set(a_judge_error)))
            # print(file_name, "\n", a_judge, "\n", t_judge, "\n", u_judge, "\n", len(u_judge), "\n", int(file_name[1:4]))
            # raise RuntimeError
            if len(u_judge) > 0:
                for ii in u_judge:
                    n_people = int(file_name[1:4])
                    n_option = 2
                    if n_people in self.operation1_people_number:
                        n_option = 1
                        pass
                    n_times = int(file_name[5:8])
                    n_sequence = int(file_name[9:12])
                    n_action = int(label[ii][0])
                    for iii in range(1, 16):
                        n_camera = iii
                        video_name = self.file_model.format(n_option, n_people, n_camera, n_times, n_sequence, n_action, self.file_suffixes)
                        # print(video_name)
                        # raise RuntimeError
                        src_path = self.src_video_path + video_name
                        dst_path = self.dst_video_path + video_name
                        if os.path.exists(src_path) and not os.path.exists(dst_path):
                            os.rename(src_path, dst_path)
                            print("\"{:s}\" has done!".format(video_name))
                            # raise RuntimeError
                            pass
                        else:
                            print("\"{:s}\" was not existed, or has been moved!".format(video_name))
                            pass
                        pass
                    pass
                pass
            pass
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

    @staticmethod
    def generate_list(original_path):
        # original_path = self.root_path
        path_list = []
        file_list = os.listdir(original_path)
        for i, ICount in enumerate(file_list):
            path_list.append(original_path + ICount)
            pass
        return path_list, file_list
        pass

    def merge2labels(self, statistical_info=None):
        """
        Merge the original label and judgment label.
        """
        label_list = self.generate_list(self.root_path)
        for i, IContent in enumerate(label_list[1]):
            if os.path.exists(self.final_path + IContent):
                print("\"{:s}\" has done.".format(IContent))
                continue
                pass
            original_label = self.read_txt(self.root_path + IContent)
            judge_label = self.read_txt(self.judge_path + IContent)
            if len(original_label) == len(judge_label):
                if statistical_info is 1:
                    # --contrast action judge--
                    self.contrast_action_judge(original_label, judge_label, IContent)
                    pass
                if statistical_info is 2:
                    # --Count the number of action errors--
                    if self.present_parameter[1] is "original":
                        count_label = original_label
                        pass
                    else:
                        count_label = judge_label
                        pass
                    self.count_action_judge_error(count_label, self.present_parameter[2], IContent)
                    pass
                if statistical_info is None:  # There are no inconsistencies.
                    final_label = np.array(judge_label)
                    final_label[:, [3, 4]] = final_label[:, [4, 3]]  # Swap columns 4 and 5 of the action judgment label
                    coded_list_label = self.generate_action_order(final_label, IContent)

                    # --Specify the time window judgement--
                    # replaced_list_label = self.replace_time_windows_judgment(None, ['31', '26', '28', '25'], '1', coded_list_label)

                    # --Save the final labels--
                    final_list_label = coded_list_label
                    save_name = self.final_path + IContent
                    np.savetxt(save_name, np.array(final_list_label), delimiter=',', fmt='%s')
                    print("\"{:s}\" has done.".format(IContent))
                    pass
                pass

            else:
                print("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                logger.info("\"{:s}\" The length of original label is different from judge label !!!".format(IContent))
                continue
                pass
            # break
            # raise RuntimeError
            pass
        if statistical_info is 2:
            self.store_json(self.temp_store_path, self.action_error)
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

    @staticmethod
    def compare_original_judge(original_path, judge_path):
        """
        Compare the number of original and judgment tag files, and print them.
        :param original_path: The file path of original label.
        :param judge_path: The file path of judge label.
        :return: No return.
        """
        original_list = os.listdir(original_path)
        judge_list = os.listdir(judge_path)
        print("There are some files not in judge list.\n", [i for i in original_list if i not in judge_list])
        print("There are some files not in original list.\n", [i for i in judge_list if i not in original_list])
        pass

    @staticmethod
    def contrast_action_judge(original_label, judge_label, file_name):
        """
        Contrast action judge, You need to deal with it, If there are inconsistencies.
        :param original_label: Reading list from original file.
        :param judge_label: Reading list from judge file.
        :param file_name: Label file name.
        :return: No return.
        """
        # print(file_name, len(np.array(original_label).shape))
        if len(np.array(original_label).shape) is 1:
            print("Original label damaged {:s}".format(file_name))
            logger.info("Original label damaged {:s}".format(file_name))
            pass
        if len(np.array(judge_label).shape) is 1:
            print("Judge label damaged {:s}".format(file_name))
            logger.info("Judge label damaged {:s}".format(file_name))
            pass
        if len(np.array(judge_label).shape) is 2 and len(np.array(original_label).shape) is 2:
            original_action = np.array(original_label)[:, 3]
            judge_action = np.array(judge_label)[:, 3]
            if np.where(original_action != judge_action)[0].size > 0:
                for ii in np.where(original_action != judge_action)[0]:
                    print("Different {:s}, {:d}, {:s}".format(file_name, ii + 1, original_label[ii][0]))
                    logger.info("Different {:s}, {:d}, {:s}".format(file_name, ii + 1, original_label[ii][0]))
                    pass
                pass
            pass
        pass

    def count_action_judge_error(self, label, judge_type=3, file_name=None):
        """
        Count the number of action errors
        :param label: Reading list from label file.
        :param judge_type: Counting the action judge value = 3 or time windows judge value = 4?
        :param file_name: Label file name.
        :return: No return.
        """
        if len(np.array(label).shape) is 2:
            judge = np.array(label)[:, judge_type]
            if np.where(judge == '2')[0].size > 0:
                for ii in np.where(judge == '2')[0]:
                    self.action_error["Total"] = self.action_error["Total"] + 1
                    if not label[ii][0] in self.action_error.keys():
                        self.action_error.update({label[ii][0]: 1})
                        pass
                    else:
                        self.action_error[label[ii][0]] = self.action_error[label[ii][0]] + 1
                        pass
                    print("{:s} {:s}, {:d}, {:s}".format(self.json_name, file_name, ii + 1, label[ii][0]))
                    logger.info("{:s} {:s}, {:d}, {:s}".format(self.json_name, file_name, ii + 1, label[ii][0]))
                    pass
                pass
            pass
        pass

    @staticmethod
    def store_json(store_path, data):
        with open(store_path, 'w') as json_file:
            json_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))

    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    my_task = AddressLabel()
    my_task.my_eliminate_task()

    # my_task.compare_original_judge(my_task.root_path, my_task.judge_path)
    # raise RuntimeError
    # if not os.path.exists(my_task.final_path):
    #     os.mkdir(my_task.final_path)
    #     pass
    # if not os.path.exists(my_task.log_path):
    #     os.mkdir(my_task.log_path)
    #     pass
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='{:s}{:s}_address_label.log'.format(my_task.log_path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
    #                     datefmt='%Y/%m/%d %H:%M:%S',
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
    # logger = logging.getLogger(__name__)
    # # my_task.merge2labels(my_task.present_parameter[3])
    # t_file_list = my_task.generate_list(my_task.final_path)
    # for i, i_content in enumerate(t_file_list[1]):
    #     t_label = my_task.read_txt(my_task.final_path + i_content)
    #     my_task.count_action_judge_error(t_label, my_task.present_parameter[1], i_content)
    #     pass
    # my_task.store_json(my_task.temp_store_path, my_task.action_error)

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass
