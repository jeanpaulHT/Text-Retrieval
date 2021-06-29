import json
import sys
from os import listdir
from os.path import isfile, join
import params

def encodeText(tweet_text):    
    tweet_text = tweet_text.replace('\n',' ')  
    #tweet_text = tweet_text.encode("utf-8") 
    return str(tweet_text)

def parse_file(file_in, file_out):
    ptrFile_in = open(file_in, "r")
    ptrFile_out = open(file_out, "w", encoding="utf-8")

    cleanLines = []
    for line in ptrFile_in:
        cleanLine = {}
        line = line.rstrip()
        if line != "":
            try:
                decoded = json.loads(line)
                cleanLine.update({"id" : decoded['id']})
                cleanLine.update({"date" : decoded['created_at']})
                if decoded.get('extended_tweet') is not None: 
                    cleanLine.update({"text": encodeText(decoded['extended_tweet']['full_text'])})
                else:
                    cleanLine.update({"text": encodeText(decoded['text'])})                
                cleanLine.update({"user_id" : decoded['user']['id']})   
                cleanLine.update({"user_name" : '@' + decoded['user']['screen_name']})   

                if decoded.get('place') is not None:                    
                    cleanLine.update({"location" : {"country": decoded['place']['country'], "city": decoded['place']['name']} })   
                else:
                    cleanLine.update({"location" : {} })

                if decoded.get('retweeted_status') is not None: 
                    cleanLine.update({"retweeted" : True })
                    if decoded.get('retweeted_status').get('extended_tweet') is not None:
                        cleanLine.update({"RT_text" : encodeText(decoded['retweeted_status']['extended_tweet']['full_text']) })
                    else:
                        cleanLine.update({"RT_text" :  encodeText(decoded['retweeted_status']['text']) })
                    cleanLine.update({"RT_user_id" :  decoded['retweeted_status']['user']['id'] })
                    cleanLine.update({"RT_user_name" : '@' + decoded['retweeted_status']['user']['screen_name'] })   
                else:
                    cleanLine.update({"retweeted" : False})   
                
                cleanLines.append(cleanLine)
            except Exception as e:
                print(e, " :: ", line)

    ptrFile_out.write(json.dumps(cleanLines, ensure_ascii=False))
    ptrFile_out.close()      

if __name__ == '__main__':
    path_in = params.folder_path 
    path_out = params.clean_path

    for f in listdir(path_in):
        file_in = join(path_in, f)    
        file_out = join(path_out, f)   
        if isfile(file_in):
            parse_file(file_in, file_out)


    

        
                
        
