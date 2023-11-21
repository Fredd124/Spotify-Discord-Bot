import os
import discord
import responses
import base64
import json
from requests import post
import dotenv
from discord.ext import commands


dotenv.load_dotenv()

def get_token(client_id, client_secret):
    """
    Get token from Spotify API
    :params client_id: Spotify client id
    :params client_secret: Spotify client secret
    :return: Spotify token
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes =  auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") 
  
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    """
    Get authorization header
    :params token: Spotify token
    :return: Authorization header
    """
    return {"Authorization": "Bearer " + token}

async def send_message(ctx, tokenSpotify, user_message, is_private):
    """
    Send message to discord
    :params ctx: Discord context
    :params tokenSpotify: Spotify token
    :params user_message: Message sent by user
    :params is_private: Boolean to check if message is private
    """
    try:
        await responses.handle_responses(ctx, tokenSpotify, user_message, is_private)
    except Exception as e:
        print(e)

def run_discord_bot():
    """
    Run discord bot
    """
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
  
    global tokenSpotify
    tokenSpotify = get_token(CLIENT_ID, CLIENT_SECRET)

    tokenBot = os.getenv('TOKEN')
    intents = discord.Intents.all()
    intents.members = True
    bot = commands.Bot(command_prefix='#', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        user_message = str(message.content)
        ctx = await bot.get_context(message)

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(ctx, tokenSpotify, user_message, True)
        else:
            await send_message(ctx, tokenSpotify, user_message, False)

    bot.run(tokenBot)
  