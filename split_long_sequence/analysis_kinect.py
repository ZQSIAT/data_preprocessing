# This code is for Conversion between different frame rates i.e.,25fps & 30fps

import os
import numpy as np
import time
import logging
import json
import cv2
import csv
import shutil as st

class AnalysisKinect(object):
    def __init__(self):
        self.perform_environment = [["/data/szj/data/", "/ssd_data/zqs/workspace/dataset-preprocessing/"],
                                    ["Z:/", "D:/pycharm_project/dataset_preprocessing/"]]
        self.dst_path = "DataSet1"
        self.present_envir = self.perform_environment[1]
        self.hikvision_path = self.present_envir[0] + "Preprocessing_Test/{:s}/RGB_HIKVISION/".format(self.dst_path)
        self.kinect_path = self.present_envir[0] + "Preprocessing_Test/{:s}/KINECT/RGB_KINECT/".format(self.dst_path)
        self.log_path = self.present_envir[1] + "/log/"
        self.logger = None
        self.analysis_frames = {"Total": [0]*19}
        self.analysis_duration = {"Total": [0.0]*19}
        self.file_model = "O{:03d}P{:03d}C{:03d}T{:03d}S{:03d}.{:s}"
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
        self.operation1_people_number = [self.names_alphabet.index(i)+1 for i in self.names_time[0:76]]
        self.operation2_people_number = [self.names_alphabet.index(i)+1 for i in self.names_time[76:]]
        self.phase1_people_number = [self.names_alphabet.index(i)+1 for i in self.names_time[0:91]]
        self.phase2_people_number = [self.names_alphabet.index(i)+1 for i in self.names_time[91:]]
        self.store_json_path = None
        self.store_csv_path = None
        pass

    def generate_video_names(self, phase=1, video_type='mp4'):
        """
        Generate the file name for video.
        :param phase:phase1: 1-91, phase2: 92-276
        :param video_type: Hikvision: video_type='mp4', Kinect: video_type='avi'
        :return:The list of video files.
        """
        # --todo--
        pass

    def statistic_frames(self, present_path):
        """
        Count the total number of frames for all video in this path.
        :param present_path:The path of videos.
        :return:No return. The results will write to a json file.
        """
        video_list = self.generate_list(present_path)
        for i, i_content in enumerate(video_list[1]):
            capture = cv2.VideoCapture(video_list[0][i])
            if capture.isOpened():
                frame = int(capture.get(7))
                rate = capture.get(5)
                duration = round(frame/rate, 3)
                if frame < 0:
                    print("{:s} frame was wrong.".format(i_content))
                    self.logger.info("{:s} frame was wrong.".format(i_content))
                    continue
                    pass
                camera = int(i_content[9:12])
                dict_key = i_content[4:8] + i_content[12:16] + i_content[16:20]
                # --read frames to dict--
                if dict_key not in self.analysis_frames.keys():
                    dict_value = [0] * 19
                    dict_value[camera - 1] = frame
                    self.analysis_frames.update({dict_key: dict_value})
                    print("{:s} has {:d} frames.".format(i_content, frame))
                    # self.logger.info("{:s} has {:d} frames.".format(i_content, frame))
                    pass
                if dict_key in self.analysis_frames.keys():
                    self.analysis_frames[dict_key][camera - 1] = frame
                    print("{:s} has {:d} frames.".format(i_content, frame))
                    # self.logger.info("{:s} has {:d} frames.".format(i_content, frame))
                    pass
                # --read duration to dict--
                if dict_key not in self.analysis_duration.keys():
                    dict_value = [0.0] * 19
                    dict_value[camera - 1] = duration
                    self.analysis_duration.update({dict_key: dict_value})
                    print("{:s} has {:.3f} seconds.".format(i_content, duration))
                    # self.logger.info("{:s} has {:.3f} seconds.".format(i_content, duration))
                    pass
                if dict_key in self.analysis_duration.keys():
                    self.analysis_duration[dict_key][camera - 1] = duration
                    print("{:s} has {:.3f} seconds.".format(i_content, duration))
                    # self.logger.info("{:s} has {:.3f} seconds.".format(i_content, duration))
                    pass
                pass
            else:
                print("{:s} was broken.".format(i_content))
                self.logger.info("{:s} was broken.".format(i_content))
                continue
                pass
        # --store static results as a json file--
        self.store_json_path = self.log_path + self.dst_path + "_" + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_frames.json"
        self.store_json(self.store_json_path, self.analysis_frames)

        self.store_json_path = self.log_path + self.dst_path + "_" + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_duration.json"
        self.store_json(self.store_json_path, self.analysis_duration)

        # --store static results as a csv file--
        self.store_csv_path = self.log_path + self.dst_path + "_" + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_frames.csv"
        self.write_csv(self.analysis_frames, self.store_csv_path)

        self.store_csv_path = self.log_path + self.dst_path + "_" + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_duration.csv"
        self.write_csv(self.analysis_duration, self.store_csv_path)

        pass

    @staticmethod
    def generate_list(original_path):
        path_list = []
        file_list = os.listdir(original_path)
        for i, ICount in enumerate(file_list):
            path_list.append(original_path + ICount)
            pass
        return path_list, file_list
        pass

    @staticmethod
    def check_video_inform(video_path):
        if os.path.exists(video_path):
            cmd_command = "ffmpeg -i {:s}".format(video_path)
            os.system(cmd_command)
            pass
        pass

    @staticmethod
    def trans_coding_video(video_path, transformed_path):
        if os.path.exists(video_path) and not os.path.exists(transformed_path):
            cmd_command = "ffmpeg -y -i {:s} -strict -2  -qscale 0 -intra {:s}".format(video_path, transformed_path)
            os.system(cmd_command)
            pass
        pass

    @staticmethod
    def trans_frame_rating_video(transformed_frame=30, video_path=None, transformed_path=None):
        if os.path.exists(video_path) and not os.path.exists(transformed_path):
            cmd_command = "ffmpeg -r {:d} -i {:s} -b 4096000 {:s}".format(transformed_frame, video_path, transformed_path)
            os.system(cmd_command)
            pass
        pass

    def log_parameter(self, log_path):
        logging.basicConfig(level=logging.DEBUG,
                            filename='{:s}{:s}_address_label.log'.format(log_path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                            datefmt='%Y/%m/%d %H:%M:%S',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        pass

    @staticmethod
    def store_json(store_path, data):
        with open(store_path, 'w') as json_file:
            json_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
            pass
        pass

    @staticmethod
    def read_json(data):
        with open(data, 'r') as load_f:
            load_dict = json.load(load_f)
            pass
        return load_dict
        pass

    @staticmethod
    def write_csv(load_json, csv_path):
        f = open(csv_path, 'w')
        csv_write = csv.writer(f)
        csv_write.writerow(load_json.keys())
        for key in load_json.keys():
            csv_write.writerow(load_json[key])
            pass
        f.close()
        pass

    @staticmethod
    def merge_frame_statistic(dict_kinect=None, dict_hikvision=None):
        for dict_key in dict_hikvision.keys():
            if dict_key not in dict_kinect.keys():
                dict_kinect.update({dict_key: dict_hikvision[dict_key]})
                print("{:s} not in the dict_kinect, and has merged.".format(dict_key))
                # self.logger.info("{:s} has {:d} frames.".format(i_content, frame))
                pass
            if dict_key in dict_kinect.keys():
                dict_kinect[dict_key][0:15] = dict_hikvision[dict_key][0:15]
                print("{:s} has merged.".format(dict_key))
                # self.logger.info("{:s} has {:d} frames.".format(i_content, frame))
                pass
            pass
        return dict_kinect
        pass

    @staticmethod
    def move_files(src_path, dst_path):
        if os.path.exists(src_path) and not os.path.exists(dst_path):
            try:
                st.move(src_path, dst_path)
                pass
            except st.Error as e:
                for Src, Dst, Msg in e.args[0]:
                    print(Src, Dst, Msg)
                    pass
                pass
            pass
        pass

    @staticmethod
    def is_path_existed_if_no_mk_it(path):
        """
        Check the path existing or not, if not create it.
        :param path: Must be a path not a file.
        :return: No return.
        """
        if not os.path.exists(path):
            os.mkdir(path)
            pass
        pass

    @staticmethod
    def read_txt(path, split_character=" "):
        f_content = []
        with open(path) as lf:
            for line in lf.readlines():
                f_line = line.strip("\n").split(split_character)
                f_content.append(f_line)
                pass
            pass
        return f_content
        pass

    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)

    my_task = AnalysisKinect()
    """
    # --move broken mp4 videos--
    t_mp4_broken_log_path = my_task.log_path + "phase1_hikvision_mp4_broken.log"
    t_mp4_broken_path = "Z:/Preprocessing_Test/DataSet1/temp_mp4_broken/"
    my_task.is_path_existed_if_no_mk_it(t_mp4_broken_path)
    list_broken_mp4 = (my_task.read_txt(t_mp4_broken_log_path))
    for ii, ii_content in enumerate(list_broken_mp4):
        src = my_task.hikvision_path + ii_content[0]
        dst = t_mp4_broken_path + ii_content[0]
        my_task.move_files(src, dst)
        print("{:d} {:s} has done.".format(ii+1, ii_content[0]))
        pass
    raise RuntimeError
    """

    """
    # --merge statistic of kinect and hikvision--
    t_k_path = my_task.log_path + "DataSet1_RGB_KINECT2019-07-08-12-30-05_statistic_frames.json"
    t_h_path = my_task.log_path + "DataSet1_RGB_HIKVISION2019-07-09-00-03-53_statistic_frames.json"
    t_m_j_path = my_task.log_path + "phase1_merged_statistic.json"
    t_m_csv_path = my_task.log_path + "phase1_merged_statistic.csv"
    merged_dict = my_task.merge_frame_statistic(my_task.read_json(t_k_path), my_task.read_json(t_h_path))
    my_task.store_json(t_m_j_path, merged_dict)
    my_task.write_csv(merged_dict, t_m_csv_path)
    raise RecursionError
    """
    my_task.log_parameter(my_task.log_path)
    my_task.statistic_frames(my_task.hikvision_path)

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass

