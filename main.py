# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import time, tweepy, sys, os, csv, codecs, json
from communicator import *

def grabUsers():
    fileName = 'users_' + time.strftime("%H:%M:%S") + '.json'
    userCommunicator = UserCommunicator(fileName)
    users = userCommunicator.get_users(max_users=50)
    userCommunicator.fill_users(users)


def grabPoliticians():
	json_data = open(os.getcwd() + '/database/' + 'handle_to_ideology.json')
	data = json.load(json_data)

	fileName = 'politicians_twitter.json'
	userCommunicator = UserCommunicator(fileName)
	userCommunicator.fill_users(data)

def sexy_beasts():
    users = {54123389 : {"handle" : "antonini3"}, 21001149 : {"handle" : "lbronner"}, 192229632 : {"handle" : "ccibils"}}
    userCommunicator = UserCommunicator("sexy_beasts.json")
    userCommunicator.fill_users(users)

if __name__ == "__main__":
	#grabPoliticians()
    grabUsers()