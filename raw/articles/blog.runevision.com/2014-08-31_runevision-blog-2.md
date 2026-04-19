---
title: runevision blog
url: https://blog.runevision.com/2014_08_31_archive.html
published: '2014-08-31'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Two weeks ago I was a week in Seattle for Unity's Unite conference. While in the city, I also had a chance to visit the [Valve](http://www.valvesoftware.com/) offices and try out their famous VR demos. The headset we tried was [the one using QR codes](http://www.roadtovr.com/hands-valves-virtual-reality-hmd-owlchemy-labs-share-steam-dev-days-experiences/) to track alignment - not the newer ["polka dots" headset](http://techcrunch.com/2014/06/03/valve-shows-off-its-polka-dot-vr-headset/) they've been showing off too this summer, though I suspect the difference is not in performance but just in demands on the physical environment.

![](../../assets/7d61775e26209cc3.png)

The guys from Valve were not only brilliant but also very friendly. We talked with them at length, and we were impressed with how they patiently and tirelessly showed the demos to each of us in turn, as well as taking us on a tour of the sizable office.

![](../../assets/3ba830cc096d1fb8.jpg)

Like everyone else who have seen their VR have already said, the demos are amazingly effective. Though the pixels are visible if you look for them, the resolution is easily high enough to not be a problem. The world around you doesn't seem pixelated either; just a tiny bit blurry. Before I go on to praise the head tracking, let me get my one reservation out of the way.

### Eye distance calibration and sense of scale

One reservation I have about the demos I was shown was that I felt only a limited sense of grand scale in those demos that were meant to showcase that. Most of the demos took place in virtual spaces of limited size (nothing was further away than about 10 meters) and those worked really great. The environment in those felt tangible and I felt a strong presence. However, a few demos placed me in environments with towering structures extending for what should amount to hundreds of meters, and those felt less real for me. In those environments it felt like objects that were supposed to be hundreds of meters away were maybe only 10 or 20 meters away, though it's very hard to judge when the perspective cues don't match the stereoscopic depth perception cues at all.

I suspect that lack of eye distance calibration (or interpupillary distance (IPD) to use the technical term) was the cause. The demos were setup to be easily viewed by many people in a row, and IPD calibration was not part of the process since it was deemed to not make a large difference. I would agree with that for the most part, though I think it does have a significant effect on the large-scale virtual environments and was the cause of the weaker sense of presence I felt in those.

Normally when a virtual object is supposed to be near-infinitely far away, the distance between it's left eye depiction and its right-eye depiction on the screen(s) of the headset should be the same as the distance between the centers of the eyes, so that the eyes will look out in parallel in order to focus on the two respective images. This will match what the eyes do in reality when converging on objects nearly infinitely far away. (For the purposes of human stereoscopic vision, anything further away than just about a hundred meters is practically infinitely far away.) If a person's actual IPD is larger than what is assumed in the VR setup (hardware and software), then the eyes will not be looking out in parallel when focusing on a virtual object nearly infinitely far away, but rather look a bit inwards. This will cause the eyes and brain to conclude that the object is in fact nearer, specifically at the distance where the focus lines of the two eyes converge and meet each other in a point.

What's worth noting here is that no amount of up-scaling of the virtual world can compensate for this. If the "infinite distance" makes the focus of the eyes converge 10 or 20 meters away, then that will be the perceived distance of anything from structures a hundred meters away to really distant objects like the moon or the stars. A corollary to this is that things in the distance will seem flattened, since an infinite amount of depth is effectively compressed into a few meters. This too matches my impression, though I didn't have much data to go on. One huge virtual object I encountered in one of the demos was of roughly spherical shape. However, it appeared flattened to me at first while it was far away, and then felt increasingly round as it came closer to me. You might say that things very far away also technically appear flat to us in reality, but in practice "flat and infinitely far away" doesn't feel flat, while "flat and 10 meters away" does.

![](../../assets/84f177af62c48d21.jpg)

Luckily, eye distance calibration is not a hard problem to solve, and Tom Forsyth from Oculus [points out that the Rift comes with a calibration utility](http://www.oculusvr.com/blog/vr-sickness-the-rift-and-how-game-developers-can-help/) for this that people are encouraged to use. I should also say that none of my colleagues who tried Valve's demos had the same reservation as me about sense of scale. It could be that their IPD better matches what was assumed in the VR setup, or it could be that potential IPD discrepancies were just less apparent to them.

### Approaches to head tracking

What I found most impressive about Valve's VR technology was that the head tracking and stabilization of the virtual world is basically solved. Unlike Oculus' Development Kit 1, the world doesn't blur at all when turning the head, and it feels completely stable as you look and move around. This makes the virtual world feel very tangible and real. You can read more about the technical details elsewhere, but it's basically achieved with a combination of low latency, high frame-rate, and screens with low persistence of vision, meaning that for every frame the screen only shows an image for a very brief period, being black the rest of the time. (Old CTR monitors and TVs were all like this, but it's not common for LCD screens.)

The tracking using QR codes worked very well then, except when it didn't. If you get close enough to a wall that the head-mounted camera can't see any one QR code fully, the positional tracking stops abruptly at that point. The effect is that of the world suddenly moving forward together with your head, until your take your head back far enough that the tracking resumes. This happened quite often during the demo and every time broke the immersion a lot while also being somewhat disorienting. Together with QR codes having to be plastered everywhere on the walls, going away from that approach is probably a good idea.

"For Crystal Cove, it's going to be just the seated experience"Nate Mitchell, Oculus

I haven't tried the Oculus Rift Development Kit 2 (at least not its tracking), but from what I've heard, it's based on a kind of camera in front of the player, recording the movement of the headset. And supposedly, it only works while approximately facing that camera. Oculus have also been issuing comments that [the Rift will be meant to be used while sitting](http://www.polygon.com/2014/1/11/5298510/oculus-rift-crystal-cove-intended-as-a-seated-experience), which matches up with that limitation. Having tried a few different VR demos, that seems awfully restricting. It will work mostly fine for cockpit-based games taking place inside any kind of car, spaceship, or other vehicle with a "driving seat" you stay in all the time. But for a much broader range of games and experiences, having to face in one direction all the time will be severely limiting or directly prohibitive. It's currently unclear whether the limitation is only for the Crystal Cove headset (Development Kit 2) or also for the final consumer version.

### Freedom of head and body movement

Luckily there seems to be hope yet that even Oculus' headsets can be used for experiences with more free movement, whether Oculus themselves will end up supporting it or not. I had a chance elsewhere in Seattle to try out a demo of [Sixense](http://sixense.com/)'s tracking and motion controller technology (also described in [this article on The Verge](http://www.theverge.com/2014/8/18/6030935/motion-controllers-make-great-virtual-reality-lightsabers)). Basically they had slabbed their own motion tracker onto the Rift headset, replacing the Rift's own head tracking, as well as equipping the player with two handles that are also motion tracked.

![](../../assets/ba4b2056f264c7d9.jpg)

The VR demo to show it off with was one of being a Star Wars Jedi training with lightsabers against that Remote sphere that hovers and shoots lasers - albeit without being blindfolded as in the original movie. The tracking of both head and hands worked wonderfully, and allowed all the attention to be on the quite engaging gameplay.

While Valve's demos were the visually most impressive spaces to be inside, the Sixense demo was easily the most overall engaging VR experience I've had. Sony have sold one-to-one motion-tracking Move Controllers with the PlayStation for years, but solid motion tracking controllers combined with VR combines into an experience that's feels real and is intuitive at a whole different level.

The promise of waving stuff around with your own hands got mainstream with the Nintendo Wii, but the tracking was crude, and only mapped on a gestural level. You swung your hand to indicate swinging a racket, and the in-game avatar would trigger a racket-swing as well, but only with the approximate same direction and not with the same timing at all. Sony's Move Controllers fixed that, but still the sense of depth was missing and it still felt more like remote-controlling a utility rather than actually holding it in your hand, and you have only very little sense of whether your aim might be correct. This limitation will always exist as long as the visuals are not in stereoscopic 3D.

![](../../assets/ac8af3e2d82ac11f.jpg)

Using accurate motion tracking of the hands in VR produces an entirely different sensation. When I tried that lightsaber demo I felt like I was really holding those lightsabers, and swinging and turning it to block the incoming lasers felt like the most intuitive thing, even though I've never - eh - blocked lasers with a lightsaber in real life, or handled any kind of sword for that matter.

### Personal style in VR

Equally impressing, when watching others play the lightsaber demo, it became apparent how much the demo and technology let people approach the gameplay with their own style and personality. Some would move the lightsabers only just enough to block the lasers, others would be swinging them more gracefully around, while yet others moved with big and stiff robotic-like moves. As the interfaces to VR begins to imitate and approach the way we move and interact with the real world, our mannerisms and ways of movement from the real world will begin to translate there as well.

To go back to the technical side of things, the Sixense technology is based on magnetic fields. A Valve employee said they'd been experimenting with tracking based on magnetic fields as well, but hadn't found it to be very reliable. Whether it's because they didn't account for disturbances in the magnetic fields as the people from Sixense claim to do, or whether it really is less reliable but just wasn't a noticeable problem in the demo in question is hard to say. What seems clear though is that there is loads of promise in these new forms of interaction, and that it will be very exciting to see what kind of experiences and interactions in VR we'll be having in the coming years.

### Dulling of reflexes

While the advances in VR have made huge strides now in a very short time towards eliminating simulator sickness and making the virtual environments appear much more real to our senses, this potentially can have a negative side as well.

As the way the virtual worlds appear to our senses get increasingly closer to how the real world does, our motor skills, reflexes, and other instincts are also increasingly transferable from one to the other. While people don't have any problem having their avatar walk off the ledge of a cliff in a traditional 3D game, many people feel physically unable to walk off the ledge of a cliff in VR, while other can, but have a hard time forcing their body to do it. A positive side of this is that VR can be used to treat a variety of physical and physiological illnesses by performing training in VR where the results transfer to the real world.

Consider though that many game scenarios tasks players to be daring and bold, subjecting themselves to hazardous environments to overcome impossible odds. And consider that failing repeatedly without real consequence is a normal part of playing such games. In a VR game, a scenario might see you dodging large rocks being hurled towards you, and failure to do so might see you die in the game, but physically being unharmed in the real world. The natural reflex for most people in such a game will be to dodge the rocks not just for gameplay reasons but even purely instinctual as well. However, one might speculate that the more times the body and brain experiences being hit by a rock in the game with no physical consequence, the more the reflex to avoid the rocks will be weakened.

Imagine too that the game is hard and won't let you win if you duck and avert the rocks too aggressively, thus loosing focus on what's going on elsewhere around you. Instead you'll need to adapt to only just avert the rocks with minimal expenditure. Your chances of averting the individual rock will be a bit lower, but your chances of winning the scenario increases.

As reflexes and adaptations to stimuli can transfer between the real world and VR, can this adaptation towards ignoring the body's natural reflexes also accidentally transfer to the real world? Will people navigating hazardous virtual environments haphazardly have a risk of reacting less acutely to hazards in the real world as well?

As far as I have gathered, this is something we don't yet know very much about. [Some studies have been made decades ago](http://www.agocg.ac.uk/reports/virtual/37/report37.htm), but based on VR technology nowhere in the same league as what we're beginning to have available today. It seems to be an important area of study though, and I'll be curious to see what the findings will be.

In the mean time I will probably lean towards indulging mostly in VR experiences that let me peacefully enjoy strange and beautiful places and use some serious moderation with experiences that will put me in a sense of danger and test my survival instincts. Deflecting lasers will be exempt from this.