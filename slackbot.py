#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A slackbot that responds to commands.
This uses the Slack RTM (Real Time Messaging) API.
Required environment variables (example only, these are not real tokens).
Get these from the Slack account settings that you are connecting to.
   BOT_USER_ID = "U20981S736"
   BOT_USER_TOKEN = "xoxb-106076235608-AbacukynpGahsicJqugKZC"
This is in Python3
"""

__author__ = "mhoelzer and LEllingwood"


import logging
import signal
import sys
import requests
import json
# import datetime
import time
import re
import os
from slackclient import SlackClient
from dotenv import load_dotenv

BOT_NAME = "the_swanson"
BOT_CHANNEL = "#the_swanson_channel"  # try to get it into other channels, too
# import .env; local from file, but token goes in heroku connfig vars
# SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
# starterbot's user ID in Slack: value is assigned after the bot starts up
# starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
# EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
exit_flag = False

load_dotenv()


def config_logger():
    """Setup logging configuration"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("the_swanson.log")
    formatter = logging.Formatter(
        fmt=("%(asctime)s %(msecs)03d %(name)s %(levelname)s [%(threadName)s]:"
             " %(message)s"),
        datefmt="%Y-%m-%d, %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


logger = config_logger()


bot_commands = {
    "help":  "Shows this helpful command reference.",
    "ping":  "Show uptime of this bot.",
    "exit":  "Shutdown the entire bot (requires app restart).",
    "raise":  "Manually test exception handler."
}


def formatted_dict(dicty_doo, k_header="Keys", v_header="Values"):
    """Renders contents of a dict into a preformatted string"""
    if dicty_doo:
        lines = []
        # find the longest key entry in d or the key header string
        width = max(map(len, dicty_doo))
        width = max(width, len(k_header))
        lines.extend(["{k:<{w}} : {v}".format(
            k=k_header, v=v_header, w=width)])
        lines.extend(["-"*width + "   " + "-"*len(v_header)])
        lines.extend("{k:<{w}} : {v}".format(k=k, v=v, w=width)
                     for k, v in dicty_doo.items())
        return "\n".join(lines)
    return "<empty>"


def command_loop(bot):
    """Process incoming bot commands"""
    if bot_commands[0]:
        print(formatted_dict(bot_commands,
                             k_header="My cmds", v_header="What they do"))
    pass


def fetch_swanson():
    """Gets random Ron Swanson quotes from API"""
    r = requests.get('https://ron-swanson-quotes.herokuapp.com/v2/quotes')
    if r.status_code != 200:
        print("Got a problem, son")
    r = r.json()
    print(r)


def fetch_cat():
    """Gets random cat images from API"""
    url = 'https://api.thecatapi.com/v1/images/search'
    cat_img = requests.get(url).json()
    return cat_img[0]['url']


def combine_swanson_cat():
    """"""
    pass


def signal_handler(sig_num, frame):
    """"""
    logger.warning("Received {}".format(sig_num))
    global exit_flag  # need to specify this as global in order to be used here
    exit_flag = True


class SlackBot:
    global slack_client

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        self.slack_client = slack_client
        self.bot_name = BOT_NAME
        self.bot_id = self.get_bot_id()
        if self.bot_id is None:
            exit(f"err no {self.bot_name}")

    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get("ok"):
            # retrieve all users so we can find our bot
            users = api_call.get("members")
            for user in users:
                if "name" in user and user.get("name") == self.bot_name:
                    return "<@{}>".format(user.get("id"))
            return None

    def __repr__(self):
        """"""
        return f"SlackBot: {self.bot_name} {self.bot_id}"

    def __str__(self):
        """"""
        pass

    def __enter__(self):
        """Implement this method to make this a context manager"""
        pass

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        pass

    def parse_commands(self, slack_events):
        """"""
        for slack_event in slack_events:
            slack_event_gotten = slack_event.get("type")
            if slack_event_gotten == "message" and "subtype" not in slack_event:
                user_id, message = self.parse_mention(
                    slack_event_gotten)
                if user_id == self.bot_id:
                    return message, slack_event["channel"]
        return None, None

    def parse_mention(self, text):
        matches = re.search(MENTION_REGEX, text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def post_message(self, msg, chan=BOT_CHANNEL):
        """Sends a message to a Slack Channel"""
        pass

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        if raw_cmd.startswith("hey"):
            response = "Sure...write some more code then I can do that!"
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )
        pass


def main():
    """"""
    global slack_client
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    bot = SlackBot(slack_client)
    if slack_client.rtm_connect(with_team_state=False):
        print("Stuff connected with {}".format(bot))
        while not exit_flag:
            command_loop(bot)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed :(")


if __name__ == "__main__":
    main()
