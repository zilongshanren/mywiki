---
title: How To Set Up Dedicated Servers for Windows and Linux For Your UE4 Game (using
  Windows)
url: https://allarsblog.com/2015/11/06/support-dedicated-servers/
author: Michael Allar
published: '2015-11-06'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

This document covers the bare basics on how to get your Unreal Engine 4 game project able to build both Windows and Linux dedicated server builds, using just a Windows machine for compiling.

# Requirements

-
For 4.9.X or older, you need

[Visual Studio Community Edition 2013](https://www.visualstudio.com/en-us/news/vs2013-community-vs.aspx?ref=allarsblog.com) -
For 4.10 or newer, you need

[Visual Studio Community Edition 2015](https://www.visualstudio.com/products/visual-studio-community-vs?ref=allarsblog.com) -
Unreal Engine 4 compiled from source code

-
Project must be a C++ code project

- If your project is a Blueprint Only project,
[follow this tutorial](https://allarsblog.com/2015/11/05/Converting-BP-Project-To-CPP)to wrap it in C++. Don't worry, you won't have to write any code.

- If your project is a Blueprint Only project,
-
Linux Toolchain for Windows installed for Linux x86 Server Support


# Adding Dedicated Server Support

Note: The word Project in any referenced file name or code will refer to your project's name. For example, my project for this tutorial is named `GenShooter`

, so in my case `Project.Target.cs`

refers to `GenShooter.Target.cs`

. `ProjectTarget`

in my case would be `GenShooterTarget`

.

- Navigate to your Project's Source folder. You should see some
`.Target.cs`

files.

![](../../assets/dcf851b6a444d6cc.png)

- Make a copy of
`Project.Target.cs`

file and rename it`ProjectServer.Target.cs`

, be sure not to grab`ProjectEditor.Target.cs`

.

![](../../assets/d2e61a5fac22c3ea.png)

- Open up
`ProjectServer.Target.cs`

in your favorite text editor. I'll be using Visual Studio here. - Rename all instances of
`ProjectTarget`

to`ProjectServerTarget`

. - Change
`Type = TargetType.Game;`

to`Type = TargetType.Server;`

. - Save this file. Your
`ProjectServer.Target.cs`

file should look something like this now:

```
// Your Copyright Text Here
using UnrealBuildTool;
using System.Collections.Generic;
public class GenShooterServerTarget : TargetRules
{
public GenShooterServerTarget(TargetInfo Target)
{
Type = TargetType.Server;
}
//
// TargetRules interface.
//
public override void SetupBinaries(
TargetInfo Target,
ref List<UEBuildBinaryConfiguration> OutBuildBinaryConfigurations,
ref List<string> OutExtraModuleNames
)
{
OutExtraModuleNames.AddRange( new string[] { "GenShooter" } );
}
}
```


# Building your Dedicated Server

- Right-click your project's
`.uproject`

file in your project's folder and "Generate Visual Studio project files".

![](../../assets/330074edf8e008f8.png)

- Now we need to build our project in Visual Studio with the
`Development Server`

configuration for the Windows platform, and for the Linux platform as well if you have the[Linux x86 Cross-Compile Toolchain](https://allarsblog.com/2015/11/06/Installing-Linux-Toolchain-On-Windows)installed. To do this, build your game project just as we built it in the[past tutorials](https://allarsblog.com/2015/11/06/Installing-Linux-Toolchain-On-Windows)but this time with the`Development Server`

build configuration.

![](../../assets/fdfdd23b25469bda.png)


When the Windows server is done building, your output should look like this.

![](../../assets/a81226672903dbc5.png)


Here is the build output for the Linux server.

![](../../assets/82d13d625ef5ec3b.png)


Now your project supports building for dedicated servers, for all platforms, including Linux. Whether Linux will compile is dependant on if your [Linux x86 Cross-Compile Toolchain](https://allarsblog.com/2015/11/06/Installing-Linux-Toolchain-On-Windows) is setup correctly.

# Packaging Your Dedicated Server

- Open up your project in the UE4 Editor.
- Open up the Project Launcher using Window -> Project Launcher.

![](../../assets/69ed9fc011cbda5c.png)


This should greet you with a window that looks like this.

![](../../assets/07a924171cf4fae0.png)


This window allows for launching various project deployment configurations.

- To build your project in dedicated server form, we need to make a custom build profile. Click the "Add a new custom launch profile" button in the bottom panel that looks like a plus sign. This should open up the custom profile editing screen.

![](../../assets/0e23ae4cbdedba47.png)


- Choose your Project in the Project drop down. If you do not see it, click browse and feed it your project's .uproject file.

![](../../assets/27ec689efd74189d.png)


- Change Cook mode from
`On the fly`

to`By the Book`

. Select the`WindowsServer`

platform under Cooked Platforms. Select the`LinuxServer`

platform as well if you have the Linux x86 Cross-Compile Toolchain installed. Also, select`en`

under Cooked Cultures, or select your base language if your project is not English centric. Click here to see what these settings look like.

![](../../assets/7fc4739e658fdb3d.png)


- Change Package mode from
`Do not package`

to`Package & store locally`

. Leave all the settings in here blank by default.

![](../../assets/33d0fd49c13bde73.png)


- Change Deploy mode to
`Do not deploy`

.

![](../../assets/961d1e466f1d1d85.png)


- Click "Back" on the top right of this window to go back to the main Project Launcher Window.
- Click the "Launch This Profile" button next to your new custom profile. This button looks like the Play button in the level editor window.

![](../../assets/df34c0af7a1fab7e.png)


- This will begin the process of cooking and packaging your dedicated servers for your selected platforms. This will take a while. When it is done, it should look like this.

![](../../assets/a4ecf59ff60c8176.png)


# Locating your Dedicated Server Builds

Now that you have packaged your dedicated server builds, you can find them in your project's `Saved\StagedBuild`

directory. If you have packaged your regular game builds, you'll see them listed here as `WindowsNoEditor`

and `LinuxNoEditor`

as well. You are free to copy these builds to your target machines and distribute them as you like.

# Note about running the Windows Dedicated Server

If you load the Windows Dedicated Server, it will seem that nothing loads up and that there is no UI or command prompt of any kind. If you open up your Windows Task Manager, you will see that your server is in fact running, but it is invisible. If you would like to see the log output of your Windows Dedicated Server, you need to run it with the `-log`

command argument. The easiest way to do this is:

- Hold Shift and Right-click the folder your Windows Dedicated Server is in and choose "Open command window here."

![](../../assets/d496f2d63f6436ca.png)


- Type in
`ProjectServer.exe -log`

and hit`Enter`

. In my case, this is named`GenShooterServer.exe -log`

- This will load your Windows Dedicated Server with a log window.

![](../../assets/58e7102158e62e13.png)


# Note about running the Linux Dedicated Server

After copying your files to your Linux server (which is outside the scope of this tutorial), you will need to run `ProjectServer`

located in your builds `Project/Binaries/Linux/`

folder.

In my case that is, loading it from a terminal would look like:

```
GenShooter/Binaries/Linux/GenShooterServer
```


If you want to load it and then send it to the background so that it will not terminate when you close your terminal session, you can load it with:

```
nohup GenShooter/Binaries/Linux/GenShooterServer &
```


To kill a server that has been sent to the background, find it's process name using the command `top`

, then route that name to `pkill`

, which would look like this:

```
pkill GenShooterServe
```


Your process name is usually your server binary's name limited to 16 characters.