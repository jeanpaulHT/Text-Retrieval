import csv
import snscrape.modules.twitter as sntwitter
import json




def main():
    keyword = "covid"
    dir = "../texts/raw"
    maxTweets = 20000
    tweetFile = 1000
    file = 0

    while (file < maxTweets / tweetFile):
        out_path = f"{dir}/{keyword}_data{file}.json"
        with open(out_path, "w+", encoding="utf8") as f_out:
            f_out.truncate(0)
        file +=1

    file = 0
    since = '2020-01-01'
    until = '2020-12-15'
    mysearch = f'{keyword} lang:es -filter:retweets since:{since} until:{until}'
    myscraper = sntwitter.TwitterSearchScraper(mysearch).get_items()
    total = 0
    counter = 0

    f_out = open(f"{dir}/{keyword}_data{file}.json", 'a', newline='\n', encoding='utf-8')
    cleanLines = []

    for tweet in myscraper:
        print(total)
        if total > maxTweets:
            f_out.write(json.dumps(cleanLines, ensure_ascii=False, default= str))
            break

        my_details = {
                    'id': ( (tweet.url).split('/')[-1] ),
                    'username': tweet.username,
                    'date': tweet.date,
                    'content': tweet.content
        }
        cleanLines.append(my_details)
        if counter == tweetFile:
            file += 1
            counter = 0
            f_out.write(json.dumps(cleanLines, ensure_ascii=False, default= str))
            f_out.write('\n')
            cleanLines.clear()
            f_out = open(f"{dir}/{keyword}_data{file}.json", 'a', newline='\n', encoding='utf-8')
        counter+=1
        total +=1



if __name__ == '__main__':
    main()
