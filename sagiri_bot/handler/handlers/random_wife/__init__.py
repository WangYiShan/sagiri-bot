import random

from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Source
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.event.message import Group, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

from sagiri_bot.internal_utils import get_command
from sagiri_bot.control import (
    FrequencyLimit,
    Function,
    BlackListControl,
    UserCalledCountControl,
)

saya = Saya.current()
channel = Channel.current()

channel.name("RandomWife")
channel.author("SAGIRI-kawaii")
channel.description("生成随机老婆图片的插件，在群中发送 `[来个老婆|随机老婆]`")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([get_command(__file__, channel.module)])],
        decorators=[
            FrequencyLimit.require("random_wife", 4),
            Function.require(channel.module, notice=True),
            BlackListControl.enable(),
            UserCalledCountControl.add(UserCalledCountControl.FUNCTIONS),
        ],
    )
)
async def random_wife(app: Ariadne, group: Group, source: Source):
    await app.send_group_message(
        group,
        MessageChain(
            [
                Image(
                    url=f"https://www.thiswaifudoesnotexist.net/example-{random.randint(1, 100000)}.jpg"
                )
            ]
        ),
        quote=source,
    )