from matplotlib import pyplot as plt
from PIL import Image, ImageChops, ImageFilter
from os import walk, listdir
from os.path import isfile
import random
import itertools


# imageBg = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/Backgrounds/020.png"

def main():
	providedPath = input("Absolute path to your directory containing the images: ")

	# check if last character is a slash
	if providedPath[-1] != '/':
		providedPath = providedPath + "/"

	dirnames = createDirectoryStructure(providedPath)

	# create some basic variables
	layers = len(dirnames)
	images = createImgList(dirnames, providedPath)
	possibilities = len(images[0]["images"])

	# ** equals to the power (possibilities^layers)
	possibleImages = possibilities ** layers

	# give user some output
	print("Index:")
	print("layers: {} \npossibilities: {} \npossibleImages: {}\n".format(layers, possibilities, possibleImages ))

	layerOrdering = setupLayerOrdering(layers, dirnames)
	print("Layer list: {}\n".format(layerOrdering))

	orderedImages = orderArray(layerOrdering, images)

	# Ask for additional input which is needed
	imageName = input("How would you like to name your images? (Format will be NAME #ID) ")

	randomOrAll = input("Generate all possible images (0) or specific count of random nonduplicates (1)? ")		

	while int(randomOrAll) != 0 and int(randomOrAll) != 1:
		randomOrAll = input("Generate all possible images (0) or specific count of random nonduplicates (1)? ")		
	if int(randomOrAll) == 0:
		# create all possible combinations of the image
		createAllImgs(orderedImages, imageName, possibleImages)
	else:
		# create only a given amount of random images
		imageAmount = input("How many images would you like to generate? ")
		while int(imageAmount) > 0 and int(imageAmount) <= possibleImages:
			createRandomImgs(imageAmount, orderedImages, imageName)
			break
		else:
			print("You are either choosing more images than possible or an impossible number!")
			imageAmount = input("How many images would you like to generate? ")


# create a specific amount of random nonduplicate images
def createRandomImgs(imageAmount, orderedImages, imageName):
	imageAmount = int(imageAmount)
	imagesArr = []
	while len(imagesArr) < imageAmount:
		innerList = []	
		for layer in orderedImages:
			randomImg = random.sample(layer["images"], 1)
			innerList.append(randomImg[0]["path"])
		imagesArr.append(innerList)
	
	id = 0
	for image in imagesArr:
		innerName = imageName + " #" + "{}".format(id)
		layerAndSaveImg(image, innerName)
		id = id + 1
	exit("{} images were generated to folder generatedImgs".format(imageAmount))



# create all possible images
def createAllImgs(orderedImages, imageName, possibleImages):
	print("There are {} possible images. This might take a while".format(possibleImages))
	allLists = []
	for layer in orderedImages:	
		allLists.append(layer["images"])

	# get all possible combinations
	allCombinations = list(itertools.product(*allLists))
	id = 0
	if (len(allCombinations) == possibleImages):
		# create array of all links only
		imagesArr = []
		for image in allCombinations:
			innerList = []
			for innerImage in image:
				innerList.append(innerImage["path"])
			imagesArr.append(innerList)
		
		# shuffle array for non linear output
		random.shuffle(imagesArr)
		# iterate over array and create images
		for image in imagesArr:
			innerName = imageName + " #" + "{}".format(id)
			layerAndSaveImg(image, innerName)
			id = id + 1	

	else:
		print("Something went wrong!")
	exit("{} images were generated to folder generatedImgs".format(id + 1))

# create ordered array
def orderArray(layerOrdering, images):
	orderedArray = []
	for i in layerOrdering:
		orderedArray.append(images[i])
	return orderedArray


# define order of layering
def setupLayerOrdering(layers, dirnames):
	for key in range(layers):
		print("{}: {}".format(key, dirnames[key]))

	layerOrdering = []
	layerOrdering.append(int(input("You have {} layers. Which layer is the background? (ID): ".format(layers))))
	processedLayers = layers - 1

	while processedLayers > 0:
		layerOrdering.append(int(input("Which Layer is next? (ID): ")))
		processedLayers = processedLayers - 1
	return layerOrdering


# create list of directories and files of the provided path
def createDirectoryStructure(providedPath):
	f = []
	for (dirpath, dirnames, filenames) in walk(providedPath):
		f.extend(filenames)
		break
	return dirnames


# create subLists of the images in every directory
def createImgList(dirnames, providedPath):
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
def layerAndSaveImg(imgList, imgName):
	bg = Image.open(imgList[0])
	for item in imgList:
		if item != imgList[0]:
			openItem = Image.open(item)
			bg.paste(openItem, (0,0), openItem)
	bg.save("generatedImgs/" + imgName + ".png")
	print("Image {} generated".format(imgName))


# init the main function
if __name__ == "__main__":
	main()
