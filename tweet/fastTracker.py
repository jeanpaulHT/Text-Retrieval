import csv
import snscrape.modules.twitter as sntwitter
import json




def main():
    keyword = "covid"
    maxTweets = 1000
    tweetFile = 500
    file = 0

    while (file <= maxTweets / tweetFile):
        out_path = f"raw/{keyword}_data{file}.json"
        with open(out_path, "w+", encoding="utf-8") as f_out:
            f_out.truncate(0)
        file +=1

    file = 0
    since = '2020-01-01'
    until = '2020-12-15'
    mysearch = f'{keyword} -filter:retweets since:{since} until:{until}'
    myscraper = sntwitter.TwitterSearchScraper(mysearch).get_items()
    total = 0
    counter = 0

    f_out = open(f"raw/{keyword}_data{file}.json", 'a', newline='\n', encoding='utf8')
    print(1)
    for tweet in myscraper:
        if total > maxTweets:
            break

        my_details = {
                    'id': tweet.id,
                    'username': tweet.username,
                    'date': tweet.date,
                    'content': tweet.content
        }
        f_out.write(json.dumps(my_details, ensure_ascii=False, default=str))
        f_out.write('\n')
        if counter == tweetFile:
            file += 1
            counter = 0
            f_out = open(f"raw/{keyword}_data{file}.json", 'a', newline='\n', encoding='utf8')
        counter+=1
        total +=1


if __name__ == '__main__':
    main()
