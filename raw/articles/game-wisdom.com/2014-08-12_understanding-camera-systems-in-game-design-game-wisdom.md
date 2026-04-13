---
title: Understanding Camera Systems in Game Design - Game Wisdom
url: https://game-wisdom.com/critical/camera-systems-game-design
author: Josh Bycer
published: '2014-08-12'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

Its lesson time once again for people who may not be familiar with game design. Our topic today is all about the different types of camera systems, what they’re used for and some common tips and missteps to be aware of.


## Differing Viewpoints:

### 2D:

While today’s post may not be all that exciting for the designers and enthusiasts out there, it’s still an important topic and one that everyone needs to be aware of. Let’s start with the one that is the most familiar and that is the side view camera, otherwise known as the 2D camera.

2D cameras obviously are seen in 2D games regardless of the genre. Mario, Super Meat Boy, Sonic and a lot more examples. 2D cameras are incredibility easy to set up and design as you are effectively locking a camera to track the player from the side similar to a moving film camera.

The character usually stays either in the middle or a little bit to the left or right depending on the direction they’re moving and the camera tracks their position. The reason this is easy is that once you’ve figured out where you want the camera to track from, then it’s just a matter of matching its movement to the player’s.

![Super Meat Boy game design](../../assets/15af6a80243b08f1.jpg)


![Super Meat Boy game design](../../assets/15af6a80243b08f1.jpg)

2D cameras are popular in games built around high skill level due to giving the player a complete view of what’s going on

2D cameras and design allow for a very “pure experience” in the sense that the player will always be able to see what’s happening and can then plan their moves around that.

There are no problems with enemies hiding off camera or worrying about the camera getting stuck when making a tricky jump.

Because of this pure experience, 2D titles are very popular among Indie developers who can create unique games without having to fuss with a camera system.

### Top Down:

Top Down is another classic 2D camera system popularized by early strategy titles like the original Command and Conquer and Warcraft. Here, the game is played as if you were looking straight down on the field. Another easy to design camera system, you’re simply pointing the camera down and either tracking the character or letting the player control it. Advanced examples may provide some depth of field or detail like Dungeons of Dredmor.

Very simple to make, top down design now exists mainly in simplified indie titles like shooters while strategy games have moved on to the one we’ll talk about next.

### Isometric:

Isometric is an almost 3/4th view of the action and again is seen in strategy titles. Here, it’s like you’re looking at a board game above and to the side. The advantage of isometric is that it allows you to view the action from above while still providing depth of field and being able to see units clearly.

In strategy games that are dealing with cityscapes or objects that can clutter the view, designers usually have different layers of view that limit what the player can see to make it easier to spot things.

![Civ 5, originally posted from 2kgames.com game design](../../assets/de81c3b98f54e310.jpg)


![Civ 5, originally posted from 2kgames.com game design](../../assets/de81c3b98f54e310.jpg)

Isometric view is great for strategy games as it provides a clear view of the situation and works in 2D or 3D titles.

Another camera system that is easy to design as once you have the perspective down, the player can simply control the pitch of it or keep it fixed in one angle.

Despite being listed in the 2D section, isometric also works in 3D strategy games like Civilization or XCom: Enemy Unknown.

### First Person:

The last 2D example is the first person camera. Even though it is popularized in 3D titles today, the camera system originally was for flat 2D games like Doom and Wolfenstein 3D (despite the 3D in the title).

This camera system obviously is about looking through the main character’s eyes and has become very popular in shooters, horror titles or cutscenes. Simple to design, you’re basically locking the camera in a position to simulate the head or usually the chest and moving the camera along with the character.

These camera systems have been the foundation for many video games and have the common attribute of being easy to design. But when we move to 3D, things do get a bit more complex.

## 3D:

### Third Person:

Third Person camera systems tend to focus on keeping the player in the center of the screen and are also commonly referred to as shoulder cams. The point is that you want to keep the player in frame while presenting enough of the environment so that they know where they are in relation to things.

The major element of a third person camera is that it stays locked to the perspective around the player and they can only rotate it to some extent.

![Dark Souls 2 game design](../../assets/4f1c7c023ecfe4e9.jpg)


![Dark Souls 2 game design](../../assets/4f1c7c023ecfe4e9.jpg)

The over the shoulder or third person cam is great for action titles. But needs extra functionality to work properly.

Some examples would be third person shooters, Dead Space and the Souls series. The problem with this camera system is that they tend to get stuck on environmental objects, either a wall blocking vision of the character or being unable to view large enemies within the frame.

Normally with this type of camera, a lock-on feature is used to allow the player to rotate around an enemy without needing to control the camera.

### Static:

A static camera is where the camera is locked to a specific perspective or view at all times. The best/worse example of this would be old school survival horror games like Resident Evil. The advantage of this system is that you completely remove the player’s ability to alter the camera and make sure that every scene is properly set up.

The problem is that it’s really awkward to view the game from and is more known for cheap scares and firing blindly than being a great system. With the focus on action horror and first person, static cameras aren’t used that much anymore.

### Perspective:

Lastly is the camera system that I like to call perspective. This is a 3/4th view similar to isometric, but controllable around the player. This camera system is used in 3d games where platforming is needed such as the 3d Mario games.

This is one of the hardest camera systems to get right and one where a lot of designers mess up on. The reason is that it needs to be both controllable by the player but still smart enough on its own to present the correct view.

Perspective view works best when the player can not only see the character and environment, but also the ground and platforms in relation to the player. This is a problem that we see in games that don’t handle the camera right, such as the Epic Mickey series.

There, the camera tends to stay horizontal to the action and makes it impossible to see the depth of the environment. This in turn made it hard to figure out the position of floating elements.

To see how it works best, you can look at almost any 3D Mario game. Even the first 3D Mario: Mario 64’s camera worked really well at scoping out the action.

The challenge is that you need to provide a balance of showing enough of the environment so that the player knows where to go, while making sure that the perspective is right so they know where their character is in relation to everything else.

## Wrapping Up:

When talking about camera system design and how each one is set up, we could spend entire posts on each one. But this should be a good primer for people new to the industry and game design in understanding camera systems.

(For more about camera systems, [here is a more recent post](https://game-wisdom.com/critical/differences-2d-3d-camera-systems-game-design) I did explaining the differences between 2D and 3D camera design)