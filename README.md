# scripts
Personal scripts for random things

### Check reddit submission for word
Check your own comment history to check for a given word, util for discussions. Needs praw to be configured.

### Check who ended the conversation
It takes an exported whatsapp conversation file and a number of hours in which we consider a conversation is "ended". Then, it check who starts and who ends the conversations and gives and aggregate of that.

### Get anime stats
It reads from a file with the names of animes, one per line and uses the API of Anilist to get some stats, such as the original name and the genre, finally it gives an aggregate of that data.

### Get upvoted posts of subreddit
Check your upvoted posts on a given subreddit and saves them to a txt file. Useful  to check quality posts that you liked. Requires praw to be configured.

### Reddit api only
A simple script which asks for a reddit token without the use of praw, it's merely an example.

### Reddit organizer (WIP)
Gets all your saved posts and comments and saves them to a DB. It aims to be more useful than that by adding search and categories, but it is still a WIP

### Send message 
It tries to use selenium to send a message in a whatsapp web conversation. Was not working that well last time I worked on it.

### Twitter backup (WIP)
A simple script which saves all your tweets, likes, followers and people you follow and saves them in case you want to delete twitter. Uses tha twitter package and requires a file with credentials. WIP
