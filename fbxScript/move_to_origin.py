import _fbx_convert_space as _convert
import os, sys

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print(sys.argv)
        exit()
    
    
    filePath = sys.argv[1]
    currentPath = os.path.split(filePath)[0]
    fileName = os.path.split(filePath)[1]
    # fileBaseName = os.path.splitext(fileName)[0]
    fileExtName = (os.path.splitext(fileName)[1]).lower()
    filePath = os.path.join(currentPath, fileName)
    
    if os.path.exists(filePath) and fileExtName==".fbx":
        print("processing file : {}".format(filePath))
        _convert.runScript(filePath,-1,rootOffset=0)
    else :
        print("file \"%s\" not exists" % (filePath))

    # pause
    input("\npress any key ...")
