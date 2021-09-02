# Create Statistics of created Images
# usage: python3 statistics.py
import json, datetime
from os.path import isfile



def main():
	providedPath = input("Provide the path to your ImageOutput file: ")	
	while isfile(providedPath) is not True:
		print("Not a real file!")
		providedPath = input("Provide the path to your ImageOutput file: ")	
	
	loadedData = loadJsonConfig(providedPath)
	parsedData = parseData(loadedData)
	res = saveJsonConfig(parsedData)
	exit("File {} was successfully created".format(res))
	

def parseData(data):
	dict = {}
	totalImgs = len(data)
	dict["TotalImages"] = totalImgs
	dict["name"] = data[0]["name"].split(" #")[0]
	for key in data[0]["usedImgs"]:
		dict[key] = {}

	for obj in data:
		for key, val in obj["usedImgs"].items():
			if val not in dict[key]:
				dict[key][val] = {} 
				dict[key][val]["absoluteCount"] = 1 
				dict[key][val]["totalPercentage"] = str(round(dict[key][val]["absoluteCount"] / totalImgs * 100, 2)) + "%"
			else:
				dict[key][val]["absoluteCount"] = dict[key][val]["absoluteCount"] + 1
				dict[key][val]["totalPercentage"] = str(round(dict[key][val]["absoluteCount"] / totalImgs * 100, 2)) + "%"
	return dict


# save the created config as json
def saveJsonConfig(config):
	timestamp = datetime.datetime.now()
	date = timestamp.strftime("%Y-%m-%d")
	path = "statistics/" + config["name"] + " - " + date + ".json"
	with open(path, "w") as f:
		json.dump(config, f, indent=4)
	return path


# load a created config
def loadJsonConfig(path):
	with open(path, "r") as f:
		data = json.load(f)
	return data




# init the main function
if __name__ == "__main__":
	main()