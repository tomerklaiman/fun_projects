import tweepy

api_key= "iy9v64JXzbN45HD8FkEfWKVep"
api_key_secret="7WXv2HhHBiGZq9fgDF2pDQ12qh6UdH9Xe8i9yu8hryxgLQwrLr"
access_token = "1368938864614793225-JHN2A7iJATPrAlzRcpIkxMZhXZAcMP"
access_token_secret= "qfdIJyPEGfIrgdmKlBx8gdB9gpmXmOGwZ6YSB13nyuAz4"


auth = tweepy.OAuth1UserHandler(
   api_key, api_key_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

search_term = "Wordle"
tweets = tweepy.Cursor(api.search_tweets,search_term).items(10000)


all_tweets = set()
tweet_count =0;
score_count=0;
for tweet in tweets:
    text= tweet.text.split("\n")[0]  #get first line of tweet where worlde score usually is
    if "/6" in text:
        arr = text.split("/6")
        line = arr[0]
        score = line[-1]
        if(score.isdigit()):
            score_count= score_count + int(score)
            tweet_count= tweet_count + 1

print(score_count/tweet_count)
