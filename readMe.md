# The Manager

### Events
- on_ready : Sents a message when the bot is online
- on_message : Sent every message to this function for debugger purpose mostly, added a restriction for users without specific roles
- on_member_join : Sends a message when a member joins the server (when it is activated)
- on_member_join : Sends a message when a member leaves the server (when it is activated)



### Commands
Every command needs to be used with a $

- switch_join_message bool : Switches if the join message will be sent
- switch_leave_message bool : Switches if the leave message will be sent
- check_join_message_status : Checks the current join message status
- check_leave_message_status : Checks the current leave messasge status
- joke : Sends a joke in the channel the request came from


- changeNickname @member (needs to be mentioned) new_nickname : Changes the nickname of the mentioned member to the new_nickname
- removeAllNicknames : Removes every nickname on the server
- removeAllNicknamesExceptRole @role (needs to be mentioned) : Removes every nickname except a specific role nickname
- changeAllNicknamesInRole @role (needs to be mentioned) text : Changes every user's nick with the role into text parameter 
- alone @member (needs to be mentioned) : not finished
- dmMe message : The bot sends you a private message with the "message-text"
- dmMember message @member(s) (needs to be mentioned) : Sends all mentioned members a private message with the content "message-text" 
- dmMemberSpam message @member(s) (needs to be mentioned) : Spams every mentioned member with the "message-text"


### PS: 
bool -> True/False