# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime, requests
from time import strftime
import pprint
import math
from ..inline.types import InlineQuery

@loader.tds
class GenUL(loader.Module):
    """Инструменты для раздачи халявы"""

    strings = {
        "name": "DistributionTools",
        "error_no_pm": "<b>[UserBot]</b> Это не чат",
        "errr_no_reply": "<b>[UserBot]</b> Не тупи, никакой это не ответ :)",
        "no_rank": "Аноним без должности",
        "_list_begin":" ╭︎ 🗂 <b>Список участников:</b>\n",
        "_list_body" : "├︎ <b>{}</b>. {}\n", 
        "_list_footer":"╰︎ <b>{}</b>. {}\n",
    }
    
    usrlist = [ ]
    max_users = 100
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
   
    async def listview(self,):
        i = 0
        list = self.usrlist
        cusers = len(list)
        listview = self.strings("_list_begin")
        for user in list:
           i += 1
           if cusers == i: listview += self.strings("_list_footer").format(i, user)
           else: listview += self.strings("_list_body").format(i, user)
        return listview   


    @loader.sudo
    async def city_inline_handler(self, query: InlineQuery):
         """[Менеджер адресов] Выбрать город """
         # Process request query.args
         pass

    @loader.sudo
    async def staff_inline_handler(self, query: InlineQuery):
         """[Менеджер адресов] Наименование товара """
         # Process request query.args
         pass

    @loader.unrestricted
    async def pulcmd(self, m: Message):
        """ <*reply> [max_users:int] - Gенерация списка участников для рулетки
           Пример генерации списока на 25 чел: .ul 25 
           
           ‼️ Для участия в отборе нужно отправить один из следующих триггеров: 
             «+», «plus», «плюс», «➕», «👍», «✔️», «✅», «☑️»
        """        
        args = utils.get_args(m)
        chatid = utils.get_chat_id(m)
        if args:
            try: max_users = int(args[0])
            except ValueError: pass

        if not m.chat:
            return await m.edit(self.string("error_no_pm"))

        reply = await m.get_reply_message()
        if not reply: return await m.edit(self.string("errr_no_reply"))
        else:
            c = 0
            async for msg in m.client.iter_messages(chatid, offset_id = reply.id, reverse=True, limit = 400):
                if self.max_users == c: break
                try:
                    if str(msg.text).lower() in self.symbols_add:
                        user = get_display_name(msg.sender)
                        if msg.sender == None:
                            user = msg.post_author
                            uid = 0
                        else:
                            uid = msg.sender.id
                        if not user: user = m.chat.title
                        if not user in self.usrlist:
                            c += 1 
                            self.usrlist.append(user)
                            
                except AttributeError: continue
                except TypeError: continue
                except NameError:
                    c += 1
                    self.usrlist.append(self.strings("no_rank"))
                
        await utils.answer(m, await self.listview())
