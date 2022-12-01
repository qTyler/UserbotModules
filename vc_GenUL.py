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
    """Инструменты для работы с пользователями"""

    strings = {'name': 'VacuumClnr.Tools'}
  
    async def listview(self, list):
        i = 0
        cusers = len(list)
        listview = f' ╭︎ 🗂 <b>Список участников:</b>\n'
        for user in list:
           i += 1
           if cusers == i: listview += f' ╰︎ <b>{i}</b>. {user}\n' # footer
           else: listview += f' ├︎ <b>{i}</b>. {user}\n' # middle 
        return listview   
        
    @loader.unrestricted
    async def ulcmd(self, m: Message):
        """ - генерация списка участников для рулетки
           • <reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей
           • [max_users] - максимальное количество пользователей в списке, по умолчанию: 100
           #Пример, список на 25 чел (ответ на сообщение): .ul 25 
           
           ‼️ Для участия в отборе нужно отправить один из следующих триггеров: 
             «+», «plus», «плюс», «➕», «👍», «✔️», «✅», «☑️»
        """        
        max_users = 100 #default
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
          
        usrlist = []
        args = utils.get_args(m)
        chatid = utils.get_chat_id(m)
        if args:
            try: max_users = int(args[0])
            except ValueError: pass

        if not m.chat:
            return await m.edit("<b>Это не чат</b>")

        reply = await m.get_reply_message()
        if not reply: return await m.edit("бля")
        else:
            c = 0
            lastmsg = []
            async for msg in m.client.iter_messages(chatid, offset_id = reply.id, reverse=True, limit = 400):
                if max_users == c: break
                lastmsg = msg
                try:
                    if str(msg.text).lower() in symbols_add:
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
                            
                except AttributeError: continue
                except TypeError: continue
                except NameError:
                    c += 1
                    usrlist.append('* Аноним без должности')
                
        await utils.answer(m, await self.listview(usrlist))
