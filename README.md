### Telegram Email Messaging Bot (EBot)
The goal of this bot is to send any forwarded to him
messages onto given email whilst providing info about sender,
such as date/time of writing, chat and, of course,
the original message.

It can also automatically upload attachments(photo, docs,
audio, etc.) onto given Google Drive and provide link in the email.

### Deploy instructions
1. Download python3 libraries declared in `requirements.txt`
2. Take a look at `assets/sensitive.properties.example`
    and provide required properties with your own value
   (you can put them into `assets/sensitive.properties`, for example)
3. Run `main.py` with python interpreter
4. ~~PROFIT!~~ Now your bot should be running
    without any errors. Congratulations! Be careful though
    with running multiple instances of the bot for a single token!
