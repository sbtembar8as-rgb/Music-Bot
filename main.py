import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
import yt_dlp
from config import *

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

# دالة لجلب رابط الصوت من يوتيوب
def get_audio_url(video_url):
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info['url']

@app.on_message(filters.command("play") & filters.group)
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("يرجى إرسال رابط يوتيوب بعد الأمر /play")
    
    url = message.command[1]
    await message.reply("جاري المعالجة والتشغيل...")
    
    try:
        audio_url = get_audio_url(url)
        await call_py.join_group_call(
            message.chat.id,
            AudioPiped(audio_url)
        )
        await message.reply("تم التشغيل بنجاح! 🎵")
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")

@app.on_message(filters.command("stop") & filters.group)
async def stop(client, message):
    await call_py.leave_group_call(message.chat.id)
    await message.reply("تم إيقاف الموسيقى.")

async def main():
    await app.start()
    await call_py.start()
    print("البوت يعمل الآن يا معتصم...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())