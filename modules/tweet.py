#!/usr/bin/env python3 
# written by Justin Wu <amersel@bibanon.org>

import json
import os

import twitter
from gbot.modules import Module
from gbot.libs.helper import filename_escape

class twitter_post(Module):
    """Lets admins post to bibanon twitter accout."""
    def __init__(self, bot):
        Module.__init__(self, bot)

        self.parse_required_value('twitter', 'consumer_key', {
            'prompt': 'Twitter consumer key:',
            'type': 'str',
        })
        self.parse_required_value('twitter', 'consumer_secret', {
            'prompt': 'Twitter consumer secret:',
            'type': 'str',
        })
        self.parse_required_value('twitter', 'access_token_key', {
            'prompt': 'Twitter access token key:',
            'type': 'str',
        })
        self.parse_required_value('twitter', 'access_token_secret', {
            'prompt': 'Twitter access token secret:',
            'type': 'str',
        })

        values = self.get_required_values('twitter')

        self.api = twitter.Api(consumer_key = values['consumer_key'],
                               consumer_secret = values['consumer_secret'],
                               access_token_key = values['access_token_key'],
                               access_token_secret = values['access_token_secret'])
        
    def cmd_twitter(self, event, command, usercommand): #post message to twitter
        """Tweet a message using the twitter api
        @usage <query>
        @alias tweet
        @channel_mode_restriction v
        """
        try:
            msg = usercommand.arguments
            status = self.api.PostUpdate(msg)
            response = '*** Message tweeted: ' + '\'' + status.text + '\''
            
        except:
            response = '*** Could not post message.'
            
            statuses = self.api.GetHomeTimeline()
            text = [s.text for s in statuses]
            if msg in text:
                response = '*** Message already exists!'
                    
            if len(msg) > 140:
                response = '*** Message longer than 140 characters.'
            
            
        event['from_to'].msg(response)

