slack-roulettebot
=================
A Slack bot based [Python-rtmbot](https://github.com/slackhq/python-rtmbot) to play Chatroulette with your team members


Installation
------------

1. Download the code

```
    git clone git@github.com:AcroMace/slack-roulettebot.git
    cd slack-roulettebot
```

2. Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

```
    pip install -r requirements.txt
```

3. Add the bot to your team by going to Slack [here](https://slack.com/services/new) and adding the "Bots" option in "DIY Integrations & Customizations"

4. Copy and paste the API Token into the `rtmbot.conf` file between the quotes for `SLACK_TOKEN`

5. Start the bot by running `./rtmbot.py`


How to use
----------

The format of the commands were taken from the [Slackroulette](http://slackroulette.com) project:

```
!online  - Become available to chat with others
!offline - Stop participating
!spin    - Start a conversation
!leave   - Leave the current conversation
```

