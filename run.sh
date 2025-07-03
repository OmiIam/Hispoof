#!/bin/bash
source .venv/bin/activate
python -m bot.main >> logs/bot.log 2>&1