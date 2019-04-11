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
# slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
# MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
exit_flag = False

load_dotenv()


def config_logger():
    """Setup logging configuration"""
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(msecs)03d %(name)s %(levelname)s [%(threadName)s]:%(message)s",
        datefmt="%Y-%m-%d, %H:%M:%S")
    logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler("the_swanson.log")
    # formatter = logging.Formatter(
    #     fmt=("%(asctime)s %(msecs)03d %(name)s %(levelname)s [%(threadName)s]:"
    #          " %(message)s"),
    #     datefmt="%Y-%m-%d, %H:%M:%S")
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.DEBUG)
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
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
    # if bot_commands[0]:
    #     print(formatted_dict(bot_commands,
    #                          k_header="My cmds", v_header="What they do"))
    logger.info("waiting for commands")
    while not exit_flag:
        chan, command = bot.parse_commands()
    logger.info("bot is going out of scope")


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
    # global slack_client

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        self.bot_start = None
        self.bot_name = BOT_NAME
        self.slack_client = SlackClient(os.environ.get(bot_user_token))
        # self.slack_client = slack_client
        self.bot_id = bot_id
        # find id
        if not self.bot_id and self.slack_client.rtm_connect(with_team_state=False):
            # Read bot's user ID by calling Web API method `auth.test`
            response = self.slack_client.api_call('auth.test')
            self.bot_id = response.get('user_id')
        self.at_bot = '<@' + str(self.bot_id) + '>'
        logger.info(f'{self.bot_name} Created new SlackBot')

    def __repr__(self):
        """"""
        return f"{self.at_bot}"

    def __str__(self):
        """"""
        return f"{self.at_bot}"

    def __enter__(self):
        """Implement this method to make this a context manager"""
        if self.slack_client.rtm_connect(with_team_state=False):
            logger.info(f"{self} is connected online")
            self.post_message(f"{self.bot_name} is running")
        return self

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        logger.info(f"{self} is disconnected")
        self.post_message("goodbye")

    def parse_commands(self):
        """"""
        slack_events = self.slack_client.rtm_read() #command listnen
        # logger.debug(slack_events)
        for slack_event in slack_events:
            slack_event_gotten = slack_event.get("type")
            if slack_event_gotten == "message" and "subtype" not in slack_event:
                if slack_event["text"].startswith(self.at_bot):
                    chan = slack_event["channel"]
                    command = slack_event["text"][len(self.at_bot) + 1:]
                    logger.info(f"got command {command} on channel {chan}")
                    return chan, command
        return None, None

    def parse_direct_mention(self, text):
        # the first group contains the username, the second group contains the remaining message
        # if text.startswith(self.at_bot)
        # return (matches.group(1), matches.group(2).strip()) if text.startswith(self.at_bot) else (None, None)
        pass

    def post_message(self, msg, chan=BOT_CHANNEL):
        """Sends a message to a Slack Channel"""
        self.slack_client.api_call(
            "chat.postMessage",
            channel=chan,
            text=msg
        )

    # def wait_for_command(self):
    #     # wait for something to happen on slack
    #     response = self.slack_client.rtm_read()
    #     for item in response:
    #         if "text" in item and self.at_bot in item["text"]:

    def handle_command(self, chan, command):
        """
        Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean. Try *{}*.".format(
            EXAMPLE_COMMAND)
        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command.startswith(EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can do that!"
        # help and ping and w/e; set exitflag
        # Sends the response back to the channel; self.sendmes; hook in api


def main():
    """"""
    # global slack_client
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    with SlackBot("SLACK_BOT_TOKEN") as bot:
        while not exit_flag:
            command_loop(bot)
            time.sleep(RTM_READ_DELAY)
            logger.debug("while loop")
            pass


if __name__ == "__main__":
    main()
