# User Manual

This API provides a command line interface for managing a bot in simple way. Using this API you can manage you bot easily with distributive system. API get details of registered user save it to own database and it is capable to send msg at any time.

## Methods in API

This API is capable of doing following things:

1. Registering a user

2. Sending a time dependent SMS (Alerm SMS)

3. Searching in a database and responding.


Following are the example task with code:

### Testing Connection

it may be possible that there may be slow internet connection or no internet connection or server may busy in that condition it is good to test the connection before using it, by code below

##### Code to test the connection

b = Bot()
b.open()
b.close()
del b
"""
output
Initilizing... Bot
Database Connecting...
Connection closed!
"""



### Getting all User Data

To get the user information we have to make an instance of user class the following code shows how to get user data. \textit{getAllUser()} returns the list of all user available at database.

##### Code

u = User()
print(u.getAllUser()) 



### Inserting New user

Insert is refers to insert the data in SQL database which is Handel by bot. Bot takes user information either from Telegram Network or manually by calling \textit{save()}.
\textit{save()} takes seven argument telegram user/group id, first name, user-name, active state, date or starting, date of ending and chat type as argument. and return true on success otherwise false.

##### Code

u = User()
u.save(1, "first_name", "user", "Y", "25-12-2018", "No", "group")


### Removing User
\textit{remove()} is used to remove a user from database. it takes one argument user id and return true if success otherwise false.

##### Code

u = User()
u.remove('1')




### Getting All Private Chats, ID
\textit{getAllPrivate()} returns all user details with there user ID as matrix  and  \textit{getAllPrivateID()} returns all private chat id only as array. 
##### Code

c = Chat()
print(c.getAllPrivate())
print(c.getAllPrivateID())



### Getting All Group Chat

To get all group information we have to call \textit{getAllGroup()} this takes none argument and return matrix of all group details.

##### Code

c = Chat()
print(c.getAllGroup())



### Getting All Time Dependent Message/Auto-Mail

Time Dependent Message/Auto-Mail acts as a alarm. These message is send by Bot in specific time period. To get list of current auto-mail we have to call \textit{getAllMailler()} which return all auto-mail as table.

##### Code

a = AutoMailer()
print(a.getAllMailler())



### Adding New Auto-Mail
\textit{newMailler()} used to set a new automail. It takes time and message and return true if successfully add.

##### Code

a = AutoMailer()
print(a.newMailler(time_hh_mm, 'This is sample Text genrated by AutoMailer'))



### Removing a Auto-Mail

\textit{deleteMailler()} deleted the automatic mail. It takes time and message and return true if successfully remove.
##### Calling

a = AutoMailer()
print(a.deleteMailler(ti, 'This is sample Text genrated by AutoMailer'))



### Run The Automailer
Automailer send message in every 24hr interal i.e it's repeat its cycle in every day. but we have to invoke a method \textit{run()} to activate.

##### Code

a = AutoMailer()
a.run()


### Open a User Registration

In this chat bot manager you can add new user for specific time to start registration you have to invoke the \textit{run()} method of Registration. and exiting the app can close the registration.

##### Code

r = Regestration()
r.run()



### Add a Search Key
Search Key is a search item which can be search by user using \textit{search} command in telegram app. Following code can insert a search item. 

##### Code


r = Regestration()
print(r.insertSerch("key2", "This is key2.", "12:30", "23:30"))



### Delete a Search Key
\textit{deleteSearch()} is used to delete a search item. It takes two parameter key and meassage and return if success.

##### Code

r = Regestration()
print(r.deleteSearch("key2", "This is key2."))



### Listen User Inputs
Like other chat-bot this manager also listen to user and response as per input command currently chat-bot respond on start, help and search command. to start listening call the \textit{polling()} method

##### Code

r = Regestration()
r.polling()


##### Telegram App Command

-----
 Command : Description  

-----
start : Start the bot 

-----
help : get all command list 

-----
search key : Search the given key 

-----
