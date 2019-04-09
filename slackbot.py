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

# import argparse
# import logging
# import signal
# import sys
# import os

BOT_NAME = "my-bot-name"
BOT_CHAN = "#bot-test"


def config_logger():
    """Setup logging configuration"""


def command_loop(bot):
    """Process incoming bot commands"""
    pass


def signal_handler(sig_num, frame):
    """"""
    pass


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

    def post_message(self, msg, chan=BOT_CHAN):
        """Sends a message to a Slack Channel"""
        pass

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        pass


bot_commands = {
    "help":  "Shows this helpful command reference.",
    "ping":  "Show uptime of this bot.",
    "exit":  "Shutdown the entire bot (requires app restart)",
    "raise":  "Manually test exception handler"
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
                     for k, v in d.items())
        return "\n".join(lines)
    return "<empty>"


print(formatted_dict(bot_commands, k_header="My cmds", v_header="What they do"))


# def create_parser():
#     """creates and returns an argparse cmd line option parser"""
#     parser = argparse.ArgumentParser(description="rnsfjnslfdnswnfeln.")
#     parser.add_argument("help", help="Lists all the commands that this bot understands")
#     parser.add_argument("ping", help="Shows the uptime of this bot")
#     parser.add_argument("exit", help="Shuts down this bot (requires app restart)")
#     parser.add_argument("quit", help="Same as exit")
#     parser.add_argument("clear", help="Remove all filters")
#     return parser


def main():
    """"""
    # parser = create_parser()
    # args = parser.parse_args(args)
    # if not args:
    #     parser.print_usage()
    #     sys.exit(1)
    pass


if __name__ == "__main__":
    # main(sys.argv[1:])
    main()
