#Github.com/Vasusen-code
from pyrogram import Client
from telethon import events, Button, errors
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = config("API_ID", "10000844", cast=int)
API_HASH = config("API_HASH", "776f257fc1d1f8aa4aea9dd35d10a45b")
BOT_TOKEN = config("BOT_TOKEN", "7080490834:AAFiwNup5PMAKxKxx4J8D4d05WKON8qFDXw")
SESSION = config("SESSION", "BQCYmcwAvTbJlV-yyHifocV0uMqNezAdzzZd3dnA4Ok2UuLEHte6M4x1Dk4RGxpKcFnCNDoO2xqLoRugcmwwBMPXXEPpO8GS6EH31_V3_I43p3c-pHV9CPRilPC-FUCj20rG2eqJjsHCKO4jwcbO204Fyyp-wxNDugTrMOtZ3Hj4PhVga83R71nbwxDMI6Zb5f00WFEJLUeSuKX2yHIB1j6-cXHDfpDFRDk7tq-X5E1vEaM79eRz8Qh9hD6mjn5j4IaXKzNzoiCi33D1SBx84M7SiijamHFM3vT0AwhlhxsE7XOnyMukIGcNEJRH_5UXqDO7t43gptSRbK6wvJnCksyfAOWfegAAAAGSXSpuAA")
FORCESUB = config("FORCESUB", "funnyzilla")
AUTH = [int(user_id.strip()) for user_id in config("AUTH", default="6750546542").split(",") if user_id.strip()]
replace_from = [word for word in config("replace_from", default="").split(',')]
replace_to = [word for word in config("replace_to", default="").split(',')]
file_from = [word for word in config("file_from", default="").split(',')]
file_to = [word for word in config("file_to", default="").split(',')]
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

userbot = Client("saverestricted", session_string=SESSION, api_hash=API_HASH, api_id=API_ID) 

@bot.on(events.NewMessage(incoming=True, pattern='/generatesession'))
async def generate_session(event):
    global SESSION
    message = event.message 
    await message.reply("Please enter your phone number in international format (e.g., +1234567890):")
    SESSION = None

    # Wait for the user's phone number response
    response = await bot.listen(events.NewMessage(incoming=True))

    if response.text.startswith("+"):
        try:
            # Create a Pyrogram session using the phone number
            await bot.sign_in(phone_number=response.text)
            await response.reply("Please check your Telegram account for the authentication code.")
            
            # Wait for the authentication code
            auth_code_response = await bot.listen(events.NewMessage(incoming=True))
            auth_code = auth_code_response.text.strip()

            # Complete the sign-in process with the authentication code
            await bot.sign_in(code=auth_code)

            # Check if two-step verification is enabled
            if await bot.is_user_authorized():
                user = await bot.get_me()
                if user.tfa_enabled:
                    await response.reply("Two-step verification is enabled. Please enter your password:")
                    # Wait for the user's password response
                    password_response = await bot.listen(events.NewMessage(incoming=True))
                    password = password_response.text.strip()
                    # Complete the sign-in process with the password
                    await bot.sign_in(password=password)
            
            # Get the session string
            session_string = await bot.export_session_string()
            
            # Update the SESSION variable
            SESSION = session_string

            await userbot.start()
            # Send the session string to the user
            await response.reply("Your session string:\n" + session_string)
        except Exception as e:
            await response.reply("An error occurred while generating the session string.")
    else:
        await response.reply("An error occurred while generating the session string.")

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    print(e)
