---
title: 6 Ways 3D Audio Can Expand Gaming Experiences
url: https://www.gamedeveloper.com/audio/6-ways-3d-audio-can-expand-gaming-experiences
author: Michel Henein
published: '2013-11-01'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# 6 Ways 3D Audio Can Expand Gaming Experiences

3D audio is an often over-looked tool available to game developers which promises to deliver a more immersive audio experience than standard stereo, 5.1, or 7.1. This blog discusses six ways 3D audio can enhance the player experience:

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

“Sound is that which does not simply add to, but multiplies the effect of the image.” Akira Kurosawa.

Intro:

Over the past few years, we’ve witnessed sound for cinema being transformed from 5.1/7.1 to the high channel-count and object-based sound formats available for today's film-makers to extend 'surround sound' to the next level of immersion for audiences (i.e. Dolby ATMOS, DTS Multi-Dimensional Audio, and Auro Technologies’ Auro 3D). These formats add speakers all around, including above the listener to emit 'elevation cues', allowing sound to pan around in all three dimensions.

Games can also use elevation cues to further expand audio in all three dimensions (without the need for additional speakers by using stereo headphones, for example); through the use of digital filters (HRTFs derived from dummy-head measurements or modeling of the auditory cortex), a convincing 3D 'effect' can be created by leveraging a sound object's XYZ position in game space to simulate a sound being heard at a corresponding point in a 3D sound-field.

Yes, 3D audio technologies and solutions have been around for quite some time but the majority of today's game developers do not implement true 3D positional audio into their games; instead developers tend to stick with standard stereo and 5.1 surround sound as the de facto standard for the vast majority of titles being produced today. Keep in mind that not all 3D audio solutions are alike and really compelling 3D audio typically requires quite a lot of processing resources — precious resources that aren't always made available for audio processing. With the explosion of multi-core processors for mobile gaming, powerful next-gen consoles arriving later this year, and dedicated audio DSP resources being offered on new GPUs (i.e. AMD's TrueAudio), the conditions are ripe for the mass adoption and standardized use of compelling and powerful 3D audio solutions by game developers for their game titles across many different platforms.

Here is what 3D sound can provide game developers:

Elevation: placement above and to some degree, below

Azimuth: placement in front, behind, and to the sides

Distance: using elevation and azimuth to define a position for a sound inside a 3D sound-field (i.e. a spherical sound-field wrapped around you) the sound can be pushed out in space with distance to allow improved depth perception (using distance cue processing, 3D room simulation, for example.)

These parameters expand the sound-field beyond what stereo, 5.1, and 7.1 can produce (which are 2D formats). For developers looking to offer a bit more realism and immersion for their players, 3D audio may be the 'lowest-hanging fruit' available to do so.

Here are 6 ways developers can use 3D audio to expand gaming experiences:

Enhanced immersion for mobile games:


There are tons of fun games on the small screen (for your mobile phone or tablet) however, 3D audio can be used to create the illusion of a larger game world through the use of an immersive sound-field that envelops the player. While there may be a bit of a disconnect between a small screen and an enveloping, spherical sound-field, 3d audio for mobile gaming can heighten the feeling of being "in the game."

Ear Monsters, by Ear Games, is a forward-thinking iOS game that employs the use of 3D audio to drive gameplay, rather than visuals. The use of 3D auditory cues to drive gameplay serves to extend the boundaries of the game world beyond the small screen of the mobile device, for example, the player can tap in the general direction of the sound being heard in 3d space (for example, tapping the top of the screen if an attack is heard coming from above.)

Sound-centric games:


Using 3D audio, sound-centric games can:

Help the visually impaired to enjoy gaming. Ear Monsters allows players to play without needing to see what’s happening on screen.

Create interactive stories using voice over and sound effects positioned in a 3D sound-field for an immersive story-telling experience.

Use darkness and lack of visibility to increase reliance on 3D sound cues can make more compelling and immersive horror games.


This list barely scratches the surface with all the possibilities that sound-centric games can offer players.

Improve situational awareness in 3D games (i.e. 3D FPS):


3D audio can improve situational awareness in FPS games by relaying sound cues from certain directions correctly to the player. For example, in most modern combat FPS games that rely use stereo, 5.1, or 7.1 audio delivery, when a player on the ground level is being shot at by a sniper who's perched high in a tower, the sound of the sniper’s shot does is not heard from above. With 3D audio, the sound of the sniper’s shot would be heard from above, like it's supposed to.

Reduction of UI graphics:


It is well known that using sound to substitute for UI (i.e. running out of ammo or player health indication using sound prompts) can help remove display clutter. 3D sound can be used to extend the sound cues by using space to indicate more information (i.e. using a sound cue with elevation to indicate a rainstorm is coming.)

Positional 3D audio for multiplayer voice chat:


By leveraging 3D audio, a '3D radio communications' of sorts can be created to hear team member communication based on actual position in the game (i.e. if a member of a squad is up on a hill, the radio communication from that player would be elevated.)

3D audio compliments the VR experience:


Conventional stereo, 5.1, or 7.1 audio playback limits the sound field to a two-dimensional plane creating a disconnect with the visual field offered by VR. 3D audio eliminates this problem by allowing a full 3D sound-field to perfectly compliment the 3D stereoscopic visual field; head-tracking (with the Oculus Rift, for example) coupled with 3D audio allows the player to move their head around and expect to hear sound all around them correctly, including sounds from above.

How can developers implement 3D audio in their games?

Games typically use audio middleware solutions (FMOD and Wwise, for example) for their run-time sound engines so developers can utilize 3D audio technologies made available from Dolby, DTS, GenAudio, Auro 3D, and Iosono (check with your audio middleware provider for available solutions.) Encourage your teams to explore using either of the various 3D audio solutions available today to enhance the aural experience for your title(s) beyond what stereo, 5.1, and 7.1 can offer.