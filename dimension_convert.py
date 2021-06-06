from mcdreforged.api.command import Literal, IllegalArgument

PLUGIN_METADATA = {
    'id': 'dimension_convert.py',
    'version': '1.0.0',
    'name': 'Dimension Convert',
    'description': 'A plugin to convert dimension coordinate.',
    'author': 'eleven',
    'link': 'https://github.com/ActiniumCraft/dimension-convert',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}

HELP_MESSAGE = '''
================= 维度坐标转换 ==================
转换主世界和地狱的对应坐标，快速搭建地狱交通。
Github: https://github.com/ActiniumCraft/dimension-convert
!!cdc 显示帮助信息
!!cdc overworld x z 将主世界坐标转为地狱坐标
!!cdc nether x z 将地狱坐标转为主世界坐标
'''


def is_args_length_match(args: list, length: int):
    return len(args) == length


def on_info(server, info):
    user_args: list = info.content.split(' ')

    if not user_args[0] == '!!cdc':
        return

    if is_args_length_match(user_args, 1):
        server.reply(info, HELP_MESSAGE)

    if is_args_length_match(user_args, 4):
        x_coordinate = float(user_args[2])
        z_coordinate = float(user_args[3])
        converted_coordinate = [0, 0]
        if user_args[1] == 'nether':
            converted_coordinate = [int(x_coordinate*8), int(z_coordinate*8)]
        if user_args[1] == 'overworld':
            converted_coordinate = [int(x_coordinate/8), int(z_coordinate/8)]
        server.reply(info, '对应维度坐标: x = {}, z = {}'.format(converted_coordinate[0], converted_coordinate[1]))


def on_load(server, prev):
    server.register_help_message('!!cdc', '转换主世界和地狱的对应坐标')
