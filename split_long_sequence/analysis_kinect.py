# This code is for Conversion between different frame rates i.e.,25fps & 30fps

import os
import numpy as np
import time
import logging
import json
import cv2
import csv
import shutil as st
from multiprocessing import Pool
import pickle
from PIL import Image
import matplotlib.pyplot as plt
import glob


class AnalysisKinect(object):
    def __init__(self):
        self.perform_environment = [["/data/szj/data/", "/ssd_data/zqs/workspace/dataset-preprocessing/"],  # 47
                                    ["Z:/", "D:/pycharm_project/dataset_preprocessing/"],  # laptop
                                    ["/data/zqs/datasets/cas_mhad/", "/data/zqs/workplace/dataset_preprocessing/"]]  # 34
        self.split_depth_path = "/data/zqs/datasets/split_depth/"
        self.temp_unzip_bin = "/data/zqs/workplace/temp/"
        self.present_envir = self.perform_environment[2]
        self.hikvision_path = self.present_envir[0] + "publish_data/RGB_HIKVISION/"
        self.kinect_path = self.present_envir[0] + "publish_data/RGB_KINECT/"
        self.kinect_capture_path = self.present_envir[0] + "publish_data/RGB_KINECT_CAPTURE/"
        self.hikvision_capture_path = self.present_envir[0] + "publish_data/RGB_KINECT_CAPTURE/"

        self.depth_path = self.present_envir[0] + "publish_data/DEPTH_KINECT/"
        self.log_path = self.present_envir[0] + "publish_data/log/"
        self.log_name = '{:s}{:s}_statistic_frames.log'.format(self.log_path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        self.final_label_path = self.present_envir[0] + "publish_data/label/"

        # self.logger = None
        self.analysis_frames = {"Total": [0] * 19}
        self.analysis_duration = {"Total": [0.0] * 19}
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
        self.operation1_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[0:76]]
        self.operation2_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[76:]]
        self.phase1_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[0:91]]
        self.phase2_people_number = [self.names_alphabet.index(i) + 1 for i in self.names_time[91:]]
        self.store_json_path = None
        self.store_csv_path = None
        self.temp_list_path = None
        self.temp_delete_path = None
        self.phase1_hikvision_frame_json = None
        self.name = None
        self.src_bin = self.split_depth_path
        self.dst_bin_tgz = "/data/zqs/datasets/tgz_split_depth/"
        pass

    def anlysis_video(self, files_list):
        # --Logging start--
        logger_handler = RewriteFileLogHandler(self.log_name)
        logger = logging.getLogger(__name__)
        logger.addHandler(logger_handler)
        logger.setLevel(logging.DEBUG)



    def split_depth(self, files_list):
        # --read hikvision frame--
        self.temp_list_path = "/data/zqs/datasets/cas_mhad/publish_data/log/phase1_hikvision_frame.txt"
        self.temp_delete_path = "/data/zqs/datasets/cas_mhad/publish_data/log/phase2_2019-08-06-12-37-31_split_avi.txt"
        self.phase1_hikvision_frame_json = self.read_txt_to_json(self.temp_list_path, ',')

        # --Logging start--
        logger_handler = RewriteFileLogHandler(self.log_name)
        logger = logging.getLogger(__name__)
        logger.addHandler(logger_handler)
        logger.setLevel(logging.DEBUG)

        # --path claiming--
        temp_7z_path = self.depth_path + files_list
        temp_unzip_path = self.temp_unzip_bin + files_list[:-3]

        # --Split the big bin file--
        label_name = files_list[4:8] + files_list[12:].replace('7z', 'txt')
        frame_25fps = float(self.phase1_hikvision_frame_json[label_name[0:-4]][0])
        if os.path.exists(self.final_label_path + label_name):
            label_list = self.read_txt(self.final_label_path + label_name, ',')

            # --Unzip the 7z file--
            temp_dst_path = self.split_depth_path + files_list.replace('.7z', 'A{:03d}.bin'.format(int(label_list[0][0])))
            if os.path.exists(temp_dst_path):
                print("The file \"{:s}\" has been done.".format(files_list))
                return
                pass
            self.is_path_existed_if_no_mk_it(temp_unzip_path)
            cmd_unzip = "7z x {:s} -o{:s} -y".format(temp_7z_path, temp_unzip_path)
            src_path = temp_unzip_path + "/depth.bin"
            if not os.path.exists(src_path):
                if os.system(cmd_unzip) is 0:
                    print("The file \"{:s}\" has been unzipped.".format(files_list))
                    # logger.info("The file \"{:s}\" has been unzipped.".format(files_list))
                    pass
                else:
                    print("The file \"{:s}\" was not decompressed successfully.".format(files_list))
                    logger.info("The file \"{:s}\" was not decompressed successfully.".format(files_list))
                    return
                    pass
                pass
            if os.path.exists(src_path):
                with open(src_path, mode='rb') as f:
                    try:
                        arr = np.int32(pickle.load(f))
                        pass
                    except:
                        logger.info("src_path \"{:s}\" have some problems.".format(src_path))
                        return
                        pass
                    coefficient = len(arr) / frame_25fps
                    for i, i_content in enumerate(label_list):
                        begin_f = round(int(i_content[1]) * coefficient)
                        end_f = round(int(i_content[2]) * coefficient)
                        dst_name = files_list.replace('.7z', 'A{:03d}.bin'.format(int(i_content[0])))
                        dst_path = self.split_depth_path + dst_name
                        if os.path.exists(dst_path):
                            print("\"{:s}\" has been existed!".format(dst_name))
                            # logger.info("\"{:s}\" has been existed!".format(dst_name))
                            continue
                            pass
                        if len(i_content) != 5:
                            self.name = "Label format has wrong!"
                            print(self.name)
                            logger.info("{},{}".format(dst_name, self.name))
                            continue
                            pass
                        if i_content[3] == "2" and i_content[4] == "2":
                            self.name = "Action judge or time windows wrong!"
                            print(self.name)
                            logger.info("{},{}".format(dst_name, self.name))
                            continue
                            pass
                        if (end_f - begin_f) <= 15:
                            print("\"{:s}\" Maybe something wrong in begin and end frames.".format(dst_name))
                            logger.info("\"{:s}\" Maybe something wrong in begin and end frames.".format(dst_name))
                            continue
                            pass
                        if (end_f - len(arr)) >= 15:
                            self.name = "End frame greater than source total frame 15!"
                            logger.info("{},{}".format(dst_name, self.name))
                            continue
                            pass
                        with open(dst_path, mode='wb') as f_s:
                            pickle.dump(arr[begin_f:end_f, :], f_s)
                            print("File \"{:s}\" has been split from file \"{:s}\".".format(dst_name, files_list))
                            logger.info("File \"{:s}\" has been split from file \"{:s}\".".format(dst_name, files_list))
                            pass
                        pass
                pass
            else:
                print("File \"{:s}\" does not existed!".format(files_list))
                # logger.info("File \"{:s}\" does not existed!".format(files_list))
                return
                pass
            pass
        else:
            print("Label file \"{:s}\" can not find!".format(label_name))
            logger.info("Label file \"{:s}\" can not find!".format(label_name))
            return
            pass
        # --Delete the temp big bin file--
        cmd_delete = "rm -r {:s}".format(temp_unzip_path)
        if os.system(cmd_delete) is 0:
            print("Temp file \"{:s}\" has been deleted!".format(temp_unzip_path))
            # logger.info("Temp file \"{:s}\" has been deleted!".format(temp_unzip_path))
            pass
        else:
            print("An error occurred while deleting the file \"{:s}\".".format(temp_unzip_path))
            logger.info("An error occurred while deleting the file \"{:s}\".".format(temp_unzip_path))
            return
            pass
        # --done--
        print("{:s} has done.".format(files_list))
        # logger.info("{:s} has done.".format(files_list))
        pass

    # This code is for compressing of split depth .bin files.
    # Take a people's data into a single .tgz compressed file.
    def batch_compress(self, people_number):
        src_bin_model = "O*P{:03d}C*T*S*A*.bin".format(people_number)
        dst_bin_model = "P{:03d}.tgz".format(people_number)
        src_path = self.src_bin + src_bin_model
        dst_path = self.dst_bin_tgz + dst_bin_model
        tar_cmd = "tar -zcvPf {:s} {:s}".format(dst_path, src_path)
        # print(tar_cmd)
        # raise RuntimeError
        if not os.path.exists(dst_path):
            s_time = time.time()
            if os.system(tar_cmd) == 0:
                print("{:s} successfully compressed!".format(dst_bin_model))
                pass
            e_time = time.time()
            print("{:s} spend {:.2f} for compressing.".format(src_bin_model, (e_time - s_time)))
            pass
        else:
            print("{:s} has been compressed!".format(dst_bin_model))
            pass
        pass

    # This function is for delete
    def batch_delete(self):
        with open(self.temp_delete_path) as lf:
            for line in lf.readlines():
                f_line = line.strip("\n")
                delete_name = "{:s}*.avi".format(f_line)
                delete_cmd = "rm " + self.kinect_capture_path + delete_name
                if os.system(delete_cmd) == 0:
                    print("{:s} has been deleted!".format(delete_name))
                    pass
                else:
                    print("{:s} error with executing delete command!".format(delete_name))
                    pass
                # raise RuntimeError
                pass
            pass
        pass

    def convert_frame_avi_kiniect(self, list_path):
        for i, i_content in enumerate(list_path):
            people = int(i_content[0][1:4])
            operation = 1
            if people not in self.operation1_people_number:
                operation = 2
                pass
            repeat_time = int(i_content[0][5:8])
            sequence = int(i_content[0][9:12])
            for ii, camera in enumerate(range(16, 20)):
                temp_avi_file_name = self.file_model.format(operation, people, camera, repeat_time, sequence, "avi")
                transformed_frame = float(i_content[ii + 1])
                self.trans_frame_rating_video(transformed_frame,
                                              self.kinect_path + temp_avi_file_name,
                                              self.s001_s007_30fps_avi_path + temp_avi_file_name)
                pass
            pass
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
        # --Logging start--
        logger_handler = RewriteFileLogHandler(self.log_name)
        logger = logging.getLogger(__name__)
        logger.addHandler(logger_handler)
        logger.setLevel(logging.DEBUG)

        video_list = self.generate_list(present_path)
        for i, i_content in enumerate(video_list[1]):
            capture = cv2.VideoCapture(video_list[0][i])
            if capture.isOpened():
                frame = int(capture.get(7))
                rate = capture.get(5)
                duration = round(frame / rate, 3)
                if frame <= 0:
                    print("{:s} frame was wrong.".format(i_content))
                    logger.info("{:s} frame was wrong.".format(i_content))
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
                logger.info("{:s} was broken.".format(i_content))
                continue
                pass
        # --store static results as a json file--
        self.store_json_path = self.log_path + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_frames.json"
        self.store_json(self.store_json_path, self.analysis_frames)

        self.store_json_path = self.log_path + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_duration.json"
        self.store_json(self.store_json_path, self.analysis_duration)

        # --store static results as a csv file--
        self.store_csv_path = self.log_path + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_frames.csv"
        self.write_csv(self.analysis_frames, self.store_csv_path)

        self.store_csv_path = self.log_path + present_path.split('/')[-2] + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "_statistic_duration.csv"
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

    def trans_frame_rating_video(self, transformed_frame=29.5, video_path=None, transformed_path=None):
        if os.path.exists(video_path) and not os.path.exists(transformed_path):
            cmd_command = "ffmpeg -r {:.1f} -i {:s} -b:v 4096000 {:s}".format(transformed_frame, video_path, transformed_path)
            os.system(cmd_command)
            print("Video {:s} has been converted from 25 fps to {:.1f} fps".format(video_path.split('/')[-1], transformed_frame))
            self.logger.info("Video {:s} has been converted from 25 fps to {:.1f} fps".format(video_path.split('/')[-1], transformed_frame))
            pass
        else:
            print("Video {:s} conversion failed".format(video_path.split('/')[-1]))
            self.logger.info("Video {:s} conversion failed".format(video_path.split('/')[-1]))
            pass
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

    @staticmethod
    def split_video(src_video, begin_time, over_time, dst_video):
        if os.path.exists(src_video) and not os.path.exists(dst_video):
            cmd_command = "ffmpeg  -i {:s} -vcodec copy -acodec copy -ss {:s} -to {:s} {:s} -y".format(src_video, begin_time, over_time, dst_video)
            os.system(cmd_command)
            print("{:s} has been cut from {:s}.".format(dst_video, src_video))
            # self.logger.info("{:s} has {:d} frames.".format(i_content, frame))
            pass
        pass

    # --Convert Bin sequence files to multiple PNG images--
    @staticmethod
    def bin_sequence_to_png(path, save_png_path=None):
        with open(path, mode='rb') as f:
            arr = np.int32(pickle.load(f))
            # file_path = path.replace('.bin', '2.bin')
            # with open(file_path, mode='wb') as f60:
            #     pickle.dump(arr[0:1625, :], f60)
            # raise RuntimeError
            for i in range(len(arr)):
                temp_arr = arr[i, :].reshape(424, 512)
                # plt.imshow(temp_arr)
                # plt.imshow(temp_arr, cmap="gray", vmin=0, vmax=8000)
                # plt.show()
                # plt.close()
                image = Image.fromarray(temp_arr)  # .convert('L')
                image.save("{:s}/{:04d}.png".format(save_png_path, i+1), 'png')
                print("{:04d} has been saved.".format(i+1))
                pass
        # raise RuntimeError
        pass

    @staticmethod
    def split_big_bin(src_path, dst_path, begin_f, end_f, frame_25fps):
        if os.path.exists(src_path) and not os.path.exists(dst_path) and begin_f < end_f:
            with open(src_path, mode='rb') as f:
                arr = np.int32(pickle.load(f))
                coefficient = len(arr) / frame_25fps
                begin_f = round(begin_f * coefficient)
                end_f = round(end_f * coefficient)
                with open(dst_path, mode='wb') as f_s:
                    pickle.dump(arr[begin_f:end_f, :], f_s)
                    return True
                    pass
                pass
            pass
        else:
            return False
            pass
        pass

    @staticmethod
    def process_log(log_path):
        logger_handler = RewriteFileLogHandler(log_path)
        logger = logging.getLogger(__name__)
        logger.addHandler(logger_handler)
        logger.setLevel(logging.DEBUG)
        return logger
        pass

    @staticmethod
    def read_txt_to_json(path, split_character=","):
        f_content = {}
        with open(path) as lf:
            for line in lf.readlines():
                f_line = line.strip("\n").split(split_character)
                f_content.update({f_line[0]: f_line[1:]})
                pass
            pass
        return f_content
        pass

    pass


# --Override the emit method in FileLogHandler class--
class RewriteFileLogHandler(logging.Handler):
    def __init__(self, file_path):
        self._fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = "{}\n".format(self.format(record))
        os.write(self._fd, msg.encode('utf-8'))


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)

    my_task = AnalysisKinect()
    my_task.statistic_frames(my_task.hikvision_path)

    # temp_bin_path = "E:/pycharm_project/temp/O002P055C019T002S003/"
    # AnalysisKinect.bin_sequence_to_png(temp_bin_path + "depth.bin", temp_bin_path)

    # my_task.batch_delete()
    # my_task.bin_sequence_to_png("/data/zqs/datasets/split_depth/O001P009C016T001S001A002.bin")

    # --generate files list--
    # depth_lst = my_task.generate_list(my_task.depth_path)[1]
    # depth_lst.sort()

    # people_ls = my_task.phase1_people_number
    # people_ls.sort()

    # # --Multiple processes--
    # p = Pool(24)
    # # p.map(my_task.split_depth, depth_lst)
    # p.map(my_task.batch_compress, people_ls)
    # p.close()
    # p.join()
    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass

