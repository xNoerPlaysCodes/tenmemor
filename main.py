import discord
import requests

# Your Discord bot token and Giphy API key
from vars import TOKEN, api_key

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Default tag for fetching a GIF
tag = "random"

# Function to fetch a GIF using the Giphy API with the specified tag
async def fetch_gif_with_tag(tag):
    url = f'https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if 'data' in data and 'images' in data['data'] and 'original' in data['data']['images']:
            gif_url = data['data']['images']['original']['url']
            return gif_url
        else:
            print("Error parsing API response: 'image_original_url' key not found.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error while fetching GIF from Giphy API:", e)
        return None
    except KeyError as e:
        print("Error parsing API response:", e)
        return None

@client.event
async def on_ready():
    print(f"Successful login as {client.user}.")
    await client.change_presence(activity=discord.Game(name='t!meme'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global tag  # Declare the global tag variable to change it if needed

    if message.content.startswith("t!settag "):
        tag = message.content[len("t!settag "):]
        await message.channel.send(f"Tag set to '{tag}'.")
    elif message.content == "t!meme":
        await message.channel.send(f"Tag is {tag}")
        gif_url = await fetch_gif_with_tag(tag)
        if gif_url:
            await message.channel.send(gif_url)
        else:
            await message.channel.send("Oops, something went wrong while fetching the GIF.")

# LOGGING INTO THE BOT ITSELF
client.run(TOKEN)
