#!/usr/bin/env python
# coding:utf8

import json
import requests
import logging

logging.basicConfig(filename='DingTalkChatbot.log', filemode='a', level=logging.DEBUG)

class DingTalkChatbot(object):
    def __init__(self, webhook):
        """
        初始化webhook
        """
        super(DingTalkChatbot, self).__init__()
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = webhook
        
    def post(self, data):
        data = json.dumps(data)
        logging.debug(data)
        try:
            response = requests.post(self.webhook, headers=self.headers, data=data)
            logging.debug(response.json())
            return response.json()
        except:
            raise
    
    def sendtext(self, content='', atMobiles=[], isAtAll=False):
        """发送消息类型为text
        
        Args:
            content: 消息内容
            isAtAll： @所有人时：true，否则为false(可选)
            atMobiles: 被@人的手机号(在content里添加@人的手机号)(可选)
        
        return: 返回消息发送结果
        """
        data = {"msgtype": "text", "at": {}}
        if not content.strip():
            logging.error("content is null!")
            raise Exception("content is null!")
        else:
            data["text"] = {"content": content}
            
        if isAtAll:
            data["at"]["isAtAll"] = isAtAll
        
        if atMobiles:
            atMobiles = list(map(str, atMobiles))
            data["at"]["atMobiles"] = atMobiles
        
        return self.post(data)
    
    def sendlink(self, title='', text='', messageUrl='', picUrl=''):
        """发送消息类型为link
        
        Args:
            title： 消息标题
            text: 消息内容。如果太长只会部分展示
            messageUrl: 点击消息跳转的URL
            picUrl: 图片URL(可选)
        
        return: 返回消息发送结果
        """
        if not title.strip():
            logging.error("title is null!")
            raise Exception("title is null!")
        elif not text.strip():
            logging.error("text is null!")
            raise Exception("text is null!")
        elif not messageUrl.strip():
            logging.error("messageUrl is null!")
            raise Exception("messageUrl is null!")
        else:
            data = {"msgtype": "link", "link": {"title": title, "text": text, "messageUrl": messageUrl, "picUrl": picUrl}}
        
        return self.post(data)
    
    def sendmarkdown(self, title='', text='', atMobiles=[], isAtAll=False):
        """发送消息类型为markdown
        
        Args:
            title： 首屏会话透出的展示内容
            text: markdown格式的消息
            atMobiles: 被@人的手机号(在text内容里要有@手机号)(可选)
            isAtAll: @所有人时：true，否则为：false(可选)
        
        return: 返回消息发送结果
        """
        if not title.strip():
            logging.error("title is null!")
            raise Exception("title is null!")
        elif not text.strip():
            logging.error("text is null!")
            raise Exception("text is null!")
        else:
            data = {"msgtype": "markdown", "markdown": {"title": title, "text": text, "at": {}}}  
            
        if isAtAll:
            data["at"]["isAtAll"] = isAtAll
            
        if atMobiles:
            atMobiles = list(map(str, atMobiles))
            data["at"]["atMobiles"] = atMobiles
        
        return self.post(data) 

