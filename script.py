# Image Generator
# usage: python3 script.py, python3 script.py /path-to-config
from PIL import Image
from os import walk, listdir
from os.path import isfile
import random, itertools, concurrent.futures, json, sys, time, datetime


def main():
	# Check for a provided config backup
	configLoaded = False
	if len(sys.argv) > 1:
		loadConfigPath = str(sys.argv[1])
		if (isfile(loadConfigPath)):
			loadConfig = loadJsonConfig(loadConfigPath)
			configLoaded = True
			print("Config loaded successfully!\n")
		else:
			exit("{} is not a file!".format(loadConfigPath))

	# only do this actions if no configuration is provided
	if configLoaded == False:
		providedPath = input("Absolute path to your directory containing the images: ")

		# check if last character is a slash
		if providedPath[-1] != '/':
			providedPath = providedPath + "/"
	else:
		providedPath = loadConfig["path"]

	dirnames = createDirectoryStructure(providedPath)

	# create some basic variables
	layers = len(dirnames)
	images = createImgList(dirnames, providedPath)
	# ** equals to the power (possibilities^layers)
	# possibleImages = possibilities ** layers
	# if not every layer has same amount the calc does not work
	# instead we are multiplicating all the imageamounts
	possibleImages = 1
	for cat in images:
		possibleImages = possibleImages * len(cat["images"])	


	# give user some output
	print("Index:\nlayers: {} \npossibleImages: {}\n".format(layers, possibleImages ))

	# only do this actions if no configuration is provided or changes in layerinng or the images were made
	if configLoaded == False or len(loadConfig["layerOrdering"]) != layers or loadConfig["possibleImages"] != possibleImages:
		layerOrdering = setupLayerOrdering(layers, dirnames)
		orderedImages = orderArray(layerOrdering, images)
		weightedList = createWeightedList(orderedImages)
	else:
		reOrder = input("Would you like to reorder your layers? (y/N) ")
		if reOrder.lower() == "y" or reOrder.lower() == "yes":
			layerOrdering = setupLayerOrdering(layers, dirnames)
		else:
			layerOrdering = loadConfig["layerOrdering"]

		orderedImages = orderArray(layerOrdering, images)
		reWeight = input("Would you like to change the weights on your images? (y/N) ")
		if reWeight.lower() == "y" or reWeight.lower() == "yes":
			weightedList = createWeightedList(orderedImages)
		else:
			weightedList = loadConfig["weightedList"]

	print("Layer order: {}\n".format(layerOrdering))
	for cat in weightedList:
		# iterate over to create total weighting
		sumOfWeights = 0
		for el, val in cat.items():
			if el != "name" and el != "imageCount":
				sumOfWeights += int(val)
		# iterate again to print
		print("Category: {}\nImageCount: {}".format(cat["name"], cat["imageCount"]))	
		print("---")
		for el,val in cat.items():
			if el != "name" and el != "imageCount":
				# get name from path
				imgName = el.split("/")[-1]
				percentage = round(int(val)/int(sumOfWeights) * 100, 2)
				print("ImageName: {}\nWeight: {}\nPercent: {}%".format(imgName, int(val), percentage))
				print("---")
		print("--------------------------------")


	global imageName
	global imageDesc
	global baseUrl
	# only do this actions if no configuration is provided
	if configLoaded == False:
		# Ask for additional input which is needed
		imageName = input("How would you like to name your images? (Format will be NAME #ID) ")
		# Ask for other Meta Data aswell here
		imageDesc = input("Give your images a description: ")
		baseUrl = input("Provide a base URL for your images: ")
	else:
		imageName = loadConfig["name"]
		imageDesc = loadConfig["desc"]
		baseUrl = loadConfig["url"]


	# Ask for config backup
	saveConfig = input("Would you like to save this config? (Y/n) ")

	if saveConfig.lower() == "y" or saveConfig.lower() == "yes" or saveConfig.lower() == "":
		saveJsonConfig({
			"name": imageName,
			"desc": imageDesc,
			"url": baseUrl,
			"path": providedPath,
			"possibleImages": possibleImages,
			"layerOrdering": layerOrdering,
			"weightedList": weightedList,
		})

	print("--- 0 --- Generate All possible images")
	print("--- 1 --- Generate specific amount of random non-duplicates")
	print("--- 2 --- Generate specific amount of random non-duplicates based on a weighted list")
	randomOrAll = input("Which option would you like to choose? ")		

	# setup var for time measurement
	global start_time

	while int(randomOrAll) < 0 and int(randomOrAll) > 2:
		randomOrAll = input("Which option would you like to choose? ")		
	if int(randomOrAll) == 0:
		# start timer
		start_time = time.time()
		# create all possible combinations of the image
		createAllImgs(orderedImages, possibleImages)
		
	if int(randomOrAll) == 1:
		# create only a given amount of random images
		imageAmount = input("How many images would you like to generate? ")
		while int(imageAmount) > 0 and int(imageAmount) <= possibleImages:
			# start timer
			start_time = time.time()
			createRandomImgs(imageAmount, orderedImages)
			break
		else:
			print("You are either choosing more images than possible or an impossible number!")
			imageAmount = input("How many images would you like to generate? ")

	if int(randomOrAll) == 2:
		# create images based on a weighted list
		imageAmount = input("How many images would you like to generate? ")
		while int(imageAmount) > 0 and int(imageAmount) <= possibleImages:
			# start timer
			start_time = time.time()
			createRandomImgs(imageAmount, orderedImages, weightedList)
			break
		else:
			print("You are either choosing more images than possible or an impossible number!")
			imageAmount = input("How many images would you like to generate? ")

	end_time = time.time()
	print("Total executiontime: --- {}s ---".format(round(end_time - start_time), 2))


# functions


# create a specific amount of random nonduplicate images
def createRandomImgs(imageAmount, orderedImages, weightedList = False):
	imageAmount = int(imageAmount)
	imagesArr = []
	# iterate as long until imagesArr has same amount as wished by user
	while len(imagesArr) < imageAmount:
		innerList = []	
		# iterate over all layers and add their path
		for i in range(len(orderedImages)):
			if weightedList == False:
				randomImg = random.choice(orderedImages[i]["images"])
			else:
				orderedWeights = [] 
				for key, val in weightedList[i].items():
					if key != "name" and key != "imageCount":
						orderedWeights.append(int(val))
				orderedWeights = tuple(orderedWeights)
				randomImg = random.choices(orderedImages[i]["images"], weights = orderedWeights, k = 1)[0]
			innerList.append(randomImg["path"])
		# innerList.append(id)
		# id = id + 1
		imagesArr.append(innerList)
		# make the array unique, no duplicates
		imagesArr = [list(x) for x in set(tuple(x) for x in imagesArr)]


	# add id to every generated image
	id = 0
	for el in imagesArr:
		el.append(id)
		id = id + 1

	saveImgSetupJson(imagesArr)

	# implement some multiprocessing to speed up things
	with concurrent.futures.ProcessPoolExecutor() as executor:
		res = executor.map(layerAndSaveImg, imagesArr)

	# max(list(res)) --> gets highest of the values in the returned list
	print("{} images were generated to folder generatedImgs".format(max(list(res)) + 1))

# save generated imgArr to json output
def saveImgSetupJson(imgArr):
	global imageName
	global imageDesc
	# make order in arr
	generatedList = []
	for image in imgArr:
		id = image[len(image) - 1]
		innerDict = {
			"name": imageName + " #" + str(id),
			"imgId": id,
			"desc": imageDesc
		}
		setupDict = {}
		for innerImage in image:
			if isinstance(innerImage, str):
				# add category as key, and name as value for indexing
				setupDict[innerImage.split("/")[-2]] = innerImage.split("/")[-1].split(".")[0]

		innerDict["usedImgs"] = setupDict
		generatedList.append(innerDict)

	# save to json
	timestamp = datetime.datetime.now()
	date = timestamp.strftime("%Y-%m-%d")
	path = "generatedConfigs/" + imageName + " - " + date + ".json"
	with open(path, "w") as f:
		json.dump(generatedList, f, indent=4)


# create all possible images
def createAllImgs(orderedImages, possibleImages):
	print("There are {} possible images. This might take a while".format(possibleImages))
	allLists = []
	for layer in orderedImages:	
		allLists.append(layer["images"])

	# get all possible combinations
	allCombinations = list(itertools.product(*allLists))
	# shuffle array for non linear output
	random.shuffle(allCombinations)
	if (len(allCombinations) == possibleImages):
		# create array of all links only
		imagesArr = []
		id = 0
		for image in allCombinations:
			innerList = []
			for innerImage in image:
				innerList.append(innerImage["path"])
			innerList.append(id)
			id = id + 1
			imagesArr.append(innerList)
		
		saveImgSetupJson(imagesArr)

		# implement some multiprocessing to speed up things
		with concurrent.futures.ProcessPoolExecutor() as executor:
			res = executor.map(layerAndSaveImg, imagesArr)	

	else:
		print("Something went wrong!")
	print("{} images were generated to folder generatedImgs".format(max(list(res)) + 1))

# create a weighted list for the choosing of the images
def createWeightedList(images):
	# iterate over categories, show user the images and ask for a weight
	print("Create weights for your images. You will need to pass one weight per image separately (element_weight / sum of all weights = percentage).")
	weightList = [] 
	for cat in images:
		print("Category: {}".format(cat["name"]))
		print("Images: {}".format(len(cat["images"])))
		tempDict = {}
		tempDict["name"] = cat["name"]
		tempDict["imageCount"] = len(cat["images"])
		for image in cat["images"]:
			print(image["path"])
			tempDict[image["path"]] = input("Give this image a weight: ")
		weightList.append(tempDict)
	return weightList


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


# save the created config as json
def saveJsonConfig(config):
	path = "generatedConfigs/" + config["name"] + ".json"
	with open(path, "w") as f:
		json.dump(config, f, indent=4)


# load a created config
def loadJsonConfig(path):
	with open(path, "r") as f:
		data = json.load(f)
	return data


# init the main function
if __name__ == "__main__":
	main()
