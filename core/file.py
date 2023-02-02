from json import load, dump



def loadFromJSON (path:str) :
	with open(path, 'r', encoding='utf8') as file :
		return load(file)


def writeToJSON (path:str, content) :
	with open(path, 'w', encoding='utf8') as file :
		return dump(content, file, ensure_ascii=1, indent=4)