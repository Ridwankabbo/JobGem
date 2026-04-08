from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .ai_tools import search_jobs, applay_job
from .agent_logic import run_agent
from .models import ChatHistory
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.exceptions import ObjectDoesNotExist
import re

User = get_user_model()

class AiAgentConsummer(AsyncWebsocketConsumer):
    
    async def connect(self):
        token = self.scope['query_string'].decode().split('token=')[-1]
        
        try:
            validate_token = UntypedToken(token)
            user_id = validate_token['user_id']
            self.user = await database_sync_to_async(User.objects.get)(id=user_id)
            self.scope['user'] = self.user
        except(InvalidToken, ObjectDoesNotExist, KeyError):
            self.close(code=4001)
            return

        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "welcome",
            "message": "হ্যালো! আমি আপনার বাংলা জব এআই অ্যাসিস্ট্যান্ট। কোন জব খুঁজবেন বা অ্যাপ্লাই করবেন?"
        }, ensure_ascii=False))
        
        
    async def receive(self, text_data = None):
        data = json.loads(text_data)
        message = data['message']
        
        chat_history = await database_sync_to_async(ChatHistory.objects.create)(
            user = self.user, message=message
        )
        
        history = await self.get_history()
        
        agent_response = await database_sync_to_async(run_agent)(
            user_query=message,
            history_list=history,
        )
        
        # Save agent reply
        chat_history.response=agent_response
        await database_sync_to_async(chat_history.save)()
        
        message_text = re.search(r"MESSAGE:\s*(.*?)(?=DATA:|$)", agent_response, re.DOTALL)
        data_json = re.search(r"DATA:\s*(\[.*\])", agent_response, re.DOTALL)
        
        chat_text = message_text.group(1).strip() if message_text else data_json
        
        product_data=[]
        
        if data_json:
            try:
                product_data = json.loads(data_json.group(1))
            except:
                product_data = []
        
        
        # Send back to React (frontend can parse MESSAGE / DATA)
        
        await self.send(text_data=json.dumps({
            "type": "agent_response",
            "message": chat_text,
            "data": product_data
        }, ensure_ascii=False))
    
    # async def send_responsed(self, message, data):
    #     await self.send(text_data=json.dumps({
    #         "type": "agent_response",
    #         "message": message,
    #         "data": data
            
    #     }, ensure_ascii=False))
    
    
    @database_sync_to_async
    def get_history(self):
        msgs = ChatHistory.objects.filter(user=self.user).order_by('-responsed_at')[:10]
        return [
            {"user": m.message , 
             "agent": m.response}
            for m in msgs
        ]
     



