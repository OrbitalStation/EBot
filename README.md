### Telegram Email Messaging Bot (EBot)
The goal of this bot is to send any forwarded to it
messages onto given email whilst providing info about sender,
such as date/time of writing, chat and, of course,
the original message.

It can also automatically upload attachments(photo, docs,
audio, etc.) onto given Google Drive or Yandex Disk
and provide link in the email.

### Deploy instructions
1. Download python3 libraries declared in `requirements.txt`

    Example(for python3): `pip install -r requirements.txt`
2. Required settings for the bot are located at `assets/sensitive.properties.example`
    Please put your values for these properties in a separate file ending in `.properties`
    inside the `assets` folder (for example `assets/sensitive.properties`)
3. Run `main.py` with python interpreter

    Example(for python3): `python main.py`
4. ~~PROFIT!~~ Now your bot should be running
    without any errors.

    Congratulations! Be careful though
    with running multiple instances of the bot for a single token!
