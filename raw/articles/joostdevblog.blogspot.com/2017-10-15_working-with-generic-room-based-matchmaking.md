---
title: Working with generic room-based matchmaking
url: http://joostdevblog.blogspot.com/2017/10/working-with-generic-room-based.html
author: Joost van Dongen
published: '2017-10-15'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

As far as I know most smallish games build their matchmaking using these generic room-based systems. The big triple-A developers seem to usually build everything themselves from scratch, but that's too much work and too much server maintenance to be feasible for most smaller developers.

Our own game

[Awesomenauts](http://www.awesomenauts.com)initially launched using these basic room-based systems. We didn't develop our own matchmaking system

*Galactron*until years later when we concluded that the requirements for a genre as demanding as a competitive MOBA don't sit well with the limitations of such generic room-based systems.

![](../../assets/3a006bdde96900b6.jpg)

The specifics of the systems that Steam, Microsoft, Sony and Nintendo offer aren't public and thus can't be discussed here, so I'm not going into any detail on how they each differ from the generic ideas described here. However, they share enough that I feel this post is very relevant if you ever make matchmaking for any of these platforms, or another platform that's built on similar ideas.

The basic concept is that the platform holder runs servers that handle

*rooms*. A room usually represents a single match with a bunch of players in it. For example, in Awesomenauts a room would have the 1 to 6 players in it that are playing together in a match. If a player wants to join a match then the game will ask the server for a list of all rooms that have a spot left for at least one more player. The game then chooses which room is the best fit and requests the server to join it. Upon joining the game receives a list of the other players in that match and can make a connection with them and start playing.

It's important to realise that the room doesn't actually run the game. It's not a gameplay server. Usually one of the players is the gameplay server. All that the room does is keep a list of who's in the match and allow players to search for matches to join. The room is only intended for finding and maintaining lists of matches and can do very little else.

Since the room doesn't handle the actual gameplay it can often be closed once the match has started and the players are connected. Only if you support drop-in do you really need to keep a room up once the match has already started. Whether closing the room once the match has started is actually how it works depends on the platform though.

The server that handles the room can do some basic logic, but generally not much. One of the most important things it does is limit how many people can be in the room. You usually set a limit and if two players try to join at the same time while there's only space for one, then the server will make sure only one actually succeeds. This solves one of the more hairy race conditions around matchmaking.

Rooms aren't just usable for matches: you can also use them for some other things. A simple example is a chatroom. This is simply a room that players use to exchange chat messages, for example if you have global chat somewhere in your game's menus. Whether rooms scale to large numbers of players for a true global chat varies per platform. This case also shows another use of rooms: often it's possible to send messages to other players in the same room through the rooms server, without actually connecting to other players.

Also, if the client is in a room it will get notifications of changes to the room and of messages being sent through the room. You shouldn't expect rooms to be able to handle high numbers of messages or send them quickly, but something like a chatroom where lag isn't really an issue might be suitable, depending on the platform.

A more common use of rooms outside gamerooms and chatrooms is setting up a party to play with: this is also usually a room. This kind of room starts out with just one player in it, and if that player invites friends to play together then they join her party. The party leader then does matchmaking to find a room with enough free spots for the entire party.

![](../../assets/7d2945d81607f093.jpg)

Joining a gameroom with a partyroom of several people is often a hairy thing to develop. If the platform holder didn't supply anything for this particular situation then there are a lot of things that can go wrong that you need to solve. For example, what if a party of 3 players starts joining a room that has 3 empty spots, but by the time two of the players in the party have joined someone from outside also joins that room, taking up the final spot? In that case you need to roll back the joining for the two players who already joined and go back to searching. The number of edge-cases that might occur here is pretty horrible and is just one example of why developing an online multiplayer game is so much more work than developing a single player game. (For some more reasons check this blogpost on

[why adding multiplayer makes game coding twice as much work](http://joostdevblog.blogspot.nl/2015/08/why-adding-multiplayer-makes-game.html).)

Another interesting challenge when using generic room-based matchmaking is what supposedly happened to one of the Gears of Wars games at launch. Rumour has it that their matchmaking broke down because lots of clients all decided that the same room was the best one to join. Only a few got in before it was full, and then the remaining players all tried joining the same next room. Since each time most would fail it often took so many tries to actually get into a room that the matchmaking took forever. This particular situation is difficult to test without a large playerbase and definitely something to consider during development.

Rooms allow for additional data to be stored in the room. This data can be used in any way the developer sees fit and will probably contain information on the game mode, the skill of the players in the match and the map on which the match takes place. This way when a player is searching for a specific game mode the game can look through the list of rooms for one that's the desired game mode. This also allows the game to check whether the other players in the room are at a similar skill level as the player. Rooms can hold arbitrary data as the developer sees fit, but they generally don't allow for a large amount of data, so only the essential stuff is stored here.

While it's often relatively easy and quick to use the matchmaking systems that platform holders provide, there are some downsides to this approach. One of the most important ones is that if you make a multiplatform game then you'll need to build this again for each platform. If you're doing simultaneous launch on 3 platforms then this is going to take a serious amount of programming work.

You might think you can reuse a lot of your code since the basic ideas behind these rooms are so similar, but in our experience the platforms have just enough differences that this approach quickly becomes a horror story. The old version of the Awesomenauts matchmaker supports 5 platforms: Steam, X1, X360, PS4 and PS3. We tried to abstract away the platform-specific details as much as possible, but adding code for all the weird edge cases each platform introduces has turned our old matchmaking codebase into one big tangled mess where any change might break any of the platforms. Designing a good architecture for handling the differences between these systems is a tough challenge, especially if you're doing it for the first time.

![](../../assets/65303b3340266405.jpg)

Note that the room systems on various platforms also can't connect to each other. So if you want to do cross-platform multiplayer then you basically need to write your own matchmaking servers.

Another problem of using these generic room systems is that they allow for very little server-side logic to be run. This is a huge limitation on how well you can match players. This is also the main reason we redid the entire Awesomenauts matchmaking code and built our own, called Galactron. This launched in 2016. The limitations on matchmaking imposed by a lack of server logic is a big enough topic that I'll write a separate blogpost about that soon.

The generic room-based matchmaking systems that platform holders provide make developing matchmaking a lot easier than without. They save you all the hassle of developing and maintaining your own servers, so unless you're doing a large production, chances are they are the best option to efficiently develop the matchmaking for your game.

hmmmmmmmmmm

ReplyDelete