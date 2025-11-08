# Run JVW Bot on Your PC

## Quick Start

Double-click `start_bot.bat` to run the bot.

## Auto-Start with Windows

1. Press `Win + R`
2. Type: `shell:startup`
3. Press Enter
4. Copy `start_bot.bat` into that folder
5. Bot will auto-start when you turn on your PC

## Stop the Bot

Press `Ctrl + C` in the terminal window.

## Run in Background (Hidden)

Create `start_bot_hidden.vbs`:
```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d ""c:\X Bot"" && python main.py", 0, False
```

Double-click this file to run bot invisibly in background.

## Check if Bot is Running

Open Task Manager → Look for "python.exe"

## View Bot Activity

Check your X account: https://x.com/All_You_Need12
