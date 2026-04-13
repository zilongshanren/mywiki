---
title: A practical tutorial to hack & protect Unity games - Alan Zucconi
url: https://www.alanzucconi.com/2015/09/02/a-practical-tutorial-to-hack-and-protect-unity-games/
author: Alan Zucconi
published: '2015-09-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If there’s a term which is often misunderstood, that’s for sure *hacking*. When it refers to softwares, it usually gets a negative connotation which smells of piracy and copyright infringements. This post will not cover any of these topics; quite the opposite, I strongly discourage readers from taking any action which will damage (directly or indirectly) other developers. That said: yes, this post will be a practical tutorial to hack into Unity games. You can use the techniques and tools described in this post to check how safe your games are. If you’re a developer, you’ll also find useful snippets of code and technique to add an extra layer of protection to your games.

### Introduction

At the heart of *hacking*, there’s *knowledge*: understanding how Unity3D compiles games is essential if you want to hack them. This post will show how resources are compiled into Unity3D, how they can be extracted and (when possible) repacked. This allows not just for extreme modding, but also to advanced debugging. Unity3D often works as a black box, and from a version to another many features have been radically changed. Over time, this has caused several issues which can only be understood by comparing how the same code has been compiled against the different versions. Decompiling a game is also the ultimate way to find its secrets. That’s actually how the solution to [the last secret](http://www.gamefaqs.com/boards/945079-fez/66110193) in FEZ has been discovered.

![fez](../../assets/91c09750d5b0c2ee.png)

### Finding the Unity3D files

If you have a Unity3D game, chances are you’ll have it on Steam. To access its folder, find the game in your library and explore its properties. “*Browse local files…*” in the “*Local files*” tab will open the folder where the game is stored.

![local files](../../assets/0b5458fc62970802.png)

When a game is compiled for Windows with Unity3D, is always packed in the same way. The destination folder will have the executable file, let’s say `Game.exe`

, and a folder called `Game_Data`

.

### Diving into PlayerPrefs

The most common way Unity3D games store data is by using [PlayerPrefs](http://docs.unity3d.com/ScriptReference/PlayerPrefs.html). If you’re on Windows they’re stored in the *system registry*. You can access them by using a tool called *Regedit* which is already installed on Windows. `PlayerPrefs`

are stored in the folder `HKEY_CURRENT_USER\Software\[company name]\[game name]`

:

![regdit](../../assets/4c935266e27ceb66.png)

While `UnityGraphicsQuality`

contains the launch configuration and is created by the Unity3D launcher, all the other entries are created by the game. Many games use `PlayerPrefs`

to remember particular settings, achievements or progress. More substantial data, such at the actual save games, are often stored in proprietary formats hence they’ll not be covered.

#### How to protect PlayerPrefs

You cannot prevent users from messing up with the system registry. Hence, you cannot prevent them from altering your `PlayerPrefs`

. What you can do, however, is adding a *checksum* which will detect any edit. To do this, you need to save another value which is somehow calculate taking into account all the other ones.

// Download: https://www.patreon.com/posts/3301589 public class SafePlayerPrefs { private string key; private List<string> properties = new List<string>(); public SafePlayerPrefs (string key, params string [] properties) { this.key = key; foreach (string property in properties) this.properties.Add(property); Save(); } // Generates the checksum private string GenerateChecksum () { string hash = ""; foreach (string property in properties) { hash += property + ":"; if (PlayerPrefs.HasKey(property)) hash += PlayerPrefs.GetString(property); } return Md5Sum(hash + key); } // Saves the checksum public void Save() { string checksum = GenerateChecksum(); PlayerPrefs.SetString("CHECKSUM" + key, checksum); PlayerPrefs.Save(); } // Checks if there has been an edit public bool HasBeenEdited () { if (! PlayerPrefs.HasKey("CHECKSUM" + key)) return true; string checksumSaved = PlayerPrefs.GetString("CHECKSUM" + key); string checksumReal = GenerateChecksum(); return checksumSaved.Equals(checksumReal); } // ... }

The class above is just an example and works with strings only. It requires the developer to specify a secret key and a list of all the items you want to be protected:

SafePlayerPrefs spp = new SafePlayerPrefs("MyGame", "PlayerName", "Score");

It can then be used as follow:

// Set PlayerPrefs as normal PlayerPrefs.SetString("PlayerName", name); PlayerPrefs.SetString("Score", score); SafePlayerPrefs.Save(); // To check if there has been an edit if (SafePlayerPrefs.HasBeenEdited()) Debug.Log("Error!");

Before savings it calculates a checkum on all the protected properties. If the player alters one of the value, he won’t be able to regenerate the checksum and cause the application to detect the change.

### Decompiling .NET

During compilation the source code of a program is converted from a Human readable language into a set of instructions, compatible with the target machine which will execute them. During this process, most of the original source code is lost. Comments and indentations are completely stripped away since they serve no purpose for machines. Very often the code is also optimised, a process which changes its structure into a more efficient one. Decompilation is the process which takes an application and converts it back into its source code. When you’e running a piece of software on your machine, you have *de facto* all of its code. When compiled for Windows, Unity3D stores its compiled resources in the *Managed* folder of the game data. They are bundled in DLL files. The ones we are interested in are `Assembly-CSharp.dll`

, `Assembly-CSharp-firstpass.dll`

and `Assembly-UnityScript.dll`

.

![files](../../assets/889d59205bca8cfe.png)

Exploring the content of a DLL is a very easy task and there are several programs which can do it for free, such as [ILSpy](http://ilspy.net/) and [dotPeek](https://www.jetbrains.com/decompiler/).

![window](../../assets/308ffdfc21fd100f.png)

This technique is particularly effective for Unity3D games because very little optimisation is actually done. Morever, Unity3D doesn’t attempt to change or hide variable names. Since they are preserved, understanding the decompiled code of a Unity3D game is actually very easy.

#### How to protect your source codes

Despite this, there are some precautions one can take. [Unity 3D Obfuscator](http://en.unity3d.netobf.com/) is a useful application which takes a compiled game and obfuscates its .NET code. Despite being very good at its job, many classes which are referred from outside of the DLL cannot be renamed since this would break their connection.

![HtmlImage](../../assets/696830c6d2718747.png)

If a part of your code is sensitive and should not be accessed, you might want to move that to a server. For instance, updating scores directly from your game is often a bad move since this might allow players to hack with your code.

### Unpacking assets and resources

The majority of resources in Unity3D are bundled in a proprietary format. These files are stored in the `_Data`

folder and have the `.assets`

and `.resource`

extensions. Currently, the best program to explore and extract these files is [Unity Assets Explorer](http://www.nexusmods.com/pillarsofeternity/mods/27/?).

![asset](../../assets/fff217e75e640e1c.png)

Unfortunately, the interface is very poorly designed and the program comes with several critical bugs. Despite these limitations, it is able to extract the majority of textures from the game. They are extracted in the most unfortunate format, DDS. If you want to visualise them outside Unity Assets Explorer, you may need [Windows Texture Viewer](http://www.nvidia.com/object/windows_texture_viewer.html).

This technique also exports shaders. They are already compiled and, to the best of my knowledge, there isn’t a tool to decompile them into Cg / HLSL. Despite this, they can still be imported into another project and they’ll work just fine. Remember that stealing a an asset *is* an act of piracy.

### Capture the geometry

There’a another aspect which has not been discussed yet: 3D models. Most models are scattered in different assets files, and some other might be generated procedurally within the game. An interesting approach is to dump them directly from the graphics card memory. When a game is running, all the data about the textures and models of the scene you’re currently playing are loaded into memory. [3D Ripper DX](http://www.deep-shadows.com/hax/3DRipperDX.htm) is a nice program which allows to grab all the geometry currently on the screen. It is not the easiest to use and you’ll need to read its guide. It also requires 3D Studio Max to import the models it exports.

![ripper](../../assets/bca9fce519bf8198.png)

### Hacking into the game’s memory

A very well known tool to hack games is called [Cheat Engine](http://www.cheatengine.org/). It read the memory where you game is and allows to change it arbitrarily. This tools is very advanced and if you don’t know what you’re doing there’s a high change you’ll just crash everything.

![Cheat_Engine_5.4](../../assets/393d4b1973e30f8f.png)

This application takes advantage of the fact that is very rare for a game to protect its variables. Health and ammos, for instance, are often store in float variables; changing them will automatically alter your stats in the game. *Cheat Engine* allows to scan the memory of the game for a certain value. For instance, let’s imagine you have 100 bullets; you can do an initial search for all the memory locations which contain the value 100. Then shooting a bullet and search for all those memory locations which now contain 99. By repeating this approach you can easily discover the majority of variables within a game. Editing them is a little bit tricky; games generally make the assumption their variables are not externally modified, so this can corrupt the state of the current play. More often, you’ll just end up with a segmentation fault and the game will crash.

#### How to protect the memory of your game

*Cheat Engine* works only because variables often have no protection. It is easy to make it ineffective just by being more careful in the way you manipulate them. The class `SafeFloat`

can be used to replace normal `float`

s, with the advantage that it will store them “encrypted”:

// Download: https://www.patreon.com/posts/3301589 public struct SafeFloat { private float offset; private float value; public SafeFloat (float value = 0) { offset = Random.Range(-1000, +1000); this.value = value + offset; } public float GetValue () { return value - offset; } public void Dispose () { offset = 0; value = 0; } public override string ToString() { return GetValue().ToString(); } public static SafeFloat operator +(SafeFloat f1, SafeFloat f2) { return new SafeFloat(f1.GetValue() + f2.GetValue()); } // ...the same for the other operators }

You can use `SafeFloat`

as follow:

SafeFloat health = new SafeFloat(100); SafeFloat damage = new SafeFloat(5); health -= damage; SafeFloat nextLevel = health + new SafeFloat(10); Debug.Log(health);

If you are displaying your health on the screen, hackers can still intercept that number and change it. But it won’t change the actual value stored in the memory.

### Conclusion

Unfortunately there’s very little you can do to protect your games. Once they’re installed onto a player’s machine, you’ve been handling all of your code, textures and models. If someone wants to decompile your game and steal your assets is just a matter of *when*, not *if*.

Despite this, there are sensible techniques you should employ when developing a game. You don’t need to live in a panic room, but at least don’t leave the door open when you’re going out.

#### Other resources

[Unity3D Attack By Reverse Engineering](https://www.hackthis.co.uk/articles/game-hacking-chapter-1-unity3d-attack-by-reverse-engineering): An interesting article which highlights common security flaws in the way scores are handled in most Unity3D games;[disunity](https://github.com/ata4/disunity/releases): Disunity is the best tool to explore and extract assets files. Unfortunately is not compatible with Unity5;[Unity Studio](http://forum.xentax.com/viewtopic.php?f=10&t=11807): an interesting tool to visualise and extract 3D models from assets file. Not compatible with Unity5.

## Leave a Reply Cancel reply