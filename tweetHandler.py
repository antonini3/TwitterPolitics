#These method should all handle tweets

def tweetToDict(original):
    tweet = {}
    tweet['text'] = original.text
    tweet['id'] = original.id
    if original.created_at.date != None:
        tweet['created'] = str(original.created_at)
    else:
        tweet['created'] = None
    tweet['geo'] = original.geo
    tweet['contributors'] = original.contributors
    tweet['coordinates'] = original.coordinates
    tweet['favorited'] = original.favorited
    if original.place != None:
        tweet['place'] = original.place.full_name
    else:
        tweet['place'] = None
    tweet['retweeted'] = original.retweeted
    tweet['retweetCount'] = original.retweet_count
    tweet['source'] = original.source
    return tweet