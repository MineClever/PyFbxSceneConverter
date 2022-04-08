# _*_ coding=utf-8 _*_
# Created By MineClever
# E-Mail: chnisesbandit@live.cn
# This Library was designed to wrap Autodesk FBX SDK Python binding

import FbxCommon
import fbx
import fbxType as fbxType

class MineFbxTool ():
    def __init__(self) :
        self.manager, self.scene = FbxCommon.InitializeSdkObjects()
        self.rootNode = self.scene.GetRootNode()
        self.ios = fbx.FbxIOSettings.Create(self.manager, fbx.IOSROOT)
        self.globalSettings = self.scene.GetGlobalSettings()
        self.ctrlPointCount = 0

    def loadScene (self,fbxFilePath):
        FbxCommon.LoadScene(self.manager, self.scene, fbxFilePath)

    def saveScene (self,fbxFilePath):
        FbxCommon.SaveScene(self.manager, self.scene, fbxFilePath)

    def saveSceneCustom(self, pFilename, pFileFormat = -1, pEmbedMedia = False):
        """copy from FbxCommon"""
        pSdkManager=self.manager
        pScene=self.scene
        lExporter = fbx.FbxExporter.Create(pSdkManager, "")
        if pFileFormat < 0 or pFileFormat >= pSdkManager.GetIOPluginRegistry().GetWriterFormatCount():
            pFileFormat = pSdkManager.GetIOPluginRegistry().GetNativeWriterFormat()
            if not pEmbedMedia:
                lFormatCount = pSdkManager.GetIOPluginRegistry().GetWriterFormatCount()
                for lFormatIndex in range(lFormatCount):
                    if pSdkManager.GetIOPluginRegistry().WriterIsFBX(lFormatIndex):
                        lDesc = pSdkManager.GetIOPluginRegistry().GetWriterFormatDescription(lFormatIndex)
                        if "ascii" in lDesc:
                            pFileFormat = lFormatIndex
                            break

        if not pSdkManager.GetIOSettings():
            ios = fbx.FbxIOSettings.Create(pSdkManager, fbx.IOSROOT)
            pSdkManager.SetIOSettings(ios)

        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_MATERIAL, True)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_TEXTURE, True)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_EMBEDDED, pEmbedMedia)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_SHAPE, True)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GOBO, True)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_ANIMATION, True)
        pSdkManager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GLOBAL_SETTINGS, True)
        pSdkManager.GetIOSettings().SetStringProp("ApplicationVendor","MineClever")
        result = lExporter.Initialize(pFilename, pFileFormat, pSdkManager.GetIOSettings())
        if result == True:
            result = lExporter.Export(pScene)
        lExporter.Destroy()
        return result

    def createNode(self, nickname=''):
        """Create a free node and add to the root node."""
        emptyNode = fbx.FbxNode.Create(self.manager, nickname)
        return emptyNode

    def createMesh(self, nickname=''):
        """Create a free mesh"""
        mesh = fbx.FbxMesh.Create(self.manager, nickname)
        return mesh

    def createMeshControlpoint(self, x, y, z):
        """Create a mesh controlpoint."""
        self.mesh.SetControlPointAt(fbx.FbxVector4(x, y, z), self.ctrlPointCount)
        self.ctrlPointCount += 1

    def getRootNodeTranslation(self):
        """Get the root node's translation."""
        return self.rootNode.LclTranslation.Get()

    def createOriginRootObj(self):
        """Create a free node and add to the root node."""
        spaceNode = fbx.FbxNode.Create(self.manager, "space_root")

        firstLayerNodesCount = self.rootNode.GetChildCount()
        firstLayernodes = []
        for nodeId in range(firstLayerNodesCount):
            node = self.rootNode.GetChild(nodeId)
            firstLayernodes.append(node)

        self.scene.AddNode(spaceNode)
        self.rootNode.AddChild(spaceNode)
        spaceNode.SetVisibility(True)

        for node in firstLayernodes:
            spaceNode.AddChild(node)
        return spaceNode

    def removeNodeInMid(self,inNode):
        childNodes = []
        parentNode = inNode.GetParent()

        for nodeId in range(inNode.GetChildCount()):
            childnode = inNode.GetChild(nodeId)
            childNodes.append(childnode)

        self.scene.DisconnectSrcObject(inNode)
        self.scene.RemoveNode(inNode)

        for childnode in childNodes:
            parentNode.AddChild(childnode)

    def convertSceneUnit (self,unit="cm"):
        """convert scene size to target size"""
        sceneUnit = self.globalSettings.GetSystemUnit()
        if sceneUnit.GetScaleFactorAsString() != unit:
            # do convert
            convertUnit = fbxType.FbxSystemUnit.GetByStr(unit)
            lConversionOptions = fbxType.FbxSystemUnit.ConversionOptions()
            lConversionOptions.defaultConversionOptions()
            convertUnit.ConvertScene(self.scene, lConversionOptions.cppType)

    def convertAxisSystem (self, inAxisSystem="maya",deep=True):
        spaceNode = self.createOriginRootObj()
        AxisSystem = inAxisSystem.lower()

        # do convert!
        if AxisSystem == "maya":
            axisSystem = fbxType.FbxAxisSystem.MayaYUp

        elif AxisSystem in ("3dmax","3dsmax","max","3ds"):
            axisSystem = fbxType.FbxAxisSystem.Max

        elif AxisSystem == "motionbuilder" or AxisSystem == "mb":
            axisSystem = fbxType.FbxAxisSystem.Motionbuilder

        elif AxisSystem == "opengl":
            axisSystem = fbxType.FbxAxisSystem.OpenGL

        elif AxisSystem == "directx" or AxisSystem == "dx":
            axisSystem = fbxType.FbxAxisSystem.DirectX

        # UE4缺省坐标系统为左手坐标系统，x向后，y向右，z向上
        elif AxisSystem in ("unreal","ue","ue4","unrealengine"):
            hand = fbxType.FbxAxisSystem.ECoordSystem.eLeftHanded
            up = fbxType.FbxAxisSystem.EUpVector.eZAxis
            front = fbxType.FbxAxisSystem.EFrontVector.eParityOdd
            axisSystem = fbxType.FbxAxisSystem(up,front,hand)

        # unity 为左手坐标系
        # X正方向为正右方, Y正方向为正上方, Z正方向为正前方
        elif AxisSystem in ("unity","u3d"):
            hand = fbxType.FbxAxisSystem.ECoordSystem.eLeftHanded
            up = fbxType.FbxAxisSystem.EUpVector.eYAxis
            front = fbxType.FbxAxisSystem.EFrontVector.eParityOdd
            axisSystem = fbxType.FbxAxisSystem(up,front,hand)
        else:
            raise Exception ("unknown define")

        if deep:
            axisSystem.DeepConvertScene(self.scene)
        else:
            axisSystem.ConvertScene(self.scene)

        self.removeNodeInMid(spaceNode)

    def removeNamespace(self):
        """
        Remove all namespaces from all nodes
        This is not an ideal method but
        """
        sceneNodes = self.getAllSceneNodes()
        for node in sceneNodes:
            orig_name = node.GetName()
            split_by_colon = orig_name.split(':')
            if len(split_by_colon) > 1:
                new_name = split_by_colon[-1:][0]
                node.SetName(new_name)
        return True

    def getAllSceneNodes(self):
        return self.__getSceneNodesRecursive(self.rootNode)

    @classmethod
    def getPropertyValue(cls, node, propertyString):
        """
        Gets the property value from an Fbx node
        property_value = fbx_file.get_property_value(node, 'no_export')
        """
        fbxProperty = node.FindProperty(propertyString)
        if fbxProperty.IsValid():
            # cast to correct property type so you can get
            castedProperty = cls.__castPropertyType(fbxProperty)
            if castedProperty:
                return castedProperty.Get()
        return None

    @classmethod
    def getNodeProperty(cls, node, propertyString):
        """
        Gets a property from an Fbx node
        export_property = fbx_file.get_property(node, 'no_export')
        """
        fbxProperty = node.FindProperty(propertyString)
        return fbxProperty

    @classmethod
    def removeNodeProperty(cls, node, propertyString):
        """
        Remove a property from an Fbx node
        removeProperty = fbx_file.removeProperty(node, 'UDP3DSMAX')
        """
        nodeProperty = cls.getNodeProperty(node, propertyString)
        if nodeProperty.IsValid():
            nodeProperty.DestroyRecursively()
            return True
        return False

    def __getSceneNodesRecursive(self, node, nodesList=[]):
        """
        Rescursive method to get all scene nodes
        this should be private, called by get_scene_nodes()
        """
        nodesList.append(node)
        for i in range(node.GetChildCount()):
            self.__getSceneNodesRecursive(node.GetChild(i),nodesList)
        return nodesList

    def __castPropertyType(self, fbx_property):
        """
        Cast a property to type to properly get the value
        """
        casted_property = None

        unsupported_types = (fbx.eFbxUndefined, fbx.eFbxChar, fbx.eFbxUChar, fbx.eFbxShort, fbx.eFbxUShort, fbx.eFbxUInt,
                                fbx.eFbxLongLong, fbx.eFbxHalfFloat, fbx.eFbxDouble4x4, fbx.eFbxEnum, fbx.eFbxTime,
                                fbx.eFbxReference, fbx.eFbxBlob, fbx.eFbxDistance, fbx.eFbxDateTime, fbx.eFbxTypeCount)

        # property is not supported or mapped yet
        property_type = fbx_property.GetPropertyDataType().GetType()
        if property_type in unsupported_types:
            return None

        if property_type == fbx.eFbxBool:
            casted_property = fbx.FbxPropertyBool1( fbx_property )
        elif property_type == fbx.eFbxDouble:
            casted_property = fbx.FbxPropertyDouble1( fbx_property )
        elif property_type == fbx.eFbxDouble2:
            casted_property = fbx.FbxPropertyDouble2( fbx_property )
        elif property_type == fbx.eFbxDouble3:
            casted_property = fbx.FbxPropertyDouble3( fbx_property )
        elif property_type == fbx.eFbxDouble4:
            casted_property = fbx.FbxPropertyDouble4( fbx_property )
        elif property_type == fbx.eFbxInt:
            casted_property = fbx.FbxPropertyInteger1( fbx_property )
        elif property_type == fbx.eFbxFloat:
            casted_property = fbx.FbxPropertyFloat1( fbx_property )
        elif property_type == fbx.eFbxString:
            casted_property = fbx.FbxPropertyString( fbx_property )
        else:
            raise ValueError( 'Unknown property type: {0} {1}'.format(property.GetPropertyDataType().GetName(), property_type))

        return casted_property

    def moveRootNodeOnTop(self):
        """move root node on scene top!"""
        asRootNode = None
        for name in ("root", "Root", "ROOT"):
            asRootNode = self.findSceneNodeByName(name)
            if asRootNode != None:
                break
        if asRootNode == None:
            print("Can not find root node, skip!!\n")
            return False
        self.scene.DisconnectDstObject(asRootNode)
        self.rootNode.AddChild(asRootNode)

    def findSceneNodeByName (self,name=""):
        return self.scene.FindNodeByName(name)

    def recoveryFirstKeyFrameToRoot (self, frameCount=-1, toOrigin=False) :
        asRootNode = asLeanRootNode = None
        # find lean_root node
        asRootNode = self.findSceneNodeByName("root")
        if not asRootNode:
            print("Can not find root node, skip!!\n")
            return False
        # find root node
        asLeanRootNode = self.findSceneNodeByName("lean_root")
        if not asLeanRootNode:
            print("Can not find lean_root node, skip!!\n")
            return False
        
        # find time info
        # -- get animation stacks!
        lDefaultAnimLayer = self.scene.GetCurrentAnimationStack().GetMember(0)
        rootJointPosCurveNode = asRootNode.LclTranslation.GetCurveNode(lDefaultAnimLayer)
        rootJointRotCurveNode = asRootNode.LclRotation.GetCurveNode(lDefaultAnimLayer)
        
        leanRootPosCurveNode = asLeanRootNode.LclTranslation.GetCurveNode(lDefaultAnimLayer)
        leanRootRotCurveNode = asLeanRootNode.LclRotation.GetCurveNode(lDefaultAnimLayer)
        
        # -- get Times on root node
        timeSpan = fbx.FbxTimeSpan(fbx.FbxTime(), fbx.FbxTime())
        hasKeyFrameTime = asRootNode.GetAnimationInterval(timeSpan)
        if not hasKeyFrameTime:
            return False
        lStartTime = None
        lEndTime = None
        startFrameCount= 0
        stopFrameCount = 0

        # -- get start time on timeline
        if not frameCount >=0 :
            lStartTime = timeSpan.GetStart()
        else:
            lStartTime = fbx.FbxTime()
            lStartTime.SetFrame(frameCount)
        lEndTime = timeSpan.GetStop()
        startFrameCount = lStartTime.GetFramedTime().GetFrameCount()
        stopFrameCount = lEndTime.GetFramedTime().GetFrameCount()
        deltaFrameCount = stopFrameCount - startFrameCount
        if deltaFrameCount <= 0:
            return False
        
        print("frame counts : {}".format(deltaFrameCount))

        # use lean_root as reference
        posChannelsCount = leanRootPosCurveNode.GetChannelsCount()
        rotChannelsCount = leanRootRotCurveNode.GetChannelsCount()
        
        # find key count
        # -- assume x,y,z alway is on same key index
        firstAnimCurve = leanRootPosCurveNode.GetCurve(0, 0)
        # -- -- return a tuple(int,int)
        firstKeyIndex = firstAnimCurve.KeyFind(lStartTime)[0]
        lastKeyIndex = firstAnimCurve.KeyFind(lEndTime)[0]
        # -- -- have to cast to int!
        keyIndexCount = int(lastKeyIndex - firstKeyIndex)
        # move root to origin or reversed to lean_root
        if toOrigin:
            print("move into origin root!")
            keyOriginValue = []
            for i in range(posChannelsCount):
                currentAnimCurve = rootJointPosCurveNode.GetCurve(i, 0)
                firstKeyValue = currentAnimCurve.KeyGetValue(firstKeyIndex)
                keyOriginValue.append(firstKeyValue)

            # move every keyframe into offset(zero)
            # -- k^i --> O(n^3)
            # -- i^k --> O(3^n)
            for k in range(keyIndexCount):
                for i in range(posChannelsCount):
                    currentIndex = firstKeyIndex+k
                    currentAnimCurve = rootJointPosCurveNode.GetCurve(i, 0)
                    currentAnimCurve.KeyModifyBegin()
                    currentKeyValue = currentAnimCurve.KeyGetValue(currentIndex)
                    currentAnimCurve.KeySetValue(currentIndex, (currentKeyValue - keyOriginValue[i]))
                    currentAnimCurve.KeyModifyEnd()
            return True
        else :
            print("move into lean root!")
            for k in range(keyIndexCount):
                for i in range(posChannelsCount):
                    currentIndex = firstKeyIndex+k
                    currentLeanRootAnimCurve = leanRootPosCurveNode.GetCurve(i, 0)
                    currentRootAnimCurve = rootJointPosCurveNode.GetCurve(i, 0)
                    currentRootAnimCurve.KeyModifyBegin()
                    currentLeanRootKeyValue = currentLeanRootAnimCurve.KeyGetValue(currentIndex)
                    currentRootAnimCurve.KeySetValue(currentIndex, currentLeanRootKeyValue)
                    currentRootAnimCurve.KeyModifyEnd()
            return True
