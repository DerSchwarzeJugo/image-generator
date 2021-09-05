# Create Metadata based on the images (1 json file per image)
# usage python3 metadata.py

import json, datetime, concurrent.futures, urllib.parse
from os.path import isfile



def main():
	url = input("Provide the URL of the folder containing the images: ")
	providedPath = input("Provide the path to your ImageOutput file: ")
	while isfile(providedPath) is not True:
		print("Not a real file!")
		providedPath = input("Provide the path to your ImageOutput file: ")	
	
	loadedData = loadJson(providedPath)
	manipulatedData = manipulateData(loadedData, url)

	# implement some multiprocessing to speed up things
	with concurrent.futures.ProcessPoolExecutor() as executor:
		res = executor.map(createMetaDataFile, manipulatedData)
	
	# save all metadata files to one json as backup
	savedTo = saveJsonConfig(manipulatedData)
	exit("Overview File was saved to {}".format(savedTo))


# load a created config
def loadJson(path):
	with open(path, "r") as f:
		data = json.load(f)
	return data


def createMetaDataFile(data):
	path = "generatedMetadata/" + data["name"] + ".json"
	with open(path, "w") as f:
		json.dump(data, f, indent=4)


# save the created config as json
def saveJsonConfig(config):
	timestamp = datetime.datetime.now()
	date = timestamp.strftime("%Y-%m-%d")
	path = "generatedConfigs/metadataOverview - " + config[0]["name"] + " - " + date + ".json"
	with open(path, "w") as f:
		json.dump(config, f, indent=4)
	return path


# create correct structure for nft metadata
def manipulateData(data, url):
	result = []
	for item in data:
		obj = {
			"name": item["name"],
			"description": item["desc"],
			"image": "https://" + url + "/" + urllib.parse.quote(item["name"]) + ".png",
			"attributes": []
		}
		for key, val in item["usedImgs"].items():
			obj["attributes"].append({"trait_type": key, "value": val})
		result.append(obj)

	return result







# init the main function
if __name__ == "__main__":
	main()