# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy, sys, codecs, os, csv, codecs
import time
import json, datetime
import tweetHandler

'''

CLASS: Authenticator
-------------------
Authenticates a given session for Twitter. Logs into "antonini3" :)

'''
class Authenticator:
    def __init__(self):

        ''' OATH AUTHENTIFICATON | DON'T CHANGE THESE '''
        consumer_key = '7qQNsEsbdrzkJf8Zx5z4DM76n'
        consumer_secret = 'CO5uOCVXRqsOAQRaSzF3JIvmy85zU4PNMolB1XYBCuUxdgA6bZ'
        access_token = '54123389-qgXroCM5FxVBkMTJGXXKOSQo8nMxGXFQdXB1tIfEl'
        access_token_secret = 'mVVF07bNaQqxzic9qHbCksmpNX0zwGH9mz3StwQ386n3J'

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        # API is main communicator with twitter
        self.api = tweepy.API(self.auth)

'''

CLASS: TweetPoliticalStreamListener
-------------------
Instance of tweepy's StreamListener which writes to file and prints out useful information.

'''
class TweetPoliticalStreamListener(tweepy.StreamListener):

    def setup(self, fileName, Terms):
        self.csvFile = codecs.open(os.getcwd() + '/database/' + fileName, 'wb', 'utf-8')
        self.terms = Terms

    def on_status(self, status):
        if self.terms == None or any(term in status.text for term in self.terms):
            try:
                print "Tweet found and being processed."
                tweet = self.safe_unicode(status.text)
                tweet = tweet.replace('\n', '\\n')
                user = self.safe_unicode(status.author.screen_name)
                userID = status.author.id
                time = status.created_at
                source = status.source
                retweet_count = status.retweet_count
                print >> self.csvFile, "%s,%s,%s,|%s|,%s,%d" % (userID, user, time, tweet, source, retweet_count)

            except Exception, e:
                print >> sys.stderr, 'ERROR! Exception:', e

    def on_error(self, status_code):
        print >> sys.stderr, 'ERROR!', repr(status_code)
        return True

    def on_delete(self, status_ID, user_ID):
        print "Deleting %s tweet made by %s user" % (status_ID, user_ID)
        return

    def on_limit(self, track):
        print "BAD JUJU! Limit notice reached:", str(track)
        return

    def on_timeout(self):
        print >> sys.stderr, 'Timeout... Gotta take a chill pill.'
        time.sleep(10)
        return True

    def safe_unicode(self, text):
        try:
            return unicode(text)
        except UnicodeDecodeError:
            return unicode(str(text).encode('string_escape'))


'''

CLASS: TweetStreamingCommunicator
-------------------
Pass in a list of words (as Terms) which you want in tweets and a list of places (as Locations)
and will make a .csv file with given filename (default is sample.csv) in database directory. You
may also specify the duration, in seconds (default is 60).

'''
class TweetStreamingCommunicator:
    def __init__(self, Terms = None, Locations = None, Duration = 60, Filename = 'sample.csv'):
        twitterAuth = Authenticator()
        polyStream = TweetPoliticalStreamListener()
        polyStream.setup(Filename, Terms)
        streamPipe = tweepy.Stream(auth=twitterAuth.auth, listener=polyStream, timeout=Duration)

        if Locations != None:
            streamPipe.filter(location = Locations)

        streamPipe.sample()


'''
CLASS: TweetCommunicator
-------------------

'''

class TweetCommunicator:
    def __init__(self, query = None, language = "en", max_tweets = 1000, locations = None):
        twitterAuth = Authenticator()
        saved_tweets = []
        last_id = -1
        while len(saved_tweets) < max_tweets:
            count = max_tweets - len(saved_tweets)
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
                saved_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError, e:
                print "ERROR:", e
                break

        for tweet in saved_tweets:
            ''' DO SOMETHING WITH TWEETS '''
            pass

class UserCommunicator:         #CHANGE THE QUERY
    def __init__(self, fileName):
        self.twitterAuth = Authenticator()
        self.jsonFile = codecs.open(os.getcwd() + '/database/' + fileName, 'wb', 'utf-8')

    def get_users(self, query = '\s', language = "en", max_users = 100, locations = None):
        twitterAuth = self.twitterAuth
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

        #for userID in userDict:
            #print >> self.jsonFile, json.dumps({userID: userDict[userID]})
        return userDict

    def fill_users(self, users):
        twitterAuth = self.twitterAuth
        for userID in users:
            allTweets = []

            new_tweets = twitterAuth.api.user_timeline(user_id = userID,count=200)
            for tweet in new_tweets:
                cleanedTweet = tweetHandler.tweetToDict(tweet)
                allTweets.append(cleanedTweet)

            oldest = allTweets[-1].id - 1

            while len(new_tweets) > 0:
                new_tweets = twitterAuth.api.user_timeline(user_id=userID,count=200,max_id=oldest)
                for tweet in new_tweets:
                    cleanedTweet = tweetHandler.tweetToDict(tweet)
                    allTweets.append(cleanedTweet)

                oldest = allTweets[-1].id - 1

            users[userID]['tweets'] = allTweets

            users[userID]['followers'] = twitterAuth.api.followers_ids(user_id=userID)

            users[userID]['following'] = twitterAuth.api.friends_ids(user_id=userID)

            favorites = []
            favs = twitterAuth.api.favorites(user_id=userID)
            for tweet in favs:
                cleanedTweet = tweetHandler.tweetToDict(tweet)
                favorites.append(cleanedTweet)
            users[userID]['favorites'] = favorites

            print >> self.jsonFile, json.dumps({userID:users[userID]})
            break



