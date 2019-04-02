# 重命名
# 取出原标签的名字，用正则匹配出编号
# -*- coding: utf-8 -*-
import os
import shutil
import time
import zipfile
from os import path


class renameKinect(object):
    def __init__(self):
        self.fileNames = []
        self.Names = [ "cairuilin", "caojunhai", "changhongguang", "changming", "changxiangxu", "chengjiawen",
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
        self.number = 0
        self.p = ""
        self.ps = []
        self.s = ""
        self.t = ""
        self.newNames = []   #重命名后的名字




    def mycopyfile(self,path10):
        for filename in os.listdir(path10): #当前路径下的文件名
            if(filename[-9:] == "FileError"):
                newname = filename[:-9] + ".7z"
                path4 = path10 + filename
                newPath = path10 + newname
                os.rename(path4, newPath)
                print("rename %s -> %s" % (filename, newname))



if __name__ == "__main__":
    print('start ...')
    t1 = time.time() * 1000
    myStart = renameKinect()
    # n是kinect编号，m是改变后的文件后缀名,v是改变后的文件夹名字
    # 其中  RGB对应.avi  bone,depth,infrared对应.7z  2D,3D对应.txt
    global n,m,v,finalFilename
    n = "1"
    #m = ".avi" # ".txt" ".7z" ".avi"
    #v = "RGB_KINECT" # "2D_BONE_KINECT" "3D_BONE_KINECT" "BONE_PICTURE_KINECT" "DEPTH_KINECT" "INFRARED_KINECT" "RGB_KINECT"
    #finalFilename = "compressed_bgr.avi"  # "compressed_bgr.avi" "kinect bone.txt" "kinect color.txt" "bone" "depth" "infrared"
    #path1 = "E:\\重命名前\\92-276_COPYED_KINECT0" + n
    #path1 = "//172.20.15.56//cas_mhad//Preprocessing_Test//1-91_KINECT0" + n
    #path1 = "E:\\重命名前\\92-276_KINECT0" + n
    #path10 = "E:\\重命名\\DataSet1\\KINECT\\" + v
    path10 ="//172.20.15.56//cas_mhad//Preprocessing_Test//DataSet1//KINECT//INFRARED_KINECT//"

    myStart.mycopyfile(path10)
    t2 = time.time() * 1000
    print('take time:' + str((t2 - t1)/1000) + 's')
    print('end.')

