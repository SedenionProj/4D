import numpy as np
class Math:
    def init(width,height):
        Math.width = width
        Math.height = height
        Math.aspectRatio = height/width

        Math.rotationX = 0
        Math.rotationY = 0
        Math.rotationZ = 0

        Math.rotationZW = 0
        Math.rotationYW = 0
        Math.rotationYZ = 0
        Math.rotationXW = 0
        Math.rotationXZ = 0
        Math.rotationXY = 0

    @staticmethod
    def ToNormalized(vert):
        return np.array([vert[0]*Math.aspectRatio,vert[1],vert[2]])*(2/Math.width)-1
    @staticmethod
    def ToScreenSpace(vert):
        v = (vert+1)*0.5*Math.height
        v[0] += (Math.width//2)-(Math.height//2)
        return v
    
    @staticmethod
    def Projection4D(vert):
        return 0.5*vert[:3]/vert[3]
    
    @staticmethod
    def Projection3D(vert):
        return 0.5*vert[:2]/vert[2]
    
    @staticmethod
    def Rotation3D_X(vert):
        a = Math.rotationX
        rot = np.array([[1,0        ,0         ],
                        [0,np.cos(a),-np.sin(a)],
                        [0,np.sin(a),np.cos(a)]])
        return rot @ vert
    
    @staticmethod
    def Rotation3D_Y(vert):
        a = Math.rotationY
        rot = np.array([[np.cos(a),0,np.sin(a)],
                        [0,1,0],
                        [-np.sin(a),0,np.cos(a)]])
        return rot @ vert
    @staticmethod
    def Rotation3D_Z(vert):
        a = Math.rotationZ
        rot = np.array([[np.cos(a),-np.sin(a),0],
                        [np.sin(a),np.cos(a) ,0],
                        [0,0,1]])
        return rot @ vert
    
    @staticmethod
    def Rotation4D_ZW(vert):
        a = Math.rotationZW
        rot = np.array([[np.cos(a),     -np.sin(a),0,0],
                        [np.sin(a),     np.cos(a),0,0],
                        [0,0,1,0],
                        [0,0,0,1]])
        return rot @ vert
    @staticmethod
    def Rotation4D_YW(vert):
        a = Math.rotationYW
        rot = np.array([[np.cos(a),0,-np.sin(a),0],
                        [0,1,0,0],
                        [np.sin(a),0,np.cos(a),0],
                        [0,0,0,1]])
        return rot @ vert
    @staticmethod
    def Rotation4D_YZ(vert):
        a = Math.rotationYZ
        rot = np.array([[np.cos(a),0,0,-np.sin(a)],
                        [0,1,0,0],
                        [0,0,1,0],
                        [np.sin(a),0,0,np.cos(a)]])
        return rot @ vert
    @staticmethod
    def Rotation4D_XW(vert):
        a = Math.rotationXW
        rot = np.array([[1,0,0,0],
                        [0,np.cos(a),-np.sin(a),0],
                        [0,np.sin(a),np.cos(a),0],
                        [0,0,0,1]])
        return rot @ vert
    @staticmethod
    def Rotation4D_XZ(vert):
        a = Math.rotationXZ
        rot = np.array([[1,0,0,0],
                        [0,np.cos(a),0, -np.sin(a)],
                        [0,0,1,0],
                        [0,np.sin(a),0, np.cos(a)]])
        return rot @ vert
    @staticmethod
    def Rotation4D_XY(vert):
        a = Math.rotationXY
        rot = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,np.cos(a), -np.sin(a)],
                        [0,0,np.sin(a), np.cos(a)]])
        return rot @ vert
    