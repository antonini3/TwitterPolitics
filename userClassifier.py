import os
import collections
import json

def read_weights():
    f = open(os.getcwd() + '/database/weightsFile.txt')
    data = json.load(f)
    return data

def read_users():
    f = open(os.getcwd() + '/database/users_testing.json')
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

def extract_features(users):
    all_features = {}
    for user in users:
        feature = collections.Counter()
        following = users[user]["following"]
        for follow in following:
            feature[follow] = 1
        all_features[int(user)] = feature
    return all_features


def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(float(d1.get(int(f), 0)) * float(v) for f, v in d2.items())

def classify(all_features, weights):
    scores = {}
    for user in all_features:
        feature = all_features[user]
        print feature
        #print weights
        score = dotProduct(feature, weights)
        scores[user] = score
    return scores

def main():
    data = read_users()
    features = extract_features(data)
    weights = read_weights()
    scores = classify(features, weights)
    for user in scores:
        print "User: " + str(user) + " has a ideology score of: " + str(scores[user])

main()
