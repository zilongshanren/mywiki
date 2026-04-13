---
title: Core network structures for games
url: http://joostdevblog.blogspot.com/2014/09/core-network-structures-for-games.html
author: Joost van Dongen
published: '2014-09-14'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here are those four basic structures (of course all kinds of hybrids and variants are possible):

![](../../assets/d01e3299560935cd.gif)

**Client-server**

In the two versions of client-server there is one computer who is alone responsible for the entire game simulation: the server. The clients cannot make real gameplay decisions. This means that if a player presses a button, it goes to the server, the server executes it and then sends back the results to the client.

This adds significant lag to all input, which is of course totally unacceptable and kills the gameplay feel. To make a game playable with this model all kinds of tricks are needed. The best trick I am aware of is described in this

[must-read article](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking)by Valve. The basic idea is this:

- When the player presses a button, the client immediately processes it as if it has the authority to do so, starting animations and such. A message is also sent to the server.
- The server receives the button press a little bit later, so the server
*rewinds*to the time of the button press, executes it, and then*re-simulates*to the current time. - The server then sends the current state to the client
- The client receives the latest state, but in the meanwhile more time has passed. So the client
*rewinds*to the time at which the server sent the message, corrects its own state with what the authoritative server had decided, and then*re-simulates*locally to the current time.

In other words: both the client and the server rewind and then re-simulate whenever a packet is received. Implementing rewinding mechanisms is a complex task and very difficult to add to an existing game. As far as I know this is nevertheless the best and most used approach.

The difference between the two client-server architectures is who the server is. Either it is one of the players, or it is a computer that the game's developer/publisher manages. A dedicated server is usually better, but much more complex and expensive as the developer needs to manage a scalable amount of servers. The fiascos at the launches of Diablo III and Sim City showed how difficult this is to do. The more successful the game, the more difficult dedicated servers are to pull off. They are also simply expensive.

**Peer to peer**

The third architecture is pure peer to peer. Here no single computer is responsible for the entire game simulation. Instead the simulation is spread out over all of the players. The challenge then is how to divide responsibilities over the players.

[Awesomenauts](http://www.awesomenauts.com)uses this model and our distribution of the simulation is simple: each player simulates his own characters and bullets. This has a big benefit: player input can always be handled immediately. No rewinding structure are needed and there is never any input lag for the player. This also makes it much easier to add to an existing game.

![](../../assets/cf2d764332e980e0.jpg)

Peer to peer has some heavy drawbacks though. The biggest one is that lag becomes much more unpredictable. While in a client server architecture only the lagging player suffers from his own lag, in a peer to peer game the other players will also notice if one player has a bad internet connection.

Peer to peer usually introduces complex synchronisation situations when the simulations of two players are not compatible. A good example of this can be found in my previous blogpost on Awesomenauts'

[infamous sliding bug](http://joostdevblog.blogspot.nl/2014/04/the-infamous-sliding-bug.html). Care needs to be taken to recognise and handle such situations. In most game concepts few of these problems will pop up though: in Awesomenauts pushing other players is the only really complex part regarding conflicting synchronisation.

Another major downside of peer to peer is in the amount of network traffic needed. Since all players need to talk to all other players it requires many more network packets. In client-server only the server needs to talk to everyone, so only one player is affected instead of all of them. Even better for packet count is using dedicated servers: the entire burden falls on servers that the game developer provides.

**Deterministic peer to peer lockstep**

The fourth and final basic structure is deterministic peer to peer lockstep. This model is mostly used for RTS games. This is also a peer to peer model but here we don't need to worry about which player manages which objects. Instead every client simulates everything in the exact same way. The only thing that needs to be sent over the network is each player's actions. The game runs as lots of really short turns: every step the game collects the commands from all players over the network and then simulates the next step. This is not limited to turn-based games: by doing lots of really short steps it can feel like a real-time game.

Deterministic peer to peer has the enormous benefit that you hardly need to send anything. Only player actions need to be sent. If everyone starts the game in the same situation and runs the exact same steps, then the game will remain in synch without ever sending updates over the network. Therefore this model is highly suitable for RTS games, since they have so many units that synchronising everything is often infeasible. An old but still great article on implementing full determinism is this one:

[1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond](http://www.gamasutra.com/view/feature/3094/1500_archers_on_a_288_network_.php).

A downside to this model is that it usually adds quite a lot of lag to controls, since actions cannot be executed until all players know about them. Such input lag can be hidden by playing sounds and visual effects immediately when the user clicks. This way the player won't notice that his units don't react immediately.

Note that deterministic lockstep can also be combined with a client/server connection model where the data always flows through the server instead of directly between all players.

![](../../assets/1561ae7994c03cc5.jpg)

Implementing full determinism is incredibly difficult. If any differences exist between the simulations on the clients, then these differences will grow over time and result in the desynchronisation of the game. Lots of tricks need to be used to achieve determinism. For example,

*floats*cannot be used because of rounding errors: all logic needs to be build on

*integers*. Random number generators can only be used if their seeds are synched and they are used in the exact same way. This might for example go wrong if one player runs on a higher graphics quality and thus has extra particles on his screen. Those particles might also use the random number generator and thus desynch it. A simple solution is to use a separate random generator for non-gameplay objects, but this is easy to forget, breaking the entire game.

Getting determinism right is such a challenge that many games that use it add a mechanism to check the correctness of the simulation. They regularly send a checksum of the entire gamestate over the network. Checksums are small so this uses hardly any bandwidth. If the checksums are not the same then the game has desynched. To fix a desynch we could pause the game, send the entire simulation over the network and then continue from there. In older games you might recognise this problem when you got kicked out of a game because of a "synchronisation error".

There are of course many more subtleties to network architecture than I have explained here. All kinds of hybrids are possible and there are many details that I have not mentioned, like vulnerability to cheaters and host migration. I cannot discuss them all today, but I hope this blogpost has given a good summary of the basics. One important topic that really needs to be explained in combination with the above information is

*relay servers*so I will cover that next week.

So what is your prefered solution?


ReplyDeleteI am using Unity 3D, and thinking about Photon cloud server to make this kind of thing happens.

Totally depends on the kind of game you are making.

DeleteI think there might be a too broad generalization of these ideas. The actual truth is that there are more variants of these models depending on the actual specifics of your game (as you already point in the last paragraph). I am working on a good example right now.


ReplyDeleteFirst, the game design is based on the client potentially receiving "false" informations from whatever is the authoritative owner of the game state. Therefore, the client/server model already seems to be the only alternative: we can't allow the client to know the actual state of the game, only the state provided by the authoritative source, here the server.

Second, we still want the game to be playable in solo and multiplayer (local or not), so I provide the server with the game, and actually all the game happen only on the server, except representation of course which happen on the client.

Third, it's a game with no physics or collision, real-time but with discrete space structure. The client does display some nicely moving things but the actual state of the game is totally discrete and is not updated very often. It's not an action game (it's a RTS) and it's not as precise as, say, Total Annihilation because it don't plays in a physical world. This case is not very common but actually it is very very interesting to explore.

I then realized that client/server latency is not a problem in this specific case. Because the game state is not updated very often and because the whole state of the game is very small by nature (even with massive maps), I can send the whole world state to all clients in no time.

So in this case, client/server with really no optimizations is ok. Still, it's a very unusual case, of course.

"I think there might be a too broad generalization of these ideas"

DeleteIt definitely is a broad generalization. But I cannot discuss everything without writing an entire book... ;)

Nicely written, Joost. One day I shall make a multiplayer RTS game with a deterministic lockstep architecture, sadly that's a while away in the future. You should think of writing a quick book about networking for games with code samples. I'd buy that! :)

ReplyDeleteHi Joost, excellent article as always a joy to read!, two question, does Awesomenauts use extrapolation to calculate others player movement or do you just update based on the position received in the messages? and what is the time interval between players position messages?

ReplyDeleteWe send position updates 30 times per second and do interpolation, not extrapolation. We want to experiment further with extrapolation, but it looked really bad when we had tried it years ago because whenever a player turns around the extrapolation will move him extra far in the wrong direction.

Deletethank you Joost for your answer!

DeleteHi. Do you know of any other games built upon the same peer-to-peer technique you've used on Awesonauts ?











ReplyDeleteI'd love to read more about it, specially to clarify how to solve

some battle engagements scenarios.

Please bear with me in the following scenario description:

Assumptions:

- player A is chasing player B to hit him.

- A has a slightly higher speed than B and

he will eventually catch up B inside of an imaginary melee hit-range.

Instant #1 (from a real world time perspective):

- A sees his true self as inside the hit-range against B and fire its melee attack.

Actually A is trying to hit a past version of B

and has not really yet grasped B inside of his range.

- B sees his true self falling in a hole

and sees a past version of A, which is not yet close enough to hit him.

Instant #2 (from a real world time perspective):

Possibility from A point-of-view: A hits B. B gets damaged.

Possibility from B point-of-view: B falls in the hole, escaping from A.

Do you have a special handle case when two players engage

against each other in a scenario like that ?

I've read the sliding bug post and it's not yet that all clear to me

how would you solve it.

Thank you very much.

We solve this situation by always favouring the attacker. If you think you are hitting someone, then you are. The benefit of this approach is that controls in Awesomenauts feel really direct and immediate, even when playing on bad internet.




DeleteThe obvious downside of this is that evading attacks is more difficult and even becomes impossible if the ping is high. We will soon be experimenting with extrapolation to see whether we can lessen that problem a bit, but right now we just take A's view and that's it.

How much of a problem this is really depends on the speed of your game and what players see. Awesomenauts is very fast so for us this is a serious problem. A game like League of Legends is much slower so that kind of game could get away with more (they don't use peer-to-peer by the way so it doesn't matter to them).

It is also much less of a problem in FPS games, since bullets fly instantly and you cannot see where your opponent is aiming exactly. In an FPS dying because of lag is much less noticeable. In Awesomenauts you see every bullet fly, which makes it a very different situation.

Many thanks for the prompt reply.

ReplyDeleteHi! I really liked your post! I know its been like 6 months since you posted it, but it helped me a lot! I'm currently developing a melee-one-hit-kill-multiplayer-arena game in Brazil using USA relay servers (130ms ping and worse). We're using interpolation and extrapolation to minimize the lag issues, this approach has been treating us well... except when it comes to kills.

ReplyDeleteWe are using the attacker's point of view to determine the kill, and when that happens we fake the attacker's position on the target's client so the user will ate least see the killer next to him. But even with all this, we have some problems syncing the animations and making the death/kill thing smooth.

The animation problem is the one that bothers me the most, since when the attacker starts its attack animation on the target's client it will not be close to the target, and some time after that when we receive the kill confirmation message the attacker will get close to the target. Because of that the animation sometimes ends before the attacker its close to the target, you can imagine the chaos.

Do you have any suggestions of ways to work around these issues?

Thank you very much! And your blog is really awesome (no pun intended)!

Are these kill animations extremely fast (below 0.2 seconds), or is your lag extremely high? Otherwise it seems odd to me that the kill animation would have finished before the kill happened. And even then, all the packages should have similar delay, so why would the kill information come in before the positional information? Are you working with extreme jitter here?




DeleteIn general for things like this it is usually best to adapt the animation or gameplay to what is feasible in terms of networking. For example, if the kill animation starts with a big jump, then you can do the position correction during the jump. That looks a lot better than shifting the character while he's standing on the ground. You could even do several kill animations depending on the distance that needs to be traversed, and use those longer distance versions only on the client and only when needed.

Bungie has a great talk on handling such issues in Halo Reach. They have custom networking code for various attacks to hide the lag wherever it can best be hidden for that particular attack. If you haven't checked it yet I highly advice doing so, it's really awesome:

http://www.gdcvault.com/play/1014345/I-Shot-You-First-Networking

I think maybe the problem is the time we chose to move the attacker to the target, if our animation lasts something near 0.6 or 0.7 seconds, when we stop moving the attacker its possible it will be in the middle of the animation.

DeleteIf we received the attack message in the target's client at 0, received the kill message at 0.3, with the time we are currently using, when we are near the target we may be at 0.5 (we are using 0.2 second to move the attacker), with our current attack animation it can seem "out of sync". Slowing down the animation may be a good option too.

I just watched the talk and its really really great! I'll try to implement some of the ideas of the talk as soon as I can hahaha!

Thank you so much for answering and for linking the talk!

I'm not sure I understand the timing you describe.




DeleteLet's say that that attack animation lasts 0.7s. On the attacker's side the attack starts at 0.0s and takes until 0.7s. So the actual kill message is sent at 0.7s.

Let's say we have 0.3s lag (very high) and no jitter (unrealistically low). On the client the start of the attack animation then arrives at 0.3s. The animation thus ends at 1.0s, which is also when the kill message arrives. That means that on the client's side you basically have from 0.3s to 1.0s to slide the attacker towards the target.

These are very different timings compared to what you describe, what causes the difference? What am I misunderstanding here?

Sorry for the late response, I was busy at work theses days! I think I'm not explaining it very well, I'm sorry hahaha





DeleteThe thing is the animation isn't a jump or something like that, is a sword slash, and in the middle of that animation we check for a kill (if the sword hits a player), and if it happens we send a kill message.

Assuming the values you said, and assuming the time we set for the attacker to move from its location to the target is 0.2s:

ATTACKER CLIENT:

0.0 - starts attack (send attack message)

0.6 - hits player (sends kill message) - this is kind of a corner case, but I think the problem is here

0.7 - ends animation, attacker is happy and well

TARGET CLIENT:

0.0 - nothing is happening

0.3 - attacker starts animating (we receive the attack message, but we don't know yet if a kill happened, so the attacker its still somewhat far from the target)

0.9 - we receive a kill message, and starts moving the attacker to the target (so we can compensate for any differences in their positions and the kill feels more realistic)

1.0 - attack animation ends

1.1 - attacker reaches target

I think if we change our animation to something that includes movement and do some treatment relative to the time we take to move the attacker to the target (maybe calculating the remaining time for the attack animation to end), we can have better results.

Sadly we can't change our character's animation right now, we are still looking for an artist, and our models and animations were pre-made assets, but what you said gave me an idea.

What if we send the attack message only at the "end" of an attack, and in that message we say if we killed anyone? Receiving that, on the other clients we will have all the information to do any adjustments we want, and the attacker won't have started its animation yet. I wrote "end" because it doesn't necessarily need to be on the end of the animation.

Do you think this could work?

And really thanks again (a million times) for taking the time to answer my question!!