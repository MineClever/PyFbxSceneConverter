from typing import NewType
import fbx as fbx

FbxDouble3 = NewType('FbxDouble3', fbx.FbxDouble3)
FbxDouble2 = NewType('FbxDouble2', fbx.FbxDouble2)
FbxDouble4 = NewType('FbxDouble4', fbx.FbxDouble4)
FbxDouble4x4 = NewType('FbxDouble4x4', fbx.FbxDouble4x4)

class FbxSystemUnit ():
    Foot = fbx.FbxSystemUnit.Foot
    Inch = fbx.FbxSystemUnit.Inch
    Mile = fbx.FbxSystemUnit.Mile
    Yard = fbx.FbxSystemUnit.Yard

    cm = fbx.FbxSystemUnit.cm
    dm = fbx.FbxSystemUnit.dm
    km = fbx.FbxSystemUnit.km
    m = fbx.FbxSystemUnit.m
    mm = fbx.FbxSystemUnit.mm

    class ConversionOptions():
        def __init__(self):
            self.cppType = fbx.FbxSystemUnit.ConversionOptions()

        @property
        def mConvertRrsNodes(self) -> bool:
            # //! This flag indicates whether or not to convert the nodes that do not inherit their parent's scale.
            # bool mConvertRrsNodes;  
            return self.cppType.mConvertRrsNodes
        @mConvertRrsNodes.setter
        def mConvertRrsNodes(self,value:bool):
            self.cppType.mConvertRrsNodes = value

        @property
        def mConvertLimits (self) ->bool:
            # //! This flag indicates whether or not to convert limits.
            # bool mConvertLimits;
            return self.cppType.mConvertLimits
        @mConvertLimits.setter
        def mConvertLimits(self,value:bool):
            self.cppType.mConvertLimits = value
            
        @property
        def mConvertClusters (self) ->bool:
            # //! This flag indicates whether or not to convert clusters.
            # bool mConvertClusters;
            return self.cppType.mConvertClusters
        @mConvertClusters.setter
        def mConvertClusters(self,value:bool):
            self.cppType.mConvertClusters = value
            
        @property
        def mConvertLightIntensity (self) ->bool:
            # //! This flag indicates whether or not to convert the light intensity property.
            # bool mConvertLightIntensity;	
            return self.cppType.mConvertLightIntensity
        @mConvertLightIntensity.setter
        def mConvertLightIntensity(self,value:bool):
            self.cppType.mConvertLightIntensity = value
            
        @property
        def mConvertPhotometricLProperties (self) ->bool:
            # //! This flag indicates whether or not to convert photometric lights properties.
            # bool mConvertPhotometricLProperties;
            return self.cppType.mConvertPhotometricLProperties
        @mConvertPhotometricLProperties.setter
        def mConvertPhotometricLProperties(self,value:bool):
            self.cppType.mConvertPhotometricLProperties = value
            
        @property
        def mConvertCameraClipPlanes (self) ->bool:
            # //! This flag indicates whether or not to convert the cameras clip planes.
            # bool mConvertCameraClipPlanes;
            return self.cppType.mConvertCameraClipPlanes
        @mConvertCameraClipPlanes.setter
        def mConvertCameraClipPlanes(self,value:bool):
            self.cppType.mConvertCameraClipPlanes = value
            
        def defaultConversionOptions(self):
            """set convert options as default statue"""
            self.mConvertRrsNodes = True
            self.mConvertLimits = True
            self.mConvertClusters = True
            self.mConvertLightIntensity = True
            self.mConvertPhotometricLProperties = True
            self.mConvertCameraClipPlanes = True

    @staticmethod
    def GetByStr(inputUnit = "cm"):
        
        unit = inputUnit.lower()
        if unit == "cm":
            return FbxSystemUnit.mm
        elif unit == "dm":
            return FbxSystemUnit.dm
        elif unit == "km":
            return FbxSystemUnit.km
        elif unit == "m":
            return FbxSystemUnit.m
        elif unit == "mm":
            return FbxSystemUnit.mm
        elif unit == "foot":
            return FbxSystemUnit.Foot
        elif unit == "inch":
            return FbxSystemUnit.Inch
        elif unit == "mile":
            return FbxSystemUnit.Mile
        elif unit == "yard":
            return FbxSystemUnit.Yard
        else :
            raise Exception ("Unknown system unit")

class FbxAxisSystem ():

    MayaZUp = fbx.FbxAxisSystem.MayaZUp
    MayaYUp = fbx.FbxAxisSystem.MayaYUp
    Max = fbx.FbxAxisSystem.Max
    Motionbuilder = fbx.FbxAxisSystem.Motionbuilder
    OpenGL= fbx.FbxAxisSystem.OpenGL
    DirectX= fbx.FbxAxisSystem.DirectX
    Lightwave= fbx.FbxAxisSystem.Lightwave
    
    class EUpVector():
        """EUpVector Specifies which canonical axis represents up in the system (typically Y or Z). """
        eXAxis = 1
        eYAxis = 2
        eZAxis = 3

    class EFrontVector():
        """
        EFrontVector  Vector with origin at the screen pointing toward the camera.
        * This is a subset of enum EUpVector because axis cannot be repeated.
        * We use the system of "parity" to define this vector because its value (X,Y or Z axis)
        * really depends on the up-vector. The EPreDefinedAxisSystem list the up-vector, parity and
        * coordinate system values for the predefined systems.
        """
        eParityEven = fbx.FbxAxisSystem.eParityEven
        eParityOdd = fbx.FbxAxisSystem.eParityOdd

    class ECoordSystem():
        """
        ECoordSystem Specifies the third vector of the system.
        * The FbxAxisSystem deduces the correct vector and direction based on this flag
        * and the relationship with the up and front vectors. The EPreDefinedAxisSystem list the up-vector, parity and
        * coordinate system values for the predefined systems.
        """
        eRightHanded = fbx.FbxAxisSystem.eRightHanded
        eLeftHanded = fbx.FbxAxisSystem.eLeftHanded

    class EPreDefinedAxisSystem():
        """
        * UpVector = ZAxis, FrontVector = -ParityOdd, CoordSystem = RightHanded\n
        eMayaZUp
        * UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded\n
        eMayaYUp
        * UpVector = ZAxis, FrontVector = -ParityOdd, CoordSystem = RightHanded\n
        eMax
        * UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded\n
        eMotionBuilder
        * UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded\n
        eOpenGL
        * UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = LeftHanded\n
        eDirectX
        * UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = LeftHanded\n
        eLightwave 
        """
        
        # UpVector = ZAxis, FrontVector = -ParityOdd, CoordSystem = RightHanded
        eMayaZUp = fbx.FbxAxisSystem.eMayaZUp
        # UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded
        eMayaYUp = fbx.FbxAxisSystem.eMayaYUp
        # UpVector = ZAxis, FrontVector = -ParityOdd, CoordSystem = RightHanded
        eMax = fbx.FbxAxisSystem.eMax
        # UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded
        eMotionBuilder = fbx.FbxAxisSystem.eMotionBuilder
        # UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = RightHanded
        eOpenGL = fbx.FbxAxisSystem.eOpenGL
        # UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = LeftHanded
        eDirectX = fbx.FbxAxisSystem.eDirectX
        # UpVector = YAxis, FrontVector =  ParityOdd, CoordSystem = LeftHanded
        eLightwave = fbx.FbxAxisSystem.eLightwave

    def __init__(self, *args, **kw):
        self.cppType = None
        argsCount = len(args)
        if argsCount == 3:
            self.__initByThreeParams(args[0], args[1], args[2])
        elif argsCount == 1:
            if isinstance(argsCount[0], fbx.FbxAxisSystem):
                self.__initBySameType(argsCount[0])
            elif isinstance(argsCount[0], fbx.FbxAxisSystem.EPreDefinedAxisSystem):
                self.__initByPreDefine(argsCount[0])
            else:
                raise Exception ("Cant initialize unknown method")

    def __initByThreeParams (self, pUpVector , pFrontVector, pCoordSystem):
        self.cppType = fbx.FbxAxisSystem(pUpVector, pFrontVector, pCoordSystem)

    def __initByPreDefine (self, preDefined):
        self.cppType = fbx.FbxAxisSystem(preDefined)

    def __initBySameType ( self, cppType ) :
        self.cppType = fbx.FbxAxisSystem(cppType)

    def ParseAxisSystem(xyz=""):
        statue,output =  fbx.FbxAxisSystem.ParseAxisSystem(xyz)
        return statue,output

    def DeepConvertScene(self, pScene):
        self.cppType.DeepConvertScene(pScene)

    def ConvertScene(self, pScene, pRoot=None):
        if pRoot != None:
            self.cppType.ConvertScene(pScene,pRoot)
        else:
            self.cppType.ConvertScene(pScene)

    def GetFrontVector(self,intSign):
        return self.cppType.GetFrontVector(int(intSign))
    
    def GetUpVector(self,intSign):
        return self.cppType.GetUpVector(int(intSign))

    def GetCoordSystem(self):
        return self.cppType.GetCoorSystem()

    def GetMatrix(self):
        return self.cppType.GetMatrix()

    def ConvertChildren(self,pRoot, pSrcSystem):
        self.cppType.ConvertChildren(pRoot, pSrcSystem)
    
    def __eq__(self, cppType):
        if not isinstance(cppType, FbxAxisSystem):
            raise Exception("have to be fbx.FbxAxisSystem")
        return self.cppType == cppType.cppType

    def __ne__(self, cppType):
        if not isinstance(cppType, FbxAxisSystem):
            raise Exception("have to be fbx.FbxAxisSystem")
        return self.cppType != cppType.cppType