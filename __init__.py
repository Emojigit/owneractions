__author__ = "Emoji"
__version__ = "1.0.0"
__url__ = "https://github.com/Emojigit/owneractions"
__description__ = "Let the bot owner to control the bot"
__dname__ = "start"
#__moreinfo__ = ["Example __moreinfo__"]

from telethon import events, utils
import config, random, string
helpmsg = []
helpmsg.append("Commands:")
helpmsg.append("- help: show this message")
helpmsg.append("- leave: let the bot kick out itself")
helpmsg = "\n".join(helpmsg)
def randomstr(length):
    return "".join(random.choice(string.ascii_letters) for i in range(length))
def setup(bot,storage):
    @bot.on(events.NewMessage(pattern="/owneractions"))
    async def owneractions_cmd(event):
        sender = event.sender
        try:
            if config.owner != sender.id:
                raise AttributeError
        except AttributeError:
            await event.respond("❌ Bot owner not set, or you are not the owner!")
            raise events.StopPropagation
        argv = event.text.split(" ",2)[1:]
        try:
            subc = argv[0]
            if subc == "help":
                await event.respond(helpmsg)
            elif subc == "leave":
                if event.is_private:
                    await event.respond("❌ This is not a group!")
                    raise events.StopPropagation
                confirm_code = storage.get("confirm_leave_code_" + str(event.chat_id),0)
                try:
                    if confirm_code != argv[1]:
                        raise IndexError
                    await event.respond("👋 Leaving this chatroom. Bye!")
                    await bot.kick_participant(event.chat, 'me')
                    storage.set("confirm_leave_code_" + str(event.chat_id),0)
                except IndexError:
                    rstr = randomstr(10)
                    storage.set("confirm_leave_code_" + str(event.chat_id),rstr)
                    await event.respond("⚠️ Do you really want to kick out the bot? If yes, please run: `/owneractions leave {}`".format(rstr))
            else:
                raise IndexError
        except IndexError:
            await event.respond("❌ Invalid subcommand!\n" + helpmsg)


