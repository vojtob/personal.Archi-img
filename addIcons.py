import sys
import os
import json
import shutil
import cv2
import numpy as np
import rectRecognition as rr
import src.python.imageUtils as imageUtils


def copyImage(imageSourcePath, imageDestPath):
    print('  copy from', imageSourcePath, 'to', imageDestPath)
    # create destination directory
    imageReleaseDir = os.path.normpath(os.path.split(imageDestPath)[0])
    if(not os.path.exists(imageReleaseDir)):
        os.makedirs(imageReleaseDir)
    shutil.copyfile(imageSourcePath, imageDestPath)

def writeRectangles2Image(img, rectangles, imageRectanglePath):
    imageRectangleDir = os.path.normpath(os.path.split(imageRectanglePath)[0])
    if(not os.path.exists(imageRectangleDir)):
        os.makedirs(imageRectangleDir)

    imgRec = np.copy(img)
    recCounter = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    for r in rectangles:
        cv2.rectangle(imgRec, r[0], r[1], (0,0,255), thickness=2)
        cv2.putText(imgRec,str(recCounter),(r[0][0],r[0][1]+30), font, 1, (0,0,255),1,cv2.LINE_AA)
        recCounter += 1

    # for y, segments in lineSegmentsHorizontal.items():
    #     for s in segments:
    #         cv2.line(img, (s[0],y),(s[1],y), (0,255,0), thickness=2)
    # for x, segments in lineSegmentsVertical.items():
    #     for s in segments:
    #         cv2.line(img, (x,s[0]),(x,s[1]), (255,0,0), thickness=2)
    cv2.imwrite(imageRectanglePath, imgRec)

def addIcons2image(imageSourcePath, imageRectanglePath, imageReleasePath, iconDefs, iconsDir):
    img = cv2.imread(imageSourcePath, cv2.IMREAD_UNCHANGED)

    # convert to BW
    imgBW =imageUtils.convertImage(img)
    # save BW image
    # cv2.imwrite(imageRectanglePath[:-4] + '_BW' + imageRectanglePath[-4:], imgBW)
    # identify rectangles
    lineSegmentsHorizontal, lineSegmentsVertical = rr.findLineSegments(imgBW, 6, 30)
    rectangles = rr.findRectangles(lineSegmentsHorizontal, lineSegmentsVertical, 4)

    # add rectangles into img
    writeRectangles2Image(img, rectangles, imageRectanglePath)

    # add icons to image
    for iconDef in iconDefs:
        print('  add icon', iconDef['iconName'])
        iconFile = os.path.join(iconsDir,  iconDef['iconName'])
        if(not os.path.exists(iconFile)):
            print('    icon image not found')
            return
        recID = iconDef['rec']
        if( recID > len(rectangles)):
            print('    icon refers to non existing rectangle')
            return
        img = imageUtils.addIcon2Image(img, rectangles[recID-1], iconFile, iconDef['size'], iconDef['x'], iconDef['y'])

    imageDir = os.path.normpath(os.path.split(imageReleasePath)[0])
    if(not os.path.exists(imageDir)):
        os.makedirs(imageDir)
    cv2.imwrite(imageReleasePath, img)

# read project dir from arguments
if (len(sys.argv) < 2):
    print('usage: generateUMLETimages.py projectPath')
    exit(1)
else:
    projectDir = os.path.normpath(sys.argv[1])

# read images icons definitions
with open(os.path.join(projectDir, 'src', 'img', 'images.json')) as imagesFile:
    imageDefs = json.load(imagesFile)

# this are global variables for whole project
imagesSourceDir = os.path.join(projectDir, 'temp', 'img_exported')
imagesRectanglesDir = os.path.join(projectDir, 'temp', 'img_rec')
imagesReleaseDir = os.path.join(projectDir, 'release', 'img')
iconsDir = os.path.join(projectDir, 'src', 'res', 'icons')

# go throug all exported files
# if there is imageDef then add icons to image
# else copy image do release
for (dirpath, dirnames, filenames) in os.walk(imagesSourceDir):
    imageRelativeDir = os.path.relpath(dirpath,imagesSourceDir)

    for f in filenames:
        imageRelativePath = os.path.join(imageRelativeDir, f)
        imageSourcePath = os.path.join(imagesSourceDir, imageRelativePath)
        imageRectanglePath = os.path.join(imagesRectanglesDir, imageRelativePath)
        imageReleasePath = os.path.join(imagesReleaseDir, imageRelativePath)

        defs = [imageDef for imageDef in imageDefs if os.path.normpath(imageDef['fileName'])==imageRelativePath]
        if(len(defs)):
            print('add icons to file', imageRelativePath)
            addIcons2image(imageSourcePath, imageRectanglePath, imageReleasePath, defs[0]['icons'], iconsDir)
        else:
            print('copy file', imageRelativePath)
            copyImage(imageSourcePath, imageReleasePath)


print('DONE addIcons.py')