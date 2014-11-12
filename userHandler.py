import json, collections, math, random, sys

def read_users(filename):
	f = open(filename, 'r')
	data = {}
	for line in f:
		jline = json.loads(line)
		data[jline.keys()[0]] = jline[jline.keys()[0]]
	return data

def increment(d1, scale, d2):
		for f, v in d2.items():
			d1[f] = d1.get(f, 0) + v * scale


def dotProduct(d1, d2):
	if len(d1) < len(d2):
		return dotProduct(d2, d1)
	else:
		return sum(d1.get(f, 0) * v for f, v in d2.items())

def norm(v):
	return math.sqrt(dotProduct(v, v))

class KMeans(object):
	def __init__(self, arg):
		self.data = arg

	def parse_tweets(self, tweets):
		tweet_map = collections.Counter()
		for tweet in tweets:
			content = collections.Counter(tweet["text"])
			tweet_map += content
		return tweet_map

	def load_kmeans(self):
		self.userid_map = {}
		for userid in self.data:
			self.userid_map[userid] = self.parse_tweets(self.data[userid]["tweets"])

	def compute_kmeans(self, K, iters):
		examples = self.userid_map.values()
		miu = random.sample(examples, K)
		z = [0 for i in range(len(examples))]

		def diff(phi, miu_k):
			result = {}
			increment(result, 1, phi)
			increment(result, -1, miu_k)
			return dotProduct(result, result)

		def assign_z(examples, z, miu):
			for i in range(len(examples)):
				MIN = sys.maxint
				mins = []
				for k in range(K):
					t = diff(examples[i], miu[k])
					if t < MIN:
						MIN = t
						mins = [k]
					elif t == MIN:
						mins.append(k)
				z[i] = mins[0] if len(mins) == 1 else mins[random.randint(0, len(mins) - 1)] 

		def avg(x, k, z, me):
			result = {}
			adder = {}
			counter = 0
			for i in range(len(z)):
				if z[i] == k:
					increment(adder, 1, x[i])
					counter += 1
			increment(result, 1.0/counter, adder)
			return result
	        
		def assign_m(examples, miu, z):
			for k in range(K):
				miu[k] = avg(examples, k, z, miu[k])

		def total_loss(z, miu, examples):
			return sum(diff(examples[i], miu[z[i]]) for i in range(len(z)))

		for i in range(iters):
			assign_z(examples, z, miu)
			assign_m(examples, miu, z)

		self.assignments = z
		self.clusters = miu
		self.loss = total_loss(z, miu, examples)

	def delta(self, userid, cluster):
		user_vector = self.userid_map[userid]
		return dotProduct(user_vector, cluster)/(norm(user_vector) + norm(cluster))

	def count_affiliates(self):
		count = collections.Counter()
		for assignment in self.assignments:
			count[assignment] += 1
		return count

	def find_delta(self, userid):
		if self.assignments == None:
			print "error"
			return
		deltas = {}
		affiliates = self.count_affiliates()
		for i in range(len(self.clusters)):
			deltas[i] = (self.delta(userid, self.clusters[i]), affiliates[i])
		return deltas


d = read_users("database/users.json")
k = KMeans(d)
k.load_kmeans()
k.compute_kmeans(2, 10)