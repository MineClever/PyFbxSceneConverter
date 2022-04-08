# _*_ coding=utf-8 _*_

from re import L
import sys
import os
from fbxTool import *
import fbx

def runScript(fbxInputPath="",frameIndex=0,rootOffset=-1,*args,**kw):
    """
    runScript 
    * process fbx for ue4

    Args:
        * fbxInputPath (str, optional): fbx input full path . Defaults to "".\n
        * frameIndex (int, optional): which frame as reference start frame. Defaults to 0.\n
        * rootOffset (int, optional): offset mode. Defaults to -1. -1:do not offset ; 0: move "root" back origin point; 1: move "root" to "lean_root"\n
    """
    # process input path
    targetPlatForm = "max"
    filePaths=os.path.split(fbxInputPath)
    currentPath = filePaths[0]
    currentFileName = os.path.splitext(filePaths[1])[0]
    fileExportPath = os.path.join(currentPath, currentFileName) + "_export_" + "ZupRH" + ".fbx"
    print("\n")
    print("^_^")
    print("_"*20 +"\nFBX convert tool created by MineClever \nE-Mail:chnisesbandit@live.cn\n"+"_"*20)
    print("export path : {}\n".format(fileExportPath))

    # process file
    fbxTool = MineFbxTool()
    # load
    fbxTool.loadScene(fbxInputPath)
    # move root node on scene top
    fbxTool.moveRootNodeOnTop()
    # root node offset
    if not rootOffset < 0:
        if  rootOffset == 0:
            fbxTool.recoveryFirstKeyFrameToRoot(frameIndex,toOrigin=True)
        elif rootOffset >= 1:
            fbxTool.recoveryFirstKeyFrameToRoot(frameIndex,toOrigin=False)
    # convert Unit
    fbxTool.convertSceneUnit("cm")
    # convert axisSystem
    fbxTool.convertAxisSystem(targetPlatForm,deep=True)
    # remove all nameSpace
    fbxTool.removeNamespace()
    # save
    fbxTool.saveSceneCustom(fileExportPath,pFileFormat=0)

