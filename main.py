# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import time, tweepy, sys, codecs, os, csv, codecs
from communicator import *
# from tokenizer.py import Tokenizer

if __name__ == "__main__":
    fileName = 'users_' + time.strftime("%H:%M:%S") + '.json'
    userCommunicator = UserCommunicator(fileName)
    users = userCommunicator.get_users(max_users=100)
    userCommunicator.fill_users(users)
