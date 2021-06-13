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


def convert_dimension_coordinate(dimension: str, x_coord: float, z_coord: float) -> dict[str, int]:
    """Convert nether/overworld dimension coordinate to its opposites dimension.

    :param dimension: The dimension name, value args are 'nether' and 'overworld'.
    :param x_coord: The x coordinate used in converting.
    :param z_coord: The z coordinate used in converting.
    :return: A dict[str, int] store the coordinate information, keys are x and z.
    """
    coordinates = {'x': 0, 'z': 0}
    if dimension == 'nether':
        coordinates = {'x': int(x_coord * 8), 'z': int(z_coord * 8)}
    if dimension == 'overworld':
        coordinates = {'x': int(x_coord / 8), 'z': int(z_coord / 8)}
    return coordinates


@new_thread(PLUGIN_METADATA['name'])
def convert_by_player_current_coordinate(source: CommandSource):
    if isinstance(source, PlayerCommandSource):
        api = source.get_server().get_plugin_instance('minecraft_data_api')
        coordinates = api.get_player_coordinate(source.player)

        dimension_translate = {0: 'overworld', -1: 'nether'}
        dimension = dimension_translate[api.get_player_dimension(source.player)]

        converted_coordinates = convert_dimension_coordinate(dimension, coordinates.x, coordinates.z)
        source.reply('对应维度坐标: x = {}, z = {}'.format(converted_coordinates['x'], converted_coordinates['z']))


@new_thread(PLUGIN_METADATA['name'])
def convert_by_nether_coordinate(source: CommandSource, *coordinates):
    if isinstance(source, PlayerCommandSource):
        converted_coordinates = convert_dimension_coordinate('nether', coordinates[0], coordinates[1])
        source.reply('对应维度坐标: x = {}, z = {}'.format(converted_coordinates['x'], converted_coordinates['z']))


@new_thread(PLUGIN_METADATA['name'])
def convert_by_overworld_coordinate(source: CommandSource, *coordinates):
    if isinstance(source, PlayerCommandSource):
        converted_coordinates = convert_dimension_coordinate('overworld', coordinates[0], coordinates[1])
        source.reply('对应维度坐标: x = {}, z = {}'.format(converted_coordinates['x'], converted_coordinates['z']))


@new_thread(PLUGIN_METADATA['name'])
def reply_help_message(source: CommandSource):
    if isinstance(source, PlayerCommandSource):
        source.reply(HELP_MESSAGE)


class IllegalPoint(CommandSyntaxError):
    def __init__(self, char_read: int):
        super().__init__('不支持的参数', char_read)


class IncompletePoint(CommandSyntaxError):
    def __init__(self, char_read: int):
        super().__init__('不完整的参数', char_read)


class PointArgument(ArgumentNode):
    """Argument node accept input x z coordinate.

    """

    def parse(self, text: str) -> ParseResult:
        total_read = 0
        coordinate = []
        for i in range(2):
            value, read = command_builder_util.get_float(text[total_read:])
            if read == 0:
                raise IncompletePoint(total_read)
            total_read += read
            if value is None:
                raise IllegalPoint(total_read)
            coordinate.append(value)
        return ParseResult(coordinate, total_read)


def on_load(server: ServerInterface, prev):
    server.register_help_message('!!cdc', '转换主世界和地狱的对应坐标')
    server.register_command(Literal('!!cdc').runs(reply_help_message).
                            then(Literal('here').runs(convert_by_player_current_coordinate)
                                 ).
                            then(Literal('overworld').
                                 then(PointArgument('coord').
                                      runs(lambda src, ctx: convert_by_overworld_coordinate(src, *ctx['coord']))
                                      )
                                 ).
                            then(Literal('nether').
                                 then(PointArgument('coord').
                                      runs(lambda src, ctx: convert_by_nether_coordinate(src, *ctx['coord']))
                                      )
                                 )
                            )
