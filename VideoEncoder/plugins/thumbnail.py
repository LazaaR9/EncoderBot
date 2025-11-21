from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from ..utils.database.access_db import db

@Client.on_message(filters.command("thumb"))
async def thumb_command(client, message):
    user_id = message.from_user.id
    thumbnail = await db.get_thumbnail(user_id)
    buttons = [
        [
            InlineKeyboardButton("Set/Replace Thumbnail", callback_data="set_thumb"),
            InlineKeyboardButton("Delete Thumbnail", callback_data="del_thumb")
        ]
    ]
    if thumbnail:
        await message.reply_photo(
            photo=thumbnail,
            caption="Your current custom thumbnail.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            "You don't have a custom thumbnail set.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_callback_query(filters.regex("^set_thumb"))
async def set_thumb_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    file_id = callback_query.photo.file_id
    await callback_query.answer(wait a sec...)
    await callback_query.message.reply_text(
        "Send me a photo to set as your custom thumbnail."
    )
    await db.set_thumbnail(user_id, file_id)
    await message.reply_text("Custom thumbnail saved!")

@Client.on_callback_query(filters.regex("^del_thumb"))
async def del_thumb_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    file_id = callback_query.photo.file_id
    await db.set_thumbnail(user_id, file_id)
    await callback_query.answer("Thumbnail deleted!", show_alert=True)
    await callback_query.message.delete()

@Client.on_message(filters.photo)
async def save_thumb(client, message):
    if message.caption and (message.caption == "/thumb" or message.caption == "/setthumb"):
        user_id = message.from_user.id
        file_id = message.photo.file_id
        await db.set_thumbnail(user_id, file_id)
        await message.reply_text("Custom thumbnail saved!")
    elif message.reply_to_message and message.reply_to_message.text == "Send me a photo to set as your custom thumbnail.":
        user_id = message.from_user.id
        file_id = message.photo.file_id
        await db.set_thumbnail(user_id, file_id)
        await message.reply_text("Custom thumbnail saved!")
