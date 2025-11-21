from asyncio import gather
from psutil import cpu_percent, virtual_memory, disk_usage, net_io_counters
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from time import time
import os

from .. import app, botStartTime, download_dir, data, sudo_users, owner
from ..utils.display_progress import humanbytes, TimeFormatter
from ..utils.helper import check_chat

# Helper function for readable time
def get_readable_time(seconds):
    return TimeFormatter(seconds)

def get_readable_file_size(size):
    return humanbytes(size)

@app.on_message(filters.command("status"))
async def mirror_status(client, message: Message):
    c = await check_chat(message, chat='Both')
    if not c:
        return

    count = len(data)

    # System Stats
    cpu = cpu_percent()
    mem = virtual_memory().percent
    disk = disk_usage(download_dir).free
    upload_speed = humanbytes(net_io_counters().bytes_sent)
    download_speed = humanbytes(net_io_counters().bytes_recv)
    uptime = get_readable_time(time() - botStartTime)

    msg = (
        f'<b>System Status</b>\n'
        f'<b>CPU:</b> {cpu}% | <b>RAM:</b> {mem}%\n'
        f'<b>FREE:</b> {get_readable_file_size(disk)}\n'
        f'<b>UP:</b> {upload_speed} | <b>DL:</b> {download_speed}\n'
        f'<b>Uptime:</b> {uptime}\n\n'
    )

    if count:
        msg += f"<b>Active Tasks:</b> {count}\n"
        # Since we don't have detailed task objects in 'data', we list queue items
        for i, task_msg in enumerate(data):
             # Try to infer what the task is
             info = "Unknown Task"
             if task_msg.text:
                 info = task_msg.text[:50] + "..." if len(task_msg.text) > 50 else task_msg.text
             elif task_msg.caption:
                 info = task_msg.caption[:50] + "..." if len(task_msg.caption) > 50 else task_msg.caption
             elif task_msg.document:
                 info = task_msg.document.file_name
             elif task_msg.video:
                 info = task_msg.video.file_name

             msg += f"{i+1}. {info}\n"
    else:
        msg += "No Active Downloads!\n"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Refresh", callback_data="status ref")]
    ])

    await message.reply(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex('^status'))
async def status_pages(client, query: CallbackQuery):
    data_split = query.data.split()
    cmd = data_split[1]

    if cmd == 'ref':
        count = len(data)

        cpu = cpu_percent()
        mem = virtual_memory().percent
        disk = disk_usage(download_dir).free
        upload_speed = humanbytes(net_io_counters().bytes_sent)
        download_speed = humanbytes(net_io_counters().bytes_recv)
        uptime = get_readable_time(time() - botStartTime)

        msg = (
            f'<b>System Status</b>\n'
            f'<b>CPU:</b> {cpu}% | <b>RAM:</b> {mem}%\n'
            f'<b>FREE:</b> {get_readable_file_size(disk)}\n'
            f'<b>UP:</b> {upload_speed} | <b>DL:</b> {download_speed}\n'
            f'<b>Uptime:</b> {uptime}\n\n'
        )

        if count:
            msg += f"<b>Active Tasks:</b> {count}\n"
            for i, task_msg in enumerate(data):
                 info = "Unknown Task"
                 if task_msg.text:
                     info = task_msg.text[:50] + "..." if len(task_msg.text) > 50 else task_msg.text
                 elif task_msg.caption:
                     info = task_msg.caption[:50] + "..." if len(task_msg.caption) > 50 else task_msg.caption
                 elif task_msg.document:
                     info = task_msg.document.file_name
                 elif task_msg.video:
                     info = task_msg.video.file_name

                 msg += f"{i+1}. {info}\n"
        else:
            msg += "No Active Downloads!\n"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Refresh", callback_data="status ref")]
        ])

        try:
            await query.message.edit(text=msg, reply_markup=buttons)
            await query.answer("Refreshed!")
        except Exception as e:
            await query.answer(f"Error: {e}")
    else:
        await query.answer("Unknown command")
