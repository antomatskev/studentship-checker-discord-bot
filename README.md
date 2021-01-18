# Discord bot for checking a studentship
A discord bot, which will check if a person is a student, then assign corresponding role to that person.

## What we want
Don't let any unwanted people post to a discord server until they confirm that they belong to a school/college/university this server is meant for. We assume, that such institution has own e-mails, so it's ensured, that a person is officially registered.

## What we do
After a person joins a discord server, our bot does the following:

- Assigns a role to that person, which doesn't allow doing anything on the server;
- Writes a private message to the joined person asking for an e-mail to send confirmation code;
- Sends a code to the entered e-mail and waits for a person to enter this code to the same private chat;

For sending e-mails we use https://github.com/kootenpv/yagmail

## Additional functionality
Also we may add:

- Mass role updating (eg from one to another). This can be useful, when students have roles indicating their grade/course, so when they go to the next one, the corresponding bot command can be issued to update all members with a role, let's say "the first course" to "the second course"
- TODO