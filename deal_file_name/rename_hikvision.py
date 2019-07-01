import os
import shutil as st
import time
from multiprocessing import Pool
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='{:s}_some_error_file.log'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
# logger.info('This is a log info')
# logger.debug('Debugging')
# logger.warning('Warning exists')
# logger.info('Finish')
class RenameHikvision(object):
    def __init__(self):

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
        self.new_name = "O{:03d}P{:03d}C{:03d}T{:03d}S{:03d}.mp4"
        self.dst_path = "//172.20.12.174/cas_mhad/Preprocessing_Test/DataSet2/RGB_HIKVISION/"
        # self.dst_path = "//172.20.12.174/cas_mhad/DATASET_BACKUP/HIKVISION/temp_dst/"
        # self.root_path = "//172.20.12.174/cas_mhad/DATASET_BACKUP/HIKVISION/temp/"
        # self.root_path = "//172.20.12.174/cas_mhad/DATASET_BACKUP/HIKVISION/1-91_HIKVISION/"
        # self.normal_samples_len = 24
        self.root_path = "//172.20.12.174/cas_mhad/DATASET_BACKUP/HIKVISION/92-276_HIKVISION/"
        self.normal_samples_len = 21
        pass

    def filter_sequence(self, key_words, src_list):
        temp = list(filter(lambda x: x.startswith(key_words), src_list))
        temp.sort()
        return temp
        pass

    def rename_hikvision(self, path):
        dst_root = self.dst_path
        now_subject_path = path
        subject = now_subject_path.split('/')[-2]
        # print(subject)
        if self.names_time.index(subject) < 66:
            option = 1
            pass
        else:
            option = 2
            pass

        people = self.names_alphabet.index(subject) + 1

        temp_sequence_list = os.listdir(now_subject_path)
        # print(len(temp_sequence_list))
        now_sequence_list = list(filter(lambda x: x.startswith('a0') or x.startswith('bla'), temp_sequence_list))
        # print(len(now_sequence_list))
        if not len(now_sequence_list) == len(temp_sequence_list):
            print("{:s} there are some files should not be here!!!".format(now_subject_path))
            logger.info("{:s} there are some files should not be here!!!".format(now_subject_path))
            pass
        if len(now_sequence_list) < 1:
            print("{:s} no files be here!!!".format(now_subject_path))
            logger.info("{:s} no files be here!!!".format(now_subject_path))
            pass
        if not len(now_sequence_list) == self.normal_samples_len:
            print("{:s} don't have {:d} samples!!!".format(now_subject_path, self.normal_samples_len))
            logger.info("{:s} don't have {:d} samples!!!".format(now_subject_path, self.normal_samples_len))
            pass

        for i, ICount in enumerate(now_sequence_list):
            if ICount[0:2] == 'a0':
                sequence = int(ICount[2])
                time = self.filter_sequence(ICount[0:3], now_sequence_list).index(ICount) + 1
                pass
            else:
                sequence = 8
                time = self.filter_sequence(ICount[0:3], now_sequence_list).index(ICount) + 1
                pass
            if time > 3:
                print("{:s} repeat more than 3 times.".format(now_subject_path + ICount[0:3]))
                logger.info("{:s} repeat more than 3 times.".format(now_subject_path + ICount[0:3]))
                pass
            if not len(os.listdir(now_subject_path + ICount)) == 15:
                print("{:s} have not enough 15 cameras.".format(now_subject_path + ICount))
                logger.info("{:s} have not enough 15 cameras.".format(now_subject_path + ICount))
                pass
            for j, JCount in enumerate(os.listdir(now_subject_path + ICount)):
                camera = int(JCount.split('_')[0].split('.')[-1])
                src_file = now_subject_path + ICount + '/' + JCount
                dst_file = dst_root + self.new_name.format(option, people, camera, time, sequence)
                if not JCount[-4:] == '.mp4':
                    print("{:s} there are some error files!!!".format(now_subject_path + ICount))
                    logger.info("{:s} there are some error files!!!".format(now_subject_path + ICount))
                    pass
                if JCount[-4:] == '.mp4' and os.path.exists(src_file) and not os.path.exists(dst_file):
                    os.rename(src_file, dst_file)
                    # print("{:s} have done.".format(src_file))
                    logger.info("{:s} have done.".format(src_file))
                    pass
                else:
                    # print("{:s} does not exists!!!".format(src_file))
                    logger.info("{:s} does not exists!!!".format(src_file))
                pass
            pass
        # raise RuntimeError
        pass

    def generate_list(self):
        original_path = self.root_path
        subject_list = []
        sequence_list = []
        file_list = os.listdir(original_path)

        for i, ICount in enumerate(file_list):
            subject_list.append(original_path + ICount  + '/')
            action_list = os.listdir(original_path + ICount)
            for j, JCount in enumerate(action_list):
                sequence_list.append(original_path + ICount + '/' + JCount + '/')
                pass
            pass
        return subject_list, sequence_list
        pass
    def save_names(self):
        my_csv = pd.DataFrame(data = self.names_alphabet)
        my_csv.to_csv(temp_path + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.csv', encoding = 'gbk')
        pass
    pass


if __name__ == "__main__":
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    temp_path = "F:/pycharm_preject/temp/"
    # name_time = ['zhuyaping', 'chenyipeng', 'sunshijie', 'haoluoying', 'lihongjian', 'fanxiaoyuan', 'guojunguang',
    #              'tianyanling', 'liqiang', 'shenguibao', 'linchuang', 'liuyuxiang', 'haojingxuan', 'liuyuan',
    #              'zhangshenghai', 'xiaozhuo', 'huangshuxian', 'huanghaiyan', 'linyanfei', 'zhaotaoling',
    #              'liujinmeng', 'lianroumin', 'chenjinbao', 'huangweijuan', 'lukaijie', 'zhongkaiyu', 'wangchao',
    #              'huangchi', 'maijinhui', 'lianshengxiong', 'linyue', 'zhulei', 'hujing', 'zhoulibing',
    #              'liujianeng', 'zhengshaoxuan', 'tanyuanqi', 'laixinjie', 'yangruohan', 'zhangyingkui', 'liwen',
    #              'lijiamin', 'zhengzegeng', 'luowei', 'chenjialing', 'guhaoying', 'wuhongzhen', 'linjiawei',
    #              'laiyingru', 'lisinan', 'zhoulikai', 'yangweijie', 'renpei', 'gongliang', 'weiliyang',
    #              'zhengzhicheng', 'xiezhuolin', 'zhangkuiqing', 'tangwenjie', 'huangxiaoqin', 'panjiadong',
    #              'lvdan', 'wangxinnian', 'laiqiqi', 'zhenglimeng', 'liangxiaosi', 'linjiaqi', 'chenjiaxing',
    #              'shangtianyu', 'pengxiaobin', 'ruanpanpan', 'guoqiong', 'sushuiqing', 'huangzihang',
    #              'huangxiaoye', 'gongyue', 'tianfangbi', 'wangjing', 'wuxudong', 'xiaofen', 'chenhongyu',
    #              'suzhilong', 'dengliucheng', 'gaochunbo', 'fuchenjie', 'caojunhai', 'zhongxinyu',
    #              'ouyangpei', 'jinxiaowan', 'geminghui', 'zhanjiaxuan', 'luokaiqian', 'pengsongqiao',
    #              'huzeming', 'zhuangyingzhen', 'limeng', 'yinli', 'quyangyang', 'musainan', 'shujun',
    #              'zhengdanna', 'yanghan', 'yangzhiguang', 'zhanghang', 'nijiangpeng', 'liyang', 'zhongyankun',
    #              'chenzhuo', 'chenyu', 'luojianming', 'chenpeng', 'xubingqi', 'qiujinyue', 'zhangyan',
    #              'changxiangxu', 'zhujingxian', 'hanbo', 'zhurongxiang', 'changming', 'xiongguangyang',
    #              'wangxingyong', 'xiangli', 'linshiyi', 'gaoyiqian', 'mayizhen', 'liucheng', 'wuhaitao',
    #              'changhongguang', 'limin', 'tanghuan', 'xiegang', 'yanyubai', 'zhangjunjie', 'wangbaoliang',
    #              'zhangbensong', 'jiangwenyao', 'wangkewei', 'liuanqi', 'zhangxiaohan', 'chenyizhu',
    #              'majiake', 'yujunyi', 'jiangjie', 'zhuzhenkun', 'chenyongfa', 'chenyongcai', 'yangkai',
    #              'liujia', 'chengjiawen', 'lvjingya', 'liqianying', 'yejiexia', 'qianyinqiu', 'wangjuan',
    #              'taoxiudian', 'chenhongxu', 'sunyuyao', 'kangping', 'wangxiufang', 'liuxinwen',
    #              'linlanfang', 'wengsifan', 'lichuanfu', 'liuchangdong', 'dutao', 'zhangge', 'xiaminghui',
    #              'zhaoqingsong', 'shangpeihan', 'zhangjin', 'hejiemin', 'zhangxiangnan', 'lizhitao',
    #              'longshixiao', 'luchunxian', 'tangjunzhi', 'zhuzhenye', 'chenxianger', 'chenyongkang',
    #              'wutong', 'lizihao', 'zanjianhuan', 'tantiancheng', 'xujiangyao', 'fanjilei', 'duxiaomeng',
    #              'wangying', 'huxinyan', 'zhouxianhang', 'guoda', 'suoya', 'huangxuanli', 'wanqiao', 'yangwensi',
    #              'liuboyi', 'chentianxiao', 'limuyou', 'jiangzhiming', 'lixingxing', 'fangyue', 'xianglei',
    #              'yurongjian', 'liyuqin', 'zengning', 'chenjiangtao', 'lizeshun', 'zhangxinyu', 'yangyuanyuan',
    #              'moningkai', 'tujiali', 'rongchuyu', 'zhouweixiao', 'yangzhaonan', 'cairuilin',
    #              'dongyijing', 'zhangbaowen', 'lixueyi', 'liuxusheng', 'luchengzhi', 'jishujian', 'zhaoshilin',
    #              'wangsi', 'zhujiayi', 'zhangna', 'yangkaibo', 'huangjianan', 'liyiling', 'chenming',
    #              'liuyaqi', 'penglingxiu', 'wuhaisi', 'liuzhao', 'dengjun', 'chenyanxia', 'xuliang', 'zhaofeng',
    #              'luojiangliu', 'xuyue', 'lixiaokai', 'huangweicong', 'lizhangjian', 'xiele', 'lijianyao',
    #              'libingbing', 'limingzhao', 'wuweixuan', 'niuyuan', 'liyongshun', 'xupei', 'hejiawen',
    #              'zhaoyuliang', 'zhangzongxin', 'tangshi', 'niebeina', 'chenliaoran', 'chenwenjie', 'xiongwei',
    #              'zhouqiuming', 'zhaowengui', 'zhaozhicheng', 'yuandawei', 'wangzhicheng', 'yaoyufeng',
    #              'zhaohaoda', 'pangwenjun', 'xujinshuang', 'huyueyan', 'linjiaxin', 'chenzejia', 'linjiaming',
    #              'chenmingting', 'xujiayang', 'xujiaohao', 'hannana', 'xuxiao', 'renjiao']
    # Names_alphabet = ["cairuilin", "caojunhai", "changhongguang", "changming", "changxiangxu", "chengjiawen",
    #                   "chenhongxu", "chenhongyu", "chenjialing", "chenjiangtao", "chenjiaxing", "chenjinbao",
    #                   "chenliaoran", "chenming", "chenmingting", "chenpeng", "chentianxiao", "chenwenjie",
    #                   "chenxianger", "chenyanxia", "chenyipeng", "chenyizhu", "chenyongcai", "chenyongfa",
    #                   "chenyongkang", "chenyu", "chenzejia", "chenzhuo", "dengjun", "dengliucheng", "dongyijing",
    #                   "dutao", "duxiaomeng", "fangyue", "fanjilei", "fanxiaoyuan", "fuchenjie", "gaochunbo",
    #                   "gaoyiqian", "geminghui", "gongliang", "gongyue", "guhaoying", "guoda", "guojunguang",
    #                   "guoqiong", "hanbo", "hannana", "haojingxuan", "haoluoying", "hejiawen", "hejiemin",
    #                   "huangchi", "huanghaiyan", "huangjianan", "huangshuxian", "huangweicong", "huangweijuan",
    #                   "huangxiaoqin", "huangxiaoye", "huangxuanli", "huangzihang", "hujing", "huxinyan",
    #                   "huyueyan", "huzeming", "jiangjie", "jiangwenyao", "jiangzhiming", "jinxiaowan", "jishujian",
    #                   "kangping", "laiqiqi", "laixinjie", "laiyingru", "liangxiaosi", "lianroumin", "lianshengxiong",
    #                   "libingbing", "lichuanfu", "lihongjian", "lijiamin", "lijianyao", "limeng", "limin", "limingzhao",
    #                   "limuyou", "linchuang", "linjiaming", "linjiaqi", "linjiawei", "linjiaxin", "linlanfang",
    #                   "linshiyi", "linyanfei", "linyue", "liqiang", "liqianying", "lisinan", "liuanqi", "liuboyi",
    #                   "liuchangdong", "liucheng", "liujia", "liujianeng", "liujinmeng", "liuxinwen", "liuxusheng",
    #                   "liuyaqi", "liuyuan", "liuyuxiang", "liuzhao", "liwen", "lixiaokai", "lixingxing", "lixueyi",
    #                   "liyang", "liyiling", "liyongshun", "liyuqin", "lizeshun", "lizhangjian", "lizhitao",
    #                   "lizihao", "longshixiao", "luchengzhi", "luchunxian", "lukaijie", "luojiangliu", "luojianming",
    #                   "luokaiqian", "luowei", "lvdan", "lvjingya", "maijinhui", "majiake", "mayizhen", "moningkai",
    #                   "musainan", "niebeina", "nijiangpeng", "niuyuan", "ouyangpei", "pangwenjun", "panjiadong",
    #                   "penglingxiu", "pengsongqiao", "pengxiaobin", "qianyinqiu", "qiujinyue", "quyangyang",
    #                   "renjiao", "renpei", "rongchuyu", "ruanpanpan", "shangpeihan", "shangtianyu", "shenguibao",
    #                   "shujun", "sunshijie", "sunyuyao", "suoya", "sushuiqing", "suzhilong", "tanghuan",
    #                   "tangjunzhi", "tangshi", "tangwenjie", "tantiancheng", "tanyuanqi", "taoxiudian",
    #                   "tianfangbi", "tianyanling", "tujiali", "wangbaoliang", "wangchao", "wangjing", "wangjuan",
    #                   "wangkewei", "wangsi", "wangxingyong", "wangxinnian", "wangxiufang", "wangying",
    #                   "wangzhicheng", "wanqiao", "weiliyang", "wengsifan", "wuhaisi", "wuhaitao", "wuhongzhen",
    #                   "wutong", "wuweixuan", "wuxudong", "xiaminghui", "xianglei", "xiangli", "xiaofen",
    #                   "xiaozhuo", "xiegang", "xiele", "xiezhuolin", "xiongguangyang", "xiongwei", "xubingqi",
    #                   "xujiangyao", "xujiaohao", "xujiayang", "xujinshuang", "xuliang", "xupei", "xuxiao", "xuyue",
    #                   "yanghan", "yangkai", "yangkaibo", "yangruohan", "yangweijie", "yangwensi", "yangyuanyuan",
    #                   "yangzhaonan", "yangzhiguang", "yanyubai", "yaoyufeng", "yejiexia", "yinli", "yuandawei",
    #                   "yujunyi", "yurongjian", "zanjianhuan", "zengning", "zhangbaowen", "zhangbensong",
    #                   "zhangge", "zhanghang", "zhangjin", "zhangjunjie", "zhangkuiqing", "zhangna", "zhangshenghai",
    #                   "zhangxiangnan", "zhangxiaohan", "zhangxinyu", "zhangyan", "zhangyingkui", "zhangzongxin",
    #                   "zhanjiaxuan", "zhaofeng", "zhaohaoda", "zhaoqingsong", "zhaoshilin", "zhaotaoling",
    #                   "zhaowengui", "zhaoyuliang", "zhaozhicheng", "zhengdanna", "zhenglimeng", "zhengshaoxuan",
    #                   "zhengzegeng", "zhengzhicheng", "zhongkaiyu", "zhongxinyu", "zhongyankun", "zhoulibing",
    #                   "zhoulikai", "zhouqiuming", "zhouweixiao", "zhouxianhang", "zhuangyingzhen", "zhujiayi",
    #                   "zhujingxian", "zhulei", "zhurongxiang", "zhuyaping", "zhuzhenkun", "zhuzhenye"]
    # error = [i for i in Names_alphabet if i not in name_time]
    # print(len(error), '\n', error)
    # txt_file = temp_path + 'name_time.txt'
    # name_time = []
    # with open(txt_file) as lf:
    #     for line in lf.readlines():
    #         lines = line.strip("\n")
    #         name_time.append(lines)
    #         pass
    #     lf.close()
    #     pass
    # print(name_time)
    my_rename_hikvision = RenameHikvision()
    # my_rename_hikvision.save_names()
    file_list = my_rename_hikvision.generate_list()
    # processing by pool map
    my_pool = Pool(4)
    my_task = my_pool.map(my_rename_hikvision.rename_hikvision, file_list[0])

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))
    pass