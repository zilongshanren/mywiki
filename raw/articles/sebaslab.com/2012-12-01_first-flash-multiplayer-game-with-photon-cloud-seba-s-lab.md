---
title: First Flash Multiplayer Game with Photon Cloud - Seba's Lab
url: https://www.sebaslab.com/first-actionscript-3-multiplayer-game-with-photon-cloud/
author: Sebastiano Mandalà
published: '2012-12-01'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

For a long time I wanted to make some experiments with [Photon Network Engine ](https://cloud.exitgames.com/)at home.

During my professional experience, I worked on several multiplayer games, therefore I was pretty curious about it.


Exit Games provides two versions of Photon Network Engine: the traditional Photon Server edition and the new Photon Cloud edition.

Photon is a server-client network engine dedicated to game development and, while the marketing department pushes the Unity3D version a lot, it has got APIs for most of the most famous development platforms existent.

Compared to the competitors, Photon Server has the advantage to be written in c++ and therefore be fast; however the server version has the limitation to work on Windows platform only, which could honestly be a problem.

Surely I would have not bothered to install the server for a tutorial, but luckily Photon comes with an amazing Cloud version with a very smart pricing model, including a free version that supports up to 20 simultaneous connections, more than enough to create the first prototype of whatever game, or a tutorial 😉

Of course Photon Cloud comes with some limitations as well. While Photon Server allows the server logic to be extended, the cloud version does not let any kind of extension, forcing to use authoritative clients while the server becomes just a simple message router (and lobby manager).

## Let’s start right away

First thing first: you need to create your development account; once done you can create immediately your first server application with very few straightforward steps.

With the app generated, you get also an unique App ID, which is the only information needed to link your application to the cloud server.

Now, before to start your first Photon project, download the[ Photon flash SDK](https://cloud.exitgames.com/Download), this includes all the client code you need to create your game.

As usual, I use *flashdevelop* as IDE, but you can do everything with your favorite one as well. Download my code from [https://github.com/sebas77/PhotonDemo](https://github.com/sebas77/PhotonDemo) and open the file* mmo.as3proj* (although it is not a MMO :P).

The project needs to include the library *PhotonCoreAS3.swc* as well as the source folder *photon_loadbalancing_lib* from the Photon SDK, so verify that everything is set correctly.

The load balancing version of the Photon client is the modern superstructure created on top of the* Photon Core* and, even if you do not need load balancing, I strongly suggest to use it, since it abstracts the Photon API even more and make everything easier to use.

Note that the code I released with this tutorial is based on my *Entity Framework*, however I never published it and the version used is just a work in progress, so do not focus on it. I think using this framework helps to highlight just the multiplayer logic implemented if everything else is used as a black box.


The code folders structure includes the startup files, the **bullet folder**, the **character folder** and the **photon folder** (plus my framework code). The Photon folder includes all the files to customize the events needed to control the game. The code I used to start is the chat example included in the SDK.

## Where everything starts from

Looking at the code you will notice that all the server logic starts from:

server = new ConnectToServer(); server.connect();

pay attention to the fact that while the game starts immediately, your avatar will not appear until the game is not connected to the server. This is the standard logic of a multiplayer game: the graphical representation of your character will appear on the screen only when the server-client communication is setup.

The *ConnectToServer* class contains the **APPLICATIONID** value that must be filled with your AppID previously generated before to execute the game.

The *ConnectToServer* class provides also a series of useful callbacks that can help having a better understanding of the network engine logic.

The first thing your application must do as client, is to connect to the master server. The connection flow starts with a **CONNECTING_TO_MASTER** event and the Photon Core handling of the server connection. If all the data entered so far is correct, in few (milli)seconds the client receives the answer from the server as a **CONNECTED_TO_MASTER** event.

Once connected to the server, our code sets, in a simple and naive way, the properties of our actor; in our demo the properties set are limited to the name of the actor only. The **actorID** will be automatically set successively, but be aware of the fact that the actorID, unique for each player, is fundamental for every operation I will show you next.

Once the connection has been authorized, the client automatically connects to the **lobby** (all these operations are done “behind the scene”, so you relatively need to worry about it). The [Lobby ](http://doc.exitgames.com/photon-server/LiteLobbyConcepts/#cat-Application%20-%20Lite%20&%20Lite%20Lobby)is a special “room” that contains the list of all the active **games** available.

A **Game** must be seen like a “chat” room where users connect to and exchange messages in.

the Photon flows continues retrieving the games list from the server, this is when our class *ConnectToServer* must decide again what to do:

If the list of games is empty, our client will create a new game; if the list is not empty, it will simply join the existing game. So, in total, our demo will never have more than one active Game running.

Even though I do not use special features for this demo, you will find out with your experiments that each game, as well as each actor, can come with special properties that can be set and broadcasted to all the clients.

Left the Lobby and Joined our Game, finally the flow reaches the event we care most, that is the *LoadBalancedJoinEvent*, but before to continue, let’s take a step back for a moment.

## Getting deeper into the code

I explained what happens just calling *server.connect()*, but now that the user joined the room it’s our turn to act.

An important class used to listen to the network events is the *LoadBalancedPeer* that I extended in our demo and called *PhotonPeer*. For convenience, it is used as Singleton, however as you know, I am not a fan of this pattern and in fact the use of this singleton makes some part of my code awkward, but this is not a big issue for this tutorial purposes (beside, *LoadBalancePeer* has been designed as a Singleton).

PhotonPeer is used both to listen and dispatch data throughout the demo code. The classes that use it are:

-
**ActorSpawner**, used to create and destroy avatars


-
**BulletSpawners**, used to create and destroy bullets


-
**CharacterEngine**, used to manage avatars


**BulletEngine**, used to manage bullets

## Let’s spawn this Actor

ActorSpawner listens to user joining and leaving games thanks to the following lines:

PhotonPeer.getInstance().addEventListener(JoinEvent.TYPE, onUserJoin); PhotonPeer.getInstance().addEventListener(LeaveEvent.TYPE, onUserLeft);

once a user joins a game, and I mean whatever user (so both the local player or a remote player), a new character Entity is created. However depending if the player who joined is the local player or a remote player, the code behaves differently creating a local or a remote character entity.

As previously mentioned, the *ActorID* is important because it is used to recognise if the joining user is the local user or a remote user thanks to the following code:

if (evt.getActorNo() == PhotonPeer.getInstance().getActorNo()) //true = local user false = remote user

However, since a user can join after other users joined already, the code must be able to query the existing list of users and recreate them on the local client as well. This is done through this function:

private function addAlreadyJoinedCharacterAfterIJoined():void { var peer:LoadBalancedPeer = PhotonPeer.getInstance(); var l:Vector.< int > = peer.getActorNumbers(); for (var i:int = 0; i < l.length; i++) { if (l[i] != peer.getActorNo()) { var characterServerModel:CharacterModel = new CharacterModel(); characterServerModel.id = l[i]; _charactersCreatedInThisWorld[characterServerModel.id] = _characterFactory.BuildClientCharacter(characterServerModel); } } }

That’s it, now the user avatar is shown and it’s time that the client can run all the game logic!

## Character Movement

*CharacterEngine* is a *System* for my Entity Framework, as far as possible, let’s use it as a black box.

CharacterEngine both listens and dispatches custom remote data. The way I used to handle this data is exploiting the **ActorEvent.TYPE** event. Remember that our server does not have any logic, so all the custom events must come from another client. In order to dispatch a custom event, I used the function *opRaiseEventWithCode* like the following example:

PhotonPeer.getInstance().opRaiseEventWithCode(GameConstants.EV_SENDPOS, _dic, 0);

The function needs the event ID (*GameConstants.EV_SENDPOS*) to recognise the type of data sent and a *Dictionary* with the data itself. For example, to send the character position and rotation, I use the following dictionary:

_dic["x"] = model.entityTransform.pos.x; _dic["y"] = model.entityTransform.pos.y; _dic["r"] = model.rotation;

at the same time, to receive the same data from other players, the relative event is listened through this code:

PhotonPeer.getInstance().addEventListener(ActorEvent.TYPE, onCustomEvent);

private function onCustomEvent(evt:ActorEvent):void { if (evt.getEventCode() == GameConstants.EV_SENDPOS) UpdateClientPosition(evt); }

CharacterEngine handles the death of the character in a similar way.

## Bullet Shooting

*BulletSpawner* and *BulletEngine* logic follow the same principles. When a character “shoots” the **GameConstants.EV_FIRED** event is dispatched from one client and broadcasted to all the other ones through the server.

## Homework: how to improve the demo

This little demo can be a start point to more interesting experiments, however I would start improving two issues:

- I sample the position update at 25 fps. Honestly the sampling can be less frequent if an interpolation method is used to avoid jittering, saving precious bandwidth
- as said the hit should be sent from the client that has been hit and not checked locally

In this game no client is authoritative, however only local clients can dispatch “death” as well as “shoot” events, since the remote clients cannot determine these events by themselves. This is not ideal since the local client should dispatch the “hit” state too, otherwise the hit count could be mismatched between the local and remote client.

## Conclusion

With this demo I showed the basic concept of Photon Cloud. The client can connect to the server, then to a specific game. All the clients can receive and dispatch data through events. It is important to notice that the data can be handled differently depending if the sender is the local user or a remote user.

To conclude, two words about the Photon documentation: it is OK, but not great. However if you have any question, the [photon forum](http://forum.exitgames.com/) is a great way to get answers quickly.

My version of the game can be played from [here](http://www.sebaslab.com/as3/photon/photon.swf) (use wasd + mouse, kinda fps style 😉 )

And now good luck with the rest of your experiments!

Hey Seba, this is great stuff!

Do you think it would be possible to combine Photon Cloud’s ActionScript API and JavaScript (“HTML5”) client so that the service could conveniently be used from a Jangaroo application?

you believe I actually thought about that? I have no clue, it would be interesting to test maybe. However take in account that Photon Cloud API is all based on sockets.

Of course, such a solution would have to rely on ExitGames’ JavaScript (for the implementation) and ActionScript (for the API) code. Currently, they only offer a beta JavaScript client for Photon Server. In their forum, you find that they are working on a JavaScript client for Photon Cloud, but they have no ETA.

P.S. I’d love to make Jangaron http://www.jangaron.net a real multiplayer game…

If you need an authoritative server I would recommend uLink. I made the switch to it from Photon and so far I’m very happy with it.

Thanks for the suggestion, I did not know that software. However Photon server does support authoritative servers of course. It is Photon Cloud to not support them.

Hey, good post. I am interested of your entity framework for unity3d. Could you share some information about it?

I never completed it, but maybe one day I will 🙂