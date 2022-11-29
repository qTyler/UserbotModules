# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime
from time import strftime
import pprint

@loader.tds
class GenUL(loader.Module):
    """Генерация списка участников"""

    strings = {'name': 'GenUserList'}
  
    async def listview(self, list):
        i = 0
        cusers = len(list)
        listview = f'🧑‍💻 [@] <b>Количество чел: </b>{cusers}!\n⊶⊷⊶⊷⊶⊷⊶\n ╭︎ '
        if cusers < 3: return '💬 <b>Количество участников должно быть не меньше трех</b>‼️'
        for user in list:
           i += 1
           if i == 1: listview += f' <b>{i}</b>. {user}\n'
           elif cusers == i: listview += f' ╰︎ <b>{i}</b>. {user}\n' # footer
           else: listview += f' ├︎ <b>{i}</b>. {user}\n' # middle 
        return listview   
    
    @loader.owner
    async def viewcmd(self, m: Message):
        users = [
            '🇻 🇱 🇦 🇬 🇦',
            'ḊḕṁṏṆ',
            'КлАуС',
            '🅚🅞🅡🅞🅛❤️👑 (🅟🅐🅝🅘🅚🅐)',
            '𝖓𝖔 𝖓𝖆𝖒𝖊',
            '<ОпТИмУс>',
            'G̴O̴D̴⚡️BL̴E̴S̴S̴',
            'ⲊⳲⲞⲨⲀ Ⳳ ⲆⲞⲊⲔⳘ',
            'Milky Way',
            '🕷️',
            'ツ ×очУ ЛЯм $ ツ',
            '𝙴𝑐тъ 𐌐p๏𝟼uƬue'
        ]
        
        await utils.answer(m, await self.listview(users))
        
    @loader.group_admin
    async def ulcmd(self, m: Message):
        """<reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей
             [max_users] - максимальное количество пользователей в списке, по умолчанию: 30
        
             * Для участия в отборе необходимо отправить одну из следующих команд: 
                 «+», «plus», «плюс», «➕», 
                 «👍», «✔️», «✅», «☑️»
        """    
        max_users = 30 #default
        symbols_add = [
            '+',
            'plus',
            'плюс',
            '➕',
            '👍',
            '✔️',
            '✅',
            '☑️'
        ]

        args = utils.get_args(m)
        chatid = utils.get_chat_id(m)
        if args:
            try: max_users = int(args[0])
            except ValueError: pass

        if not m.chat:
            return await m.edit("<b>Это не чат</b>")

        usrlist = []
        reply = await m.get_reply_message()
        if not reply:
            return await m.edit("бля")
        else:
            c = 0
            async for msg in m.client.iter_messages(chatid, offset_id = reply.id, reverse=True, limit = 400):
                if max_users == c: break
                try:
                    if msg.text.lower() in symbols_add:
                        user = get_display_name(msg.sender)
                        if msg.sender == None:
                            user = msg.post_author
                            uid = 0
                        else:
                            uid = msg.sender.id
                        if not user: user = m.chat.title
                        if not user in usrlist:
                            c += 1 
                            usrlist.append(user)
                except TypeError: continue
                except NameError:
                    c += 1
                    usrlist.append('* Аноним без должности')
                
        await utils.answer(m, await self.listview(usrlist))
