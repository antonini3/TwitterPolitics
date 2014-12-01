# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy, sys, codecs, os, csv, codecs, thread, threading
import time
import json, datetime
import tweetHandler
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import unicodedata, re
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
        self.jsonFile = codecs.open(os.getcwd() + '/database/' + fileName, 'ab', 'utf-8')
        self.fileName = fileName

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

        lock = threading.Lock()

        def read_existing_data():
            print "Reading past politicians..."
            f = open(os.getcwd() + '/database/' + self.fileName)
            data = {}
            counter = 0
            for line in f:
                try:
                    jline = json.loads(line)
                    data[jline.keys()[0]] = jline[jline.keys()[0]]
                except:
                    counter += 1
                    pass
            set_of_users = set(data.keys())

            print "Number wrong:", counter
            if len(set_of_users) > 0:
                print "Random user (sanity check):", random.sample(set_of_users, 1)
            print "Num users:", len(set_of_users)
            return set_of_users


        def multithreaded_grab(user_items):

            def grab_alpha(userID):
                grab_user_info(userID, self.twitterAuthAlpha)

            def grab_beta(userID):
                grab_user_info(userID, self.twitterAuthBeta)

            def grab_gamma(userID):
                grab_user_info(userID, self.twitterAuthGamma)
                
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

            first_marker = len(users) / 3
            second_marker = (len(users) * 2) / 3
            alphaUsers = dict(user_items[:first_marker])
            betaUsers = dict(user_items[first_marker:second_marker])
            gammaUsers = dict(user_items[second_marker:])

            a = threading.Thread(target=runAlpha, args=(alphaUsers,))
            b = threading.Thread(target=runBeta, args=(betaUsers,))
            g = threading.Thread(target=runGamma, args=(gammaUsers,))

            a.start()
            b.start()
            g.start()

            a.join()
            b.join()
            g.join()

        def singlethreaded_grab(user_items):
            for user in dict(user_items):
                grab_user_info(user, self.twitterAuthGamma)

        def grab_user_info(userID, twitterAuth):
            def grab_tweet_info():
                allTweets = []
                print "Starting collection of tweets for", userID
                new_tweets = twitterAuth.api.user_timeline(id=userID,count=200)
                for tweet in new_tweets:
                    cleanedTweet = tweetHandler.tweetToDict(tweet)
                    allTweets.append(cleanedTweet)

                oldest = new_tweets[-1].id - 1 if len(new_tweets) > 0 else 0

                while len(new_tweets) > 0:
                    print "We have added %d number of new tweets; total number of tweets is %d" % (len(new_tweets), len(allTweets))

                    new_tweets = twitterAuth.api.user_timeline(id=userID,count=200,max_id=oldest)
                    for tweet in new_tweets:
                        cleanedTweet = tweetHandler.tweetToDict(tweet)
                        allTweets.append(cleanedTweet)

                    if len(new_tweets) > 0:
                        oldest = new_tweets[-1].id - 1

                print "Ended collection of tweets for", userID

                return allTweets

            def grab_follower_info():
                print "Getting follower info from: ", userID                
                follower_id = []
                for page in tweepy.Cursor(twitterAuth.api.followers_ids, id=userID).pages():
                    follower_id.extend(page)
                print "Ending follower info from: ", userID 
                return follower_id

            def grab_following_info():
                print "Getting following info from: ", userID
                following_id = []
                for page in tweepy.Cursor(twitterAuth.api.friends_ids, id=userID).pages():
                    following_id.extend(page)
                print "Ending following info from: ", userID
                return following_id


            def grab_favorites_info():
                all_favs = []
                print "Starting collection of favorites for", userID
                new_favs = twitterAuth.api.favorites(id=userID,count=200)
                for tweet in new_favs:
                    cleanedTweet = tweetHandler.tweetToDict(tweet)
                    all_favs.append(cleanedTweet)

                
                oldest_fav = new_favs[-1].id - 1 if len(new_favs) > 0 else 0

                while len(new_favs) > 0:
                    print "We have added %d number of new favorites; total number of favorites is %d" % (len(new_favs), len(all_favs))

                    new_favs = twitterAuth.api.favorites(id=userID,count=200,max_id=oldest_fav)
                    for tweet in new_favs:
                        cleanedTweet = tweetHandler.tweetToDict(tweet)
                        all_favs.append(cleanedTweet)

                    if len(new_favs) > 0:
                        oldest_fav = new_favs[-1].id - 1
                
                print "Finished collection of favorites for", userID
                return all_favs

            try:
                if userID not in past_users:
                    users[userID]['tweets'] = grab_tweet_info()
                    users[userID]['followers'] = grab_follower_info()
                    users[userID]['following'] = grab_following_info()
                    users[userID]['favorites'] = grab_favorites_info()
                    lock.acquire()
                    temp = json.dumps({userID:users[userID]})
                    print >> self.jsonFile, temp
                    lock.release()
            except Exception as e:
                print e
                print ">> ERROR!"
                print "User: ", userID
                print "Shpiel: ", users[userID]

        past_users = read_existing_data()
        multithreaded_grab(users.items())
        # singlethreaded_grab(users.items())
