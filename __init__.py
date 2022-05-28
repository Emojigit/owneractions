__author__ = "Emoji"
__version__ = "1.0.0"
__url__ = "https://github.com/Emojigit/owneractions"
__description__ = "Let the bot owner to control the bot"
__dname__ = "owneractions"
#__moreinfo__ = ["Example __moreinfo__"]

from telethon import events, utils
import config, random, string, traceback, asyncio, math
helpmsg = []
helpmsg.append("Commands:")
helpmsg.append("- help: show this message")
helpmsg.append("- leave: let the bot kick out itself")
helpmsg.append("- exec: Run Python codes")
helpmsg.append("- eval: Run Python expression and get the result")
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
            elif subc == "exec":
                try:
                    execarg = argv[1]
                except IndexError:
                    await event.respond("❌ No code!")
                    raise events.StopPropagation
                g = globals().copy()
                await event.respond("⚙️ Executing...")
                def newprint(*args, sep=" ", end="\n",**kwargs):
                    f = asyncio.ensure_future(event.respond(sep.join(str(x) for x in args) + end))
                g["print"] = newprint
                try:
                    exec(execarg,g,locals())
                except:
                    await event.respond("❌ Error!\n```" + traceback.format_exc() + "```")
                else:
                    await event.respond("✅ Done!")
            elif subc == "eval":
                try:
                    execarg = argv[1]
                except IndexError:
                    await event.respond("❌ No code!")
                    raise events.StopPropagation
                msgs = ["⚙️ Executing..."]
                msg = await event.respond("⚙️ Executing...")
                g = globals()
                mathfunc = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'ldexp', 'lgamma', 'log', 'log1p', 'log10', 'log2', 'modf', 'pow', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'prod', 'perm', 'comb', 'pi', 'e', 'tau', 'inf', 'nan']
                for x in mathfunc:
                    g[x] = getattr(math,x)
                try:
                    r = eval(execarg,g)
                except:
                    msgs.append("❌ Error!\n```" + traceback.format_exc() + "```")
                else:
                    msgs.append("✅ Done! Result: `{}`".format(r))
                await msg.edit("\n".join(msgs))
            elif subc == "sendto":
                try:
                    group, msg = argv[1].split(" ",1)
                except ValueError:
                    await event.respond("❌ Missing arguments!")
                    raise events.StopPropagation
                try:
                    group = int(group)
                except ValueError:
                    if group[0] == "@":
                        group = group[1:]
                try:
                    group = await bot.get_input_entity(group)
                    if group == None:
                        raise ValueError
                except ValueError:
                    await event.respond("❌ Target not found!")
                    raise events.StopPropagation
                await event.respond("⚙️ Sending...")
                try:
                    await bot.send_message(group,msg)
                except Exception as e:
                    await event.respond("❌ Message not sent, error occured!\n" + e.__str__())
                else:
                    await event.respond("✅ Done!")
            else:
                raise IndexError
        except IndexError:
            await event.respond("❌ Invalid subcommand!\n" + helpmsg)
        raise events.StopPropagation


