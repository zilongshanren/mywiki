---
title: How to Convert a Blueprint Only Project to a C++ Project (using Windows)
url: https://allarsblog.com/2015/11/05/converting-bp-project-to-cpp/
author: Michael Allar
published: '2015-11-05'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

This document covers how to convert a Blueprint Only project to a C++ project without writing any C++ code using Windows. This isn't intended to fold down your Blueprint Logic to C++, it is meant only to wrap your Blueprint Project with a C++ project. Some plugins and engine features require a C++ project and this is an easy way to still work in Blueprints but not be constrained by this limitation.

# Requirements

- For 4.9.X or older, you need
[Visual Studio Community Edition 2013](https://www.visualstudio.com/en-us/news/vs2013-community-vs.aspx?ref=allarsblog.com) - For 4.10 or newer, you need
[Visual Studio Community Edition 2015](https://www.visualstudio.com/products/visual-studio-community-vs?ref=allarsblog.com)- Make sure you install Visual C++. 2015 doesn't do this by default
- During installation, choose Custom, not Typical
- Make sure Visual C++ and all children are selected
- If you skipped installing Visual C++ and Unreal Engine 4 is complaining about not being able to find it, you can fix this by: re-running the downloaded installer and choosing "Modify", then selecting Visual C++ and clicking "Update".


# Convert Process

- Open Your Project in the Unreal Engine 4 Editor.
- Open up the New C++ Class Dialog by using File -> New C++ Class...
- Choose a new "None" class and hit "Create Class."
- You may be prompted with a warning message about being able to compile the game module. You can safely ignore this and hit No.
- Close any pop-ups, warnings, or success notifications, then close the Editor.
- Navigate to your project's folder, right click your project's .uproject file, and click "Generate Visual Studio project files."
- Open your project in Visual Studio by double-clicking your project's .sln file.
- Visual Studio should load. If it asks you what theme you would like, pick what looks best to you. I prefer the Dark theme.
- Find and select your project in Visual Studio's Solution Explorer.
- Set the build configuration drop down to "Development Editor"
- Right-click your project in the Solution Explorer and click Build.
- This should result in your project being compiled successfully with zero errors.
- Set the build configuration drop down to "Development".
- Right-click your project in the Solution Explorer and click Build, again.
- This build will take much longer, on the order of several minutes. This should result in your project being compiled successfully with zero errors though, again.

# Finished

Your Blueprint Project is now a C++ Project. You are able to open up your project just as before and nothing has changed in terms of your project's functionality, but you are now able to use Engine features that require C++ Projects, such as third-party plugins, Subsystem integrations, dedicated servers, etc. You shouldn't have to open Visual Studio ever again unless you do some C++ code, but you still have to keep Visual Studio installed.