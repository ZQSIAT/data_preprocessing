# -*- coding: utf-8 -*-
'''
This python file is to move capture video.

'''
import os
import shutil as st
import time

#移动文件夹
def MoveFiles(a = "D:/VideoData/", b = "E:/DATASET/"):
    LongSequenceDirs = os.listdir(a)
    for i,IContent in enumerate(LongSequenceDirs):
        Src = a + IContent
        Dst = b
        try:
            st.move(Src, Dst)
            pass
        except st.Error as e:
            for Src, Dst, Msg in e.args[0]:
                print(Src, Dst, Msg)
                pass
            pass
        pass
        print("\"{:s}\" has moved!!!".format(IContent))
        # break
    pass
if __name__ == '__main__':

    print("Start move processing...")
    StartTime = time.time()
    print("-" * 120)

    SrcFilesDir = "C:/VideoData/"
    DstFilesDir = "I:/DATASET/"
    MoveFiles(SrcFilesDir,DstFilesDir)

    EndTime = time.time()
    print("-" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((EndTime - StartTime) / 60.0))
    raise RuntimeError
    pass
