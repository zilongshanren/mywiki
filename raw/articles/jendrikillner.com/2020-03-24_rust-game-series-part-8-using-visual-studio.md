---
title: Rust Game Series - Part 8 - Using Visual Studio
url: https://www.jendrikillner.com/post/rust-game-part-8/
author: Jendrik Illner
published: '2020-03-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

There are articles on how to use Visual Studio Code with Rust already, but I prefer to use Visual Studio.

This article presents my setup on how to use Visual Studio with Rust. It’s not a perfect setup, but it is good enough for me.

## Extension

There exists a Visual Studio [extension for Rust](https://marketplace.visualstudio.com/items?itemName=dos-cafe.Rust).
I have it installed, but mostly using it to get syntax highlighting, it’s not essential to use it.

## Project Setup

To use Rust with Visual Studio, I am using a Makefile Project.

![Visual Studio makefile project Visual Studio makefile project](../../assets/b5298085d412d268.png)


After creating the project, my first step is to delete the Win32 configuration. Since I am not interested in developing x86 applications. Other platforms could be added as required.

![Delete Win32 configuration Delete Win32 configuration](../../assets/e42b13a8e39af352.png)


Next I create a few extra configurations:

![Extra configurations Extra configurations](../../assets/d7a7a2a70c7b235f.png)


The names should be mostly self-explanatory what the purposes are

- Run Clippy
- Build the game
- Run unit tests

These configurations allow the common operation to be accessed right from within Visual Studio. Configuration management is mostly done with property sheets.

![Property Sheets Property Sheets](../../assets/617a6efea6aedc87.png)


RustBase provides the default settings, such as OutputDirectory and IntermidiateDirectory. And the more specific property sheets provide the necessary Cargo commands to be executed via nmake.

With all the setup, I am now able to compile the game, debug the game using the Visual Studio debugger, run Clippy as well as Unit Tests.

## Debug Unit Test executables

Debugging Unit Tests is a bit more tricky because Cargo doesn’t generate deterministic file names for Unit Test executables.
There is an open [issue](https://github.com/rust-lang/Cargo/issues/1924) for it. It doesn’t seem to have gained much traction, though.

The solution that I am using is very primitive. When the Unit Tests are compiled, it will print the name of the generated executable. I then manually copy this name into the debug command.

![Debug UnitTest Debug UnitTest](../../assets/804fdfa7268a7086.png)


This name seems to be deterministic for the same version of Rust, but after a version update, the name changes, and I need to copy it again. Not a great solution, but it works.

If you know a better way, please let me know :)

### Rustfmt integration

Cargo formatting is a handy command to have easy access to. I suggest creating an External Tool in Visual Studio to enable one-click access to the tool.

The setup is shown below
![Cargo fmt integration Cargo fmt integration](../../assets/13e86118b0f45c6d.png)


And with the external tool entry created, it is now accessible from the Tools category. With a single click, the source code will be formatted with the specified guidelines.

![External Cargo fmt tool External Cargo fmt tool](../../assets/3819e7cad1ab28c4.png)


## Rust Debugging Advice

A few extra recommendations to make your Rust debugging experience better.

### Debug Panics

Rust panics will generally try to unwind the stack or abort the application execution. But when a debugger is attached, I generally want to halt the debugger at the point when a panic occurs to inspect the program state.

Rust provides the possibility to do this, but it’s not very well documented.
The rust panic handler is internally always calling the unmangled function `rust_panic`

, that also never gets inlined.

It is possible to set a function breakpoint on this function.

![Rust Panic Breakpoint Rust Panic Breakpoint](../../assets/9eaaab131cb9fe3a.png)


With this breakpoint set each time a panic occurs, you will get a breakpoint in the debugger.

The function is sadly only called with a deep call stack. We will need to go a few levels up the stack until you find the user code.

![Panic Callstack Panic Callstack](../../assets/a11499e6c0addcea.png)


### Rust source code

As you might notice in the previous screenshot, I have symbols as well as source code for the Rust implementation itself. When you hit the panic breakpoint from Visual Studio the first time, it will not be able to resolve symbols but instead, ask for the source code location.

![Delete Win32 Delete Win32](../../assets/33d90a557f1f89c9.png)


The Rust installations ships with full source code. It can be found in the rustup installation folder, for me it’s located in this location:

```
C:\Users\jendr\.rustup\toolchains\stable-x86_64-pc-windows-msvc\lib\rustlib\src\rust\src
```


Pointing Visual Studio at the correct location will resolve the symbols and show you the Rust code for the position. It also will allow you to step through the Rust implementations. Really useful to learn about how Rust library functionality is internally implemented.

That’s it for today.

Next time I m going to improve the Rust code organization a little bit before continuing the programming of the game.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-8)