---
title: Hacking & Contributing to Servo On Windows – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/04/hacking-contributing-to-servo-on-windows/
author: Jason Williams
published: '2017-04-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Like many cross-platform open source projects, [Servo](https://research.mozilla.org/rust/), the high-performance browser engine project written in Rust, has always been a bit of a nightmare to build and run on Windows. Luckily, thanks to the Rust team and Servo community, most of the issues have been squashed and we can now launch it with nothing more than just [PowerShell](https://en.wikipedia.org/wiki/PowerShell), plus with a full stack of native Windows libraries and tool usage.

Why did this take so long to happen?

## A brief history..

Back in 2013 when Servo development started, it only ran on Linux systems and OSX. This was largely due to the developers of Servo being on those operating systems.

As a byproduct, Servo ended up with many Linux-based dependencies (make, gcc, etc.), the build system would make hard-coded calls to `/bin/:/usr/bin/[etc]`

. Migrating these to cross-platform took time. Servo engineer [Lars Bergstrom](https://twitter.com/larsberg_) explains:


“Certainly font support and build system stuff has taken the most effort. In general, making sure that all of the hundreds of crates in the Servo dependency graph not only build but work correctly on Windows has taken a lot of effort.

A lot of things (including Servo) were also easy to get over on“[MinGW]with a “unixy” Windows experience, but getting a true, native Windows experience using MSVC took a lot longer.

A year later, the quick and easy solution to running Servo on Windows was to emulate a Linux environment, so this led to arcane setup instructions using `msys`

and `mingw`

on Windows. Although Servo would build, it seemed like more of a temporary solution.

A Windows branch of Servo was created, with many build steps fixed over time; and modules, which used only Linux components, stubbed out. One by one, we were able to [tick off the incompatibilities](https://github.com/servo/servo/issues/12125).

There’s been a [push](https://github.com/servo/servo/issues/1908) by a few of us, with a lot of help from [Vlad](https://github.com/vvuk), to have Servo properly building on Windows and using the Microsoft Visual C++ compiler (MSVC) for some time. And finally we’re there!

So how to begin developing? For these examples I will be using Windows 10 x64.


## Let’s get started

You don’t have to do your editing in here, but Visual Studio (VS) allows us to actually debug the binary. We can pause at any moment and edit breakpoints (more on this later).

Let’s go to [https://www.visualstudio.com/downloads/](https://www.visualstudio.com/downloads/) and download “Visual Studio 2017 Community”.

Once it downloads, and you get the options to come up, navigate to the *individual components* tab and select:

- C++/CLI support
- Profiling Tools
- Visual C++ tools for Cmake
- VC++ 2017 v141 toolset

We will need to add the build tools VS has given us to our system path.

Navigate to environment variables, and add this to the Path variable:

`C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.10.25017\bin\HostX64\x64``


While you’re here you should set a new environment variable, `VisualStudioVersion`

to `15.0`

(yes 15.0 even though it’s VS 2017). This enables cmake-using crates (libssh2-sys, etc) to build.

We’re done here for now.

## rustup

[rustup](https://www.rustup.rs/) will manage our Rust installation and let us switch between releases, plus nightly and stable branches. It makes it very easy to update. We will be needing nightly later, so rustup is the best way to start.

Go to [rustup.rs](https://www.rustup.rs/) and download the installer, it will mention installing the Visual C++ build tools, but VS should have already given us this stuff from earlier, so just proceed.

Press 1 and follow the default installation.

## Install rust-src

Open up PowerShell: You should now have Rust installed, you can try it out with:

`$ rustc --version`


Our next task is to install the rust-src, this helps VS find the source it’s looking for. (This is also a helpful step for racer support.)

Before we go ahead though, we should switch to nightly. Nightly gives us [Natvis](https://msdn.microsoft.com/en-us/library/jj620914).

```
$ rustup default nightly
$ rustup component add rust-src
```


You will now have some files located at:

`C:\Users\[User]\.multirust\toolchains\nightly-x86_64-pc-windows-msvc\lib\rustlib\src\rust\src`


Although not useful for now, you’ll need this path for *Optional: Stepping into the standard Library* further down.

## Add Natvis for Rust

Natvis files gives Visual Studio-friendly visualisations of native objects in Rust. The Rust team have added Vec, LinkedList, VecDeque, String, Option plus many more Natvis visualizations.

Here’s how to use them:

`C:\Users\[User]\.multirust\toolchains\nightly-x86_64-pc-windows-msvc\lib\rustlib\src\rust\src\etc\natvis`


Copy the .natvis files in here, and place them in

`C:\Users\[User]\Documents\Visual Studio 2017\Visualizers`


Don’t worry if Visualizers isn’t there, you can create this directory.

## Building Servo

I won’t go too much into setting up Servo here, as that’s covered in: [https://github.com/servo/servo/#on-windows-msvc–mingw](https://github.com/servo/servo/#on-windows-msvc--mingw)

Build the latest version using `--dev`

, I’m just running

`$ mach.bat build --dev`


in PowerShell here. It’s important you use the `--dev`

option as debugging will not work without it.

## Back to Visual Studio

Now that we have Servo built, let’s run it.

You can open up Visual Studio, File, Open, Project/Solution, change “All Project Files” to “Exe project files” and navigate to your servo.exe binary, usually in `target/debug/servo.exe`

.

If you need to pass in arguments you can right click Servo in the solution explorer on the right. Once ready, you can click start at the top.

This should load up Servo and you may see some fancy memory profiling in the background in VS. You can pause at any point and it should land in the code where it’s paused. If this doesn’t happen make sure that Thread: is set to “Main Thread”.

For example, if the browser is idle and we pause, we may land on this line:

`self.window.events_receiver.recv().ok()`


## Optional: Stepping into the standard Library

Remember the rust-src we installed earlier? Well this is useful if we want to see what the standard library is doing, otherwise the debugger may moan when you click on std::* functions. So in order to tell VS about rust source code we right click on the solution name on the right “Solution ‘servo’” and select properties, then inside “Common Properties/Debug Source Files” add that path to the top window.

## Setting breakpoints

This is straightforward too, you can drag any Rust file from the project into VS and set a breakpoint. Click start again and the program should stop at that point. You can then step in and out of functions or use continue and breakpoints to inspect the execution of your program. You can see the stack trace and variables within scope at the bottom too!

If everything went to plan, you should have something similar to this.

## Contributing

So you want to contribute but not sure where to start?

[https://starters.servo.org/](https://starters.servo.org/) has some great first-PR tickets, plus there are still quite a few [easy tickets](https://github.com/servo/servo/issues?utf8=%E2%9C%93&q=is%3Aopen%20is%3Aissue%20label%3AE-easy) outstanding too.

## About
[
Jason Williams ](http://jason-williams.co.uk)

Jason is a Principal Developer and Tech Lead at the BBC

## 10 comments

Ahmed CharlesApril 7th, 2017 at 01:43Lars BergstromApril 7th, 2017 at 10:12Lars BergstromApril 12th, 2017 at 17:29VolkerApril 7th, 2017 at 04:32Lars BergstromApril 7th, 2017 at 10:11Michael “notriddle” HowellApril 13th, 2017 at 08:43KamalApril 9th, 2017 at 20:54Lars BergstromApril 10th, 2017 at 11:13Lars BergstromApril 14th, 2017 at 06:42Elahn IentileApril 13th, 2017 at 16:06