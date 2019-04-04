<img align=left width=200 src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Slack_Technologies_Logo.svg/2000px-Slack_Technologies_Logo.svg.png" /><br clear=left>

In the next few days we are going to explore building a [Slackbot](https://www.entrepreneur.com/article/302409) using Python.  Of course there are many third-party platforms out there that can automate the process of creating AI-driven bots. But as emerging software engineers, we understand that by diving deep and exploring the nuts and bolts, we acquire a rich knowledge of _how_ things work which will serve us well in the future, as well as honing our set of general best practices.  Phase 1 is NOT a one-day assignment-- you will be researching, planning, and experimenting and task-switching between other activities this week.

This assignment integrates many concepts that you have learned over the last few weeks.  In the end, you will have created a slackbot framework that you can take with you to extend, adapt, and reuse in many ways.

### Learning Objectives
 - Become comfortable with self-guided API research and experimentation
 - Create, test, deploy, manage a long running program in a cloud environment 
 - Apply best practices in repository structure
 - Use a virtual environment on a project
 - Learn how to create an integration between two APIs

### Goal
The goal is to create a long-running Slackbot that responds to user commands, and integrates to a secondary API to acquire data.  The secondary API choice is up to the student, and can be any open api that provides some interesting data that can be present in a slack channel and does not require a paid subscription.  A list of public APIs is available [here](https://github.com/toddmotto/public-apis)

### Setup - Slack
For this assignment, we will be using two separate, private Slack Team accounts.  These accounts are only used by the SE cohorts for this assignment, there are no other users.  The reason for using two separate accounts is because Slack free team accounts limit the number of app integrations to max of 10.  Please ask your instructor to send you the self signup links when you are ready.  Once you are in, send a msg to your instructor to ask for admin privilege.  You will need `admin` to create a bot application.


### Part A: Slackbot Client
 - Create a virtual environment for your project
 - Install the [slackclient](https://python-slackclient.readthedocs.io/en/latest/) python library in your virtual environment.
 - Implement your slackbot using a Python class object.  Starter code is available in [slackbot.py](slackbot.py)
 - Connect your app to one of the KenzieBot workspaces as a bot user
 - Send a message to a default channel announcing that your bot is online
 - Wait for and process events/messages in an infinite while-loop
 - Ignore any messages that don't contain a direct `@mention` of your bot name
 - Create a command parser that can act upon any command directed at your bot
 - Be sure to implement a `help` command that lists all commands that your bot understands
 - Implement `ping` command that will show the uptime of the bot
 - Implement an internal self-test command that will `raise` different kinds of exceptions within your bot.  This will help to "harden" your bot against unforeseen errors, and test its recovery path.
 - Exit your bot program if you receive an exit command.  For example, if your bot is named `example-bot` then your program should exit gracefully when it receives a slack message such as `@example-bot exit`

### Part B: API Integration
Now that you have a working Slack client that responds to commands, connect it to another API.  Fetch a picture, or a stock price, or the weather forecast or a traffic report.  Have the bot render the data back to the slack channel.


### Deployment Details

NOTE: This section assumes that you have already created a Heroku account from previous assignments, and you have the [Heroku CLI tools](https://devcenter.heroku.com/articles/heroku-cli) installed on your local development machine.  
Most of the python Heroku deployment examples on the internet assume that you are developing a web app, but in this case you are deploying a simple standalone python script without a framework or [WSGI gateway](https://www.fullstackpython.com/wsgi-servers.html).  In order to deploy your bot to Heroku, your github repo must contain some special files named `Procfile` and `runtime.txt`.  Procfile tells Heroku which program to run when you activate your free dyno instance.  Procfile contents should look like this:

    worker: python slackbot.py

Runtime.txt tells Heroku which python interpreter version to use, when it constructs a docker image for your slackbot.  You should select a version that matches the one that you used while developing in your virtual environment.  See which python versions are supported by Heroku [here](https://devcenter.heroku.com/articles/python-runtimes).  Sample contents of `runtime.txt`:

    python-3.7.2

Your slackbot application is designed to be long-running, so it seems natural to try and deploy it on a cloud hosting platform such as Heroku.  However, Heroku limits the free-tier cloud hosting 'dynos' to a maximum uptime of 18 hours per 24-hour period.  So your bot will be forcibly euthanized every so often (unless you upgrade to Hobby tier -- $7.00/month). 

    heroku create my_unique_slackbot_name
    git push heroku master

Remember that your .env file should contain your slackbot API tokens, and it should not be part of your repo (that is, .env should be listed in your .gitignore).  You will need to copy your API tokens directly into Heroku config vars:

    heroku config:set BOT_USER_TOKEN="xoxb-431941958864-124971466353-2Ysn7vyHOUkzjcABC76Tafrq"

Now everything should be ready to run.  Start up your slackbot and check the logs:

    heroku ps:scale worker=1

## Guidance Notes
You will submit a link to a github repository, but you will create and curate this repository on your own instead of forking a Kenzie repo.  Remember that your work on github will become your own personal portfolio that you will want to show off to recruiters and potential employers.   With that said, here are a few best-practices that we will be looking for in your repo:

### Source Code Best Practices
 - PEP8: No warnings
 - if `__name__ == "__main__"` Python idiom
 - Docstrings and #comments for functions and modules
 - `__authors__` = "My Name"
 - Non-monolithic structure (short, concise class methods) that mostly adhere to the [single-responsibility](https://en.wikipedia.org/wiki/Single_responsibility_principle)
 - Readability, maintainability

### Development Best Practices
 - Collaborate with your Teammate. Research and plan .. Use VSCode Liveshare for pairing sessions
 - Create and use a project virtual environment
 - Pip-install any new packages into your virtualenv
 - Configure your IDE to use the interpreter from your virtual environment
 - Use your IDE and debugger to run, step, and view
 - Use local environment variables for API tokens and keys
 - Use python logging (not print statements) for all output messages.

### Repo Best Practices
 - Have a descriptive top-level README.md.  If you don't know what a good README looks like, google "README best practices"
 - `.gitignore` is present, ingorning `.vscode/` and `.env` and `.log` and `venv/`
 - `requirements.txt` from pip freeze
 - No hard-coded API keys or tokens anywhere.  [**DO NOT LEAK TOKENS**](https://labs.detectify.com/2016/04/28/slack-bot-token-leakage-exposing-business-critical-information/)
 - [Small commits](https://blog.hartleybrody.com/git-small-teams/) with meaningful messages-- not "more changes" or "blah foo bar" or "asdfadfadfadfadfasdfasdf"
 - Don't commit log files or virtual envs to the repo!

**Logging** - Your Slackbot app should log to both the console and a file.  Low-frequency events should be logged at INFO level, and high-frequency at DEBUG.  Exception handlers should log at ERROR or above for anything unhandled. Other levels are self-explanatory.  Use an environment variable to select logging output level when your Bot starts.  Log startup and shutdown events, as well as slack client connection info and any disconnect events.  Log every message that your Bot receives and sends to the Slack API.  Manage your file logging with some kind of time rotation or deleting schedule so that logs do not grow unbounded.  The Python logging module has built-in ways to do this.

**OS Signal Handling** - Your Bot should handle SIGTERM and SIGINT just like in the Dirwatcher assignment.  Log every OS signal that your Bot receives.  In a free-dyno Heroku deployment, your program WILL receive a SIGTERM at least once per day, when it wants your Bot to go to sleep.  Take that opportunity to gracefully close any open connections to Slack or other API and send a buh-bye message.

**Exception Handling** - Bot should not ever exit unless it is requested (either by user command or OS signal).  Your Bot should handle exceptions in order from most detailed (narrow, specific) to most broad.  Unhandled exceptions (the ones without specific handlers) should log full stack traces.  Strive for high availability by running your Bot in a local test environment for as long as you can.  We have a linux desktop server on site for this. Harden against wifi outages and whimsical disconnections of your slack and twitter clients by inserting exception handlers for specific cases you encounter.  When you catch an unhandled exception, pause for a few seconds before restarting your loop.  Don't spam the logs with a ton of "Restarting ..." messages-- allow a few moments for the OS process manager to send your Bot a SIGINT or SIGTERM if the process monitor thinks that Bot is misbehaving.  You can test your exception handler by adding a special bot command of your own design, that will manually raise any exception from within your program.   Hint:  This uses the `raise` Python function ..

## Demos
Group demos of their slackbot projects are TBD depending on how fast the end of quarter is approaching.  Please see your instructor if you would like to demo a cool extra feature that you added to your app.  Otherwise, we'll mostly be seeing the fruits of your project effort unfold before us, in the KenzieBot and KenzieBot2 slack workspaces.

## Final Words
This assignment brings together many concepts that you have learned in the preceding months.  While it is not an SE capstone project, it does have significant point value and we encourage your team to get started early.  Good Luck!!
