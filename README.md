![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Slack_Technologies_Logo.svg/2000px-Slack_Technologies_Logo.svg.png)

In the next few days we are going to explore building a [Slackbot](https://www.entrepreneur.com/article/302409) using Python.  Of course there are many third-party platforms out there that can automate the process of creating AI-driven bots. But as emerging software engineers, we understand that by diving deep and exploring the nuts and bolts, we acquire a rich knowledge of _how_ things work which will serve us well in the future, as well as honing our set of general best practices.  Phase 1 is NOT a one-day assignment-- you will be researching, planning, and experimenting and task-switching between other activities this week.

This assignment integrates many concepts that you have learned over the last few weeks.  In the end, you will have created a slackbot framework that you can take with you to extend, adapt, and reuse in many ways.

### Phase 1: Bare Bones Bot

Your first implementation of the bot will run on your local development machine, and should be able to perform these basic functions:
*   Make sure you use python classes and objects when you implement. [Here](https://github.com/KenzieAcademy/backend-slackbot/) is a starter code and some suggested methods 
*   Connect your app to the [KenzieBot](https://kenziebot.slack.com) workspace as a bot user
*   Send a message to a channel announcing that it is online
*   Wait for and process events/messages in an infinite while-loop
*   Ignore any messages that don't contain a direct \`@mention\` of your bot name
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

Tips for Getting Started 
-------------------------

*   Join the [KenzieBot](https://join.slack.com/t/kenziebot/signup) slack workspace as yourself (this is not the Kenzie Academy slack).  Do this by requesting an invitation from the instructor.  After you join the workspace, the instructor (or other admin) will grant you Admin permissions.  You need Admin permission to create apps and bot users.
*   Read the fine documentation and tutorials about [building Slack Apps](https://api.slack.com/slack-apps), and creating bot users.
*   Investigate if there are any python packages such as **[python-slackclient](https://github.com/slackapi/python-slackclient)** that can help you.
*   Read about environment variables and how to bring them into your program.
*   Try out the simple yet elegant **[python-dotenv](https://github.com/theskumar/python-dotenv)** package to help load your environment variables from within python.
*   Ask for instructor or team help if you get stuck.  Ask in Cohort slack channel so all may benefit, if you feel comfortable.

And Finally ... 
----------------

[RIGHT THEN!   OFF YOU GO!](https://www.youtube.com/watch?v=nLJ8ILIE780)
