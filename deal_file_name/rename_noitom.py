# 重命名
# 取出原标签的名字，用正则匹配出编号
# -*- coding: utf-8 -*-
import os
import shutil
import time


class renameNoitom(object):
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
        return switcher.get(var, 'error')

    def findP(self,name):
        index = self.Names.index(name)
        if (index < 9):
            self.p = "P00" + str(index + 1);
        elif (index >= 9 and index < 99):
            self.p = "P0" + str(index + 1);
        else:
            self.p = "P" + str(index + 1);
        #print("我的P是：", self.p)


    def findS(self, xulie):
        xuhao = xulie[0:3]
        #print("我的序号是：",xuhao)
        self.s = self.switchS(xuhao)


    def mycopyfile(self,path1,path10):
        for filename in os.listdir(path1): #当前路径下的文件名
            #print("我要得到的人名是：", filename)
            self.findP(filename)
            path2 = path1 + "\\" + filename
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
                path3 = path2 + "\\" + xulie + "\\" + "inertial.txt"
                newName = self.p + "T00" + self.t + self.s + ".txt"
                newPath = path10 + "\\" + newName
                if os.path.isfile(newPath):
                    print(newName,"已存在")
                else:
                    shutil.copyfile(path3, newPath)  # 复制文件
                    print("copy %s -> %s" % (path3, newPath))


if __name__ == "__main__":
    print('start ...')
    t1 = time.time() * 1000
    myStart = renameNoitom()
    path1 = "E:\\重命名前\\NOITOM\\92-276_NOITOMDATA"
    path10 = "E:\\重命名\\DataSet1\\NOITOM"
    myStart.mycopyfile(path1,path10)
    t2 = time.time() * 1000
    print('take time:' + str((t2 - t1)/1000) + 's')
    print('end.')

