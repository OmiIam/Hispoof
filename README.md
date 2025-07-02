# hispoof

A Telegram bot for placing spoofed SIP calls using the python-telegram-bot library and PJSUA.

## Features
- Start interaction with /start
- Place calls with a spoofed caller ID
- Set custom caller ID
- View current caller ID status

## Requirements
- Python 3.11 (recommended via Conda)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- PJSUA (SIP client)
- Telegram Bot Token

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd hispoof
```

### 2. Create and activate a Conda environment
```bash
conda create -n hispoof python=3.11
conda activate hispoof
```

### 3. Install dependencies
```bash
pip install python-telegram-bot python-dotenv
```

### 4. Prepare your `.env` file
Create a `.env` file in the project root with the following content:
```ini
TELEGRAM_TOKEN=your_telegram_token
SIP_USER=your_sip_user
SIP_PASS=your_sip_pass
PJSUA_PATH=/full/path/to/pjsua
DYLD_LIB_PATH=/full/path/to/dyld_lib
```

- `TELEGRAM_TOKEN`: Your Telegram bot token
- `SIP_USER`/`SIP_PASS`: Your SIP credentials
- `PJSUA_PATH`: Full path to the PJSUA executable
- `DYLD_LIB_PATH`: Path to dynamic libraries needed by PJSUA (macOS)

### 5. Run the bot
```bash
python uibot.py
```

## Usage
- Start the bot in Telegram with `/start`
- Use the menu to place calls, set caller ID, or check status

## Notes
- Make sure PJSUA is installed and accessible at the path you provide
- This bot is for educational/research purposes only. Use responsibly and comply with all applicable laws. # Hispoof
