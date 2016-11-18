import maya.cmds as cmds
import random

#global variables
rgb = (0,0,0)
angleChoice = 90
#first level functions ******************************************************
#main function to create standard block
def standardBlock():
    cubeDimensions = getTheSelectedDimension("StandardBlockWidth", "StandardBlockHeight", "none")
    createBasicRec(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2])
    createExtrusions(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2], cubeDimensions[3], cubeDimensions[4])
    addColor()
    
#main function to create round beam   
def roundBeam():
    cubeDimensions = getTheSelectedDimension("RoundBeamWidth", "none", "none")
    createBasicRec(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2])
    createSideAngles(cubeDimensions[3])
    createHoles(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2], cubeDimensions[3], cubeDimensions[4])
    addColor()
#main function to create square beam      
def squareBeam():
    cubeDimensions = getTheSelectedDimension("RoundBeamWidth", "none", "none")
    createBasicRec(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2])
    createPipeExtrusion(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2], cubeDimensions[3], cubeDimensions[4])
    createHoles(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2], cubeDimensions[3], cubeDimensions[4])
    addColor()
#main function to create angled beam      
def angledBeam():
    multiShape = ['','']

    for i in range(2):
        if i == 1:
            passVar = "angledBeam"
        else:
            passVar = "none"
        cubeDimensions = getTheSelectedDimension("AngledBeamWidth", "none", passVar)
        createBasicRec(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2])
        multiShape[i] = cu[0]
        createSideAngles(cubeDimensions[3])
        createHoles(cubeDimensions[0], cubeDimensions[1], cubeDimensions[2], cubeDimensions[3], cubeDimensions[4])
        multiShape[i] = addColor()
    moveBeam(multiShape, cubeDimensions[3], cubeDimensions[6])
#main function to create the wheel         
def wheel():
    createTire()  
    addColor() 
#main function to create the hub of the wheel     
def wheelHub():
    createWheelHub()
    addColor()
#main function to create the axel
def axel():
    length = createMainAxel("AxelWidth")
    addColor()
#main function to create the grooved axel    
def grooveAxel():
    length = createMainAxel("GrooveAxelWidth")
    createGroovedAxel(length)
    addColor()
#main function to create the cross axel       
def crossAxel():
    createCrossAxel()
    addColor()

    
#first level functions end ***************************************************
  
    
    
#second level functions ******************************************************

#creates the basic rectangle shape
#parameters computed X dimension, computed Y dimension, computed Z dimesion
def createBasicRec(cubeSizeX, cubeSizeY, cubeSizeZ):
    global cu
    cu = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ, sz=cubeSizeX, sx=cubeSizeX)
    cmds.move((cubeSizeY/2.0), moveY=True)   
 
# creates the extrusions for the basic block
#parameters computed X dimension, computed Y dimension, computed Z dimesion
#           the height and width without computations
def createExtrusions(cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth):

    for i in range(blockWidth):
        for j in range(blockDepth):
            cyl = cmds.polyCylinder(r=0.24, h=0.16)
            cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
            cmds.delete(ch=True)
            cu[0] = cmds.polyUnite(cu[0], cyl[0], n=":block", ch=False)
            
            
#creates the shader and assigns color            
def addColor():    

    myShader = cmds.shadingNode('phong', asShader=True)  
    cmds.setAttr ( (myShader + '.color'), rgb[0], rgb[1], rgb[2], type = 'double3' )
    cmds.select( cu[0] )
    cmds.hyperShade( assign=myShader )
    cmds.delete(ch=True)

    return cu[0]

# based on selected length does necessary calculations
# parameters the name of the sliders
def getTheSelectedDimension(reference1, reference2, reference3):
   
    blockWidthOrg = cmds.intSliderGrp(reference1, query=True, value=True)

    if reference3 == "angledBeam":
        blockWidth = blockWidthOrg/2.0
        cubeSizeX = blockWidth * 0.8
    else:
        cubeSizeX = blockWidthOrg * 0.8
        
    if reference2 == "none":
        blockDepth = 1
    else:
        blockDepth = cmds.intSliderGrp(reference2, query=True, value=True)
    if reference1 == "StandardBlockWidth":
        blockHeight = .96
    else:
        blockHeight = 1.92
        
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32
    
    if reference3 == "angledBeam":
        allCubeSizes = (cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth, blockHeight, blockWidthOrg)
    else:
        allCubeSizes = (cubeSizeX, cubeSizeY, cubeSizeZ, blockWidthOrg, blockDepth, blockHeight, blockWidthOrg)
    
    return allCubeSizes
    
# creates the holes in the blocks
#parameters computed X dimension, computed Y dimension, computed Z dimesion
#           the height and width without computations
def createHoles(cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth):

    
    blockWidth =str(blockWidth).rsplit(".", 1)[0] 
    blockWidth = int(blockWidth)

    for i in range(blockWidth - 1):
        cylinderDepth = blockDepth + (blockDepth * 0.3);
        cyl = cmds.polyCylinder(r=0.24, h=cylinderDepth)
        cmds.move((cubeSizeY - 0.30), moveY=True, a=True)
        cmds.move(((i  * 0.8) - (cubeSizeX/2.0) + 0.8), moveX=True, a=True)
        cmds.move(((0 * 0.8) - (cubeSizeZ/2.0) + 0.25), moveZ=True, a=True)
        cmds.rotate(90,0,0)
        cmds.delete(ch=True)
        cu[0] = cmds.polyBoolOp( cu[0], cyl[0], op=2, n="block" + str(i), ch=False)

    createBevels(cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth)
    
# creates the extrusions for the square block
#parameters computed X dimension, computed Y dimension, computed Z dimesion
#           the height and width without computations
def createPipeExtrusion(cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth):
    
    blockWidth =str(blockWidth).rsplit(".", 1)[0] 
    blockWidth = int(blockWidth)
    
    for i in range(blockWidth):
        for j in range(blockDepth):
            cyl = cmds.polyPipe(r=0.24, h=0.34, t=0.05)
            cmds.move((cubeSizeY + 0.05), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
            cmds.delete(ch=True)

            cu[0] = cmds.polyBoolOp( cu[0], cyl[0], op=1, n="block", ch=False)

#finds the selected color and sets it as a global variables
# parameter is the selected color from the dropdown            
def selectedColor(selectedColorVar):
    global rgb
    if selectedColorVar == "Blue":
        rgb = (0,0.3412,0.6588)
    elif  selectedColorVar == "Green":
        rgb = (0,0.4823,0.1569)
    elif  selectedColorVar == "Yellow":
        rgb = (0.9961,0.7686,0)
    elif  selectedColorVar == "Orange":
        rgb = (0.9059,0.3882,0.09412)
    elif  selectedColorVar == "Pink":
        rgb = (0.933,0.6157,0.7647)
    elif  selectedColorVar == "Brown":
        rgb = (0.3568,0.1098,0.0470)
    elif  selectedColorVar == "Purple":
        rgb = (0.1725,0.0824,0.4667)
    else:
        rgb = (0,0,0)
    if cmds.swatchDisplayPort("theSwatch", ex=True) == False:
        cmds.rowColumnLayout( numberOfColumns=1)
        cmds.swatchDisplayPort("theSwatch", wh=(40, 30), bgc=(rgb[0],rgb[1],rgb[2]))
        cmds.setParent( '..' )
    else:
        print("Color Fail")

# creates a basuc axel
# parameter is value from slider    
def createMainAxel(referenceSlider):
    global cu
    
    length = cmds.intSliderGrp(referenceSlider, query=True, value=True)
    cu = cmds.polyCylinder(r=0.31, h=length, sz=4, sy=48)
    cmds.rotate(90,0,0)
    cmds.delete(ch=True)
    distance1 = 0.2
    distance2 = 0.22
    createSideEdgesAxel(length, distance1, distance2)

    return length
    
 #moves the cylinders to the sides to create the axel
 #parameters are the chosen length, and distances to move the cylinders   
def createSideEdgesAxel(length, distance1, distance2):
    
    cyl1 = cmds.polyCylinder(r=0.15, h=length+ 0.1, sz=4, sy=24)
    cmds.rotate(90,0,0)
    cmds.move((distance1), moveY=True, a=True)
    cmds.move((distance2), moveX=True, a=True)
    cmds.move((-1*(0.003)), moveZ=True, a=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( cu[0], cyl1[0], op=2, n="block", ch=False)
    
    cyl2 = cmds.polyCylinder(r=0.15, h=length+ 0.1, sz=4, sy=12)
    cmds.rotate(90,0,0)
    cmds.move((distance1), moveY=True, a=True)
    cmds.move((-1*(distance2)), moveX=True, a=True)
    cmds.move((-1*(0.003)), moveZ=True, a=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( cu[0], cyl2[0], op=2, n="block", ch=False)
    
    cyl3 = cmds.polyCylinder(r=0.15, h=length+ 0.1, sz=4, sy=12)
    cmds.rotate(90,0,0)
    cmds.move((-1*(distance1)), moveY=True, a=True)
    cmds.move((distance2), moveX=True, a=True)
    cmds.move((-1*(0.003)), moveZ=True, a=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( cu[0], cyl3[0], op=2, n="block", ch=False)
    
    cyl4 = cmds.polyCylinder(r=0.15, h=length+ 0.1, sz=4, sy=12)
    cmds.rotate(90,0,0)
    cmds.move((-1*(distance1)), moveY=True, a=True)
    cmds.move((-1*(distance2)), moveX=True, a=True)
    cmds.move((-1*(0.003)), moveZ=True, a=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( cu[0], cyl4[0], op=2, n="block", ch=False)

#function to create tire
def createTire():
    global cu
    cu = cmds.polyTorus(sx=2, sy=2, r=0.5, sr=0.25)
    cmds.scale(1,1.712,1)
    cmds.delete(ch=True)
    middle = cmds.polyCylinder(r=0.45, h=2, sz=4, sy=12)
    cu[0] = cmds.polyBoolOp(cu[0], middle[0], op=2, n="block", ch=False)
    extrudeForTire()
    cmds.delete(ch=True)
    pip1 = cmds.polyPipe(r=0.4906, h=1.5094, t=0.0755)
    cu[0] = cmds.polyUnite( cu[0], pip1[0], n="block", ch=False)
    pip2 = cmds.polyPipe(r=0.4150, h=1.1321, t=0.0)
    cu[0] = cmds.polyUnite( cu[0], pip2[0], n="block", ch=False)

#creates the axel with grooves int it
#parameters is the chosen length   
def createGroovedAxel(length):
        
        for i in range(2):

            cylTop = cmds.polyCylinder(r=0.15, h=1, sz=4, sy=12)
            cmds.rotate(0,0,90)
            if i == 0:
                cmds.move(((length/3.5)), moveZ=True, a=True)
            else:
                cmds.move((-1 * ((length/3.5))), moveZ=True, a=True)
            cmds.move((0.34), moveY=True, a=True)
            cmds.delete(ch=True)
            cu[0] = cmds.polyBoolOp(cu[0], cylTop[0], op=2, n="block", ch=False)
            
            cylTop = cmds.polyCylinder(r=0.15, h=1, sz=4, sy=12)
            cmds.rotate(0,0,90)
            if i == 0:
                cmds.move(((length/3.5)), moveZ=True, a=True)
            else:
                cmds.move((-1 * ((length/3.5))), moveZ=True, a=True)
            cmds.move((-0.34), moveY=True, a=True)
            cmds.delete(ch=True)
            cu[0] = cmds.polyBoolOp(cu[0], cylTop[0], op=2, n="block", ch=False)
            
            cylTop2 = cmds.polyCylinder(r=0.15, h=1, sz=4, sy=12)
            cmds.rotate(0,0,180)    
            if i == 0:
                cmds.move(((length/3.5)), moveZ=True, a=True)
            else:
                cmds.move((-1 * ((length/3.5))), moveZ=True, a=True)
            cmds.move((0.29), moveY=True, a=True)
            cmds.move((0.34), moveX=True, a=True)
            cmds.delete(ch=True)
            cu[0] = cmds.polyBoolOp(cu[0], cylTop[0], op=2, n="block", ch=False)
            
            cylTop2 = cmds.polyCylinder(r=0.15, h=1, sz=4, sy=12)
            cmds.rotate(0,0,180)    
            if i == 0:
                cmds.move(((length/3.5)), moveZ=True, a=True)
            else:
                cmds.move((-1 * ((length/3.5))), moveZ=True, a=True)
            cmds.move((0.29), moveY=True, a=True)
            cmds.move((-0.34), moveX=True, a=True)
            cmds.delete(ch=True)
            cu[0] = cmds.polyBoolOp(cu[0], cylTop[0], op=2, n="block", ch=False)

#Creates the cross axel           
def createCrossAxel():
    
    length = createMainAxel("CrossAvelWidth")
    cmds.select( cu[0] )
    cmds.scale(1,1,1.5)
    sideCylin1 =cmds.polyCylinder(r=0.4, h=length, sz=12, sx=12, sy=12)
    cmds.rotate(90,0,0)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(sideCylin1[0], cu[0], op=2, n="block", ch=False)
    Tor = cmds.polyTorus(sx=2, sy=2, r=0.377, sr=0.037)
    cmds.rotate(90,0,0)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(Tor[0], cu[0], op=1, n="block", ch=False)
    Tor2 = cmds.polyTorus(sx=2, sy=2, r=0.377, sr=0.037)
    cmds.rotate(90,0,0)
    cmds.move(length/3.2, moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(Tor2[0], cu[0], op=1, n="block", ch=False)
    Tor3 = cmds.polyTorus(sx=2, sy=2, r=0.377, sr=0.037)
    cmds.rotate(90,0,0)
    cmds.move(-1*(length/3.2), moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(Tor3[0], cu[0], op=1, n="block", ch=False)
    cmds.select( cu[0] )
    cmds.rotate(0,0,45)
    distance1 = 0.33
    distance2 = 0.35
    createSideEdgesAxel(length, distance1, distance2)


#Creates slight extrusions on the side of the cross axel        
def createSideAngles(blockWidth):

    sideCylin1 =cmds.polyCylinder(r=0.31, h=0.8, sz=1)
    cmds.rotate(90, 0, 0)
    cmds.move((-1 * (((blockWidth * 0.8)/2.0))), moveX=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(sideCylin1[0], cu[0], op=1, n="block", ch=False)

    sideCylin = cmds.polyCylinder(r=0.31, h=0.8, sz=1)
    cmds.rotate(90, 0, 0)
    cmds.move((((blockWidth* 0.8)/2.0)), moveX=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(sideCylin1[0], cu[0], op=1, n="block", ch=False)
    
    sideCylin2 = cmds.polyCylinder(r=0.28, h=0.15, sz=1)
    cmds.rotate(90, 0, 0)
    cmds.move((-1 * (((blockWidth * 0.8)/2.0))), moveX=True)
    cmds.move(((0 * 0.05) - (1/2.0) + 0.829), moveZ=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(cu[0],sideCylin2[0], op=2, n="block", ch=False)

    sideCylin3 = cmds.polyCylinder(r=0.28, h=0.15, sz=1)
    cmds.rotate(90, 0, 0)
    cmds.move((((blockWidth* 0.8)/2.0)), moveX=True)
    cmds.move(((0 * 0.05) - (1/2.0) + 0.829), moveZ=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(cu[0], sideCylin3[0], op=2, n="block", ch=False)
   
    
    difference1 = cmds.polyCylinder(r=0.24, h=2)
    cmds.rotate(90, 0, 0)
    cmds.move((-1 * ((blockWidth* 0.8)/2.0)), moveX=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(cu[0], difference1[0], op=2, n="block", ch=False)
    
    difference2 = cmds.polyCylinder(r=0.24, h=2)
    cmds.rotate(90, 0, 0)
    cmds.move((((blockWidth* 0.8)/2.0)), moveX=True)
    cmds.move(0.31, moveY=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp(cu[0], difference2[0], op=2, n="block", ch=False)
    
#creates the notches in the side of the cross axel
def createBevels(cubeSizeX, cubeSizeY, cubeSizeZ, blockWidth, blockDepth):
    
    for i in range(blockWidth - 1):
        cyl = cmds.polyCylinder(r=0.28, h=0.15)
        cmds.move((cubeSizeY - 0.30), moveY=True, a=True)
        cmds.move(((i  * 0.8) - (cubeSizeX/2.0) + 0.8), moveX=True, a=True)
        cmds.move(((0 * 0.05) - (cubeSizeZ/2.0) + 0.8), moveZ=True, a=True)
        cmds.rotate(90,0,0)
        cmds.delete(ch=True)
        cu[0] = cmds.polyBoolOp( cu[0], cyl[0], op=2, n="block" + str(i), ch=False)
#moves the second beam for the angled beam
#parameter           
def moveBeam(multiShape, width, width2):

    temp =str(cu[0]).rsplit("'", 1)[0]   
    temp2 =temp.rsplit("'", 1)[1]   
    temp2 = str(temp2)
    cmds.move((-width2/5.0), temp2+ ".rotatePivot", moveX=True)
    cmds.move(0.31, temp2+ ".rotatePivot", moveY=True)
    cmds.rotate(0,0,angleChoice)
    cmds.move( ((width) + float(width2))/2.5  , moveX=True)


    cmds.delete(ch=True)
    cmds.polyUnite( multiShape[0], multiShape[1], n="block", ch=False)
    
#does the extrusion for the tire
def extrudeForTire():

    temp =str(cu[0]).rsplit("'", 1)[0]   
    temp2 =temp.rsplit("'", 1)[1]   
    temp2 = str(temp2)
    cmds.polyExtrudeFacet( temp2 + '.f[161]', temp2 + ".f[163]", temp2 + ".f[165]", temp2 + ".f[167]", temp2 + ".f[169]", temp2 + ".f[171]", temp2 + ".f[173]", temp2 + ".f[175]", temp2 + ".f[177]",
    temp2 + ".f[179]", temp2 + ".f[181]", temp2 + ".f[183]", temp2 + ".f[185]", temp2 + ".f[187]", temp2 + ".f[189]", temp2 + ".f[191]", temp2 + ".f[193]", temp2 + ".f[195]", temp2 + ".f[197]",
    temp2 + ".f[199]", temp2 + ".f[201]", temp2 + ".f[203]", temp2 + ".f[205]", temp2 + ".f[207]", temp2 + ".f[209]", temp2 + ".f[211]", temp2 + ".f[213]", temp2 + ".f[215]", temp2 + ".f[217]",
    temp2 + ".f[219]", temp2 + ".f[221]", temp2 + ".f[223]", temp2 + ".f[225]", temp2 + ".f[227]", temp2 + ".f[229]", temp2 + ".f[231]", temp2 + ".f[233]", temp2 + ".f[235]", temp2 + ".f[237]",
    temp2 + ".f[239:240]", temp2 + ".f[242]", temp2 + ".f[244]", temp2 + ".f[246]", temp2 + ".f[248]", temp2 + ".f[250]", temp2 + ".f[252]", temp2 + ".f[254]", temp2 + ".f[256]", temp2 + ".f[258]",
    temp2 + ".f[260]", temp2 + ".f[262]", temp2 + ".f[264]", temp2 + ".f[266]", temp2 + ".f[268]", temp2 + ".f[270]", temp2 + ".f[272]", temp2 + ".f[274]", temp2 + ".f[276]", temp2 + ".f[278]",
    temp2 + ".f[280]", temp2 + ".f[282]", temp2 + ".f[284]", temp2 + ".f[286]", temp2 + ".f[288]", temp2 + ".f[290]", temp2 + ".f[292]", temp2 + ".f[294]", temp2 + ".f[296]", temp2 + ".f[298]",
    temp2 + ".f[300]", temp2 + ".f[302]", temp2 + ".f[304]", temp2 + ".f[306]", temp2 + ".f[308]", temp2 + ".f[310]", temp2 + ".f[312]", temp2 + ".f[314]", temp2 + ".f[316]", temp2 + ".f[318]", kft=True, scaleX= 1.1, scaleY= 1.1, scaleZ= 1.1,  divisions= 0, twist= 0, taper= 1, thickness= 0, n="block" )

#does the wheel hub
def createWheelHub():
    global cu
    cu = cmds.polyCylinder(r=0.4, h=0.8, sz=2, sx=2, sy=2)
    temp =str(cu[0]).rsplit("'", 1)[0]   
    cmds.select(temp + ".e[40:59]")
    cmds.scale(0.768657, 0.768657, 0.768657 )
    cyl = cmds.polyCylinder(r=0.3, h=1, sz=2, sx=2, sy=2)
    cu[0] = cmds.polyBoolOp( cu[0], cyl[0], op=2, n="block", ch=False)
    cyl2 =cmds.polyCylinder(r=0.35, h=.3, sz=2, sx=2, sy=2)
    cu[0] = cmds.polyBoolOp( cyl2[0], cu[0], op=1, n="block", ch=False)
    
    Tor1 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( 0.128 , moveX=True)
    cmds.move( -0.039 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor1[0], cu[0], op=1, n="block", ch=False)
    Tor2 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( 0.013 , moveX=True)
    cmds.move( -0.134 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor2[0], cu[0], op=1, n="block", ch=False)
    Tor3 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( -0.123 , moveX=True)
    cmds.move( -0.082 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor3[0], cu[0], op=1, n="block", ch=False)
    Tor4 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( -0.123 , moveX=True)
    cmds.move( 0.065 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor4[0], cu[0], op=1, n="block", ch=False)
    Tor5 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( -0.017 , moveX=True)
    cmds.move( 0.155 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor5[0], cu[0], op=1, n="block", ch=False)
    Tor6 = cmds.polyPipe(r=0.07, t=0.04, h=0.9434)
    cmds.move( 0.115 , moveX=True)
    cmds.move( 0.109 , moveZ=True)
    cmds.delete(ch=True)
    cu[0] = cmds.polyBoolOp( Tor6[0], cu[0], op=1, n="block", ch=False)

def selectedAngle(angle):
   global angleChoice
   angleChoice = angle


#second level functions end **************************************************

#create Window
window = cmds.window(title="Lego Blocks", menuBar=True,
widthHeight=(883, 403))

#main GUI Layout ******************************************************
cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True,force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

#colour Choice
cmds.rowColumnLayout( numberOfColumns=1)
cmds.optionMenu(label="Colour Choice", changeCommand=selectedColor)
cmds.menuItem( label='Blue')
cmds.menuItem( label='Green')
cmds.menuItem( label='Yellow')
cmds.menuItem( label='Orange')
cmds.menuItem( label='Pink')
cmds.menuItem( label='Brown')
cmds.menuItem( label='Purple')
cmds.setParent( '..' )
#size selection

cmds.rowColumnLayout( numberOfColumns=2)
cmds.intSliderGrp('StandardBlockWidth', label="Width", field=True, min=1, max=12, value=6)
cmds.button(label="Create Standard Block", command=('standardBlock()'))
cmds.setParent( '..' )
cmds.rowColumnLayout( numberOfColumns=1)
cmds.intSliderGrp('StandardBlockHeight', label="Height", field=True, min=1, max=12, value=6)
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('RoundBeamWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Round Beam", command=('roundBeam()'))
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('SquareBeamWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Square Beam", command=('squareBeam()'))
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('AngledBeamWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Angled Beam", command=('angledBeam()'))

cmds.setParent( '..' )
cmds.rowColumnLayout( numberOfColumns=2, cw=[(1,140)], cal=[(2,"right")])
cmds.text(l="")
cmds.optionMenu(label="Angle", changeCommand=selectedAngle)
cmds.menuItem( label='90')
cmds.menuItem( label='45')
cmds.setParent( '..' )


cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('AxelWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Axels", command=('axel()'))
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('GrooveAxelWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Grove Axels", command=('grooveAxel()'))
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=2, cal=[(2,"right")])
cmds.intSliderGrp('CrossAvelWidth', label="Length", field=True, min=1, max=12, value=6)
cmds.button(label="Create Cross Axels", command=('crossAxel()'))
cmds.setParent( '..' )


cmds.rowColumnLayout( numberOfColumns=4, cw=[(3,100)], cal=[(2,"right")])
cmds.text(l="")
cmds.text(l="")
cmds.text(l="")
cmds.button(label="Create Wheel", command=('wheel()'))
cmds.setParent( '..' )

cmds.rowColumnLayout( numberOfColumns=4, cw=[(3,100)], cal=[(2,"right")])
cmds.text(l="")
cmds.text(l="")
cmds.text(l="")
cmds.button(label="Create Wheel Hub", command=('wheelHub()'))
cmds.setParent( '..' )


#main GUI Layout end ****************************************************

cmds.showWindow( window )


