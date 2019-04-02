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

    def switchS(self,var):
        switcher= {
            'a01': "S001",
            'a02': "S002",
            'a03': "S003",
            'a04': "S004",
            'a05': "S005",
            'a06': "S006",
            'a07': "S007",
            'bla': "S008",
        }
        return switcher.get(var, 'sError')

    def switchC(self,var):
        switcher= {
            '1': "C016",
            '2': "C017",
            '3': "C018",
            '4': "C019",
        }
        return switcher.get(var, 'cError')

    def switchFile(self,var):
        switcher= {
            "compressed_bgr.avi": "RGB_KINECT",
            "kinect color.txt": "2D_BONE_KINECT",
            "kinect bone.txt": "3D_BONE_KINECT",
            "bone.7z": "BONE_PICTURE_KINECT",
            "infrared.7z": "INFRARED_KINECT",
            "depth.7z": "DEPTH_KINECT",
        }
        return switcher.get(var, 'FileError')

    def switchHouZhui(self,var):
        switcher= {
            "compressed_bgr.avi": ".avi",
            "kinect color.txt": ".txt",
            "kinect bone.txt": ".txt",
            "bone.7z": ".7z",
            "infrared.7z": ".7z",
            "depth.7z": ".7z",
        }
        return switcher.get(var, 'HouZhuiError')

    def findP(self,name):
        index = self.Names.index(name)
        if (index < 9):
            self.p = "P00" + str(index + 1)
        elif (index >= 9 and index < 99):
            self.p = "P0" + str(index + 1)
        else:
            self.p = "P" + str(index + 1)
        #print("我的P是：", self.p)


    def findS(self, xulie):
        xuhao = xulie[0:3]
        #print("我的序号是：",xuhao)
        self.s = self.switchS(xuhao)

    def findC(self):
        self.c = self.switchC(n)

    def findO(self,name):
        index = self.Names.index(name)
        if (index <= 66):
            self.o = "O001";
        else :
            self.o = "O002";

    def FError(self,Exception):
        pass


    def mycopyfile(self,path1,path10):
        self.findC();   #先把C得到
        for filename in os.listdir(path1): #当前路径下的文件名
            #print("我要得到的人名是：", filename)
            self.findP(filename)
            self.findO(filename)    #得到人名就可以得到o了
            path2 = path1 + "//" + filename
            count = 0
            for xulie in os.listdir(path2):
                #print("我的序列是：", xulie)
                s1 = self.s
                self.findS(xulie)
                if (self.s != s1):
                    count = 0
                count = count + 1
                self.t = str(count)
                #print("我的T是：", self.t)
                #print("我的P是：", self.p)
                path3 = path2 + "//" + xulie
                for finalFilename in os.listdir(path3):
                    v = self.switchFile(finalFilename)
                    if(v == "FileError"):
                        raise self.FError("原文件有问题,请检查原文件名字")
                    m = self.switchHouZhui(finalFilename)
                    if (m == "HouZhuiError"):
                        raise self.FError("原文件有问题，请检查原文件后缀或者是否已经压缩")
                    path11 = path10 + v
                    path4 = path2 + "//" + xulie + "//" + finalFilename
                    newName = self.o + self.p + self.c + "T00" + self.t + self.s + m
                    newPath = path11 + "//" + newName

                    # if os.path.isdir(path3):    #如果path3能打开，说明是文件夹。
                    #     print("我是文件夹")
                    #     fpath = path.replace(path3, '')     # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                    #     z = zipfile.ZipFile(newPath, 'w', zipfile.ZIP_DEFLATED)  # 参数一：压缩后文件的名字
                    #     print("compressing %s -> %s" % (finalFilename, newName))
                    #     z.write(path3)
                    #     z.close()
                    if os.path.isfile(newPath):
                        print(newName, "已存在")
                    else:
                        os.rename(path4, newPath)  # 剪切文件
                        print("remove %s -> %s" % (path3, newPath))



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
    #path1 = "E:\\重命名前\\92-276_COPYED_KINECT0" + n  1-91_KINECT0" + n DataSet1//KINECT//
    path1 = "//172.20.15.56//cas_mhad//Preprocessing_Test//1-91_KINECT0" + n
    #path1 = "E:\\重命名前\\92-276_KINECT0" + n
    #path10 = "E:\\重命名\\DataSet1\\KINECT\\" + v
    path10 ="//172.20.15.56//cas_mhad//Preprocessing_Test//DataSet1//KINECT//"

    myStart.mycopyfile(path1,path10)
    t2 = time.time() * 1000
    print('take time:' + str((t2 - t1)/1000) + 's')
    print('end.')

    # zqs

