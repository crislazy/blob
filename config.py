# ==== Config.py ====

# ==== TOKEN ====
bot_secret = "placeholder123"

# ==== ROLES ====
mod_roles_id = [123456789] # Moderator roles
member_role_id = 123456789 # The role that is automaticly given to new members

# ==== CHANNELS ====
welcome_channel_id = 123456789 # Where it sends a welcome message on join/leave

# ==== FEATURES ====
# Toggle Features(True = On ; False = Off)

ENABLE_WELCOME_MESSAGE = True # Send a message on join
ENABLE_GOODBYE_MESSAGE = True # Send a message on leave
AUTO_ROLE = True # Gives a role on join
PING_RESPOND = True # Responds with a message when pinged
SEND_AS_BOT = True # Send a message as the bot
CUSTOM_STATUS = True # Have a Custom Status
STATUS_TEXT = "Mining In BlobCraft" # Status Text
STATUS_TYPE = "playing"  # playing / watching / listening
HELP_COMMAND = True
ENABLE_USERINFO = True
ENABLE_8BALL = True
ENABLE_CAT = True

# ==== MESSAGES ====
welcome_messages = [
    "{user} boarded the plane",
    "{user} joined the server",
    "{user} got teleported here"
]

goodbye_messages = [
    "{user} jumped off the plane",
    "{user} got kicked off the plane",
    "{user} left",
    "{user} had a stroke",
    "{user} might have been kicked, idk tbh"
]

blob_messages = [
    "Yes?",
    "No",
    ":3",
    "This is a response to your message, please shut up"
]

ballresponse = ["Yes", "No", "Maybe", "Definitely", "Absolutely not"]