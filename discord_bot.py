#!/usr/bin/env python3
"""
Discord bot for anime download automation
Uses buttons and dropdowns for easy interaction
"""

import discord
from discord.ext import commands
import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')  # format: username/repo-name
GITHUB_OWNER = os.getenv('GITHUB_OWNER')  # username

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

class AnimeView(discord.ui.View):
    """View with buttons for anime selection"""
    
    def __init__(self):
        super().__init__()
        self.add_item(AnimeSelect())

class AnimeSelect(discord.ui.Select):
    """Dropdown to select anime"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="Search anime...", value="search"),
            discord.SelectOption(label="You and I Are Polar Opposites", value="polar-opposites"),
            discord.SelectOption(label="One Piece", value="one-piece"),
            discord.SelectOption(label="Black Clover", value="black-clover"),
            discord.SelectOption(label="Re:ZERO", value="rezero"),
            discord.SelectOption(label="Overgeared", value="overgeared"),
        ]
        super().__init__(
            placeholder="Select an anime...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "search":
            await interaction.response.send_message("Please type the anime name you want to search for:")
            # Wait for user response
            def check(m):
                return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)
            
            try:
                msg = await bot.wait_for('message', check=check, timeout=60.0)
                # Search functionality would go here
                await interaction.followup.send(f"Searching for: {msg.content}")
            except TimeoutError:
                await interaction.followup.send("Search timed out. Please try again.")
        else:
            # Show version selection
            await interaction.response.send_message(
                f"Selected: {selected}\nWhich version do you want?",
                view=VersionView(selected)
            )

class VersionView(discord.ui.View):
    """View with version selection buttons"""
    
    def __init__(self, anime_name):
        super().__init__()
        self.anime_name = anime_name
    
    @discord.ui.button(label="German Dub Only", style=discord.ButtonStyle.primary)
    async def dub_only(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"German Dub selected for {self.anime_name}\nWhich episodes?",
            view=EpisodeView(self.anime_name, "german-dub")
        )
    
    @discord.ui.button(label="German Sub Only", style=discord.ButtonStyle.secondary)
    async def sub_only(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"German Sub selected for {self.anime_name}\nWhich episodes?",
            view=EpisodeView(self.anime_name, "german-sub")
        )
    
    @discord.ui.button(label="Both (Merge)", style=discord.ButtonStyle.success)
    async def both_merge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Merge German Audio + German Subtitles selected for {self.anime_name}\nWhich episodes?",
            view=EpisodeView(self.anime_name, "merge")
        )

class EpisodeView(discord.ui.View):
    """View with episode selection options"""
    
    def __init__(self, anime_name, version):
        super().__init__()
        self.anime_name = anime_name
        self.version = version
    
    @discord.ui.button(label="Latest Episode", style=discord.ButtonStyle.primary)
    async def latest(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Downloading latest episode of {self.anime_name} ({self.version})...",
            ephemeral=True
        )
        # Trigger GitHub Action here
        await trigger_download(self.anime_name, "latest", self.version, interaction)
    
    @discord.ui.button(label="Season Selection", style=discord.ButtonStyle.secondary)
    async def season(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Select a season:",
            view=SeasonSelectView(self.anime_name, self.version)
        )
    
    @discord.ui.button(label="Custom Range", style=discord.ButtonStyle.secondary)
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Please specify the episode range (e.g., '1-5' or 'episodes 3, 7, 10'):",
            ephemeral=True
        )
        # Wait for user input
        def check(m):
            return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)
        
        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            await interaction.followup.send(f"Downloading episodes {msg.content}...")
            await trigger_download(self.anime_name, msg.content, self.version, interaction)
        except TimeoutError:
            await interaction.followup.send("Input timed out. Please try again.")

class SeasonSelectView(discord.ui.View):
    """View with season selection dropdown"""
    
    def __init__(self, anime_name, version):
        super().__init__()
        self.anime_name = anime_name
        self.version = version
        self.add_item(SeasonSelect())
    
    async def confirm_download(self, interaction: discord.Interaction, season: str):
        await interaction.response.send_message(
            f"Downloading {self.anime_name} Season {season} ({self.version})...",
            ephemeral=True
        )
        await trigger_download(self.anime_name, f"season-{season}", self.version, interaction)

class SeasonSelect(discord.ui.Select):
    """Dropdown to select season"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="Season 1", value="1"),
            discord.SelectOption(label="Season 2", value="2"),
            discord.SelectOption(label="Season 3", value="3"),
            discord.SelectOption(label="Season 4", value="4"),
            discord.SelectOption(label="All Seasons", value="all"),
        ]
        super().__init__(
            placeholder="Select a season...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        view = self.view
        await view.confirm_download(interaction, selected)

async def trigger_download(anime_name, episodes, version, interaction):
    """Trigger GitHub Action to download the anime"""
    
    # This is a placeholder - you'd need to map anime names to actual aniworld.to URLs
    # For now, we'll use a placeholder URL
    aniworld_url = f"https://aniworld.to/anime/stream/{anime_name.replace(' ', '-').lower()}/staffel-1/episode-1"
    
    # Trigger GitHub repository_dispatch event
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "event_type": "download-anime",
        "client_payload": {
            "url": aniworld_url,
            "anime": anime_name,
            "episodes": episodes,
            "version": version,
            "user_id": str(interaction.user.id)
        }
    }
    
    try:
        response = requests.post(
            f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/dispatches",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 204:
            await interaction.followup.send(
                "✅ Download started! I'll notify you when it's ready (this may take 10-30 minutes)."
            )
        else:
            await interaction.followup.send(
                f"❌ Failed to start download. Error: {response.text}"
            )
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    print(f'Bot ID: {bot.user.id}')

@bot.command()
async def start(ctx):
    """Start the anime download process"""
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("🎬 Anime Download Bot\n\nSelect an anime to download:", view=AnimeView())
    else:
        await ctx.send("Please DM me to use this bot!")

@bot.command(name='info')
async def info(ctx):
    """Show help message"""
    help_text = """
    🎬 Anime Download Bot Commands:
    
    !start - Start the download process
    !info - Show this help message
    
    Just DM me and use !start to begin!
    """
    await ctx.send(help_text)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables")
        sys.exit(1)
    
    bot.run(DISCORD_TOKEN)
