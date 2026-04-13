---
title: Ways to deploy a Java Game
url: https://blog.gemserk.com/2011/02/09/ways-to-deploy-a-java-game/
published: '2011-02-09'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

When you develop Java games for PC, you have different ways to deploy them. We want to talk a bit about some of them.

### Downloadable

The user has to download the game to run it on his machine, probably it comes with an installer to install the game before he can play it.

#### Pros

- The game can be played offline when it has no online requirements.
- User knows where the game is installed and sometimes decides where he wants to install it. They also can uninstall the game.
- It is the only way to deploy a game in portals like
[Steam](http://store.steampowered.com/),[Altitude Game](http://altitudegame.com/)is an example of that.

#### Cons

- Users have to download a patch each time there is a new version. As a developer, you can implement something to download patches and apply them.
- As a developer, you have to implement an installer. Also, you have to make different installers for each platform, an example of that is
[Revenge of the Titans](http://www.puppygames.net/revenge-of-the-titans/)(ROTT) from[Puppy Games](http://www.puppygames.net/). - You have to create patches and deploy new files to be downloaded each time you have a new version of the game after a bug fix or new feature. Else, you force people to download large files each time you have an updated version.
- Java Runtime Environment (JRE) must be installed or you have to embed JRE with your game. In the second case, your game file becomes bigger, for larger games that is not a problem but for small games embedded JRE could be, for example, 300% of the game size (at today, JRE weight is about 20MB). Even though there could be a JRE installed, being able to execute your program directly depends on a good configuration of the JRE within the OS. To solve that, developers usually generate a native wrapper that detects where the installed JRE is, and if it is not installed prompts the user to download one, or reports the error to the user.

### Applets

Java Applets works inside the browser, as well as other web technologies like Flash and Unity. Users only have to open a page with a Java Applet inside and it is loaded by the web browser. [Minecraft](http://www.minecraft.net/) is an example of a successful Java Applet Game (it has other deployment options as well).

#### Pros

- Users only have to follow a link to play the game. No game install is required.
- Users are always playing the latest game version, because it is being downloaded from the server.
- As other web technologies, you can add information or even ads to your applet page without having to put that inside the game.
- Java Applets are as powerful as a Java Desktop application.
- New Generation Java Applets accepts Java Networking Launching Protocol (JNLP) files (more info on next blog posts).
[Pack200](http://download.oracle.com/javase/1.5.0/docs/guide/deployment/deployment-guide/pack200.html)and GZip compression support to reduce jar download sizes (only using plugin2).

#### Cons

- JRE must be installed on the client machine. However, nowadays you can assume the required plugin is installed on most of the client machines.
- You need a web server to deploy your game jars or you have to use a games portal like
[GameJolt](http://gamejolt.com/)or[Games4j](http://games4j.com). - Dependning on the Java Applet technology you are using (plugin2, etc), firefox can freeze when the applet is loading, or could not work on Mac OS (more information on next blog posts).
- As a developer, you need to sign your jars with a certificate if you want to have full access (to do extra stuff like writing a configuration file on user’s home folder).
- If you ask for full access, a security dialog box is displayed. It tends to scare users, if you have a valid certificate then it is a bit less scary.

### Web Start

Java Web Start is some kind of mixing between the last two. As developer you use a JNLP file to describe which resources must be downloaded. Users only have to click on a JNLP link and then the game is opened automatically by Java Web Start.

#### Pros

- Users only have to follow a link to play the game. No game install is required.
- Automatically downloads the latest version of your game from the server each time the user wants to play a game.
- It has a cache for downloaded resources, so if you only update one jar then it is the only one downloaded by the user’s machine the next time the user opens the game.
- As a developer you can specify to run the game offline.
- It has a clean way to specify your game’s resources using the JNLP file.
[Pack200](http://download.oracle.com/javase/1.5.0/docs/guide/deployment/deployment-guide/pack200.html)and GZip compression support to reduce jar download sizes.

#### Cons

- Some browsers are not configured correctly (for example, Google Chrome) and they don’t open the JNLP automatically using Java Webstart, they just download the file.
- Same thing with certificates and signing as the Java Applet.
- As a developer you need a web server to put all your game’s resources, we don’t know any portal which accepts JNLP games yet.
- Java Webstart Cache and Log files are difficult to find on user’s machine.

### Getdown

[Getdown](https://code.google.com/p/getdown/) is a custom solution made by [Three Rings](http://www.threerings.net) in order to replace Java Web Start technology due to its limitations, as it is explained on [Getdown’s project Wiki](https://code.google.com/p/getdown/wiki/Rationale). We lack experience and information about this solution, so the pros/cons section could be a bit empty.

#### Pros

- Open source, that means you know what is happening, and you can collaborate, something impossible with Java Web Start.
- Working examples of mmo games like
[Sprial Knights](http://spiralknights.com/)from Three Rigns and[Tribal Trouble 2](http://www.tribaltrouble2.com/)from[Oddlabs](http://oddlabs.com/).

#### Cons

- It is custom made. That means, as a developer you have to be aware that if something goes wrong you may have no support (note the conditional). But can’t say it is really a cons because with Java Web Start you don’t have any support at all from Oracle’s team.

### References

- Altitude Game -
[http://altitudegame.com/](http://altitudegame.com/) - GameJolt -
[http://gamejolt.com/](http://gamejolt.com/) - Games4j -
[http://games4j.com](http://games4j.com) - Getdown -
[http://code.google.com/p/getdown/](https://code.google.com/p/getdown/) - Java Plug-In Technology -
[http://www.oracle.com/technetwork/java/index-jsp-141438.html](http://www.oracle.com/technetwork/java/index-jsp-141438.html) - Minecraft -
[http://www.minecraft.net/](http://www.minecraft.net/) - Oddlabs -
[http://oddlabs.com/](http://oddlabs.com/) - Pack200 -
[http://download.oracle.com/javase/1.5.0/docs/guide/deployment/deployment-guide/pack200.html](http://oddlabs.com/) - Puppy Games -
[http://www.puppygames.net/](http://www.puppygames.net/) - Revenge of the Titans -
[http://www.puppygames.net/revenge-of-the-titans/](http://www.puppygames.net/revenge-of-the-titans/) - Sprial Knights -
[http://spiralknights.com/](http://spiralknights.com/) - Steam -
[http://store.steampowered.com/](http://store.steampowered.com/) - Three Rings -
[http://www.threerings.net](http://www.threerings.net) - LWJGL Wiki -
[http://www.lwjgl.org/wiki/index.php?title=General_FAQ#Distributing_LWJGL_Applications](http://www.lwjgl.org/wiki/index.php?title=General_FAQ#Distributing_LWJGL_Applications)

UPDATE: added link to LWJGL wiki page about how to distribute LWJGL Java Applications (most of them applies for Java Applications in general)