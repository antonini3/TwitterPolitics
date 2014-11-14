import json
import os, codecs

def read_file():
    f = open(os.getcwd() + '/database/all_politicians_twitter_old.json')
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

def main():
    newFile = codecs.open(os.getcwd() + '/database/' + "all_politicians_twitter.json", 'wb', 'utf-8')
    politicianData = read_file()
    for politician in politicianData:
        politicianData[politician]["ideology"] = float(politicianData[politician]["ideology"]) - 0.5
        print >> newFile, json.dumps({politician:politicianData[politician]})

if __name__ == "__main__":
    main()