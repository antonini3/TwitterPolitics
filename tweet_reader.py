# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy, sys, codecs, os, csv, codecs
from time import clock


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

CLASS: PoliticalStreamListener
-------------------
Instance of tweepy's StreamListener which writes to file and prints out useful information.

'''
class PoliticalStreamListener(tweepy.StreamListener):

	def open_file(self, fileName):
		self.csvFile = codecs.open(os.getcwd() + '/database/' + fileName, 'wb', 'utf-8')

	def set_terms(self, Terms):
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
		print 'ERROR!', repr(status_code)
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

CLASS: Communicator
-------------------
Pass in a list of words (as Terms) which you want in tweets and a list of places (as Locations)
and will make a .csv file with given filename (default is sample.csv) in database directory. You
may also specify the duration, in seconds (default is 60).

'''
class Communicator:
	def __init__(self, Terms = None, Locations = None, Duration = 60, Filename = 'sample.csv'):
		current_dir = os.getcwd()
		database_dir = current_dir + '/database/'
		datafile_name = 'sample.csv'
		twitterAuth = Authenticator()
		polyStream = PoliticalStreamListener()
		polyStream.set_terms(Terms)
		polyStream.open_file(Filename)
		streamPipe = tweepy.Stream(auth=twitterAuth.auth, listener=polyStream, timeout=Duration)
		
		if Locations != None:
			streamPipe.filter(location = Locations)
		
		streamPipe.sample()


# For testing purposes		
if __name__ == "__main__":
	Communicator(Terms = ["the"], Locations = None)

