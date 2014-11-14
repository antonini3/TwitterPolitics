# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy, sys, codecs, os, csv, codecs, thread, threading
import time
import json, datetime
import tweetHandler
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import unicodedata

import random

'''

CLASS: Authenticator
-------------------
Authenticates a given session for Twitter. Logs into "antonini3" :)

'''
class Authenticator:
    def __init__(self, person_char = 'a'):
        self.person = person_char
        if person_char == 'A' or person_char == 'a':
            consumer_key = '7qQNsEsbdrzkJf8Zx5z4DM76n'
            consumer_secret = 'CO5uOCVXRqsOAQRaSzF3JIvmy85zU4PNMolB1XYBCuUxdgA6bZ'
            access_token = '54123389-qgXroCM5FxVBkMTJGXXKOSQo8nMxGXFQdXB1tIfEl'
            access_token_secret = 'mVVF07bNaQqxzic9qHbCksmpNX0zwGH9mz3StwQ386n3J'
        elif person_char == 'L' or person_char == 'l':
            consumer_key = 'pLrNhYtZ1fejZp6ieXBESWdL3'
            consumer_secret = 'nM3VY8IPdhezYwYXFH7u2EcWFVCwg4a3U0PXlsp0GUF2pn94mH'
            access_token = '21001149-wyjVaXQFOdvbbK8ok70X9wu5zinilSnRojaoFtBI9'
            access_token_secret = 'LyxbkfaxKIuU8K1TfrPWF8BvOSoeRzUr1aUIs0n1fjQkH'    
        elif person_char == 'C' or person_char == 'c':
            consumer_key = 'FN2skjivUJaJc78nst5pK30ou'
            consumer_secret = '4AYR4SOJYJ6e1Z1sI7mX1GJ88XgHUHoJXkE2tQh52z5jLrlGIa'
            access_token = '192229632-dEBH8e8RzqmihGDqGV1X1GnzQTNWEIMcKeo1PLJM'
            access_token_secret = '3GJqnJF5ByzgiabsgF3CVufqj0NuEsCRWcIb5eDM3GbOu'
        else:
            print 'Not a valid individual! Try again with \'l\' or \'a\'.' 
            return       

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        # API is main communicator with twitter
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

class UserCommunicator:
    def __init__(self, fileName):
        self.twitterAuthAlpha = Authenticator('a')
        self.twitterAuthBeta = Authenticator('l')
        self.twitterAuthGamma = Authenticator('c')
        self.jsonFile = codecs.open(os.getcwd() + '/database/' + fileName, 'wb', 'utf-8')

    def get_users(self, query = '\s', language = "en", max_users = 100, locations = None):
        twitterAuth = self.twitterAuthAlpha
        users = set()
        num_total_tweets = 0
        last_id = -1
        userDict = {}
        while len(users) < max_users:
            count = sys.maxint - num_total_tweets
            try:
                if query == None:
                    if locations == None:
                        new_tweets = twitterAuth.api.search(count=count, lang=language, max_id=str(last_id - 1), show_user=True)
                    else:
                        new_tweets = twitterAuth.api.search(count=count, lang=language, max_id=str(last_id - 1), geocode = locations, show_user=True)
                else:
                    if locations == None:
                        new_tweets = twitterAuth.api.search(q=query, lang=language, count=count, max_id=str(last_id - 1), show_user=True)
                    else:
                        new_tweets = twitterAuth.api.search(q=query, lang=language, count=count, max_id=str(last_id - 1), geocode = locations, show_user=True)
                if not new_tweets:
                    break
                num_total_tweets += len(new_tweets)
                last_id = new_tweets[-1].id

                for tweet in new_tweets:
                    author = tweet.author
                    user = author.screen_name
                    userID = author.id
                    if (userID, user) not in users:
                        userInfo = {}
                        userInfo['handle'] = user
                        userDict[userID] = userInfo

                    users.add((userID, user))


            except tweepy.TweepError, e:
                print "ERROR:", e
                break

        return userDict

    def fill_users(self, users):

        def grab_alpha(userID):
            grab_user_info(userID, self.twitterAuthAlpha)

        def grab_beta(userID):
            grab_user_info(userID, self.twitterAuthBeta)

        def grab_gamma(userID):
            grab_user_info(userID, self.twitterAuthGamma)

        def grab_user_info(userID, twitterAuth):
            allTweets = []


            print "Starting collection of tweets for", userID
            new_tweets = twitterAuth.api.user_timeline(id=userID,count=200)
            for tweet in new_tweets:
                cleanedTweet = tweetHandler.tweetToDict(tweet)
                allTweets.append(cleanedTweet)

            oldest = new_tweets[-1].id - 1

            counter = len(allTweets)

            while len(new_tweets) > 0:
                print "We have added %d number of new tweets; total number of tweets is %d" % (len(new_tweets), len(allTweets))

                new_tweets = twitterAuth.api.user_timeline(id=userID,count=200,max_id=oldest)
                for tweet in new_tweets:
                    cleanedTweet = tweetHandler.tweetToDict(tweet)
                    allTweets.append(cleanedTweet)

                if len(new_tweets) > 0:
                    oldest = new_tweets[-1].id - 1

            print "Ended collection of tweets for", userID

            users[userID]['tweets'] = allTweets

            #users[userID]['followers'] = twitterAuth.api.followers_ids(id=userID)

            #users[userID]['following'] = twitterAuth.api.friends_ids(id=userID)


            #favorites = []
            #favs = twitterAuth.api.favorites(id=userID)
            #for tweet in favs:
                #cleanedTweet = tweetHandler.tweetToDict(tweet)
                #favorites.append(cleanedTweet)
            #users[userID]['favorites'] = favorites

            print >> self.jsonFile, json.dumps({userID:users[userID]})

        user_items = users.items()
        first_marker = len(users) / 3
        second_marker = (len(users) * 2) / 3
        alphaUsers = dict(user_items[:first_marker])
        betaUsers = dict(user_items[first_marker:second_marker])
        gammaUsers = dict(user_items[second_marker:])

        def runAlpha(users):
            alphaPool = ThreadPool(3)
            alphaResults = alphaPool.map(grab_alpha, alphaUsers)
            alphaPool.join()

        def runBeta(users):
            betaPool = ThreadPool(3)
            betaResults = betaPool.map(grab_beta, betaUsers)
            betaPool.join()
            

        def runGamma(users):
            gammaPool = ThreadPool(3)
            gammaResults = gammaPool.map(grab_gamma, gammaUsers)
            gammaPool.join()

        a = threading.Thread(target=runAlpha, args=(alphaUsers,))
        b = threading.Thread(target=runBeta, args=(betaUsers,))
        g = threading.Thread(target=runGamma, args=(gammaUsers,))

        a.start()
        b.start()
        g.start()

        a.join()
        b.join()
        g.join()
