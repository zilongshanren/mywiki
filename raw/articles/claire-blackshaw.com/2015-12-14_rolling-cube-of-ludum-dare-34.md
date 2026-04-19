---
title: Rolling Cube of Ludum Dare 34
url: https://claire-blackshaw.com/blog/2015/12/ld34/
author: Claire Blackshaw
published: '2015-12-14'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Rolling Cube of Ludum Dare 34](../../assets/57f8129bc82d65b9.gif)

So while it’s fresh I’m writing up LD34, a successful failure.

First time ever the theme’s were tied so we ending up doing both growing and two button. Which are both great themes. My idea quickly came once I dismissed anything based on plant growing for reasons I shan’t discuss here. So I quickly settled on the idea of a ball bouncing away from an explosion shedding mass, grabbing other bits of shrapnel and trying to keep gaining mass to stay alive and ahead of the explosion.

We are getting ahead of ourselves, Ludum Dare preparation is a critical stage. Every Ludum Dare my preparation tends to match my results. When I do a successful warm up I do a successful game. I made the decision to work on Psybrus, @Neilogd engine, which I’m currently using for a personal project.

- Let’s look at the warm-up commits.
- Initial Psybrus submodule at revision...
- Trying to get skeleton working
- Fixed the state but still broken
- Fixed transition bug by adding dummy object
- Rendering working with new stateless render
- Testing physics, collision broken
- Fixed physics and tweaked camera
- Found Crash when deleting model - Psybrus related
- Basic menu controls, select a bunch of mucking about with the camera

Psybrus is a component based engine and in warmup I found some issues with attachment and detachment most of which were solved, some weren’t. The physics test took a bit to get working though the biggest thing found in warmup was moving to the new stateless renderer. It’s a lovely improvement but meant a lot of my skeleton code wasn’t up to snuff. A basic state machine, menu and camera in place I had warmed the tools but no game was made to prove out bits.

Friday I ran off to Cambridge to visit friends and ask my maid of honour to be my maid of honour. So arriving back at midnight I was already tied and hadn’t done pre-jam warm up. So now let's look at how the Jam itself went. As I said I got an idea rather quickly and immediately set off.

First step get a rolling cube escaping an explosion.

- LD48 Start and game idea
- Basic Render working
- Rolling Cube
- Rolling Shrinking Cube

This all went fairly well. Simple but the cube that is rendering is actually generated mesh not a model. I wasted some time on this but my plan was to generate the mesh for the junk ball so I could make it more interesting and “wear” it away in an interesting way. Though I never ended up using that.

- Falling blocks, crashes when you press r to reset
- Stupid crash fixed but still crashed when you press R to restart due...

I lost a bunch of time due to the attachment / detachment issues. The physics was unhappy with deletion. So I spent a bunch of time debugging that bit of the engine. I looked into pooling objects but dismissed it as the engine wasn’t setup for that just yet, outside the particle system.

- Crane Arm in and split off junk ball
- Fire Red Beam
- Fields of Rocks
- Eat Junk
- Stuff deletes now

I fired up Blender to make the first model, oh no wait I installed it first because I forgot to prep my 3D tools. There was some faffing remembering the controls and getting Blender export settings to match what I need. Generating the field of rocks was simple enough and the gameplay started showing up. Physics caused a range of issues. I spent hours poking and prodding Bullet. I lost hours digging into Bullet looking for ways for collider to respond to raycast without rigidbody but no luck. Some talk of ghost objects but I had issues. Though finally I just went in and hacked the physics code to force the position. It finally complied after hours lost. Eating junk was awesome when it went in but I hit that deletion issue. Managed to resolve it mostly by poking the engine. Engine commits aren’t shown here.

- Fixed AABB boxes
- Update Psybrus

So some stuff wasn’t rendering as we rolled into the distance. I realised that the AABB boxes weren’t using the correct transform. It was at this point Neilogd pointed out the AABB box had a simple intersection function. After swearing and groaning I missed this in my search, I marked it off as a lesson and moved on.

- Manual Camera Modes
- Rolling Scrap Balls

I added camera modes to flip between aiming mode, shooting mode and similar. Also I added the rotation code to the junk objects which really livened them up. The camera was planned to add a smoother transition but I didn’t get around to it.

- Sky Shader

At this point I lost a whole whack of time. To the frankly fun task of writing a fullscreen shader for a cool neon sky and floor grid. It immediately added a punch to the game that it needed. I loved the colours and I’m glad I did it, even if it did take a bunch of time.

- Crane Mock over

More time playing around in Blender figuring out bits but mostly remembering. Lots of time was lost to not warming up Blender. Things like making a sculpt stick, UV unwrapping, the PNG export being upside down and general issues.

- Fucking particles... well they work
- Fucking hacks for submission

From 21:30 until the 02:15 I lost a LOT of time to particles. It started off because I was looking at a bad particle example with Psybrus which was special case and 2D. So I lost a ton of time there. Finally getting the 2d/3d problem solved I have a bunch of transform and shader issues. Lots of poking with RenderDoc and finally the particles were rendering roughly in the right spot but DAMN IT they were slightly off. Finally after much bitching with and at Neil he was like, just times by two. Turns out it was a bug that he hit a previous LD and forgot to bug. Annoying but a laugh.

Particles barely working and looking kinda shit, I quickly rushed a shooting function in, hacked particles to slow down when the game did. It was kinda crap but I figured I would submit. Forgetting as I did the production build that I had a shitty kinda broken menu. It is skipped in debug for iteration speed.

### Conclusion

Yes this would have be faster in a flash engine, Unity or some other some such. Though I felt in control the whole time. Edit and Continue sorta works but is very flaky and I need to investigate. Honestly the build and iteration time was probably the biggest negative. Though I really like jamming in C++ esp as my day job isn’t game dev anymore and more game tech and supporting stuff. At all times I felt like I could dig in, either with RenderDoc or stepping through and hacking the engine.

Most of my time was lost to tools not being warmed up, obsessing over stupid tech stuff I should have hacked around and not being as familiar as I need to be with Psybrus. Though I keenly look forward to the next Jam and I likely will be doing that one in Psybrus as well.