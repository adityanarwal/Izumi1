"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import wget
import speedtest

from PIL import Image
from config import BOT_USERNAME as bname

from driver.filters import command
from driver.decorators import sudo_users_only
from driver.core import bot as app
from driver.utils import remove_if_exists

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["speedtest", f"speedtest@{bname}"]) & ~filters.edited)

async def run_speedtest(_, message: Message):
    m = await message.reply_text("Γ π±ππππππ πππ π‘πππ π²πΎπππΎπ π²ππΎπΎπ½π³πΎππ !!")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("Γ π£ππππ«ππΊπ½ π²ππΎπΎπ½ β‘οΈ")
        test.download()
        m = await m.edit("Γ π΄ππ«ππΊπ½ π²ππΎπΎπ½ β‘οΈ")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit(e)
        return
    m = await m.edit("Β» π²ππΎπΎπ½π³πΎππ π±πΎπππππ π₯πππ π³ππΎ πππ π²πΎπππΎπ !!")
    path = wget.download(result["share"])
    try:
        img = Image.open(path)
        c = img.crop((17, 11, 727, 389))
        c.save(path)
    except BaseException:
        pass

    output = f"""**Β» πππ Bα΄α΄ Sα΄Κα΄ α΄Κ Sα΄α΄α΄α΄ !!**
    
<u>**Client:**</u>
**β’ πΈππΏ Β»** {result['client']['isp']}
**β’ π²ππππππ’ Β»** {result['client']['country']}
  
<u>**Server:**</u>
**β’ π½πππ Β»** {result['server']['name']}
**β’ ππππππ Β»** {result['server']['country']}, {result['server']['cc']}
**β’ πππππππ Β»** {result['server']['sponsor']}
**β’ π»ππππππ’ Β»** {result['server']['latency']}

β‘οΈ **β’ πΏπππ Β»** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    remove_if_exists(path)
    await m.delete()
