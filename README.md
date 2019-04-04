<img align=left width=200 src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Slack_Technologies_Logo.svg/2000px-Slack_Technologies_Logo.svg.png" /><br clear=left>

In the next few days we are going to explore building a [Slackbot](https://www.entrepreneur.com/article/302409) using Python.  Of course there are many third-party platforms out there that can automate the process of creating AI-driven bots. But as emerging software engineers, we understand that by diving deep and exploring the nuts and bolts, we acquire a rich knowledge of _how_ things work which will serve us well in the future, as well as honing our set of general best practices.  Phase 1 is NOT a one-day assignment-- you will be researching, planning, and experimenting and task-switching between other activities this week.

This assignment integrates many concepts that you have learned over the last few weeks.  In the end, you will have created a slackbot framework that you can take with you to extend, adapt, and reuse in many ways.

### Phase 1: Bare Bones Bot

Your first implementation of the bot will run on your local development machine, and should be able to perform these basic functions:
*   Connect your app to the [KenzieBot](https://kenziebot.slack.com) or [KenzieBot2](https.kenziebot2.slack.com) workspace as a bot user
*   Send a message to a default channel announcing that your bot is online
*   Wait for and process slack events/messages in an infinite while-loop
*   Ignore any messages that don't contain a direct `@mention` of your bot name
*   Exit your bot program if you receive an exit message.  For example, if your bot is named \`example-bot\` then your program should exit gracefully when it receives a slack message such as \`@example-bot exit\`

### Guidance Notes

This assignment will be more of a free-form creative endeavor than in your previous work.  You will be required to submit a link to a github repo named **backend-kenziebot-assessment**, but you will create and curate this repository on your own instead of forking a Kenzie repo.  Remember that your work on github will become your own personal portfolio that you will want to show off to recruiters and potential employers.  In addition, you will be building additional functionality into your Slackbot in Phase 2 of this assignment.  With that said, here are a few best-practices that we will be looking for in your repo:

#### **Source Code Best Practices**

*   PEP8: No warnings
*   if \_\_name\_\_ == "\_\_main\_\_" Python idiom
*   Docstrings and #comments for functions and modules
*   Unit Tests that are discoverable and passing
*   Non-monolithic structure (short, concise functions)
*   Readability, maintainability

#### **Development Best Practices**

*   Research and plan.
*   Create and use a virtual environment
*   Pip-install any new packages into your virtualenv
*   Configure your IDE to use the interpreter from your virtual environment
*   Use your IDE and debugger to run, step, and view
*   Use local environment variables for API tokens and keys

#### **Repo Best Practices**

*   Have a descriptive top-level README.md
*   .gitignore is present, with .vscode/ and .env
*   requirements.txt from pip freeze
*   No hard-coded API keys or tokens anywhere.  [DO NOT LEAK TOKENS](https://labs.detectify.com/2016/04/28/slack-bot-token-leakage-exposing-business-critical-information/).
*   [Small commits](https://blog.hartleybrody.com/git-small-teams/)
*   LICENSE file

### **Deployment Details**

NOTE: This section assumes that you have already created a Heroku account from previous assignments, and you have the [Heroku CLI tools](https://devcenter.heroku.com/articles/heroku-cli) installed on your local development machine.  
Most of the python Heroku deployment examples on the internet assume that you are developing a web app, but in this case you are deploying a simple standalone python script without a framework or WSGI gateway.  In order to deploy your bot to Heroku, your github repo must contain some special files named \`Procfile\` and \`runtime.txt\`.  Procfile tells Heroku which program to run when you activate your free dyno instance.  Procfile contents should look like this:

worker: python slackbot.py

Runtime.txt tells Heroku which python interpreter version to use, when it constructs a docker image for your slackbot.  You should select a version that matches the one that you used while developing in your virtual environment.  See which python versions are supported by Heroku [here](https://devcenter.heroku.com/articles/python-runtimes).  Sample contents of \`runtime.txt\`:

python-3.6.6

Your slackbot application is designed to be long-running, so it seems natural to try and deploy it on a cloud hosting platform such as Heroku.  However, Heroku limits the free-tier cloud hosting 'dynos' to a maximum uptime of 18 hours per 24-hour period.  So your bot will be forcibly euthanized every so often (unless you upgrade to Hobby tier -- $7.00/month). 

    heroku create my_unique_slackbot_namegit push heroku master

Remember that your .env file should contain your slackbot API tokens, and it should not be part of your repo (that is, .env should be listed in your .gitignore).  You will need to copy your API tokens directly into Heroku config vars:

heroku config:set BOT\_USER\_TOKEN="xoxb-431941958864-124971466353-2Ysn7vyHOUkzjcABC76Tafrq"

Now everything should be ready to run.  Start up your slackbot and check the logs:

    heroku ps:scale worker=1

Tips for Getting Started 
-------------------------

*   Join the [KenzieBot](https://join.slack.com/t/kenziebot/signup) slack workspace as yourself (this is not the Kenzie Academy slack).  Do this by requesting an invitation from the instructor.  After you join the workspace, the instructor (or other admin) will grant you Admin permissions.  You need Admin permission to create apps and bot users.
*   Read the fine documentation and tutorials about [building Slack Apps](https://api.slack.com/slack-apps), and creating bot users.
*   Investigate if there are any python packages such as **[python-slackclient](https://github.com/slackapi/python-slackclient)** that can help you.
*   Read about environment variables and how to bring them into your program.
*   Try out the simple yet elegant **[python-dotenv](https://github.com/theskumar/python-dotenv)** package to help load your environment variables from within python.
*   Ask for instructor or team help if you get stuck.  Ask in Cohort slack channel so all may benefit, if you feel comfortable.

