from functools import reduce

async def create_css(channel, message_id):
    msg = await channel.fetch_message(message_id)
    users = msg.mentions
    colors_str = color_part(users, msg.content)
    common_str = common_part()
    css_str = ['各メンバーカラー部分です。' + '```css\n' + colors_str + '```', '共通部分です。' + '```css\n' + common_str + '```']
    return css_str


def common_part():
    return '.voice-container .voice-states .voice-state .avatar {\n  height: 100px;\n  width: 100px;\n  border-radius: 10%;\n}\n.voice-container .voice-states .voice-state .user .name {\n    position: absolute;\n    top: 79px;\n    left: 6px;\n    max-width: 65px;\n    white-space: nowrap;\n    overflow: hidden;\n}\n.voice-container .voice-states .voice-state {\n  display: inline-block;\n  position: relative;\n}\n.voice-container .avatar {\n    border: 6px solid white !important;\n}\n.avatar.speaking,\n.avatar.speaking + .user {\n    transform: translateY(-17px);\n}\n.avatar.speaking + .user .name {\n    background: #41DAC6!important;\n}\n.avatar.speaking + .user .name::before {\n    animation: speaking 0.2s ease 0s forwards;\n}\n'


def color_part(users, msg_content):
    colors_str_list = map(lambda u: color_id_concat(u, msg_content), users)
    colors_str = reduce(lambda str, pre: f'{pre}\n{str}', colors_str_list, '')
    return colors_str


def color_id_concat(user, msg_content):
    idx = msg_content.rfind(user.display_name) + len(user.display_name) + 1
    color_str = msg_content[idx:idx + 3]
    return color_css_str(user.id, color_str)


def color_css_str(id, color_str):
    str1 = '.voice-container .voice-state[data-reactid*="%s"] .avatar {' % id
    str2 = ''
    if color_str == 'レッド':
        str2 = '    border: 6px solid red !important;'
    elif color_str == 'ブルー':
        str2 = '    border: 6px solid blue !important;'
    elif color_str == 'グリー':
        str2 = '    border: 6px solid green !important;'
    elif color_str == 'ピンク':
        str2 = '    border: 6px solid fuchsia !important;'
    elif color_str == 'オレン':
        str2 = '    border: 6px solid orange !important;'
    elif color_str == 'パープ':
        str2 = '    border: 6px solid purple !important;'
    elif color_str == 'イエロ':
        str2 = '    border: 6px solid yellow !important;'
    elif color_str == 'ブラッ':
        str2 = '    border: 6px solid black !important;'
    elif color_str == 'ホワイ':
        str2 = '    border: 6px solid white !important;'
    elif color_str == 'シアン':
        str2 = '    border: 6px solid aqua !important;'
    elif color_str == 'ライム':
        str2 = '    border: 6px solid lime !important;'
    elif color_str == 'ブラウ':
        str2 = '    border: 6px solid saddlebrown !important;'
    elif color_str == 'コーラ':
        str2 = '    border: 6px solid lightcoral !important;'
    elif color_str == 'グレー':
        str2 = '    border: 6px solid gray !important;'
    elif color_str == 'マルー':
        str2 = '    border: 6px solid maroon !important;'
    elif color_str == 'バナナ':
        str2 = '    border: 6px solid lemonchiffon !important;'
    elif color_str == 'ローズ':
        str2 = '    border: 6px solid #FFD5EC !important;'
    elif color_str[:2] == 'タン':
        str2 = '    border: 6px solid #666633 !important;'
    else:
        str2 = ''
    str3 = '}'
    return f'{str1}\n{str2}\n{str3}\n'
