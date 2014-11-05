# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy, sys, codecs, os, csv, codecs
from communicator import *
# from tokenizer.py import Tokenizer

if __name__ == "__main__":
    #fileName = 'sample.csv'
    fileName = 'users.json'
    # TweetStreamingCommunicator(Terms = ["the"], Locations = None, Filename = fileName)
    # TweetCommunicator()
    userCommunicator = UserCommunicator(fileName)
    users = userCommunicator.get_users(max_users=10000)
    userCommunicator.fill_users(users)