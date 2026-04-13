---
title: Fast retro gaming on mobile – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/10/fast-retro-gaming-on-mobile/
author: Guillaume Cedric Marty
published: '2013-10-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Emulation is the cool technique that makes retro gaming possible, i.e. play old video games on modern devices. It allows pixel lovers to revive gaming experiences from the past. In this article we will demonstrate that the web platform is suitable for emulation, even on mobile where by definition everything is limited.

## Emulation is a challenge

Emulation consists of recreating all the internals of a game console in JavaScript. The original CPU and its functions are totally reimplemented. It communicates with both video and sound units whilst listening to the gamepad inputs.

Traditionally, emulators are built as native apps, but the web stack is equally powerful, provided the right techniques are used. On web based OSes, like Firefox OS, the only way to do retro gaming is to use HTML and JavaScript.

Emulators are resource intensive applications. Running them on mobile is definitely a challenge. Even more so that Firefox OS is designed to power low-end devices where computational resources are further limited. But fear not because techniques are available to make full speed retro gaming a reality on our beloved handhelds.

## In the beginning was the ROM

Video game emulation starts with ROM image files (ROM files for short). A ROM file is the representation of a game cartridge chip obtained through a process called dumping. In most video game systems, a ROM file is a single binary file containing all aspects of the game, including:

- The logic (player movements, enemies’ artificial intelligence, level designs…)
- The characters and backgrounds sprite
- The music

Let’s now consider the Sega Master System and Game Gear consoles. Take the homebrew game [Blockhead](http://www.smspower.org/Homebrew/Blockhead-SMS) as an example and examine the beginning of the file:

| 0xF3 | 0xED | 0x56 | 0xC3 | 0x6F | 0x00 | 0x3F | 0x00 | 0x7D | 0xD3 | 0xBF | 0x7C | 0xD3 | 0xBF | 0xC9 | 0x00 | |||
| 0x7B | 0xD3 | 0xBF | 0x7A | 0xD3 | 0xBF | 0xC9 | 0x00 | 0xC9 | 0x70 | 0x72 | 0x6F | 0x70 | 0x70 | 0x79 | 0x00 | |||
| 0xC9 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0xC9 | 0x62 | 0x6C | 0x6F | 0x63 | 0x6B | 0x68 | 0x65 | |||
| … |

The elements listed above are mixed together in the ROM. The difficulty consists of telling apart the different bytes:

- opcodes (for operation code, they are CPU instructions, similar to basic JavaScript functions)
- operands (think of it as parameters passed to opcodes)
- data (for example, the sprites used by the game)

If we highlight these elements differently according to their types, this is what we get:

| 0xF3 | 0xED 0x56 | 0xC3 | 0x6F 0x00 | 0x3F | 0x00 | 0x7D | 0xD3 | 0xBF | 0x7C | 0xD3 | 0xBF | 0xC9 | 0x00 | |||||
| 0x7B | 0xD3 | 0xBF | 0x7A | 0xD3 | 0xBF | 0xC9 | 0x00 | 0xC9 | 0x70 0x72 0x6F | 0x70 0x70 0x79 | 0x00 | |||||||
| 0xC9 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | 0xC9 | 0x62 0x6C 0x6F | 0x63 0x6B 0x68 0x65 | ||||||||
| … |

| Opcode | Operand | Data |

## Start small with an interpreter

Let’s start playing this ROM, one instruction at a time. First we put the binary content into an [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBuffer) (you can use [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) or the [File API](https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsArrayBuffer()) for that). As we need to access data in different types, like 8 or 16 bit integers, the easiest way is to pass this buffer to a [DataView](https://developer.mozilla.org/en-US/docs/Web/API/DataView).

In Master System, the entry point is the instruction located at index 0. We create a variable called `pc`

for program counter and set it to 0. It will keep a track of the location of the current instruction. We then read the 8 bit unsigned integer located at the current position of `pc`

and place it into a variable called `opcode`

. The instruction associated to this opcode will be executed. From there, we just repeat the process.

```
var rom = new DataView(romBuffer);
var pc = 0x0000;
while (true) {
var opcode = rom.getUint8(pc++);
switch(opcode) {
// ... more to come here!
}
}
```

For example, the 3rd instruction, located at index 3, has value 0xC3. It matches opcode `JP (nn)` (JP stands for jump). A jump transfers the execution of the program to somewhere else in the ROM. In terms of logic, that means update the value of `pc`

. The target address is the operand. We simply read the next 2 bytes as a 16 bit unsigned integer (0x006F in this case). Let’s put it all together:

```
var rom = new DataView(romBuffer);
var pc = 0x0000;
while (true) {
var opcode = rom.getUint8(pc++);
switch(opcode) {
case 0xC3:
// Code for opcode 0xC3 `JP (nn)`.
pc = rom.getUint16(pc);
break;
case 0xED:
// @todo Write code for opcode 0xED 0x56 `IM 1`.
break;
case 0xF3:
// @todo Write code for opcode 0xF3 `DI`.
break;
}
}
```

Of course, for the sake of simplicity, many details are omitted here.

Emulators working this way are called interpreters. They are relatively easy to develop, but the fetch/decode/execute loop adds significant overhead.

## Recompilation, the secret to full speed

Interpreters are just a first step to fast emulation, using them ensures everything else is working: video, sound, and controllers. Interpreters can be fast enough on desktop, but are definitely too slow on mobile and drain battery.

Let’s step back a second and examine the code above. Wouldn’t it be great if we could generate JavaScript code to mimic the logic? We know that when `pc`

equals 0x0000, the next 3 instructions will always be executed one after another, until the jump is reached.

In other words, we want something like this:

```
var blocks = {
0x0000: function() {
// @todo Write code for opcode 0xF3 `DI`.
// @todo Write code for opcode 0xED 0x56 `IM 1`.
// Code for opcode 0xC3 `JP (nn)`.
this.pc = 0x006F;
},
0x006F: function() {
// @todo Write code for this opcode...
}
};
pc = 0x0000;
while (true) {
blocks[pc]();
}
```

This technique is called recompilation.

The reason why it is fast is because each opcode and operand is only read once when the JavaScript code is compiled. It is then easier for the JavaScript VM to optimise the generated code.

Recompilation is said to be static when it uses static analysis to generate code. On the other hand, dynamic recompilation creates new JavaScript functions at runtime.

In [jsSMS](https://github.com/gmarty/jsSMS), the emulator in which I implemented these techniques, the recompiler is made of 4 components:

- Parser: determines what part of the ROM is opcode, operand and data
- Analyser: groups instructions into blocks (e.g. a jump instruction closes a block and open a new one) and output an
[AST (abstract syntax tree)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) - Optimiser: apply several passes to make the code even faster
- Generator: convert the AST to JavaScript code

Generating functions on the fly can take time. That’s why one of the approaches is to use static recompilation and generate as much JavaScript code as possible before the game even starts. Then, because static recompilation is limited, whenever we find unparsed instructions at runtime, we generate new functions as the game is being played.

## So it is faster, but how faster?

According to the benchmarks I ran on mobile, recompilers are about 3-4 times faster than interpreters.

Here are some benchmarks on different browser / device pairs:

- Firefox OS v.1.1 Keon
- Firefox OS v.1.1 Peak
- Firefox 24 Samsung Galaxy S II
- Firefox 24 LG Nexus 4

![](../../assets/8e3bce7bd5fdbc20.png)


## Optimisation considerations

When developing jsSMS, I applied many optimisations. Of course, the first thing was to implement the improvements suggested by this [article about games for Firefox OS](https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/).

Before being more specific, keep in mind that emulators are a very particular type of gaming app. They have a limited number of variables and objects. This architecture is static, limited and as such is easy to optimise for performance.

### Use typed arrays wherever possible

Resources of old consoles are limited and most concepts can be mapped to typed arrays (stack, screen data, sound buffer…). Using such arrays makes it easier for the VM to optimise.

### Use dense arrays

A dense array is an array without holes. The most usual way is to set the length at creation and fill it with default values. Of course it doesn’t apply to arrays with unknown or variable size.

```
// Create an array of 255 items and prefill it with empty strings.
var denseArray = new Array(255);
for (var i = 0; i < 255; i++) {
denseArray[i] = '';
}
```

### Variables should be type stable

The type inferrer of the JavaScript VM tags variables with their type and uses this information to apply optimisations. You can help it by not changing the types of variables as the game runs. This implies the following consequences:

- Set a default value at declaration. ‘var a = 0;` instead of `var a;` Otherwise, the VM considers that the variable can be either number or undefined.
- Avoid recycling a variable for different types. E.g. number then string.
- Make Boolean variables real Boolean. Avoid truthy or falsey values and use `!!` or `Boolean()` to coerce.

Some syntaxes are ambiguous to the VM. For example, the following code was tagged as unknown arithmetic type by SpiderMonkey:

```
pc += d < 128 ? d : d - 256;
```

A simple fix was to rewrite this to:

```
if (d >= 128) {
d = d - 256;
}
pc += d;
```

### Keep numeric types stable

SpiderMonkey stores all JavaScript numeric values differently depending on what they look like. It tries to map numbers to internal types (like u32 or float). The implication of this is that maintaining the same underlying type is very likely to help the VM.

To target these type changes, I used to use JIT inspector, an extension for Firefox that exposes some internals of SpiderMonkey. However, it is not compatible with the latest versions of Firefox and no longer produce a useful output. There is a bug to follow the issue, but don’t expect any changes soon: [https://bugzilla.mozilla.org/show_bug.cgi?id=861069](https://bugzilla.mozilla.org/show_bug.cgi?id=861069).

### … and as usual profile and optimise

Using a JavaScript profiler will help you in finding the most frequently called functions. These are the ones you should focus on and optimise first.

## Digging deeper in code

If you want to learn more about mobile emulation and recompilation, have a look at this talk in which the slides are actually a ROM running inside the emulator!

## Conclusion

Mobile emulation shows how fast the web platform is, even on low-end devices. Using the right techniques and applying optimisations allows your games to run smoothly and at full speed. The documentation about emulation on the browser is scarce on the net, specially using modern JavaScript APIs. May this article address this lack.

There are so many video game consoles and so few web based emulators, so now, enough with the theory, and let’s start making apps for the sake of retro gaming!

## About
[
Guillaume Cedric Marty ](http://gu.illau.me)

Guillaume has been working in the web industry for more than a decade. He's passionate about web technologies and contributes regularly to open source projects, which he writes about on his [technical blog](http://gu.illau.me/). He's also fascinated by video games, animation, and, as a Japanese speaker, foreign languages.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 11 comments

IodineOctober 22nd, 2013 at 13:24Mindaugas J.October 22nd, 2013 at 18:04Guillaume Cedric MartyOctober 25th, 2013 at 12:51Nick FitzgeraldOctober 22nd, 2013 at 21:18Guillaume Cedric MartyOctober 25th, 2013 at 12:40Nick FitzgeraldOctober 22nd, 2013 at 21:19Grant GalitzOctober 26th, 2013 at 11:25Grant GalitzOctober 26th, 2013 at 11:37Grant GalitzOctober 27th, 2013 at 19:52Martin BuchnerNovember 21st, 2013 at 03:05Guillaume Cedric MartyNovember 21st, 2013 at 03:23