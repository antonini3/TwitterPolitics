import sys, codecs, os, collections, threading, json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool



def extractor(filename, all_politicians, past_politicians):

    def extractFeatures(politician_str):
        print "Extracting features from this dumbass:", politician_str
        features = collections.Counter()
        politician = all_politicians[politician_str]
        if "tweets" in feature_set:
            info, counts = extract_tweets(politician["tweets"])
            features += info
            features += counts
        if "followers" in feature_set:
            features += extract_follow(politician["followers"], "followers")
        if "following" in feature_set:
            features += extract_follow(politician["following"], "following")

        lock.acquire()
        print >> json_file, json.dumps({politician_str + ' ' + str(politician['ideology']): features})
        lock.release()
        

    def extract_follow(followers, typeUsers):
        follower_dict = collections.Counter()
        for follower in followers:
                follower_dict[follower] = 1
        return follower_dict

    def extract_tweets(tweets):
        tweet_info = collections.Counter()

        counts = collections.Counter()
        hashtag_count = 0
        total_words = 0
        total_chars = 0
        total_tweet_length = 0
        for tweet in tweets:
            text = tweet['text']
            total_tweet_length += len(text)
            for word in text.split():

                total_chars += len(word)
                total_words += 1

                counts[word] += 1
                if word[0] == '#':
                    hashtag_count += 1

        tweet_info['num_hashtags'] = hashtag_count
        # tweet_info['avg_word_length'] = round(total_chars / float(total_words), 1) if total_words != 0 else 0
        # tweet_info['avg_tweet_length'] = round(total_tweet_length / float(len(tweets)), 1) \
        #     if len(tweets) != 0 else 0
        
        return tweet_info, counts 


    json_file = codecs.open(os.getcwd() + '/database/' + filename, 'wb', 'utf-8')
    lock = threading.Lock()
    feature_set = ['tweets', 'followers', 'following']

    for p in past_politicians:
        del all_politicians[p.split()[0]]
    
    pool = ThreadPool(30)
    pool.map(extractFeatures, all_politicians)

    # for politician in all_politicians:
    #     extractFeatures(politician)
    


def get_data_from_file(fileName, tp = 'set'):
    try:
        f = open(os.getcwd() + '/database/' + fileName)
        data = {}
        counter = 0
        for line in f:
            try:
                jline = json.loads(line)
                data[jline.keys()[0]] = jline[jline.keys()[0]]
            except Exception as e:
                print e
                counter += 1
                pass

        return set(data.keys()) if tp == 'set' else data
    except Exception as e:
        print e
        return set() if tp == 'set' else dict()


if __name__ == "__main__":

    info_file_name = 'politicians_twitter_data_all.json'
    output_file_name = 'politician_features.json'

    all_politicians = get_data_from_file(info_file_name, tp = 'dict')
    # past_politicians = get_data_from_file(output_file_name, tp = 'set')
    past_politicians = set()
    print 'Past politicians:', len(past_politicians)
    print 'All politicians:', len(all_politicians)
    extractor(output_file_name, all_politicians, past_politicians)

