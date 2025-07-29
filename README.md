
# Recoil Bot + Flask Deployment (Railway)

## 🛠 Files
- `bot.py`: Your Discord + Flask bot (uses py-cord)
- `Procfile`: Tells Railway to run the bot
- `requirements.txt`: Dependencies
- `.env`: Set environment variables in the Railway UI

## 🚀 Deployment Instructions

1. Go to [https://railway.app](https://railway.app)
2. Create a new project → Deploy from GitHub (or CLI upload)
3. Upload these files to your GitHub repo:
   - `bot.py`
   - `Procfile`
   - `requirements.txt`
4. In Railway, go to the "Variables" tab and add:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```
5. Railway will automatically install dependencies and start the bot.
6. You're done! Check your logs for output.

## ✅ Notes
- The Flask `/verify` endpoint runs on port 5000
- The Discord bot runs with slash command support
