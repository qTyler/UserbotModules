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
    """Генерация списка пользователей"""

    strings = {'name': 'GenUserList'}
    
    def listview(list):
        i = 0
        cusers = len(list)
        listview = f'-- <b>Халявщиков найдено: {cusers}!</b> --\n\n'
        for user in list:
           i += 1
           if cusers == i: # footer
              listview += f'<b>📌{i}</b>. {user}\n'
           else: # middle 
              listview += f'<b>{i}</b>. {user}\n'
        return listview   
    
    @loader.owner
    async def sglcmd(self, m: Message):
        """<reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей
        [max_users] - максимальное количество пользователей в списке, по умолчанию: 30"""
            
        max_users = 30 #default
        symbols_add = [
            '+',
            'plus',
            'плюс',
            '➕',
            '👍'
        ]

        chatid = utils.get_chat_id(m)
        if not m.chat:
            return await m.edit('m.chat: {}'.format(chatid))
            #return await m.edit("<b>Это не чат</b>")

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
                            #uid = 0
                        else:
                            uid = msg.sender.id
                        if not user: user = m.chat.title
                        if not user in usrlist:
                            c += 1
                            usrlist.append(user)
                except TypeError: continue
                except NameError: usrlist.append('* Аноним без должности')
                #userlist.append('{}. {}\n'.format(c, user))
                
        await utils.answer(m, listview(usrlist))     
                    
