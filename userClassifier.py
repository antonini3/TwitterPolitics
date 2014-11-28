import os
import collections
import json
import math

def read_weights():
    f = open(os.getcwd() + '/database/weightsFile.txt')
    data = json.load(f)
    weights = collections.Counter()
    for key, value in data.iteritems():
        weights[int(key)] = value
    return weights

def read_users():
    f = open(os.getcwd() + '/database/all_politicians_twitter.json')
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

def extract_features(users, feature_set):
    all_features = {}
    for user in users:
        feature = collections.Counter()
        if "following" in feature_set:
            following = users[user]["following"]
            for follow in following:
                feature[follow] = 1
        if "followers" in feature_set:
            followers = users[user]["followers"]
            for follow in followers:
                feature[follow] = 1
        all_features[user] = feature

    return all_features


def dotProduct(d1, d2, sum_weights):
    if len(d1) < len(d2):
        return dotProduct(d2, d1, sum_weights)
    else:
        non_zero = 0
        for f, v in d2.items():
            if float(d1.get(f, 0)) * float(v) != 0:
                non_zero += 1
        return (sum(float(d1.get(f, 0)) * float(v) for f, v in d2.items())/ float(sum_weights))

def classify(all_features, weights, normalizer):
    scores = {}
    for user in all_features:
        feature = all_features[user]
        score = dotProduct(feature, weights, normalizer)
        scores[user] = score
    return scores

def get_testing_data():
    f = open(os.getcwd() + '/database/testing_data.json')
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

    real_ideology = collections.Counter()
    for d in data:
        real_ideology[d] = data[d]['ideology']
    return data, real_ideology


def actual_results():
    f = open(os.getcwd() + '/database/all_politicians_twitter.json')
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
    real_ideology = collections.Counter()
    for d in data:
        real_ideology[d] = data[d]['ideology']
    return real_ideology

def find_error(actual, scores):
    total_error = 0.0
    for user in actual:
        error = math.fabs(actual[user] - scores[user])
        total_error += error
    total_error /= len(actual)
    return total_error

def find_baseline_error(actual, scores):
    total_error = 0
    for user in actual:
        if (actual[user] < 0 and scores[user] < 0) or (actual[user] > 0 and scores[user] > 0):
            total_error += 1
    total_error /= float(len(actual))
    return total_error

def main(feature_set):
    #actual = actual_results()
    #data = read_users()
    #features = extract_features(data)
    weights = read_weights()
    testing_data, actual = get_testing_data()
    features = extract_features(testing_data, feature_set)

    normalizer = 0
    for key, value in weights.items():
        normalizer += value
    scores = classify(features, weights, normalizer)

    error = find_error(actual, scores)
    baseline_error = find_baseline_error(actual, scores)

    return scores, error, baseline_error

if __name__ == "__main__":
    main()
