import os
import discord
from dotenv import load_dotenv

from message_service import abst_message, member_contents_str
from db_service import init_setting, add_member, delete_contents

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
    if word_list[0] == '/sd':
        if word_list[1] == 'abst':
            # try:
                channel_id = int(word_list[2])
                message_id = int(word_list[3])
                msg = await abst_message(message.guild, channel_id, message_id)
                await message.channel.send(msg)
                await message.delete()
            # except:
                # await message.channel.send('なんか知らんけど無理だった')
            # finally:
                # await message.delete()
        elif word_list[1] == 'add':
            user_id = int(word_list[2])
            content_list = word_list[3:]
            add_member(content_list, user_id)
            await message.channel.send(f'{user_id}を登録しました。')
        elif word_list[1] == 'del':
            user_id = int(word_list[2])
            delete_contents(user_id)
            await message.channel.send(f'{user_id}を削除しました。')
        else:
            await message.channel.send('コマンドとして許可されているのは "abst" と "add" のみです。')
    if word_list[0] == '/setting_db':
        init_setting()


client.run(TOKEN)
