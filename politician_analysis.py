import csv, json, codecs
import sys, os, unicodedata

def getIdeology():

	''' ID TO IDEOLOGY '''
	idIdeologyMap = {}
	with open(os.getcwd() + '/database/' + 'sponsorshipanalysis.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if len(row) > 0 and row[0] != 'ID':
				govtrack_id = row[0]
				ideology = row[1] # 0 -> far left, 1 -> far right
				idIdeologyMap[govtrack_id] = ideology

	''' TWITTER HANDLE TO IDEOLOGY '''
	twitterIdeologyMap = {}
	with open(os.getcwd() + '/database/' + 'legislators-current.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		count = 0
		for row in reader:
			if len(row) > 23 and row[0] != 'last_name':
				govtrack_id = row[22]
				if govtrack_id in idIdeologyMap:
					ideologyDict = {}
					ideology = idIdeologyMap[govtrack_id]
					ideologyDict['ideology'] = ideology
					twitterHandle = row[12]
					if twitterHandle != '':
						twitterIdeologyMap[twitterHandle] = ideologyDict

	''' JSON FILE '''
	jsonFile = codecs.open(os.getcwd() + '/database/' + 'handle_to_ideology.json', 'wb')
	print >> jsonFile, json.dumps(twitterIdeologyMap)
				


if __name__ == "__main__":
	getIdeology()