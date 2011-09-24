#!/usr/bin/env python3
# ----------------------------------------------------------------------------  
# "THE BEER-WARE LICENSE" (Revision 42):  
# <danneh@danneh.net> wrote this file. As long as you retain this notice you  
# can do whatever you want with this stuff. If we meet some day, and you think  
# this stuff is worth it, you can buy me a beer in return Daniel Oakley  
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module
from gbot.libs.girclib import escape, unescape
import urllib.request, urllib.parse, urllib.error
import json

class google(Module):
    name = 'google'
    
    def __init__(self):
        self.events = {
            'commands' : {
                'google' : [self.google_search, '<query> --- google something, get results', 0],
                'youtube' : [self.youtube_search, '<query> --- searches, then returns youtube video', 0],
            },
        }
    
    def google_search(self, event, command):
        calc_result = self.google_calc_search(command.arguments)
        if calc_result:
            response = '*** /c12G/c4o/c8o/c12g/c3l/c4e/c: ' + calc_result
            self.bot.irc.servers[event.server].privmsg(event.from_to, response)
            return
        
        encoded_query = urllib.parse.urlencode({b'q' : unescape(command.arguments)})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (encoded_query)
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape(json_result['responseData']['results'][0]['unescapedUrl'])
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** /c12G/c4o/c8o/c12g/c3l/c4e/c: ' + url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)
    
    def google_calc_search(self, query):
        url = 'http://www.google.com/ig/calculator?'
        url += urllib.parse.urlencode({b'q' : unescape(query)})
        
        calc_result = urllib.request.urlopen(url)
        calc_read = calc_result.read().decode('utf-8')
        calc_split = calc_read.split('"')
        
        try:
            #q_from = json_result['lhs']
            #q_to = json_result['rhs']
            q_from = calc_split[1]
            q_to = calc_split[3]
            if q_from == '' or q_to == '':
                return False
            final_result = '/i' + escape(q_from) + '/i is /i' + escape(q_to) + '/i'
        except:
            final_result = False
        
        return final_result
    
    def youtube_search(self, event, command):
        encoded_query = urllib.parse.urlencode({b'q' : unescape(command.arguments)})
        url = 'http://gdata.youtube.com/feeds/api/videos?alt=jsonc&v=2&max-results=1&%s' % (encoded_query)
        
        try:
            search_results = urllib.request.urlopen(url)
            json_result = json.loads(search_results.read().decode('utf-8'))
            try:
                url_result = escape(json_result['data']['items'][0]['title'])
                url_result += escape(' - http://youtu.be/')
                url_result += escape(json_result['data']['items'][0]['id'])
            except:
                url_result = 'No Results'
        except urllib.error.URLError:
            url_result = 'Connection Error'
        
        response = '*** You/c5Tube/c: '+url_result
        
        self.bot.irc.servers[event.server].privmsg(event.from_to, response)