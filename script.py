from matplotlib import pyplot as plt
from PIL import Image, ImageChops, ImageFilter
from os import walk, listdir
from os.path import isfile


# imageBg = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/Backgrounds/020.png"
# imageHa = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/HandAcc/016.png"
# imageMa = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/MouthAcc/012.png"
# imageBo = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/Body/008.png"

# bg = Image.open(imageBg)
# ha = Image.open(imageHa)
# ma = Image.open(imageMa)
# bo = Image.open(imageBo)

# bg.paste(ha, (0,0), ha)
# bg.paste(ma, (0,0), ma)
# bg.paste(bo, (0,0), bo)
# bg.save("bg.png")

def createDirectoryStructure(providedPath):
	# create list of directories and files of the provided path
	f = []
	for (dirpath, dirnames, filenames) in walk(providedPath):
		f.extend(filenames)
		break
	return dirnames

# create subLists of the images in every directory
def createImgList(dirnames):
	images = []
	for directory in dirnames:
		tempDict = {
			"name": directory,
			"path": providedPath + directory,
		}
		tempList = [] 
		for image in listdir(tempDict["path"]):
			if (isfile(tempDict["path"] + "/" + image)):
				innerTempDict = {
					"name": image,
					"path": tempDict["path"] + "/" + image,
				}
				tempList.append(innerTempDict)
		tempDict["images"] = tempList
		images.append(tempDict)
	return images

# adds all the layers together in correct order and saves the image
def layerImg(imgList):
	bg = imgList[0]
	for item in imgList:
		if item != imgList[0]:
			bg.paste(item, (0,0), item)
	bg.save("bg.png")

# Program Starts here

providedPath = input("Provide the absolute path to your directory containing the images: ")

# check if last character is a slash
if providedPath[-1] != '/':
	providedPath = providedPath + "/"

dirnames = createDirectoryStructure(providedPath)

layers = len(dirnames)
images = createImgList(dirnames)
possibilities = len(images[0]["images"])
# ** equals to the power (possibilities^layers)
possibleImages = possibilities ** layers

print("layers: {} \npossibilities: {} \npossibleImages: {}".format(layers, possibilities, possibleImages ))



