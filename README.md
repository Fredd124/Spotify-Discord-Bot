# Spotify-Discord-Bot

## Introduction
This repository contains scripts for a Discrod Bot. The bot provides various functionalities related to Spotify, such as fetching artist information, album details, track features, and more. It utilizes the Spotify API and integrates with Discord to offer an interactive experience.

## Repository Structure
  1. `main.py`: The main script to run the Spotify Bot on Discord.
  2. `bot.py`: It sets up the Discord bot, its main events and initializes the token for the Spotify API.
  3. `responses.py`: Contains the core functionalities of the Spotify Bot. It includes functions to process user commands, interact with the Spotify API, and send responses back to the Discord server.
  4. `high_scores.txt`: Saves the best scores from all players, to display them later at the end of the games.

## Main Features 
  * Artist Info: Fetches detailed information about artists from Spotify.
  * Album Details: Provides information about albums, including tracks and release dates.
  * Track Features: Analyzes track features like danceability, energy, and more.
  * Game Mode: Engages users with a higher or lower game related to music popularity and artist knowledge.

## Requirements
- Python 3
- Libraries: discord.py, spotipy, requests, json, asyncio
- Spotify Developer Account for API credentials
- Discord Bot Token

## Setup and Instalation
  1. Clone the repository or download the scripts.
   ```bash
     git clone git@github.com:Fredd124/Spotify-Discord-Bot.git
     cd Spotify-Discord-Bot
   ```
  2. Install the required Python libraries:
   ```bash
   pip install discord.py spotipy requests asyncio
   ````
  3. Set up credentials:
      * Spotify Developer Credentials:
        * Register your application on the Spotify Developer Dashboard.
        * Obtain CLIENT_ID and CLIENT_SECRET.
      * Discord Bot Token:
        * Create a new bot on the Discord Developer Portal.
        * Generate a bot token under the 'Bot' section.
        * To add the bot to a server, navigate to 'OAuth2' > 'URL Generator', select 'bot' scope, and the necessary permissions. Use the generated URL to invite the bot to your server.
  4. Run `main.py` to start the bot:
   ```bash
   python3 main.py
   ```
## Usage
  * Users can interact with the bot by sending commands on the Discord server. Commands include #artist, #album, #track, and more, each providing specific information or functionalities. For more information about the commands, type `#help` in a discord channel where the bot can read messages.
     
