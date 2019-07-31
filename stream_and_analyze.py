import sys
import tweepy
import custom_twitter
import os
from nfl_twitter_tags import nfl_tags_dict
from team import Team


def get_tokens(token_file):
    with open(token_file, "r", encoding='utf-8') as tf:
        file_lines = tf.readlines()
    personal_keys = ["", "", "", ""] # consumer, consumer secret, access, access secret
    bot_keys = ["", "", "", ""]
    for i in range(4):
        personal_keys[i] = file_lines[i + 1].split()[-1].strip()
        bot_keys[i] = file_lines[i + 7].split()[-1].strip()
    return personal_keys, bot_keys


def stream(tags, auth_tokens, data_path):
    twitter_account = custom_twitter.TwitterAccount(auth_tokens[0], auth_tokens[1], auth_tokens[2], auth_tokens[3])
    stream_listener = custom_twitter.MyStreamListener(twitter_account, data_path)
    stream = tweepy.Stream(auth = twitter_account.auth, listener = stream_listener)
    stream.filter(track=tags)



if __name__ == "__main__":
    # TODO define the tags from all the teams (btw how we doing teams now?)
    # TODO: fork a stream to gather data

    # The following bit of code is my solution to being able to test this without
    # my twitter account keys showing up in the code or having to remember to
    # delete them all the time.
    token_file = sys.argv[1]
    personal_token_list, bot_token_list = get_tokens(token_file)

    data_path = os.getcwd() + os.sep + "datafiles"
    nfl_tags = []
    league = {}
    for team_name in nfl_tags_dict:
        nfl_tags += nfl_tags_dict[team_name]
        league[team_name] = Team(team_name, nfl_tags_dict[team_name], data_path)

    newpid = os.fork()
    if newpid == 0:
        while True:
            try:
                print("child is streaming")
                stream(nfl_tags, bot_token_list, data_path)
            except:
                # TODO error logging
                pass
    else:
        print("parent process")
    # TODO: loop through games and perform analysis if time_until_game < 1 hour
    # NOTE: Games in clean_schedule.csv are in chronological order
    pass
