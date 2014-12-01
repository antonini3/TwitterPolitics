import supervisedPoliticianLearner
import userClassifier

def create_feature_set():
    feature_set = set()

    # feature_set.add("following")
    feature_set.add("followers")

    return feature_set

def print_info(scores, error, baseline_error):
    for user in scores:
        print "User: " + str(user) + " has a ideology score of: " + str(scores[user])
    print 'ERROR:', error
    print 'BASELINE PERCENT CORRECT:', baseline_error

def main():
    numIterations = 1

    total_error = 0
    total_baseline_error = 0

    feature_set = create_feature_set()

    for i in range(numIterations):
        supervisedPoliticianLearner.politicianLearner(feature_set)
        scores, error, baseline_error = userClassifier.main(feature_set)

        print_info(scores, error, baseline_error)

        total_error += error
        total_baseline_error += baseline_error

    print "average error is: " + str(float(total_error)/numIterations)
    print "average baseline error is: " + str(float(total_baseline_error)/numIterations)

if __name__ == "__main__":
    main()