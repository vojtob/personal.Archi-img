import cv2
import numpy as np

def addPointToSegments(lineSegments, keyCoordinate, lenCoordinate, reallySmallGap, minSegmentLength):
    """ add a point to segments """
    if(lineSegments.get(keyCoordinate)):
        # there is a segment with key coordinate equal to keyCoordinate
        segments = lineSegments[keyCoordinate]
        # the last segment
        s = segments.pop()
        # check how close is the point to the last segment
        if( (lenCoordinate-s[1]) <= reallySmallGap ):
            # the point is too close to the last segment, we prolong this segment (poped element replaced with longer)
            segments.append((s[0],lenCoordinate))
        else:
            # the point is too far from previous segment
            # check, if the previous segment is long enough
            if( (s[1]-s[0]) > minSegmentLength ):
                # last segment is long enough, we should return it back to list (removed by pop)
                segments.append(s)
            # we should create a new segment, only one point long
            segments.append((lenCoordinate,lenCoordinate))
    else:
         # the very first segment for this key coordinate, create list of segments and a new segment       
         segments = []
         segments.append((lenCoordinate,lenCoordinate))
         lineSegments[keyCoordinate] = segments

def removeShortSegments(lineSegments, minSegmentLength):
    emptyList = []
    for keyCoordinate, segments in lineSegments.items():
        s = segments[-1]
        if( (s[1]-s[0]) < minSegmentLength ):
            segments.pop()
        if(len(segments) < 1):
            emptyList.append(keyCoordinate)
    for keyCoordinate in emptyList:
        lineSegments.pop(keyCoordinate)

def findLineSegments(img, reallySmallGap, minSegmentLength):
    """find line segments with minimal length"""

    # line segments are indexed by x or y coordinate and
    # for a particular x contain list of line segment
    # x : (y1,y2), (y3,y4)  - it means segments (x,y1, x,y2) and (x,y3, x,y4)
    lineSegmentsHorizontal = {}
    lineSegmentsVertical = {}

    # in this run we identify all line segments (even with length 1)
    # short segments could be only the last in list
    # opencv coordinate system is (row,col), therefore swith x-y
    maxY, maxX = img.shape[:2]
    for x in range(maxX):
        for y in range(maxY):
            # opencv coordinate system is (row,col), therefore swith x-y
            if(img[y,x]):
                # here is a point that should be added to segments
                addPointToSegments(lineSegmentsHorizontal, y, x, reallySmallGap, minSegmentLength)
                addPointToSegments(lineSegmentsVertical, x, y, reallySmallGap, minSegmentLength)

    # check segments for length
    removeShortSegments(lineSegmentsHorizontal, minSegmentLength)
    removeShortSegments(lineSegmentsVertical, minSegmentLength)

    return lineSegmentsHorizontal, lineSegmentsVertical

def findVerticalEdge(startX, startY, cornerGap, lineSegmentsVertical):
    xKeys = lineSegmentsVertical.keys()
    for x in sorted(xKeys):
        if(x < (startX-cornerGap)):
            # too small x
            continue
        if(x > (startX+cornerGap)):
            # too big
            return None
        # this x is in interval
        verticalEgdeCandidates = lineSegmentsVertical[x]
        for edge in verticalEgdeCandidates:
            if(edge[0] < (startY-cornerGap)):
                # too high
                continue
            if(edge[0] > (startY+cornerGap)):
                # too low
                # return None
                break
            return edge

def findBottomEdge(startX, endX, startY, cornerGap, lineSegmentsHorizontal):
    yKeys = lineSegmentsHorizontal.keys()
    for y in sorted(yKeys):
        if(y < (startY-cornerGap)):
            # too small
            continue
        if(y > (startY+cornerGap)):
            # too big
            return None
        # this y is in interval, find by left and right ends
        horizontalEgdeCandidates = lineSegmentsHorizontal[y]
        for edge in horizontalEgdeCandidates:
            if(edge[0] < (startX-cornerGap)):
                # too high
                continue
            if(edge[0] > (startX+cornerGap)):
                # too low
                # return None
                break
            # left corner OK, check right corner
            if(edge[1] < (endX-cornerGap)):
                # too small
                # return None
                break
            if(edge[1] > (endX+cornerGap)):
                # too big
                # return None
                break
            return edge

def findRectangles(lineSegmentsHorizontal, lineSegmentsVertical, cornerGap):
    rectangles = []

    # iterate over horizontal segments a consider them as horizontal top line of rectangle
    for y in sorted(lineSegmentsHorizontal.keys()):
        topSegments = lineSegmentsHorizontal[y]
    # for y, topSegments in lineSegmentsHorizontal.items():
        # start with TOP edge
        for topEdge in topSegments:
            leftEdge = findVerticalEdge(topEdge[0], y, cornerGap, lineSegmentsVertical)
            if(not leftEdge):
                # left edge not found
                continue
            rightEdge = findVerticalEdge(topEdge[1], y, cornerGap, lineSegmentsVertical)
            if(not rightEdge):
                # right edge not found
                continue
            # try to find bottom edge
            bottomEdge = findBottomEdge(topEdge[0], topEdge[1], (leftEdge[1]+rightEdge[1])//2, cornerGap, lineSegmentsHorizontal)
            if(not bottomEdge):
                continue
            # we found a rectangle
            rectangles.append( ( (topEdge[0],leftEdge[0]), (bottomEdge[1],rightEdge[1]) )  ) 

    return rectangles