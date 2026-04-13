---
title: Haxe development environment setup
url: https://dewitters.com/haxe-development-environment-setup/
published: '2017-10-15'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

[Haxe](https://haxe.org/) is an awesome programming language for making cross-platform games. And I’m sure it will only gain in popularity.

But setting up a proper development environment is not easy. The Haxe ecosystem is still maturing. There are a lot of very nice things happening. But unfortunately, some basic things are missing. Which makes it hard to get started. So I hope this guild can help you.

Since I’m currently moving the ActionScript 3 codebase of my [RPG making tool](http://rpgplayground.com) to Haxe, it’s obvious that I need to have a proper development environment.

So let me get you up to speed to what I discovered.

First I will show you why I made certain choices. And then I will show you how to practically set them up.

You can use this guide as a starting point, or you can follow it and have the ultimate Haxe development environment ;).

# Go shopping

Let’s see and evaluate what is currently available. Open Source only!

## IDE

There are 2 major IDE’s for Haxe: HaxeDevelop and Visual Studio Code. And their difference is very fundamental.

### HaxeDevelop

HaxeDevelop is a rebranding release of FlashDevelop, with its latest release in September 2016.

All my ActionScript 3 code was written in FlashDevelop, and I absolutely loved it. Believe me, I used plenty of IDE’s and editors during my lifetime: Microsoft QuickBasic, Emacs, Vi, (Embedded) Visual Studio, both for C++ and C#, Netbeans, Eclipse, even Oberon, if you know what that is :). And I can tell you, FlashDevelop is awesome.

I switched from Linux to Windows to use it, and I know others did the same.

But what about HaxeDevelop? Well, it didn’t impress me. The latest release is from 2016, so it wasn’t able to keep up with the new Haxe frameworks. Maybe the effort behind this project has stalled? I don’t know, but their [latest tweet](https://twitter.com/flashdevelop) is also from 2016.

The [features described on the website](http://haxedevelop.org/features.html) look very promising.


HaxeDevelop has built-in support for many workflows.

Of course all Haxe target platforms are integrated. You can also start using frameworks like OpenFL, Lime, Flambe, Kha, HaxeFlixel, Adobe Flash and Adobe AIR with the build-in project templates. You can create, customize and share your own project templates.

But unfortunately, nobody seemed to have the time to implement this. OpenFL and Lime yes, the rest, I didn’t see.

### Visual Studio Code

Visual studio code is an entirely different beast. While HaxeDevelop is specifically focussed on Haxe (and ActionScript3), Visual Studio Code is more of a generic IDE, and tries to support any language.

The benefit is that the community is larger, because it goes beyond Haxe and AS3 developers. And if you compare the commit stats of [VSCode](https://github.com/Microsoft/vscode/graphs/contributors) and [HaxeDevelop](https://github.com/fdorg/flashdevelop/graphs/contributors), they don’t lie.

Want to run it on Linux? You got it. Want a VI keybindings plugin? You got it! Want language extension for YAML? You got it! Want to have Git, Mercurial or any other versioning system integration? You got it! Want to have a new update every time you blink your eyes? You got it!

Visual Studio Code even supports Unity 3D development, so what is there not to like?

But is developing Haxe in VSCode as good as developing AS3 in FlashDevelop? Definitely not :(. But first of all, we should compare it to Haxe in HaxeDevelop. And secondly, we should also consider the future potential. And for now, VSCode seems to have way more potential than HaxeDevelop.

Although I do miss the FlashDevelop toolbar at the top, where you can select which build you want to use. Or the GUI dialogs for config. VSCode is more text/command oriented.

**Conclusion: Visual Studio Code for the win!**

## Building your Haxe project

When it comes to building your Haxe project, it’s a fucking mess. And yes, I am allowed to swear in this case.

Before I show you what a mess it is, I will first explain what other programming languages are doing.

First, there is a compiler, which is pretty obvious. In Haxe’s case, a cross-compiler, which is fine.

Then, there is a build automation tool. Java has Ant and Maven, Microsoft has msbuild, Linux has Make, JavaScript has Grunt, and Haxe has… wait… what? That’s right, Haxe doesn’t have it.

But don’t worry, it has plenty of things that come really close. But unfortunately, this makes it even more complex :(.

### What does build automation do?

That part is easy, so let me give you some examples.

Want to build your sources:* make build*. Want to have a release package: *make release*. Want to run your unit tests: *make test*. Want to clean your build files: *make clean*. Want to push your release package to your website: *make upload*.

So let’s take a look at all the things that come close, but unfortunately not quite.

### hxml

You may think the Haxe [hxml](https://haxe.org/manual/compiler-usage-hxml.html) files are like a Makefile, but you are wrong. hxml files do nothing more than store the compiler arguments in a file.

### Framework package tools

Because Haxe is limited to the language and cross-compiler, game frameworks were forced to make their own packaging tools. This is necessary because next to cross compilation, those compiled source files need to be actually build, and packaged together with asset and resource files.

So [Lime](https://github.com/openfl/lime) originally did this with lime-tools. Afterwards they tried to make a generic build automation tool for Haxe, called Aether. Unfortunately, it never became generic, and the lime build tool is now specific for lime projects, or those built on Lime such as OpenFL and HaxeFlixel. More info on this is [explained](https://stackoverflow.com/questions/27673969/what-exactly-is-lime-lime-tools-aether-etc#28052367) at StackOverflow.

Same for [Kha](http://kha.tech/), which has khamake as a packing tool. And the same applies for snow of course, which has [flow](https://snowkit.github.io/flow/).

### Conclusion: You are on your own

Since hxml stores nothing more than compiler arguments, and the game frameworks only offer packaging tools, there is no build automation tool for Haxe.

So what can you do? Either use one you are already familiar with, such as Ant or Grunt, and make that work. Or do what I do, and write your build automation in Python or any other scripting environment, such as node.js. From there you can call your frameworks packaging tool, or anything else.

Or another option is to use Visual Studio Code tasks to call shell commands. This last part you will need anyway, because your build automation tool also needs to be called from VSCode.

# Let’s do this!

So enough of investigation. Roll up your sleeves and get ready for some hard work.

## Step 1: Download and install

### Software

[Haxe](https://haxe.org/) & [Visual Studio Code](https://code.visualstudio.com/) of course

### VSCode Extensions

Visual Studio Code features a lot of extensions. So open up VSCode after installation, and press on the “Extensions” button on the left. Install the relevant extensions:

**Haxe Extension Pack**, which includes- Haxe. This is
[vshaxe](https://github.com/vshaxe/vshaxe), and supports intellisense, syntax highlighting, etc..Note that if you come across[vscode-haxe](https://github.com/jcward/vscode-haxe), that is the deprecated one! - Haxe Debug: this only support Flash debugging.
- codedox: Yes, you need to document your code. So yes, you need this extension.

- Haxe. This is
**Debugger for Chrome**: If HTML5 is one of your targets, you need this.

### Haxe Libraries

If your project needs Haxe libraries, you should install them through [haxelib](http://lib.haxe.org/). But you want to make sure to install libraries inside your project directory, and not in the global system.

The way how to do this is go to your project directory and run:

*haxelib newrepo*

This will put the libraries inside a local *.haxelib* directory, which you can check-in into your versioning control. This makes sure you can always build your project later on, using the same versions of the libraries.

Next, install your libraries as described in the [user manual](http://lib.haxe.org/documentation/using-haxelib/#install).

## Step 2: Coding Environment

### Syntax highlighting, Intellisense, etc.

The usual editor enhancements such as code completion, syntax highlighting, etc, are handled by the vshaxe extension.

To operate, it needs access to the .hxml file. And this part might be a problem if you are using a library such as Kha. But no worries, the [documentation of vshaxe](https://github.com/vshaxe/vshaxe/wiki) is top notch. All you need to do is [change the working directory](https://github.com/vshaxe/vshaxe/wiki/Configuration#changing-the-working-directory) to the one that contains the .hxml file.

## Step 3: Building

Ah, building a Haxe project, with VSCode, the serious pain in the butt*. **Yes, I can say this, uncensored. *

As stated before, Haxe really doesn’t have any build automation tool, so there is nothing for VSCode to call. And if there was something, how would VSCode call this?

Well my fellow, VSCode has this thing called [tasks](https://code.visualstudio.com/Docs/editor/tasks). You will need custom tasks, defined in the *.vscode/tasks.json *file inside your project directory.

Basically, you need to read the [tasks documentation](https://code.visualstudio.com/Docs/editor/tasks) and try to compose your tasks to what is applicable to you.

If you have issues with VSCode recognizing the compiler errors, do as I do and put this in your task:

"problemMatcher": { "base": "$haxe", "fileLocation": "absolute" },

Good luck to you.

## Step 4: Debugging

You can debug your HTML5 project with the *Debugger for Chrome* extension.

Debugging in VSCode is configured in the *.vscode/launch.json* file. Mine looks like this:

{ "version": "0.2.0", "configurations": [ { "type": "chrome", "request": "launch", "name": "Launch Chrome against localhost", "url": "http://localhost:8080", "webRoot": "${workspaceRoot}" }, { "type": "chrome", "request": "attach", "name": "Attach to Chrome", "port": 9222, "webRoot": "${workspaceRoot}" } ] }

First of all you need to have a server running at port 8080, serving your project. What I do is keep my server running, because it picks up changes when refreshing the page anyway.

The next thing the debugger needs, is access to the .map file. What is the .map file? Well, this is generated by the Haxe compiler when compiling with the *debug* option. So make sure the .hxml file contains the -debug option!

This .map file basically maps code lines back from the generated JavaScript to the original Haxe line numbers. This allows the debugger to break in your Haxe code instead of the JavaScript.

# Rounding up

I miss the time where I could just open FlashDevelop, click “new project”, and select what kind of project I want to make. Just code and click the debug button. I didn’t really care what was going on in the background.

But that is currently not possible. You need to do a bit more manual work to get things going. But once you do, you have a nice IDE with debugger, and that’s all you need.

If you need more info, the [VSCode documentation](https://code.visualstudio.com/docs) and[ vshaxe extension docs](https://github.com/vshaxe/vshaxe/wiki) are excellent to get you started.


Have fun developing your project!

deWiTTERS


## 0 Comments