# Anime Download Bot with MEGA Storage

A Discord bot that automates downloading anime episodes from aniworld.to, merging German audio with German subtitles, and storing them on MEGA cloud storage.

## Features

- 🤖 Discord bot with buttons and dropdowns for easy interaction
- 🎬 Downloads German Dub and German Sub versions from aniworld.to
- 🔀 Merges German audio with German subtitles using ffmpeg
- ☁️ Uploads merged videos to MEGA (20GB free storage)
- 🚀 Fully automated via GitHub Actions
- 💰 Completely free (no credit card required)

## Architecture

```
Discord Bot (Replit - Free)
    ↓ (User triggers download)
GitHub Actions (Free)
    ↓ (Downloads, merges, uploads)
MEGA Storage (20GB Free)
    ↓ (Download link sent back)
Discord Bot
```

## Setup Instructions

### Step 1: Create MEGA Account

1. Go to https://mega.nz/
2. Sign up for a free account (20GB storage)
3. Note your email and password

### Step 2: Create GitHub Repository

1. Go to https://github.com and sign in
2. Create a new repository (e.g., `anime-download-bot`)
3. Upload all files from this project to the repository

### Step 3: Create Discord Bot

1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Anime Bot"
3. Go to "Bot" tab → Click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent
5. Click "Reset Token" to generate a bot token (copy this!)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot`
8. Select permissions: `Send Messages`, `Use Slash Commands`, `Read Messages/View Channels`
9. Copy the generated URL and open it in browser
10. Add the bot to your server (or DM it directly)

### Step 4: Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it "Anime Bot"
4. Select scopes: `repo` (full control of private repos)
5. Generate and copy the token

### Step 5: Configure GitHub Secrets

In your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `MEGA_EMAIL`: Your MEGA email
   - `MEGA_PASSWORD`: Your MEGA password
   - `DISCORD_TOKEN`: Your Discord bot token
   - `GITHUB_TOKEN`: Your GitHub personal access token

### Step 6: Deploy Discord Bot to Replit

1. Go to https://replit.com/
2. Create a new Python Repl
3. Upload all files to the Repl
4. Create `.env` file with:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=anime-download-bot
   GITHUB_OWNER=your_github_username
   MEGA_EMAIL=your_mega_email
   MEGA_PASSWORD=your_mega_password
   ```
5. Install dependencies: `pip install -r requirements.txt`
6. Run the bot: `python discord_bot.py`
7. Enable "Always On" in Replit settings (may need Hacker plan for 24/7)

### Step 7: Test the Bot

1. DM the Discord bot
2. Type `!start`
3. Select an anime from the dropdown
4. Choose "Both (Merge)" to merge German audio + subtitles
5. Select episodes
6. Wait for the process (10-30 minutes)
7. Receive download link from MEGA

## Usage

1. DM the Discord bot
2. Type `!start` to begin
3. Select anime from dropdown or search
4. Choose version:
   - German Dub Only
   - German Sub Only
   - Both (Merge) - Recommended
5. Select episodes:
   - Latest Episode
   - Season Selection
   - Custom Range
6. Wait for completion
7. Download from MEGA link

## Limitations

- GitHub Actions has a 6-hour time limit per job
- Replit free tier may sleep the bot when inactive (wakes up on message)
- MEGA free tier: 20GB storage
- Single episode processing: ~10-30 minutes

## Troubleshooting

**Bot not responding:**
- Send another message to wake it up (Replit free tier limitation)
- Check if bot token is correct

**Download fails:**
- Check aniworld.to URL format
- Verify aniworld package is working

**MEGA upload fails:**
- Check MEGA credentials
- Ensure file size fits in remaining storage

**GitHub Actions not triggering:**
- Verify GitHub token has `repo` scope
- Check repository dispatch event type matches

## Future Improvements

- [ ] Add anime search functionality from aniworld.to
- [ ] Support batch episode downloads
- [ ] Add progress updates during download
- [ ] Implement queue system for multiple downloads
- [ ] Add file management (list, delete stored videos)
- [ ] Support for other cloud storage providers

## License

MIT License - Free to use and modify
