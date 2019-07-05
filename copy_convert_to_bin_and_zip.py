# -*- coding: utf-8 -*-
'''
This python file is convert the png files to bin files, then compress to zip files.

'''

import os
import time
import numpy as np
from PIL import Image
import pickle
import shutil as st
from multiprocessing import Pool
import matplotlib.pyplot as plt # plt 用于显示图片

# 写入infrared png图片到bin文件中
def no_map_Infrared_ImageToBin(a,b = "infrared"):
    # real_time2 = time.time()
    # global broken_png_file
    # broken_png_file = open('{:s}_broken_file_name.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')
    for i,ICount in enumerate(a):
        process_dir = ICount.split('/', 4)[1]
        File_Path = ICount + "/" + b + ".bin"
        File_Path_7z = ICount.replace(process_dir, "C_" + process_dir) + "/" + b + ".7z"

        if (os.path.exists(ICount + '/' + b) and (os.listdir(ICount + '/' + b)) and (not os.path.exists(File_Path_7z))):
            ImageDir = os.listdir(ICount + '/' + b)
            ImageDir.sort()
            # raise RuntimeError
            N = len(ImageDir)
            img_array_list = []
            for j, JCount in enumerate(ImageDir):
                PictureDir = ICount + "/" + b + "/" + JCount
                Temp = ImageToBinNoSave(PictureDir)
                img_array_list.append(Temp)
                # raise RuntimeError
                pass

            img_array = np.concatenate([np.expand_dims(x, 0) for x in img_array_list], axis=0).reshape(N, 217088)

            with open(File_Path, mode='wb') as f:
                pickle.dump(img_array, f)
            Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
            os.system(Cmd_Compress)
            print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

            Split_ICount = ICount.split('/', 4)
            Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]

            # Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
            # os.system(Cmd_Delete_Depth)# 删除原始的深度图片
            # print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

            Cmd_Delete_bin = "del " + Dir_Delete + "\\" + b + ".bin"
            os.system(Cmd_Delete_bin)
            print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b + ".bin"))

            print("*" * 120)
            print("{:s} has done~~~!!!~~".format(ICount))
            pass
        else:
            print("{:s} does not exist~~~!!!~~".format(ICount + '/' + b))
            pass
        pass
    pass

# 写入depth png图片到bin文件中
def Depth_ImageToBin(ICount,b = "depth"):
    # real_time = time.time()
    global broken_png_file
    broken_png_file = open('{:s}_broken_file_name.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

    process_dir = ICount.split('/')[1]
    File_Path = ICount + "/" + b + ".bin"
    File_Path_7z = ICount.replace(process_dir, "C_" + process_dir) + "/" + b + ".7z"

    if (os.path.exists(ICount + '/' + b) and (os.listdir(ICount + '/' + b)) and (not os.path.exists(File_Path_7z))):
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

        with open(File_Path, mode='wb') as f:
            pickle.dump(img_array, f)

        Cmd_Compress = "Bandizip.exe c \"" + File_Path_7z + "\" \"" + File_Path + "\""
        # print(Cmd_Compress)
        # raise RuntimeError
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))
        # raise RuntimeError
        # Split_ICount= ICount.split('/', 4)
        # Split_ICount= ICount.split('/', 4)
        # Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]
        # Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        # os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        # print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

        # Cmd_Delete_bin = "del " + Dir_Delete + "\\" + b + ".bin"
        # os.system(Cmd_Delete_bin)
        os.remove(File_Path)
        print("{:s} has deleted~~~!!!~~".format(File_Path))

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

    process_dir = ICount.split('/', 4)[1]
    File_Path = ICount + "/" + b + ".bin"
    File_Path_7z = ICount.replace(process_dir, "C_" + process_dir) + "/" + b + ".7z"

    if (os.path.exists(ICount + '/' + b) and (os.listdir(ICount + '/' + b)) and (not os.path.exists(File_Path_7z))):
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

        img_array = np.concatenate([np.expand_dims(x, 0) for x in img_array_list], axis=0).reshape(N, 217088)

        with open(File_Path, mode='wb') as f:
            pickle.dump(img_array, f)
        Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

        Split_ICount= ICount.split('/', 4)
        Dir_Delete = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]

        # Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        # os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        # print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))

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
    b = a.split('/')

    # 判断后操作
    if (os.path.exists(a) and b[-1][-3:] == "png"):
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
            print("{:s} has done~~~!!!~~".format(a))
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
    print("*" * 120)
    process_dir = ICount.split('/', 4)[1]
    File_Path = ICount + "/" + b
    File_Path_7z = ICount.replace(process_dir,"C_" + process_dir) + "/" + b + ".7z"
    if (not os.path.exists(File_Path_7z) and (os.listdir(ICount + '/' + b))):
        Cmd_Compress = "Bandizip.exe c " + File_Path_7z + " " + File_Path
        os.system(Cmd_Compress)
        print("{:s} has compressed~~~!!!~~".format(File_Path_7z))

        Split_ICount= ICount.split('/', 4)
        copy_dirs = Split_ICount[0] + '\\' + Split_ICount[1] + '\\' + Split_ICount[2] + '\\' + Split_ICount[3]
        copy_dst = copy_dirs.replace(process_dir,"C_"+process_dir)

        cmd_copy_avi = "copy /y \"{:s}\" \"{:s}\"".format(copy_dirs+"\\compressed_bgr.avi",copy_dst+"\\compressed_bgr.avi")
        os.system(cmd_copy_avi)
        print("{:s} has copy~~~!!!~~".format(copy_dirs+"\\compressed_bgr.avi"))

        cmd_copy_bone = "copy /y \"{:s}\" \"{:s}\"".format(copy_dirs+"\\kinect bone.txt",copy_dst+"\\kinect bone.txt")
        os.system(cmd_copy_bone)
        print("{:s} has copy~~~!!!~~".format(copy_dirs+"\\kinect bone.txt"))

        cmd_copy_color = "copy /y \"{:s}\" \"{:s}\"".format(copy_dirs+"\\kinect color.txt",copy_dst+"\\kinect color.txt")
        os.system(cmd_copy_color)
        print("{:s} has copy~~~!!!~~".format(copy_dirs+"\\kinect color.txt"))

        # Cmd_Delete_Depth = "rmdir /s/q " + Dir_Delete + "\\" + b
        # os.system(Cmd_Delete_Depth)# 删除原始的深度图片
        # print("{:s} has deleted~~~!!!~~".format(Dir_Delete + "\\" + b))
        # print("{:s} has done~~~!!!~~".format(ICount))
        print("*" * 120)
        pass
    else:
        print("{:s} does not exist~~~!!!~~".format(File_Path))
        pass
    pass

def Copy_avi_liyidataset(ICount):
    process_dir = "LIYI_setdata"
    src_File_Path = ICount
    dst_Path = ICount.replace(process_dir,"C_" + process_dir)
    if not os.path.exists(dst_Path):
        os.makedirs(dst_Path)
        pass
    src_avi_dirs = src_File_Path + "/bgr.avi"
    dst_avi_dst = dst_Path + "/bgr.avi"
    if not os.path.exists(dst_avi_dst) and os.path.exists(src_avi_dirs):
        st.copyfile(src_avi_dirs,dst_avi_dst)
        # raise RuntimeError
        print("\"{:s}\" has copyed!!!!".format(src_avi_dirs))
        pass
    else:
        print("{:s} copy failed :( :( :( :( :(".format(src_avi_dirs))
        pass
    src_inertial_dirs = src_File_Path + "/inertial.txt"
    dst_inertial_dst = dst_Path + "/inertial.txt"
    if not os.path.exists(dst_inertial_dst) and os.path.exists(src_inertial_dirs):
        st.copyfile(src_inertial_dirs, dst_inertial_dst)
        print("\"{:s}\" has copyed!!!!".format(src_inertial_dirs))
        pass
    else:
        print("{:s} copy failed :( :( :( :( :(".format(src_inertial_dirs))
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
        if not os.path.exists("F:/{:s}_depth".format(a.split('/')[-2], i)):
            os.mkdir("F:/{:s}_depth".format(a.split('/')[-2],i))
            pass
        image.save("F:/{:s}_depth/{:04d}_bin.png".format(a.split('/')[-2], i), 'png')
            # raise RuntimeError
        print("{:04d} has done~~~!!~~~~".format(i))

        pass

    pass

# 将单个Bin文件转为png图像
def BinToImage(a = ""):
    with open(a, mode='rb') as f:
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
def GetPictureList(a = "K:/DATASET/"):
    ActionList = []
    SubjectDirs = os.listdir(a)
    for i,ICount in enumerate(SubjectDirs):
        LongSequenceList = os.listdir(a + ICount)
        for j,JCount in enumerate(LongSequenceList):
            action_list = os.listdir(a + ICount + "/" + JCount)
            for k,KCount in enumerate(action_list):
                ActionList.append(a + ICount + "/" + JCount + "/" + KCount)
                # print(ActionList)
                # raise RuntimeError
                pass
            pass
        pass
        #break
    return ActionList
    pass
# 剪贴与复制
def copy_cut_paste(a):
    for i,ICount in enumerate(a):
        src_dir = ICount
        dst_dir = ICount.replace("KINECT","C_KINECT")
        if not os.path.exists(dst_dir.replace(dst_dir.split('/',4)[3],"")):
            os.mkdir(dst_dir.replace(dst_dir.split('/',4)[3],""))
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        if os.path.exists(src_dir + "/bone.7z") and not os.path.exists(dst_dir + "/bone.7z"):
            os.rename(src_dir + "/bone.7z", dst_dir + "/bone.7z")
            pass
        if os.path.exists(src_dir + "/depth.7z") and not os.path.exists(dst_dir + "/depth.7z"):
            os.rename(src_dir + "/depth.7z", dst_dir + "/depth.7z")
            pass
        if os.path.exists(src_dir + "/infrared.7z") and not os.path.exists(dst_dir + "/infrared.7z"):
            os.rename(src_dir + "/infrared.7z", dst_dir + "/infrared.7z")
            pass

        st.copy(src_dir+"/compressed_bgr.avi", dst_dir+"/compressed_bgr.avi")
        st.copy(src_dir + "/kinect bone.txt", dst_dir + "/kinect bone.txt")
        st.copy(src_dir + "/kinect color.txt", dst_dir + "/kinect color.txt")

        print(src_dir,dst_dir)
        # break
        # raise RuntimeError
        pass

    pass

if __name__ == "__main__":

    bin_to_image_root = "C:/Users/zqs20/Desktop/样例/KINECT/INFRARED/"
    TestBinToImage(bin_to_image_root + "infrared (4).bin")

    raise RuntimeError

    # DataSourceDir = "E:/KINECT03/"
    DataSourceDir = "X:/LIYI_setdata/"
    # print(GetPictureList())
    #ImageToBin(a="test.png")
    # label_sequence = GetPictureList(DataSourceDir)

    # raise RuntimeError
    #BinToImage("test.bin")
    print("Start processing...")
    start_time = time.time()
    print("#" * 120)

    # global broken_png_file
    # broken_png_file = open('{:s}_broken_file_name.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

    # processing by pool map
    # p = Pool(8)
    # res1 = p.map(Copy_avi_liyidataset, label_sequence)
    # res2 = p.map(Depth_ImageToBin, label_sequence)
    # res3 = p.map(Infrared_ImageToBin, label_sequence)
    # res3 = p.map(copy_cut_paste, label_sequence)
    # copy_cut_paste(label_sequence)

    # TestBinToImage("depth.bin")
    # no_map_Infrared_ImageToBin(label_sequence)

    # broken_png_file.close()
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

    print("hello word~~")
    print("hhewoiawghrghuire")
