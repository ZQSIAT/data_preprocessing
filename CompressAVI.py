import os
import shutil as st

def CompressFiles(a = "D:/0000DATA/kinectvideo/subjectname/"):
    FilesDir = os.listdir(a)
    for i, IContent in enumerate(FilesDir):
        ActionFlies = os.listdir(a + IContent)
        for j, JContent in enumerate(ActionFlies):
            Src = a + IContent + '/' + JContent+ '/' + "bgr.avi"
            Dst = a + IContent + '/' + JContent + '/' + "compressed_bgr.avi"
            if os.path.exists(Src):
                cmd_name = ("ffmpeg -y -i " + Src + " -b 4096k " + Dst)
                os.system(cmd_name)
                print("{:s} has compressed~~".format(JContent))
                os.remove(Src)
                print("{:s} has delete!!".format(Src))
                pass
            else:
                print("{:s} can not find~~~!!!~~".format(JContent))
                pass
            pass
        # break
        pass
    pass


def Print(a):
    print(a)
    pass

if __name__ == '__main__':
    InputFileName = "F:/dataset/"
    OutFileName = "D:/0000DATA/kinectvideo/subjectname/"
    CompressFiles(InputFileName)

    pass


# cmd_name = ['ffmpeg -y -i bgr.avi -s 160x120 -vcodec libx264 -b 900000 ' outfilename];
