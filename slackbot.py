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
import datetime
import re
import os
from slackclient import SlackClient

BOT_NAME = "the_swanson"
BOT_CHANNEL = "#the_swanson_channel"  # try to get it into other channels, too
# import .env; local from file, but token goes in heroku connfig vars
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
# starterbot's user ID in Slack: value is assigned after the bot starts up
# starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
# EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
exit_flag = False


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


def signal_handler(sig_num, frame):
    """"""
    logger.warning("Received {}".format(sig_num))
    global exit_flag  # need to specify this as global in order to be used here
    exit_flag = True


class SlackBot:

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        pass

    def __repr__(self):
        """"""
        pass

    def __str__(self):
        """"""
        pass

    def __enter__(self):
        """Implement this method to make this a context manager"""
        pass

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        pass

    def post_message(self, msg, chan=BOT_CHANNEL):
        """Sends a message to a Slack Channel"""
        pass

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        pass


def main():
    """"""
    pass


if __name__ == "__main__":
    main()
