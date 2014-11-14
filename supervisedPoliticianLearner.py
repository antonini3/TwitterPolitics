import collections
import os, codecs
import json

def read_file():
	f = open(os.getcwd() + '/database/temp_politicians_twitter.json')
	data = {}
	counter = 0
	for line in f:
		try:
			jline = json.loads(line)
			data[jline.keys()[0]] = jline[jline.keys()[0]]
		except:
			counter += 1
			pass
	print counter
	return data

def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def parse_tweets(tweets):
	tweet_map = collections.Counter()
	for tweet in tweets:
		content = collections.Counter(tweet["text"])
		tweet_map += content
	return tweet_map

def extract_follow(followers, typeUsers):
	follower_dict = collections.Counter()
	for follower in followers:
		follower_dict[typeUsers + ": " + str(follower)] = 1
	return follower_dict

def extractFeatures(politician):
	features = collections.Counter()
	#features += parse_tweets(politician["tweets"])
	features += extract_follow(politician["followers"], "followers")
	features += extract_follow(politician["following"], "following")
	#all other features
	return features

def politicianLearner():
	politicians = read_file()
	weightsFile = codecs.open(os.getcwd() + '/database/' + 'weightsFile.txt' , 'wb', 'utf-8')

	training_data = []
	for politician in politicians:
		features = extractFeatures(politicians[politician])
		y = float(politicians[politician]["ideology"])
		training_data.append((features, y))

	weights = collections.Counter()

	def dirLoss(features, y):
		dot_product = dotProduct(weights, features)
		residual = 2 * (dot_product - y)
		for feature in features:
			features[feature] *= residual
		return features

	stepSize = 0.001
	numIters = 20
	for i in range(numIters):
		sum_der_loss = collections.Counter()
		for politician in training_data:
			features, y = politician
			sum_der_loss += dirLoss(features, y)
		der_loss = collections.Counter()
		for item in sum_der_loss:
			der_loss[item] = sum_der_loss[item] / float(len(politicians))
		increment(weights, -stepSize, der_loss)
	print >> weightsFile, weights

if __name__ == "__main__":
	politicianLearner()

