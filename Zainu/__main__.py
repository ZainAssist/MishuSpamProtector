import asyncio
import re
from importlib import import_module as import_

from pyrogram import filters, idle
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from pyrogram.enums import ChatType

from Zainu import BOT_USERNAME, conn, session, Zainu
from Zainu.core import ikb
from Zainu.modules import MODULES
from Zainu.utils.misc import once_a_day, once_a_minute, paginate_modules

HELPABLE = {}


async def main():
    await Zainu.start()
    # Load all the modules.
    for module in MODULES:
        imported_module = import_(module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    print("STARTED !")
    loop = asyncio.get_running_loop()
    loop.create_task(once_a_day())
    loop.create_task(once_a_minute())
    await idle()
    conn.commit()
    conn.close()
    await session.close()
    await Zainu.stop()


@Zainu.on_message(filters.command(["help", "start"]), group=2)
async def help_command(_, message: Message):
    if message.chat.type != ChatType.PRIVATE:
        kb = ikb({"Help": f"https://t.me/{BOT_USERNAME}?start=help"})
        return await message.reply("Pm Me For Help", reply_markup=kb)
    kb = ikb(
        {
            "Help": "bot_commands",
            "Channel🥹": "https://github.com/t.me/About_Zain",
            "Add Me To Your Group": f"https://t.me/{BOT_USERNAME}?startgroup=new",
            "Support Chat🎧": "https://t.me/MusicOnMasti",
        }
    )
    mention = message.from_user.mention
    await message.reply_photo(
        "https://graph.org/file/f16bc0eeefa25c88f5a20-e09d47a1829fbe8fa2.jpg",
        caption=f"Hi {mention},I'm Mishu SpamProtector Robot🔰,"
        + " Choose An Option From Below.",
        reply_markup=kb,
    )


@Zainu.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, cq: CallbackQuery):
    text, keyboard = await help_parser(cq.from_user.mention)
    await asyncio.gather(
        cq.answer(),
        cq.message.delete(),
        Zainu.send_message(
            cq.message.chat.id,
            text=text,
            reply_markup=keyboard,
        ),
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help")
        )
    return (
        f"Hello {name}, I'm Mishu SpamProtector Robot, I can protect "
        + "your group from Spam and NSFW media using "
        + "machine learning. Choose an option from below.",
        keyboard,
    )


@Zainu.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query: CallbackQuery):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    u = query.from_user.mention
    top_text = (
        f"Hello {u}, I'm Mishu SpamProtector Robot, I can protect "
        + "your group from Spam and NSFW media using "
        + "machine learning. Choose an option from below."
    )
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "back", callback_data="help_back"
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


@Zainu.on_message(filters.command("runs"), group=3)
async def runs_func(_, message: Message):
    await message.reply("What am i? Rose?")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
