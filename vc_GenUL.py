# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime, requests
from time import strftime
import pprint

@loader.tds
class GenUL(loader.Module):
    """Инструменты для работы с пользователями"""

    strings = {
        'name': 'PositiveToolsBy@VacuumCleanr',
        "processing": (
            "<emoji document_id=5451732530048802485>⏳</emoji> <b>Работаю...</b>"
        ),
        "no_pm": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Эту команду нужно"
            " выполнять в чате</b>"
        ),
        "leaked": (
            "<emoji document_id=5465169893580086142>☎️</emoji>[<code>{}</code>] <b>Слитые номера в "
            " чате «{}»:</b>\n\n{}"
        ),
        "404": (
            "<emoji document_id=5465325710698617730>☹️</emoji> <b>Тут нет слитых"
            " номеров</b>"
        ),
        "_cmd_doc_bulkcheck": "Проверить все участников чата на слитые номера",
        "_cls_doc": "Проверяет всех участников чата на слитые номера",
    }
    #@loader.unrestricted
    #async def deanoncmd(self, m: Message):
    #    """ - деанонит всех пользователей группы, если хватит привилегий😀"""
    #   chatid = utils.get_chat_id(m)
    #  
    #   from telethon.tl.types import ChannelParticipantsAdmins
    #   from asyncio import sleep
    #   async for user in m.client.iter_participants(chatid, filter=ChannelParticipantsAdmins):
    #      await utils.answer(m, '<code>{0}</code>'.format(user.stringify()))    
    #        await sleep(10)

    async def mchcmd(self, message: Message):
        """
         ╰ ☎️ Проверка пользователей группы по базе Murix (☎️ слитых тел. номеров)
        """
        chatid = utils.get_chat_id(m)
        enty = self._client.get_input_entity(chatid)
        if message.is_private:
            await utils.answer(message, self.strings("no_pm"))
            return

        await self._client.send_message("me", pprint.pprint(enty))
        message = await utils.answer(message, self.strings("processing"))

        results = []
        async for member in self._client.iter_participants(message.peer_id):
            result = (
                await utils.run_sync(
                    requests.get,
                    f"http://api.murix.ru/eye?uid={member.id}&v=1.2",
                )
            ).json()
            if result["data"] != "NOT_FOUND":
                results += [
                    "<b>▫️ <a"
                    f' href="tg://user?id={member.id}">{utils.escape_html(get_display_name(member))}</a></b>:'
                    f" <code>+{result['data']}</code>"
                ]

        await message.delete()
        await message.client.send_message(
            "me",
            self.strings("leaked").format("id", "title", "\n".join(results))
            if results
            else self.strings("404"),
        )
        
    async def listview(self, list):
        i = 0
        cusers = len(list)
        listview = f' ╭︎ 🗂 <b>Список участников:</b>\n'
        for user in list:
           i += 1
           if cusers == i: listview += f'╰︎ <b>{i}</b>. {user}\n' # footer
           else: listview += f'├︎ <b>{i}</b>. {user}\n' # middle 
        return listview   
        
    @loader.unrestricted
    async def ulcmd(self, m: Message):
        """ 
         ╰ 📄 Gенерация списка участников для рулетки
           • <reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей
           • [max_users] - максимальное количество пользователей в списке, по умолчанию: 100
           #Пример, список на 25 чел: .ul 25 
           
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
