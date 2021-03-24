# TeleIG_Bot
**This is a personal project, interracting with instagram**<br>
The app uses telegram chat-bot as an interface for recieving data fron consumers.<br>
_Telegram chat bot is written using aiogram and threading libraries for making asynchronous requests_<br><br>
__DataBase - SQLite3__<br>
__all the SQL requests and tests are contained in ./utils/db_api__<br><br>
Container volume - volume_data
./volume_data contains
  - Users <br>_here's a directory for each user with such files as:_
    - followers (with a list of instagram followers)
    - cookies file (cookies data for instagram)
    - following (with a list of instagram follows)
    - checked ( with a list of users that were checked previously)
    - unfollowed (with a list of unfollowed accounts. Or due the check on artificialness either the check of back follow request)
  - insta_log 
    - contains logs named by the time they were created 
  - DB <br>_contains 2 tables_:
    - IG_users ( the main table with identification and proxy data)
    - Trial_users ( for those who ran the trial version) 
