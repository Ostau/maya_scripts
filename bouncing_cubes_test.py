import maya.cmds as cmds
import random

numCubes = 50

# Pick the seed for the cube placement
random.seed(1234)

# Clear all of the cubes
cubeList = cmds.ls('cube*')
if len(cubeList) > 0:
    cmds.delete(cubeList)

# Create the first cube
result = cmds.polyCube(w=1, h=1, d=1, name='cube#')
transformName = result[0]

# Create a group for all of the cubes
instanceGroupName = cmds.group(empty=True, name=transformName + '_instance_grp#')

# Create 50 random cubes
for i in range(0, numCubes):
    # Create another instance of the cube
    instanceResult = cmds.instance(transformName, name=transformName + '_instance#')
    
    # Place the cube in the group
    cmds.parent( instanceResult, instanceGroupName)
    
    # Apply a random transformation to it
    x = random.uniform(-10,10)
    y = random.uniform(0, 20)
    z = random.uniform(-10, 10)
    cmds.move(x, y, z, instanceResult)
    
    # Apply a random rotation to it
    xRot = random.uniform(0, 360)
    yRot = random.uniform(0, 360)
    zRot = random.uniform(0, 360) 
    cmds.rotate(xRot, yRot, zRot, instanceResult)
    
    # Apply a random scaling to it
    scalingFactor = random.uniform(0.3, 1.5)
    cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)
 
# Hide the original cube    
cmds.hide(transformName)

# Put the pivots to the center of each cube
cmds.xform(instanceGroupName, centerPivots=True)

# Scrub through the timeline, move the cubes in vertical direction and key each time
cmds.select(instanceGroupName)
for i in range(0, numCubes):
    cmds.currentTime(i)
    cmds.move(0,1,0)
    cmds.setKeyframe()
