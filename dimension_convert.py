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
!!cdc overworld x y z 将主世界坐标转为地狱坐标
!!cdc nether x y z 将地狱坐标转为主世界坐标
'''


def on_load(server, prev):
    server.register_help_message('!!cdc', '转换主世界和地狱的对应坐标')
