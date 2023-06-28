def forward_from(message):
    chat = message.chat.first_name
    name = message.forward_from.first_name
    username = message.forward_from.username
    sender = name + f' (@{username})'

    return chat, sender


def forward_from_chat(message):
    chat = message.forward_from_chat.title

    if message.forward_signature is None:
        sender = "Аноним 🦹"
    else:
        sender = message.forward_signature

    return chat, sender
