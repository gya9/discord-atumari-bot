import sys, discord, requests, json, traceback, time, asyncio, os, pickle
import numpy as np
import pandas as pd
import datetime as dt
from pytz import timezone
from keys import token_str, dev_id


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    # async def sendbotchannel(self, msg):
    #     '''bot用チャンネルに書き込む'''
    #     bot_channel = self.get_channel(id_bot_channel)
    #     await bot_channel.send(msg)

    async def send2developer(self, msg):
        '''開発者にDMを送る'''
        developer = self.get_user(dev_id)
        dm = await developer.create_dm()
        await dm.send(msg)

    async def send2user(self, user_id, msg):
        try:
            tmp_user = self.get_user(user_id)
            dm = await tmp_user.create_dm()
            await dm.send(msg)
        except Exception:
            await self.send2developer(traceback.format_exc())

    async def on_ready(self):
        msg = f'Logged on as {self.user}!'
        await self.send2developer(msg)

    async def on_message(self, message):
        """ メッセージ受信時のイベントハンドラ """
        try:
            if message.author.id == self.user.id:
                return

            if "高崎" in message.content:
                m = ":person_gesturing_no: 高崎　:person_gesturing_ok: 高先"
                await message.channel.send(m)

            if message.content.startswith("おはよう"):
                m = "おはようございます、" + message.author.name + "さん！"
                await message.channel.send(m)

            if message.content.startswith("おやすみ"):
                m = "おやすみなさい、" + message.author.name + "さん！"
                await message.channel.send(m)

            if message.content.startswith('!bye'): # 終了用コマンド
                await self.close()

        except Exception: # エラー発生時にはトレースバックがDMで送られてくる
            await self.send2developer(traceback.format_exc())

client = MyClient()
client.run(token_str)