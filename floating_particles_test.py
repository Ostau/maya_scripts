import maya.cmds as cmds
import random

# Number of particles you want to generate
numParticles = 100

# Number of frames you want the animation to span
numFrames = 80

# Adjust for future use
numFrames = numFrames / 2

# Pick the seed for the particle placement
random.seed(1234)

# Clear all of the particles
partList = cmds.ls('particle_*')
if len(partList) > 0:
    cmds.delete(partList)

# Calculates a rotation based on the current rotation and the frame for which the rotation 
# needs to be calculated
def calcRot(curr, frame):
    rotation = (curr + ((360/numFrames) * frame))
    return rotation;

# Sets the rotation and moves the particle and then keys it
def setParticleFrame(i, x, y, z, xRot, yRot, zRot):
    newY = (y + i / 4.0) % 10
    cmds.move(x, newY, z)
    cmds.rotate(calcRot(xRot, i), calcRot(yRot, i), calcRot(zRot, i))
    cmds.setKeyframe()
    return newY;

# Moves and rotates the particle for each frame and keys it there
def keyParticle(instanceResult, x, y, z, xRot, yRot, zRot):
    cmds.select(instanceResult)
    for i in range(1, numFrames + 1, 1):
        cmds.currentTime(i * 2)
        if (setParticleFrame(i, x, y, z, xRot, yRot, zRot) > 9.5):
            cmds.currentTime((i * 2) + 1)
            setParticleFrame(i + 1, x, y, z, xRot, yRot, zRot)

# Grab the particle
transformName = 'particle'

# Create a group for all of the particles
instanceGroupName = cmds.group(empty=True, name=transformName + '_instance_grp#')

# Create 50 random particles
for i in range(0, numParticles):
    # Create another instance of the particle
    instanceResult = cmds.instance(transformName, name=transformName + '_instance#')
    
    # Place the particle in the group
    cmds.parent( instanceResult, instanceGroupName)
    
    # Generate a random transformation for it
    x = random.uniform(-3,3)
    y = random.uniform(0, 10)
    z = random.uniform(-3, 3)
    
    # Generate a random rotation for it
    xRot = random.uniform(0, 360)
    yRot = random.uniform(0, 360)
    zRot = random.uniform(0, 360) 
    
    # Generate a random scaling for it
    scalingFactor = random.uniform(0.05, 0.2)
    cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)
    
    # Key the particle on all relevant frames
    keyParticle(instanceResult, x, y, z, xRot, yRot, zRot)

# Put the pivots to the center of each particle
cmds.xform(instanceGroupName, centerPivots=True)