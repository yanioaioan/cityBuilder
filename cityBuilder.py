import maya.cmds as cmds
import math
import random
import time
import maya.mel as mel


cmds.select(all=True)
cmds.delete()

def getVtxPosList( shapeNode ) :
 
	vtxWorldPosition = []    # will contain positions un space of all object vertex
 
	vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
	
	#randomize vertices positions
	for i in range(1,9):
	    for j in range(1,9):
	        t=(i+10)*j
	         
	        curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(t)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]/10
	    	moveFactorX=random.randint(-25,40)/100.0
	    	moveFactorZ=random.randint(-20,20)/100.0
	    	curPointPosition[0]+=moveFactorX
	    	curPointPosition[2]+=moveFactorZ
	    	#print curPointPosition
	    	cmds.xform( str(shapeNode)+".vtx["+str(t)+"]", translation=curPointPosition, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]/10
	    	
	    	vtxWorldPosition.append( curPointPosition )
 
	return vtxWorldPosition


#create a plane
myplane=cmds.polyPlane(w=10,h=10, ch=0)
cmds.select(all=True)
cmds.delete(ch=True)

#get all vertices and randomize their position
sphereVertexList=getVtxPosList('pPlane1')

#select the plane's faces
object=cmds.ls( selection=True )
cmds.select(object[0]+'.f[:15]')

#numberOfSelectedFacesFaces represent the building bases-or could be block bases
numberOfSelectedFacesFaces=cmds.polyEvaluate( fc=True )

individualFaceLevel1List=[]

#for all faces selected
for facesnumber in range(numberOfSelectedFacesFaces):
#for index in range(0,i):
        
    index=facesnumber
    
    floorsperBuilding=1
            
    #cmds.refresh()
    #time.sleep(1)
    
    #create block
    base=cmds.polyExtrudeFacet( "%s.f[%d]"%(myplane[0], index), ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards
    
    ##add divisions to block
    base2=cmds.polySubdivideFacet( "%s.f[%d]"%(myplane[0], index),  dv=1, m=0, ch=0)
    
    #and now for all regions of this block select its faces..
    restOfDividedFaces=cmds.ls( selection=True )
    cmds.select(restOfDividedFaces)
    selectedInnerFaces=cmds.polyEvaluate( fc=True )
    
    innerFaces= cmds.ls(sl=True)
    
    cmds.select(all=True)
    cmds.delete(ch=True)
    
    #for innerfacesnumber in (innerFaces):
    
    #print innerfacesnumber
    individualFaceLevel1=cmds.filterExpand(innerFaces, sm=34)
    individualFaceLevel1List.append(individualFaceLevel1)
    #print innerFaces
    #print individualFace
    

  
    
#############################################################################
#create another nested block
for faceLevel1 in (individualFaceLevel1List):
    cmds.refresh()
    cmds.select(faceLevel1)
    # Average all the vertices
    #cmds.polyAverageVertex()
    
    #maya.mel.eval("polyCleanupArgList \"3\" { \"0\",\"1\",\"1\", \"0\", \"1\", \"1\", \"1\", \"0\", \"0\", \"1e-05\", \"0\", \"1e-05\", \"0\", \"1e-05\", \"0\", \"1\", \"1\"};")
    #time.sleep(1)
    ##cmds.refresh()
    #time.sleep(1)
    
    cmds.select(all=True)
    cmds.delete(ch=True)
    print faceLevel1
    base=cmds.polyExtrudeFacet( faceLevel1 , ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards
    
    ##add divisions to this nested block
    base2leveled=cmds.polySubdivideFacet(faceLevel1,  dv=1, m=0, ch=0)
    
    #and now for all regions of this block select its faces..
    restOfDividedFaces=cmds.ls( selection=True )
    cmds.select(restOfDividedFaces)
    selectedInnerFaces=cmds.polyEvaluate( fc=True )
    
    innerFaces= cmds.ls(sl=True)
    
    individualFaceLevel1=cmds.filterExpand(innerFaces, sm=34)

    individualFace=individualFaceLevel1
    
    #if each one of these nested faces is just one..create one pavement-building      
    if len(individualFace) == 1:        
        #index=innerfacesnumber
        #print individualFace
   
        #create block
        base=cmds.polyExtrudeFacet( individualFace, ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards
        
        cmds.polyExtrudeFacet(individualFace, localTranslate=[0.0, 0.0, 0.002], kft=True, ch=0)#up
        
        #cmds.refresh()
        #time.sleep(1)
        
        cmds.polyExtrudeFacet(individualFace, ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards
        
        #cmds.refresh()
        #time.sleep(1)
        
        #for j in range(0,floorsperBuilding):
        cmds.polyExtrudeFacet(individualFace, localTranslate=[0.0, 0.0, floorsperBuilding*random.random()], kft=True, ch=0)#up
        #cmds.refresh()
        cmds.select(all=True)
        cmds.delete(ch=True)
            
    #if each one of these nested faces has multiple nested faces..create one pavement-building      
    elif len(individualFace) > 1:
        #for each one of these multiple nested faces create one pavement-building
        for indFace in (individualFace):
            
            indFace=cmds.filterExpand(indFace, sm=34)
            print indFace   
            
            #create block
            base=cmds.polyExtrudeFacet( indFace, ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards            
            
            cmds.polyExtrudeFacet(indFace, localTranslate=[0.0, 0.0, 0.002], kft=True, ch=0)#up
            
            #cmds.refresh()            
            
            cmds.polyExtrudeFacet(indFace, ls=[0.8, 0.8, 0.8], kft=True, ch=0)#inwards
            
            #cmds.refresh()
            
            
            #for j in range(0,floorsperBuilding):
            cmds.polyExtrudeFacet(indFace, localTranslate=[0.0, 0.0, floorsperBuilding*random.random()], kft=True, ch=0)#up
            #cmds.refresh()
            cmds.select(all=True)
            cmds.delete(ch=True)
        


'''

for facesnumber in range(numberOfSelectedFacesFaces):
#for index in range(0,i):
    index=facesnumber
    
    floorsperBuilding=7
    cmds.delete(ch=True)  
    
    #cmds.refresh()
    #time.sleep(1)

    cmds.polyExtrudeFacet("%s.f[%d]"%(myplane[0], index), localTranslate=[0.0, 0.0, 0.01], kft=True)#up
    
    #cmds.refresh()
    #time.sleep(1)
    
    cmds.polyExtrudeFacet("%s.f[%d]"%(myplane[0], index), ls=[0.8, 0.8, 0.8], kft=True)#inwards
    
    #cmds.refresh()
    #time.sleep(1)
    
    for j in range(0,floorsperBuilding):
        cmds.delete(ch=True)
        cmds.polyExtrudeFacet("%s.f[%d]"%(myplane[0], index), localTranslate=[0.0, 0.0, 0.08], kft=True)#up
        #cmds.refresh()
		cmds.select(all=True)
        cmds.delete(ch=True)
            
    

'''