---
title: Bitcrunching numbers for bandwidth optimisation
url: http://joostdevblog.blogspot.com/2014/01/bitcrunching-numbers-for-bandwidth.html
author: Joost van Dongen
published: '2014-01-04'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)is optimising bandwidth usage. Without optimisations, just sending position updates for one character to one other player already costs 240 bytes per second (30 updates per second at 4 bytes each for both X and Y). And this is just a fraction of what we need to send: Awesomenauts can have up to 35 characters running around the game world, and we need to synchronise much more than just their positions. As you can see, bandwidth usage quickly spirals out of control, so we need to be smarter than just naively sending all the data all the time.

In the many months we spent on bandwidth optimisation, we employed lots of different techniques. The one I would like to talk about today can massively decrease bandwidth by crunching numbers on the level of individual bits. This technique not only worked great for the multiplayer implementation of Awesomenauts, but I am now also using this extensively for reducing the size of our replays.

Let's have a look at the core idea here. Storing one

*unsigned int*normally costs 32 bits. In this we can store a value in the range of 0 to over 4 billion. However, we rarely need a range as big as that. For example, the amount of Solar you collect during an Awesomenauts match rarely goes over 5,000. In a really long match we might go past that, so let's bet on the safe side and say we want to store Solar values up to 10,000. This could be stored in 14 bits, since 2^14 = 16,384. That is less than half of the normal 32 bits used for a value like this!

Using too many bits is not a problem in memory since modern computers have plenty of that. But when sending the Solar over the network, we would like to use only those 14 bits we actually need. However, normally we can only handle data on a byte level, not on a bit level, so the best we can easily do is to store this in two bytes (16 bits).

What we need here to solve this is a

*bitstream*, something that we can use to group together a lot of values on a bit-level. This way we can just grab a block of memory and push in all the values we want to send over the network. The idea is quite straightforward, so let's jump right in and have a look at how one could use that:

//Class for pushing bits into a block of memory class BitInStream { public: BitInStream(char* data); void addUnsignedInt(unsigned int value, unsigned int numBits); void addBool(bool value); }; //Class for reading bits from a block of memory class BitOutStream { public: BitOutStream(const char* data); unsigned int getUnsignedInt(unsigned int numBits) const; bool getBool() const; }; //Example of using these void main() { //The bits are stored in this char data[4]; //Example of writing some values BitInStream bitInStream(data); bitInStream.addUnsignedInt(solar, 14); bitInStream.addUnsignedInt(itemsBought, 6); bitInStream.addBool(isAlive); bitInStream.addUnsignedInt(damageDone, 10); //Read back values BitOutStream bitOutStream(data); solar = bitOutStream.getUnsignedInt(14); itemsBought = bitOutStream.getUnsignedInt(6); isAlive = bitOutStream.getBool(); damageDone = bitOutStream.getUnsignedInt(10); } |

The details of actually implementing the bitstreams itself is too much for this blogpost, so I will leave that as a fun exercise for the reader. Hint: you can use bitwise operators like |, ‹‹, &.

When looking at this code there are a number of observations to make. First is that I am actually using only 31 bits while storing them in 4 bytes. In other words: I am wasting 1 bit here! This is something that almost always happens when using bits: at some point they need to turn into bytes, since that is what network packets are measured in, and we usually waste a couple of bits there. This loss can be decreased by using larger bitstreams with many more values in them.

A much more important realisation here is how easy it is to break this code. If I read back the solar with the wrong number of bits, then not only will the solar be complete garbage, but also all values after it. The same happens if I accidentally read back values in the wrong order, or forget to read one. The compiler will not warn you of any of these things and debugging on a bit-level is difficult, so this produces extremely stubborn bugs! Another easy mistake is to use too few bytes for the data, resulting in buffer overflows and thus memory corruption, or to use too many bytes, resulting in wasting bandwidth. In short: use bitstreams only when you

*really*need them and be extremely careful around them!

So far we have only stored the easy kinds of data:

*bools*and

*unsigned ints*translate very easily to bits. However, many things in a game are

*floats*. When using an

*unsigned int*, taking just its first 10 bits results in a valid number, just with a smaller range. But with a

*float*taking those same 10 bits results in nonsense. How can we send

*floats*with arbitrary numbers of bits?

The trick here is rather simple. A

*float*has a number of properties that we usually don't need.

*Floats*have very high precision near 0, but when storing a position, we want the same precision everywhere.

*Floats*also have an extremely large range, but for that same position we already know the size of the world and we don't need to be able to store values outside that range.

![](../../assets/bb5eced1ec1b4beb.gif)

Knowing these things we can store positions (and most other

*floats*) in a different way. Levels in Awesomenauts happen to all be in the range -10.0 to 30.0. Knowing this we can just store the x-position as an

*unsigned int*with an arbitrary number of bits. If we want to store a position in 8 bits, then the lowest value (0) means position -10.0, and the highest value (255) means position 30.0. Values in between are just interpolated. This is a simple and very effective trick. Depending on how much precision we need, we can use more or less bits.

![](../../assets/0c12bee7772b912b.gif)

When synching over the network we actually don't need all that much precision, since the receiver is not using the position for a physics simulation. He mostly just uses it for visualisation and checking whether a bullet hits. So in Awesomenauts we use 13 bits for synching the x-position and another 13 bits for the y-position, which is a lot less than the normal 32 bits each would need as a

*float*!

The same idea can be applied to many other things that are also

*floats*and for which we know the range. Some things even need extremely little precision. For example, the health of other players is only visualised in their healthbar, so we only need to synch as many bits of that as are needed to make the healthbar look correct. Since healthbars are usually in the order of 100 pixels wide, we can store health in 7 bits, even if the actual range of the health might be 0.0 to 2000.0. With 7 bits our for that range would be only 15.625, but more isn't needed because the difference is not visible in the healthbar anyway. The simulation is not influenced at all by this, since the owner of the character still stores the full precision float for the health.

![](../../assets/43ad85e3d960a434.jpg)

Using tricks like these we managed to get the bandwidth usage of Awesomenauts down to around 16 kilobyte per second. This is the total upload needed at the player who manages bots and turrets. The five other players in a match don't manage those bots and turrets, so they use far less bandwidth still. For comparison: our very first network implementation in the Awesomenauts prototype we had four years ago used around 50x (!) more bandwidth. Bit-crunching numbers as explained in this blogpost is just one of the many tricks we used to decrease bandwidth, but it was definitely one of the strongest!

Very interesting post. I feel bandwidth optimisation is an huge subject same as AI stuff, and others.. I tried few years ago to make a realtime network multiplayer game and It turned out to be a mess.



ReplyDeleteI read a lot about client-side prediction, data synchronisation and so on. How much did you use this kind of things in Awesomenauts ?

(Just to say, I'm really interested on more post about networking and multiplayer :) )

Awesomenauts being a complex online multiplayer game, we of course spend ages on all the aspects of multiplayer. :)




DeleteWe tried client-side prediction, but it turned out to be really messy: it is possible to instantly turn around in Awesomenauts and that means that whenever you do that, the client predicts the wrong movement. Correcting that looked pretty bad, so I removed it. Either I am misunderstanding some important aspects, or client-side prediction just doesn't work as good in a game with movement as erratic as in Awesomenauts. I guess it works better in a more predictable game like a racing game, where the only drastic frame-to-frame changes that can happen are collisions, which the client can also predict. Things like suddenly braking, steering and accelerating are relatively smooth effects and thus won't break the prediction as much.

Having said that, there are still plenty of opportunities for client-side prediction in specific elements. We are specifically going to experiment with predicting bullet movement in Awesomenauts in the coming months, hopefully this will decrease lag problems a bit. If that works well, we might look into specific skills to see what elements in them are predictable.

A big challenge here is that context-specific prediction implementations make a mess of code, but I don't think a generalised prediction system can work well in Awesomenauts.

You can actually further optimize this.






ReplyDeleteThe example of determining the size of the world and store that as position is still a 'naive' approach.

What actually changes is the change since the last network transmission.

So what you could do is check if the position is changed since the last network transmission. But again, keeping track of the absolute position is unnecessary. Creeps can only move a certain amount of units each network transmission interval. So instead of storing the complete position. Split the world up in cells of eg 16, again split each cell of 16 up in 16 smaller, again and again. For example a recursion of 4. Note for this is no data structure necessary.

Now when the position of a creep changes see if its position in the virtual biggest 16 cells is actually changed. Do this for the 16 smaller, and the other 16 smaller and once again.

Now if you split the world in to some clever value so that actually only the smallest cell changes (due to the network transmission interval) only the change in that cell has to be sent.

This incurs an overhead of 4 bits on top of the position since you have to let the recipient know whether a cell has changed and need to be read out.

So in worst case scenario when all cells are different, you actually sent 4 bits more than needed but that is the worst case scenario which only can actually happen when a unit teleports.

We actually already have something like that on positions in Awesomenauts, so on average they use a lot less than 13 bits. It did get rather complex in combination with unreliable packets, but it worked really well to further halve the average bits used for storing positions. :)

DeleteI'm wondering if you considered using Google's Protocol Buffers for this? It solves pretty much this exact problem.

ReplyDeleteInteresting, I had never heard of that! I just looked it up and read the basic description, but in practice I doubt it would have worked for us: we ended up using a lot of context-specific tricks for further optimisations (on top of the ones this blogpost is about), and such libraries usually combine really poorly with such custom requirements.

Deletebrilliant article! I have been using byte streams for this, but a bit stream is a brilliant optimization.






ReplyDeleteOne useful tip for your stream class, the stream should able to go into a read and write mode, then you can both read and write from a single function:

void parseUnsignedInt(unsigned int& value, unsigned int numBits); // reads bits in read mode, otherwise writes bits in write mode

This saves a huge amount of maintenance and dramatically avoids the chance of mismatching your parsing, which as you said is difficult to debug.

This post misses out on the high-level techniques concerned with multiplayer code such as delta compression, input sync, etc but the techniques would apply to most networking implementations. Thank you Joost!

"This post misses out on the high-level techniques concerned with multiplayer code "

DeleteI try to pick a single small topic and go into depth on that, so there are indeed dozens of other interesting multiplayer topics I could be writing about. I really should do more of them in the future and cover more ground. :)

Please do, this is really interesting stuff!

Delete