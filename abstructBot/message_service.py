import datetime
from functools import reduce
from db_service import read_contents


async def abst_message(ctx, message_id: int):
    msg = await ctx.fetch_message(message_id)
    guild = msg.guild
    users = await msg.reactions[0].users().flatten()
    if len(users) > 1:
        mention_str = reduce(concat_mention, users, '')
    else:
        mention_str = users[0].mention
    template1 = '明日の開催概要です！'
    template2 = '当日に仕事の事情や体調不良等ありましたら我慢せずご連絡ください。'
    msg_content = msg.content
    return f'{mention_str}\n\n{template1}\n\n{datetime_map_part(msg_content)}\n\n{template2}\n\n{member_part(guild, users)}{color_part(guild, users)}'


def concat_mention(user, pre_str):
    return f'{pre_str} {user.mention}'


def datetime_map_part(content: str):
    datetime_title_str = '【時間】'

    # 構文解析用に基準文字の index を取得
    index_of_brackets_start = content.find('[')
    index_of_wavy_line = content.find('~')
    index_of_brackets_end = content.find(']')
    index_of_content_end = content.find('【')

    # 日付の文字列
    date_str = content[0:index_of_brackets_start]

    # 集合時間の文字列
    start_time = content[index_of_brackets_start + 1:index_of_wavy_line]
    meeting_time = datetime.datetime.strptime(start_time, '%H:%M') - datetime.timedelta(minutes=15)
    meeting_time_str = meeting_time.strftime('%H:%M') + ' VC集合'

    # 開始時間の文字列
    start_time_str = f'{start_time} 配信開始'

    # 終了時間の文字列
    end_time = content[index_of_wavy_line + 1:index_of_brackets_end]
    end_time_str = f'{end_time}前後 解散'

    # マップ部分の作成
    map_title_str = '【マップ】'
    
    map_str = f'{content[index_of_brackets_end + 1:index_of_content_end]}'

    return f'{datetime_title_str}\n{date_str}\n{meeting_time_str}\n{start_time_str}\n{end_time_str}\n{map_title_str}{map_str}'


def member_part(guild, users):
    member_title_str = '【参加者一覧】'
    member_str_list = map(lambda u: member_contents_str(guild, u), users)
    concat_member_str = reduce(lambda str, pre: f'{pre}\n{str}', member_str_list, '')
    return f'{member_title_str}\n\n{concat_member_str}'


def member_contents_str(guild, user):
    user_id = user.id
    member = guild.get_member(user_id)
    contents = map(lambda c: c[2], read_contents(user_id))
    contents_str = reduce(lambda str, pre: f'{pre}\n{str}', contents, '')
    return f'{member.display_name}\n{contents_str}'


def color_part(guild, users):
    color_title_str = '【今回の色一覧です】\n※今までの使用色と全員の希望色から主催が勝手に選別致しました※'
    color_str_list = map(lambda u: color_str(guild, u), users)
    concat_color_str = reduce(lambda str, pre: f'{pre}\n{str}', color_str_list, '')
    return f'{color_title_str}\n\n{concat_color_str}'


def color_str(guild, user):
    member = guild.get_member(user.id)
    role = filter(lambda r: r.name[0] == '①', member.roles).__next__()
    return f'{member.display_name}・{role.name[1:]}'
