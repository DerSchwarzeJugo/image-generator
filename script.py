from PIL import Image
from os import walk, listdir, cpu_count 
from os.path import isfile
import random
import itertools
from multiprocessing import Process, Pool
import concurrent.futures


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
	global imageName
	imageName = input("How would you like to name your images? (Format will be NAME #ID) ")

	randomOrAll = input("Generate all possible images (0) or specific count of random nonduplicates (1)? ")		


	while int(randomOrAll) != 0 and int(randomOrAll) != 1:
		randomOrAll = input("Generate all possible images (0) or specific count of random nonduplicates (1)? ")		
	if int(randomOrAll) == 0:
		# create all possible combinations of the image
		createAllImgs(orderedImages, imageName, possibleImages)
		
		# * unpacks the result of range
		idList = [*range(possibleImages - 1)]
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
	id = 0
	# iterate as long as imagesArr has same amount as wished by user
	while len(imagesArr) < imageAmount:
		innerList = []	
		# iterate over all layers and add their path and id
		for layer in orderedImages:
			randomImg = random.sample(layer["images"], 1)
			innerList.append(randomImg[0]["path"])
			innerList.append(id)
		id = id + 1
		imagesArr.append(innerList)
	
	# implement some multiprocessing to speed up things
	with concurrent.futures.ProcessPoolExecutor() as executor:
		res = executor.map(layerAndSaveImg, imagesArr)

	# max(list(res)) --> gets highest of the values in the returned list
	exit("{} images were generated to folder generatedImgs".format(max(list(res)) + 1))



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
		id = createImgFromPath(imagesArr, imageName)	

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
# imgList equals a list of paths of the combined images
def layerAndSaveImg(imgList):
	global imageName
	# get last element which is id
	id = imgList[len(imgList) - 1]  
	imgName = imageName + " #" + str(id)
	bg = Image.open(imgList[0])
	for item in imgList:
		# filter out first and last element, corresponding to background and id
		if item != imgList[0] and item != id:
			openItem = Image.open(item)
			bg.paste(openItem, (0,0), openItem)
	bg.save("generatedImgs/" + imgName + ".png")
	print("Image {} generated".format(imgName))
	return id


# init the main function
if __name__ == "__main__":
	main()
