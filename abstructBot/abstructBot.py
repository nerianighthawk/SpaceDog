import os
import discord
from dotenv import load_dotenv

from message_service import abst_message
from db_service import init_setting, add_member

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# 環境変数からトークンを取得
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.typing = False
client = discord.Client(intents=intents)


@client.event
async def on_message(message: discord.Message):
    word_list = message.content.split()
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if word_list[0] == '/spacedog':
        try:
            if word_list[1] == 'abst':
                message_id = int(word_list[2])
                msg = await abst_message(message.channel, message_id)
                await message.channel.send(msg)
            elif word_list[1] == 'add':
                user_id = int(word_list[2])
                content_list = word_list[3:]
                add_member(content_list, user_id)
                await message.channel.send('登録しました。')
            else:
                await message.channel.send('コマンドとして許可されているのは "abst" と "add" のみです。')
        except:
            await message.channel.send('なんか知らんけど無理だった')
        finally:
            await message.delete()
    if word_list[0] == '/setting_db':
        init_setting()


client.run(TOKEN)
