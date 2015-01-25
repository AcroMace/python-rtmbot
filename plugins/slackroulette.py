from collections import deque


################################################################################
# Setup                                                                        #
################################################################################

# Messages to be sent
outputs = []

# Direct message channels of available users
#  Since the earliest joiners are at the front,
#  they will be matched first
users_available = deque([])
# Tuples of the channels of matched users
users_matched   = []


################################################################################
# Helper functions                                                             #
################################################################################

# Send a message to a channel with a message
def send_message(channel, message):
  outputs.append([channel, message])

# Check if a user is online
def user_is_online(channel):
  return channel in users_available

# Check if a user is offline
def user_is_offline(channel):
  return not user_is_online(channel)

# Check if the user is in a conversation
#  Returns the index of the tuple if they are
#  Returns -1 if not
def user_conversation_index(channel):
  for index, pair in enumerate(users_matched):
    if pair[0] == channel or pair[1] == channel:
      return index
  return -1

# Check if the user is in a conversation
def user_is_in_conversation(channel):
  return user_conversation_index(channel) >= 0

# Get the other user in the conversation
# Returns None if no user is found
def user_conversation_other_user(channel, index=-1):
  # Search for index if it was not specified
  if index is -1:
    index = user_conversation_index(channel)
  # If other user was not found, return None
  if index is -1:
    return None
  else:
    pair = users_matched[index]
    return pair[1] if channel == pair[0] else pair[0]

# Make the user online if they are not already online
#  Return True if the was previously offline
def user_ensure_online(channel):
  if user_is_offline(channel):
    users_available.append(channel)
    return True
  else:
    return False

# Start a conversation between two users
# Must be at least two users in users_available
def user_start_conversation(channel):
  match = users_available.popleft()
  # The first one on the list may be the user
  if match == channel:
    match = users_available.popleft()
  else:
    users_available.remove(channel)
  users_matched.append((channel, match))
  send_message(channel, "You are now in a conversation!")
  send_message(match, "You are now in a conversation!")

# End a conversation, notify the users that the conversation has ended
#  Returns True if a conversation was ended
#  Returns False if the user was not in a conversation
def user_end_conversation(channel):
  # Ensure that the user is in a conversation
  index = user_conversation_index(channel)
  other_user = user_conversation_other_user(channel, index)
  if other_user is None:
    return False
  # Add the users back into the available pool
  users_available.append(channel)
  users_available.append(other_user)
  # Remove the users from the conversation pool
  del users_matched[index]
  # Notify the users that the conversation has ended
  send_message(channel, "You have left the conversation!")
  send_message(other_user, "The other person has left the conversation!")
  return True

# Send a message from a user to the other user if in a conversation
#  Return True if in a conversation
#  Return False if not
def user_send_message(channel, message):
  other_user = user_conversation_other_user(channel)
  if other_user is None:
    send_message(channel, "You are not currently in a conversation!")
    return False
  else:
    send_message(other_user, message)


################################################################################
# Commands                                                                     #
################################################################################

# Add the user to the available list
def command_online(channel):
  if user_is_offline(channel) and not user_is_in_conversation(channel):
    users_available.append(channel)
    send_message(channel, "Yay! You're now online! :)")
  else:
    send_message(channel, "Oops! You were already online!")

# Remove the user from the available list
def command_offline(channel):
  try:
    # Stop any existing conversation
    # Does not raise errors if not in conversation
    user_end_conversation(channel)
    # Users will be added back to the available pool on user_end_conversation
    users_available.remove(channel)
    send_message(channel, "You are now offline!")
  except ValueError:
    send_message(channel, "You're already offline!")

# Start a conversation with another user
def command_spin(channel):
  user_ensure_online(channel)
  if len(users_available) <= 1:
    send_message(channel, "Sorry! No one is available to chat :(")
  elif user_is_in_conversation(channel):
    send_message(channel, "You are already in a conversation!")
  else:
    user_start_conversation(channel)

# Leave from a conversation
def command_leave(channel):
  if not user_end_conversation(channel):
    send_message(channel, "You are not currently in a conversation!")

# Respond to an unknown command
def command_unknown(channel):
  send_message(channel, "Command not recognized. " +
                        "Type !help to see what commands are availble!")


################################################################################
# Main                                                                         #
################################################################################


# Called when a message arrives
def process_message(data):
  channel = data['channel']
  text    = data['text']

  # A message with a 'reply_to' field is sent after a disconnect
  if 'reply_to' in data: return
  # Make sure that the message is a direct message
  if not channel.startswith("D"): return

  # Check if the user has issued a command
  if text.startswith("!"):
    if   text == "!online":  command_online(channel)
    elif text == "!offline": command_offline(channel)
    elif text == "!spin":    command_spin(channel)
    elif text == "!leave":   command_leave(channel)
    else:                    command_unknown(channel)
  else:
    user_send_message(channel, text)

  print("Current users: {}".format(users_available))
