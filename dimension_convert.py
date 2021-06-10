from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'dimension_convert',
    'version': '1.1.0',
    'name': 'Dimension Convert',
    'description': 'A plugin to convert dimension coordinate.',
    'author': 'eleven',
    'link': 'https://github.com/ActiniumCraft/dimension-convert',
    'dependencies': {
        'mcdreforged': '>=1.0.0',
        'minecraft_data_api': '*'
    }
}

HELP_MESSAGE = '''
================= §b维度坐标转换§r ==================
§l转换主世界和地狱的对应坐标，快速搭建地狱交通。§r
§6Github: https://github.com/ActiniumCraft/dimension-convert§r
§7!!cdc§r 显示帮助信息
§7!!cdc here§r 将玩家当前所在坐标转换为对应坐标
§7!!cdc overworld x z§r 将主世界坐标转为地狱坐标
§7!!cdc nether x z§r 将地狱坐标转为主世界坐标
'''


def is_args_length_match(args: list[str], length: int) -> bool:
    """Compare the args list by giving length.

    :param args: The args list. For example: ['!!cdc', 'nether', '8', '8'].
    :param length: The args expects to be. For example: 4 match giving args list ['!!cdc', 'nether', '8', '8'].
    :return: The bool value. True when args length match; otherwise, it's False.
    """
    return len(args) == length


def convert_dimension_coordinate(dimension: str, x_coord: float, z_coord: float) -> dict[str, int]:
    """Convert nether/overworld dimension coordinate to its opposites dimension.

    :param dimension: The dimension name, value args are 'nether' and 'overworld'.
    :param x_coord: The x coordinate used in converting.
    :param z_coord: The z coordinate used in converting.
    :return: A dict[str, int] store the coordinate information, keys are x and z.
    """
    coordinate = {'x': 0, 'z': 0}
    if dimension == 'nether':
        coordinate = {'x': int(x_coord * 8), 'z': int(z_coord * 8)}
    if dimension == 'overworld':
        coordinate = {'x': int(x_coord / 8), 'z': int(z_coord / 8)}
    return coordinate


@new_thread(PLUGIN_METADATA['name'])
def execute_convert_command_by_player_coordinate(source: Info) -> None:
    """Execute the dimension convert command by giving player command source info.

    :param source: The command source info.
    :return: None.
    """
    api = source.get_server().get_plugin_instance('minecraft_data_api')
    coordinate = api.get_player_coordinate(source.player)
    dim_convert_dict = {0: 'overworld', -1: 'nether'}
    dimension = dim_convert_dict[api.get_player_dimension(source.player)]
    converted_coordinate = convert_dimension_coordinate(dimension, coordinate.x, coordinate.z)
    source.get_server().reply(source, '对应维度坐标: x = {}, z = {}'.format(converted_coordinate['x'],
                                                                      converted_coordinate['z']))


def convert_if_command_is_here(user_args, info) -> None:
    if user_args[1] == 'here':
        execute_convert_command_by_player_coordinate(info)


def on_user_info(server: ServerInterface, info: Info):
    user_args = info.content.split(' ')
    command_prefix = user_args[0]

    if not command_prefix == '!!cdc':
        return

    if is_args_length_match(user_args, 1):
        server.reply(info, HELP_MESSAGE)

    if is_args_length_match(user_args, 2):
        convert_if_command_is_here(user_args, info)

    if is_args_length_match(user_args, 4):
        dimension = user_args[1]
        x_coordinate = float(user_args[2])
        z_coordinate = float(user_args[3])

        converted_coordinate = convert_dimension_coordinate(dimension, x_coordinate, z_coordinate)
        server.reply(info, '对应维度坐标: x = {}, z = {}'.format(converted_coordinate['x'], converted_coordinate['z']))


def on_load(server, prev):
    server.register_help_message('!!cdc', '转换主世界和地狱的对应坐标')
