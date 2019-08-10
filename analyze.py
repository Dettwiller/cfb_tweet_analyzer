import sys
import os
import tools
from nfl_twitter_tags import nfl_tags_dict
from team import Team
import custom_twitter
import time

if __name__ == "__main__":
    debug = True
    analysis_log_filename = "analysis_status.txt"
    schedule_filename = "clean_schedule_with_preseason.csv"
    # The following bit of code is my solution to being able to test this without
    # my twitter account keys showing up in the code or having to remember to
    # delete them all the time.
    token_file = sys.argv[1]
    personal_token_list, bot_token_list = tools.get_tokens(token_file)

    bot_account = custom_twitter.TwitterAccount(bot_token_list[0], bot_token_list[1], bot_token_list[2], bot_token_list[3])

    schedule_file = os.getcwd() + os.sep + "schedule" + os.sep + schedule_filename
    data_path = os.getcwd() + os.sep + "datafiles"
    raw_data_path = data_path + os.sep + "raw"
    analyzed_data_path = data_path + os.sep + "analyzed"
    team_data_dir = data_path + os.sep + "team"
    league = {}
    for team_name in nfl_tags_dict:
        league[team_name] = Team(team_name, nfl_tags_dict[team_name], team_data_dir)

    analysis_log_file = os.getcwd() + os.sep + "logs" + os.sep + analysis_log_filename
    next_matchup = tools.get_next_matchup(schedule_file, league, debug=debug)

    running = True
    while running:
        tools.get_to_analysis(next_matchup, analysis_log_file, raw_data_path, analyzed_data_path, debug=debug)
        next_matchup.analyze(bot_account, analyzed_data_path, threshold = 0.1, print_result = True, send_tweet = False, debug=debug)
        next_matchup = tools.get_next_matchup(schedule_file, league, previous_matchup=next_matchup, debug=debug)
        # running = not debug
