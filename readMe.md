# The Manager

### Events
- on_ready : Sents a message when the bot is online
- on_message : Sent every message to this function for debugger purpose mostly
- on_member_join : Sends a message when a member joins the server (when it is activated)
- on_member_join : Sends a message when a member leaves the server (when it is activated)



### Commands
Every command needs to be used with a $

- switch_join_message : Switches if the join message will be sent
- switch_leave_message : Switches if the leave message will be sent

- changeNickname @member (needs to be mentioned) new_nickname : Changes the nickname of the mentioned member to the new_nickname
- removeAllNicknames : Removes every nickname on the server
- removeAllNicknamesExceptRole : Removes every nickname except a specific role nickname