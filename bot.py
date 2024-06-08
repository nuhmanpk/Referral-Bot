# © BugHunterBotLabs ™
# © bughunter0
# © Nuhman Pk
# 2021 - 2024
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserNotParticipant


app = Client(
    "ReferralBot",
    bot_token="TOKEN",
    api_id='1234',
    api_hash="API_HASH",
)

invite_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Invite Someone ➡️", callback_data="cb_invite")]]
)
back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ back", callback_data="cb_back")]])


@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    if len(message.command) > 1:
        referrer_id = message.command[1]
        await message.reply(
            f"Hey {message.from_user.mention}. You were referred by user {referrer_id}."
        )
        user = await app.get_users(referrer_id)
        user_info_button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ℹ️ Show User Info",
                        callback_data=f"show_user_info_{referrer_id}",
                    )
                ]
            ]
        )
        await message.reply(
            f"Click the button below to view user info.", reply_markup=user_info_button
        )
        # Here you can save referral details to the server.
        # For example, you can call a function that writes the referral information to a database.
        # save_referral_details(referrer_id, message.from_user.id)
    else:
        await message.reply(
            f"Hey {message.from_user.mention}. This is a sample bot.",
            reply_markup=invite_button,
        )


@app.on_callback_query(filters.regex("cb_invite"))
async def send_invite_link(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    your_bot_name = "bughunter0TestBot"
    invite_link = f"https://t.me/{your_bot_name}?start={user_id}"
    invite_link_button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Invite Link ➡️", url=invite_link)]]
    )
    await callback_query.message.reply(
        f"Click the link to copy \n`{invite_link}`", reply_markup=invite_link_button
    )


@app.on_callback_query(filters.regex(r"show_user_info_(\d+)"))
async def show_user_info(client, callback_query: CallbackQuery):
    referrer_id = int(callback_query.data.split("_")[-1])
    try:
        user = await app.get_users(referrer_id)
        user_info_text = f"👤 **User Information** 👤\n\n"
        user_info_text += f"🆔 ID: `{user.id}`\n"
        user_info_text += f"🖋 Username: @{user.username}\n" if user.username else ""
        user_info_text += f"📛 First Name: {user.first_name}\n"
        user_info_text += f"📛 Last Name: {user.last_name}\n" if user.last_name else ""
        user_info_text += (
            f"📧 Phone Number: {user.phone_number}\n" if user.phone_number else ""
        )
        user_info_text += f"🤖 Bot: {'Yes' if user.is_bot else 'No'}\n"
        await callback_query.answer(text="ℹ️ User information displayed.")
        await callback_query.message.edit_text(user_info_text, reply_markup=back)
    except UserNotParticipant:
        await callback_query.answer(
            text="You need to start a chat with the user to get their information."
        )
    except Exception as e:
        print(e)
        await callback_query.answer(
            text="An error occurred while fetching user information."
        )


@app.on_callback_query(filters.regex(r"cb_back"))
async def back_to_main_menu(client, callback_query):
    await callback_query.answer()
    await callback_query.message.delete()


app.run(print("BOT is Cooking...👨‍🍳 "))
