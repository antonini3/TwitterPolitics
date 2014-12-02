import collections
import os, codecs
import json
import random
import math

def read_file(fileName):
	f = open(os.getcwd() + fileName)
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

def export_testing_data(testing_data):
	testing_data_file = codecs.open(os.getcwd() + '/database/' + 'testing_data.json' , 'wb')
	for testing in testing_data:
		print >> testing_data_file, json.dumps({testing:testing_data[testing]})

def politicianLearner(feature_set = None):
	feature_dict = read_file('/database/politician_features.json')

	weightsFile = codecs.open(os.getcwd() + '/database/' + 'weightsFile.txt' , 'wb', 'utf-8')

	testing_data = {}
	testing_data_keys = random.sample(feature_dict.keys(), 100)
	for key in testing_data_keys:
		testing_data[key] = feature_dict[key]
		del feature_dict[key]
	export_testing_data(testing_data)

	training_data = []
	for politician in feature_dict:
		# features = extractFeatures(politicians[politician], feature_set)
		splitting = politician.split()

		features = feature_dict[politician]
		y = float(splitting[1])
		name = splitting[0]
		training_data.append((name, features, y))

	weights = collections.Counter()

	def dirLoss(features, y):
		dot_product = dotProduct(weights, features)
		residual = 2 * (dot_product - y)
		new_features = collections.Counter()
		for feature in features:
			new_features[feature] = float(features[feature]) * float(residual)
		return new_features

	stepSize = 0.00011
	numIters = 10
	counter = 0
	for i in range(numIters):
		#if i > 0:
			#stepSize = 0.0001/float(math.sqrt(i))
		sum_der_loss = collections.Counter()
		for politician in training_data:
			name, features, y = politician
			dirL = dirLoss(features, y)
			for feature in dirL:
				sum_der_loss[feature] = sum_der_loss[feature] + dirL[feature]
		der_loss = collections.Counter()
		for item in sum_der_loss:
			der_loss[item] = sum_der_loss[item] / float(len(feature_dict))
		increment(weights, -stepSize, der_loss)
		print "done: " + str(counter)

		counter += 1
	new_weights = {}

	weight_tuples = []
	max_weight = (float("-infinity"), 0)
	min_weight = (float("infinity"), 0)

	for weight in weights:
		if weights[weight] > max_weight[0]:
			max_weight = (weights[weight], weight)
		if weights[weight] < min_weight[0]:
			min_weight = (weights[weight], weight)

		weight_tuples.append((weights[weight], weight))

		new_key = weight
		new_weights[new_key] = weights[weight]

	sorted_weight_tuples = sorted(weight_tuples, key = lambda s: s[0])

	top_weights = sorted_weight_tuples[:100]
	bottom_weights = sorted_weight_tuples[-100:]

	print >> weightsFile, json.dumps(new_weights)

if __name__ == "__main__":
	politicianLearner()

