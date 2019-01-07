import cv2
import numpy as np
import os
import posixpath

def createRedImage(color_image, dir_name):
    height, width, ch = color_image.shape
    redCol = np.zeros((height, width), np.uint8)

    for i in range(height):
        for j in range(width):
            redCol[i][j] = color_image[i][j][2]

    cv2.imwrite(dir_name + "/red.jpg", redCol)
    return redCol

def redContour(redCol, color_image, dir_name):
    retRed, threshRed = cv2.threshold(redCol, 127, 255, 0)
    im2Red, contoursRed, hierarchyRed = cv2.findContours(threshRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    outputImageLst = []

    for idx, contour in enumerate(contoursRed):
        (x,y,w,h) = cv2.boundingRect(contour)

        if ((w/h >= 1.01 and w/h <= 1.74) or (h/w >= 1.01 and h/w <= 1.74)) and (w > 300 and h > 300) and (w < 2100 and h < 1500):
            print(len(hierarchyRed[0][idx]), " >>> ",idx, " >>> ",(x,y,w,h))

            colr = color_image[y:y+h, x:x+w]

            hsvImg = cv2.cvtColor(colr, cv2.COLOR_BGR2HSV)
            cv2.imwrite(dir_name + "/hsv-" + str(idx) + '.jpg', hsvImg)
        
            # 95,99,198
            # 102,107,211
            # 114,117,226
            # 85,69,219
            # 189,155,239

            # Red Color Combination for lower and Higher Limit
            lower = np.array([81, 65, 182], dtype = "uint8")
            upper = np.array([190, 160, 240], dtype = "uint8")
        
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(colr, lower, upper)
            output = cv2.bitwise_and(colr, colr, mask = mask)
            # mask = mask.astype('bool')
            # output = colr * np.dstack((mask, mask, mask))
            print(output.shape)
            cv2.imwrite(dir_name + "/colr-" + str(idx) + '.jpg', colr)
            cv2.imwrite(dir_name + "/mask-" + str(idx) + '.jpg', output)

            grayImg = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(dir_name + "/gray-" + str(idx) + '.jpg', grayImg)

            retG, threshG = cv2.threshold(grayImg, 127, 255, 0)
            cv2.imwrite(dir_name + "/thresh-" + str(idx) + '.jpg', threshG)

            # width = np.mean(threshG, axis=0)
            # height = np.mean(threshG, axis=1)

            width = np.mean(grayImg, axis=0)
            height = np.mean(grayImg, axis=1)

            xmin,xmax,ymin,ymax = 0, 0, 0, 0

            for i in range(len(width)):
                if(width[i] > 0.0):
                    xmin = i
                    break

            for i in range(len(width)-1,0, -1):
                if(width[i] > 0.0):
                    xmax = i
                    break
            
            for i in range(len(height)):
                if(height[i] > 0.0):
                    ymin = i
                    break

            for i in range(len(height)-1,0, -1):
                if(height[i] > 0.0):
                    ymax = i
                    break

            print((xmin, ymin), " >>>> ", (xmax, ymax))
            cv2.rectangle(color_image, (x,y), (x+w,y+h), (0, 255, 255), 3)
            
            if (xmax != 0 or ymax != 0) and (w > h):
                # cv2.rectangle(color_image, (x,y), (x+w,y+h), (0, 255, 255), 3)

                centerx = int(x+(xmin + xmax)/2)
                centery = int(y+(ymin + ymax)/2)
                axis_major = int(ymax / 2)
                axis_minor = int(xmax / 3)
                print("Center >>>> ",(centerx, centery), " >>>> ",(axis_major, axis_minor))

                cv2.ellipse(color_image,(centerx, centery),(axis_major, axis_minor),0,0,360,(0, 0, 255),3)
                print("\n\n")

            elif (xmax != 0 or ymax != 0) and (w < h):
                # cv2.rectangle(color_image, (x,y), (x+w,y+h), (0, 255, 255), 3)

                centerx = int(x+(xmin + xmax)/2)
                centery = int(y+(ymin + ymax)/2)
                axis_major = int(ymax / 3)
                axis_minor = int(xmax / 2)
                print("Center >>>> ",(centerx, centery), " >>>> ",(axis_major, axis_minor))

                cv2.ellipse(color_image,(centerx, centery),(axis_major, axis_minor),0,0,360,(0, 0, 255),3)
                print("\n\n")

    cv2.imwrite(dir_name + "/output.jpg", color_image)
    return color_image


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def createFile(path_file, sourceDir):
    filename, ext = os.path.splitext(os.path.basename(path_file))

    # dirname = os.path.dirname(path_file)

    # dest_dirname = os.path.join(dirname, filename)
    if(ext == '.jpg' or ext == '.JPG'):
        # dest_dirname = posixpath.join("/home/hardik/interview/group_k_genetics/test/data", filename)
        dest_dirname = posixpath.join(sourceDir, filename)

        if not os.path.exists(dest_dirname):
            os.mkdir(dest_dirname)

        color_image = cv2.imread(path_file, 1)

        if color_image is not None:

            hei, wid, ch = color_image.shape

            # if hei > wid:
            #     # rotated = imutils.rotate_bound(color_image, 90)
            #     rotated = rotateImage(color_image, 90)
            #     color_image = rotated


            print(dest_dirname, " >>>> ", filename, " >>>>>> ", color_image.shape)
            cv2.imwrite(dest_dirname + "/original.jpg", color_image)

            red_image = createRedImage(color_image, dest_dirname)

            output_image = redContour(red_image, color_image, dest_dirname)
            return output_image
        
        else:
            return "Image is not readable"
    else:
        return "No jpg file exist"

# createFile("/home/hardik/interview/group_k_genetics/test/Lights on in lab/D3 Lights on, in lab/IMG_0367.JPG")


def readFile(path_dirname):
    list_file = os.listdir(path_dirname)
    print(list_file)
    for i in list_file:
        single_source = posixpath.join(path_dirname, i)

        test = createFile(single_source, "/home/hardik/interview/group_k_genetics/test/Hallway-data")        

# readFile("/home/hardik/interview/group_k_genetics/test/Lights off in lab/D2 no light, in lab")


def readRecurrentFolder(parentDirname):
    listDir = os.listdir(parentDirname)
    print(listDir)
    for i in listDir:
        single_source = posixpath.join(parentDirname, i)

        readFile(single_source)

# readRecurrentFolder("/home/hardik/interview/group_k_genetics/test/Hallway")

