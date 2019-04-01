# -*- coding: utf-8 -*-
'''
This python file is convert the png files to bin files, then compress to zip files.

'''

import os
import time
import numpy as np
from PIL import Image
import pickle
from multiprocessing import Pool
import matplotlib.pyplot as plt # plt 用于显示图片

# 写入depth png图片到bin文件中
def Depth_ImageToBin(ICount,b = "depth"):
    # real_time = time.time()
    global broken_png_file
    broken_png_file = open('{:s}_broken_file_name.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')
    if (os.path.exists(ICount + '/' + b) and (os.listdir(ICount + '/' + b))):
        ImageDir = os.listdir(ICount + '/' + b)
        ImageDir.sort()
        # raise RuntimeError
        N = len(ImageDir)
        img_array_list = []
        for j,JCount in enumerate(ImageDir):
            PictureDir = ICount + "/" + b + "/" + JCount
            Temp = ImageToBinNoSave(PictureDir)
            img_array_list.append(Temp)
            # raise RuntimeError
            pass

        img_array = np.concatenate([np.expand_dims(x, 0) for x in img_array_list], axis=0).reshape(N,217088)

        File_Path = ICount + "/" + b + ".bin"
        File_Path_7z = ICount + "/" + b + ".7z"
        with open(File_Path, mode='wb') as f:
            pickle.dump(img_array, f)
        Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

        Split_ICount= ICount.split('/', 4)
        Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]
        Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

        Cmd_Delete_bin = "del " + Dir_Delete + "\\" + b + ".bin"
        os.system(Cmd_Delete_bin)
        print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b + ".bin"))

        print("*" * 120)
        print("{:s} has done~~~!!!~~".format(ICount))
        pass
    else:
        print("{:s} does not exist~~~!!!~~".format(ICount + '/' + b))
        pass
    broken_png_file.close()
    pass
# 写入infrared png图片到bin文件中
def Infrared_ImageToBin(ICount,b = "infrared"):
    # real_time2 = time.time()
    global broken_png_file
    broken_png_file = open('{:s}_broken_file_name.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')
    if (os.path.exists(ICount + '/' + b) and (os.listdir(ICount + '/' + b))):
        ImageDir = os.listdir(ICount + '/' + b)
        ImageDir.sort()
        # raise RuntimeError
        N = len(ImageDir)
        img_array_list = []
        for j,JCount in enumerate(ImageDir):
            PictureDir = ICount + "/" + b + "/" + JCount
            Temp = ImageToBinNoSave(PictureDir)
            img_array_list.append(Temp)
            # raise RuntimeError
            pass

        img_array = np.concatenate([np.expand_dims(x, 0) for x in img_array_list], axis=0).reshape(N,217088)

        File_Path = ICount + "/" + b + ".bin"
        File_Path_7z = ICount + "/" + b + ".7z"
        with open(File_Path, mode='wb') as f:
            pickle.dump(img_array, f)
        Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

        Split_ICount= ICount.split('/', 4)
        Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]
        Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

        Cmd_Delete_bin = "del " + Dir_Delete + "\\" + b + ".bin"
        os.system(Cmd_Delete_bin)
        print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b + ".bin"))

        print("*" * 120)
        print("{:s} has done~~~!!!~~".format(ICount))
        pass
    else:
        print("{:s} does not exist~~~!!!~~".format(ICount + '/' + b))
        pass
    broken_png_file.close()
    pass
def ImageToBinNoSave(a = ""):
    # 文件名称的处理
    b = a.split('/', 6)
    # 判断后操作
    if (os.path.exists(a) and b[5][-3:] == "png"):
        try:
            image = Image.open(a)
            pass
        except:
            print("ERROR !!!! The {:s} png file was broken~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~".format(a))
            broken_png_file.write(str(a) + "\n")
            return np.zeros(217088)
            pass
        else:
            LenImage = image.size[0] * image.size[1]
            arr = np.array(image, dtype=np.uint16).reshape(LenImage)
            print("{:s} has done~~~!!!~~".format(b[5]))
            # os.remove(a)
            # print("{:s} has delete!!".format(b[5]))
            return arr
            pass
    else:
        print("{:s} can not find~~~!!!~~".format(a))
        return np.zeros(217088)
        pass
    pass

# 压缩bone文件
def Compress_Bone(ICount,b = "bone"):
    File_Path = ICount + "/" + b
    File_Path_7z = ICount + "/" + b + ".7z"
    if (os.path.exists(File_Path) and (os.listdir(ICount + '/' + b))):
        Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

        Split_ICount= ICount.split('/', 4)
        Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]

        Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

        print("*" * 120)
        print("{:s} has done~~~!!!~~".format(ICount))
        pass
    else:
        print("{:s} does not exist~~~!!!~~".format(File_Path))
        pass
    pass

def SingleImageToBin(a = ""):
    # 文件名称的处理
    b = a.split('/', 6)
    d = b[0] + '/' + b[1] + '/' + b[2] + '/' + b[3] + '/' + b[4] + '/'
    c = b[5]
    c = c[:-4] + ".bin"
    # 判断后操作
    if (os.path.exists(a) and b[5][-3:] == "png"):
        image = Image.open(a)
        # plt.imshow(image)
        # plt.show()
        LenImage = image.size[0] * image.size[1]
        arr = np.array(image, dtype=np.uint16).reshape(LenImage)
        file_path = d + c
        with open(file_path, mode='wb') as f:
            pickle.dump(arr, f)
        os.remove(a)
        print("{:s} has delete!!".format(b[5]))
    else:
        print("{:s} can not find~~~!!!~~".format(a))
        pass
    pass
# 将Bin序列文件转为多个png图像
def TestBinToImage(a = ""):
    with open(a,mode='rb') as f:
        arr = pickle.load(f) #加载并反序列化数据
    arr = np.int32(arr)
    for i in range(len(arr)):
        temp_arr = arr[i, :].reshape(424, 512)
        # plt.imshow(temp_arr)
        # plt.imshow(temp_arr, cmap="gray", vmin=0, vmax=8000)
        # plt.show()
        # plt.close()
        image = Image.fromarray(temp_arr) #.convert('L')
        image.save("F:/pycharm_preject/Dataset_preprocessing/depth/{:04d}_bin.png".format(i), 'png')
        # raise RuntimeError
        print("{:04d} has done~~~!!~~~~".format(i))
        pass

    pass

# 将单个Bin文件转为png图像
def BinToImage(a = ""):
    with open(a,mode='rb') as f:
        arr = pickle.load(f) #加载并反序列化数据
    arr = arr.reshape(424, 512)
    arr = np.int32(arr)
    print(arr)
    image = Image.fromarray(arr) #.convert('L')

    image.save("bin.png", 'png')
    # plt.imshow(image)
    # plt.show()
    pass
# 获得文件列表
def GetPictureList(a = "F:/DATASET/"):
    ActioLiat = []
    SubjectDirs = os.listdir(a)
    for i,ICount in enumerate(SubjectDirs):
        LongSequenceList = os.listdir(a + ICount)
        for j,JCount in enumerate(LongSequenceList):
            ActioLiat.append(a + ICount + "/" + JCount)
            pass
        pass
        #break
    return ActioLiat
    pass


if __name__ == "__main__":

    DataSourceDir = "F:/test/"
    # print(GetPictureList())
    #ImageToBin(a="test.png")
    label_sequence = GetPictureList(DataSourceDir)
    #BinToImage("test.bin")
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)

    # processing by pool map
    p = Pool(6)
    res1 = p.map(Compress_Bone, label_sequence)
    # res2 = p.map(Depth_ImageToBin, label_sequence)
    # res3 = p.map(Infrared_ImageToBin, label_sequence)
    # TestBinToImage("depth.bin")

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))

    print("#" * 120)
    txt_dir = os.getcwd()
    txt_list = os.listdir(txt_dir)
    txt_list = list(filter(lambda x: x.endswith('.txt'), txt_list))
    txt_list.sort()
    for i,ICount in enumerate(txt_list):
        if (os.path.getsize(txt_dir + "/" + ICount) == 0):
            os.remove(txt_dir + "/" + ICount)
            pass
        else:
            print("{:s} need to precessing!!!!!!!!!!!!!".format(ICount))
            pass
        pass
    print("#" * 120)
    pass

