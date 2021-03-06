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
import requests
import datetime
import time
import os
from slackclient import SlackClient
from dotenv import load_dotenv

BOT_NAME = "the_swanson"
BOT_CHANNEL = "#the_swanson_channel"  # try to get it into other channels, too
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
exit_flag = False

load_dotenv()


def config_logger():
    """Setup logging configuration"""
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s %(msecs)03d %(name)s %(levelname)s "
                "[%(threadName)s]:%(message)s"),
        datefmt="%Y-%m-%d, %H:%M:%S")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("the_swanson.log")
    formatter = logging.Formatter(
        fmt=("%(asctime)s %(msecs)03d %(name)s %(levelname)s \
    [%(threadName)s]:"
             " %(message)s"),
        datefmt="%Y-%m-%d, %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = config_logger()


bot_commands = {
    "help": "Shows this helpful command reference.",
    "ping": "Show the endurance of The Swanson!",
    "exit": "Shutdown the entire bot (requires app restart).",
    "raise": "Manually test exception handler.",
    "speak": "Hear The Wisdom.",
    "see": "See The Cat.",
    "meme": "The Best of Both Worlds.",
    "suffer": "Suffer :)."
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
    logger.info("Waiting for commands...")
    while not exit_flag:
        chan, command = bot.parse_slack_events()
        if chan and command:
            bot.handle_command(chan, command)
    logger.info("Bot is going out of scope.")


def fetch_swanson():
    """Gets random Ron Swanson quotes from API"""
    r = requests.get('https://ron-swanson-quotes.herokuapp.com/v2/quotes')
    # if r.status_code != 200:
    #     print("Got a problem, son")
    r.raise_for_status()
    r = r.json()
    return str(r[0])


def fetch_cat():
    """Gets random cat images from API"""
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url).json()
    return r[0]['url']


def signal_handler(sig_num, frame):
    """Handles incoming signals"""
    logger.warning(f"Received {sig_num}.")
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
        if (not self.bot_id and
                self.slack_client.rtm_connect(with_team_state=False)):
            # Read bot's user ID by calling Web API method `auth.test`
            response = self.slack_client.api_call('auth.test')
            self.bot_id = response.get('user_id')
        self.at_bot = '<@' + str(self.bot_id) + '>'
        logger.info(f'Created new SlackBot: {self.bot_name}.')

    def __repr__(self):
        """Identifies bot"""
        return f"{self.at_bot}"

    def __str__(self):
        """Identifies bot (meant for end user)"""
        return f"{self.at_bot}"

    def __enter__(self):
        """Implement this method to make this a context manager"""
        if self.slack_client.rtm_connect(with_team_state=False):
            logger.info(f"{self} is connected online")
            self.post_message(f"{self.bot_name} is running")
        self.bot_start = datetime.datetime.now()
        return self

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        logger.info(f"{self} is disconnected.")
        self.post_message("goodbye")

    def parse_slack_events(self):
        """Listens to slack events for our bot's name;
            returns command in channel"""
        slack_events = self.slack_client.rtm_read()  # command listnen
        for slack_event in slack_events:
            slack_event_gotten = slack_event.get("type")
            if slack_event_gotten == "message" and \
                    "subtype" not in slack_event:
                if slack_event["text"].startswith(self.at_bot):
                    chan = slack_event["channel"]
                    command = slack_event["text"][len(self.at_bot) + 1:]
                    logger.info(f"Got command {command} on channel {chan}")
                    return chan, command
        return None, None

    def post_message(self, msg, chan=BOT_CHANNEL, attachments=None):
        """Sends a message to a Slack Channel"""
        self.slack_client.api_call(
            "chat.postMessage",
            channel=chan,
            text=msg,
            attachments=attachments
        )

    def handle_command(self, chan, command):
        """
        Executes bot command if the command is known
        """
        # Default response is help text for the user
        logger.info(f"Received command {command} on channel {chan}")
        cmd = command.split()[0]
        if cmd not in bot_commands or cmd == 'help':
            help_text = formatted_dict(
                bot_commands, k_header="Swanson command",
                v_header="The Meaning of Swanson")
            # img = "https://thumbs.gfycat.com/MalePresentFlyinglemur-size_restricted.gif"
            img = "https://slack-redir.net/link?url=https%3A%2F%2Fthumbs.gfycat.com%2FMalePresentFlyinglemur-small.gif"
            response = (f'Stop being dense. Try one of '
                        f'these: \n ```{help_text}```')
            attachments = [{"title": "", "image_url": img}]

        if cmd == 'ping':
            uptime = (datetime.datetime.now() - self.bot_start).total_seconds()
            response = (f'Swanson lives and has done so '
                        f'for {uptime: .3f} seconds, dummy.')

        if cmd == 'exit':
            response = f'Swanson out.'
            global exit_flag
            exit_flag = True

        if cmd == 'speak':
            response = fetch_swanson()

        if cmd == 'see':
            response = fetch_cat()

        if cmd == 'meme':
            response = fetch_swanson() + "\n" + fetch_cat()

        if cmd == 'suffer':
            img = "https://media1.tenor.com/images/d94ef5a9025e88f6ca180284ff3c407e/tenor.gif?itemid=8268738"
            response = img

        if cmd == 'raise':
            raise Exception("User-generated exception.")

        if response:
            self.post_message(response, chan, attachments)


def main():
    """
    Runs the bot and it's commands as a long running program
    watches for sigint/sigterm signals
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    exception_flag = False

    with SlackBot("SLACK_BOT_TOKEN") as bot:
        while not exit_flag:
            try:
                if exception_flag:
                    # TODO: stretch goal fetch the last X number of lines in \
                    # the log to show the user
                    bot.post_message("YOU TRIED TO KILL ME! I WILL NEVER DIE!")
                exception_flag = False
                command_loop(bot)
                logger.debug("While loop...")
            except Exception as e:
                logger.error(str(e))
                logger.error(
                    'You tried to kill me. I will come back in 5 seconds.')
                exception_flag = True
                time.sleep(5)
            time.sleep(RTM_READ_DELAY)


if __name__ == "__main__":
    main()
