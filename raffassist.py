# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime, requests
from time import strftime

@loader.tds
class RaffAss(loader.Module):
    """Модуль-помощник в проведении розыгрышей и рулеток"""

    strings = {
        "name": "Raffle Assistant",
        "error_no_pm": "<b>[UserBot]</b> Это не чат",
        "errr_no_reply": "<b>[UserBot]</b> Не тупи, никакой это не ответ :)",
        "no_rank": "Аноним без должности",
        "_list_begin":" ╭︎ 🗂 <b>Список участников:</b>\n",
        "_list_body" : "├︎ <b>{}</b>. {}\n", 
        "_list_footer":"╰︎ <b>{}</b>. {}\n",
    }
    
    usrlist = [ ]
   
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue( # self.config["max_users"]
                "max_users",
                doc=lambda: "Максимальное количество участников. Значение по умолчанию",
                validator=loader.validators.Integer(100)
            ),
            loader.ConfigValue( # self.config["ignored_users"]
                "ignored_users",
                doc=lambda: "Список пользователей которым запрещено учавствовать в отборе на рулетку",
                validator=loader.validators.Choice()
            ),                 
            loader.ConfigValue( # self.config["trigger_symbols"]
                "trigger_symbols",
                doc=lambda: "Список символов и слов для участие в отборе на рулетку",
                validator=loader.validators.Choice(['+', 'plus', 'плюс', '➕', '👍', '✔️', '✅', '☑️'])
            ),
    )
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

    @loader.unrestricted
    async def ulcmd(self, m: Message):
        """ <*reply> [max_users:int] - Gенерация списка участников для рулетки
           Пример генерации списка на 25 чел: .ul 25 
           
           ‼️ Для участия в отборе нужно отправить один из следующих триггеров: 
             «+», «plus», «плюс», «➕», «👍», «✔️», «✅», «☑️»
        """
        
        args = utils.get_args(m)
        chatid = utils.get_chat_id(m)
        max_users = self.config["max_users"]
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
                if max_users == c: break
                try:
                    if str(msg.text).lower() in self.config["trigger_symbols"]: #self.symbols_add:
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
