from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from restltform.models import follow
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,get_object_or_404
User=get_user_model()
class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self,data):
        #print("fetching",data)
        reciver=data['to'].replace(data['from'],"")
        from_user=get_object_or_404(User,username=data['from'])
        reciver_user=get_object_or_404(User,username=reciver)
        messages=Message.get_messages(from_user=from_user,to_user=reciver_user)
        #messages=Message.last_10_messages(Message)
        content={
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_message(content)
    def new_message(self,data):
        #print("new")
        author=data['from']
        reciver=data['to'].replace(author,"")
        reciver_obj=get_object_or_404(User,username=reciver)
        author_user=User.objects.filter(username=author)[0]
        message=Message.objects.create(author=author_user,content=data['message'],reciver=reciver_obj)
        content={
            'command':'new_message',
            'message':{'author':message.author.username,'content':message.content,'timestamp':str(message.timestamp)}
        }

        return self.send_chat_message(content)
    def messages_to_json(self,messages):
        result=[]
        for msg in messages:
            result.append({'author':msg.author.username,'content':msg.content,'timestamp':str(msg.timestamp)})
        return result
    commands={
        "fetch_messages":fetch_messages,
        "new_message":new_message
    }
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user=self.scope['user']
        #print(user.profile_user.status)
        _user=get_object_or_404(follow,user=user)
        _user.status=True
        _user.save()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        user=self.scope['user']
        _user=get_object_or_404(follow,user=user)
        _user.status=False
        _user.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data= json.loads(text_data)
        #print(data)
        self.commands[data['command']](self,data)
        # Send message to room group
    def send_chat_message(self,message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def send_message(self,message):
        self.send(text_data=json.dumps(message))
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))