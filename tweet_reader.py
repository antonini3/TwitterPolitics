# Tweepy documentation: http://tweepy.readthedocs.org/en/v2.3.0/index.html
import tweepy

class Communicator:

	def __init__(self):
		''' DON'T CHANGE THESE '''
		consumer_key = '7qQNsEsbdrzkJf8Zx5z4DM76n'
		consumer_secret = 'CO5uOCVXRqsOAQRaSzF3JIvmy85zU4PNMolB1XYBCuUxdgA6bZ'
		access_token = '54123389-qgXroCM5FxVBkMTJGXXKOSQo8nMxGXFQdXB1tIfEl'
		access_token_secret = 'mVVF07bNaQqxzic9qHbCksmpNX0zwGH9mz3StwQ386n3J'
		
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		
		# API is main communicator with twitter
		self.API = tweepy.API(auth)



if __name__ == "__init__":
	cm = Communicator()