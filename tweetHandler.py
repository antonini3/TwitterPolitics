#These method should all handle tweets
def cleanText(text):
    if text != None:
        text.replace(unichr(8232), '')
        text.replace(unichr(8233), '')
    return text

def tweetToDict(original):
    tweet = {}
    tweet['text'] = cleanText(original.text)
    tweet['id'] = cleanText(original.text)
    # if original.created_at.date != None:
    #     tweet['created'] = cleanText(str(original.created_at))
    # else:
    #     tweet['created'] = None
    # tweet['geo'] = cleanText(original.geo)
    # tweet['contributors'] = original.contributors
    # tweet['coordinates'] = original.coordinates
    # tweet['favorited'] = original.favorited
    # if original.place != None:
    #     tweet['place'] = cleanText(original.place.full_name)
    # else:
    #     tweet['place'] = None
    # tweet['retweeted'] = original.retweeted
    # tweet['retweetCount'] = original.retweet_count
    # tweet['source'] = cleanText(original.source)
    return tweet