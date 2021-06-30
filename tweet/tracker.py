#Import the necessary methods from tweepy library
import tweepy
from datetime import datetime
import time
import params

#This is a basic listener that just prints received tweets to stdout.
class TweetListener(tweepy.StreamListener):
    def __init__(self, base_filename):
        self.__base_filename = base_filename

    def __open_file(self):
        now=datetime.now()
        filename = self.__base_filename + "_" + now.strftime("%Y-%m-%d")+".json"
        ptrFile = open(filename, "a+")
        return ptrFile

    def on_data(self, data):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " :: tweet read" )
        ptrFile = self.__open_file()        
        ptrFile.write(data + "\n")
        ptrFile.close()
        return True

    def on_error(self, status):
        print("--- ERROR " + status + " ----")
        if status == 420:
            print("--- Waiting 15 minutes ---")
            time.sleep(15*60) #waiting by 15 minutes


if __name__ == '__main__':
    listener = TweetListener(params.folder_path + "tweets")

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = tweepy.OAuthHandler(params.consumer_key, params.consumer_secret)
    auth.set_access_token(params.access_token, params.access_token_secret)
    stream = tweepy.Stream(auth, listener)
    
    listaTrack = []
    for k, v in params.tracklist.items(): 
        listaTrack = listaTrack + v

    while(True):
        try:
            stream.filter(track=listaTrack)
        except:
            print("---- CONNECTION ERROR ----")
            pass