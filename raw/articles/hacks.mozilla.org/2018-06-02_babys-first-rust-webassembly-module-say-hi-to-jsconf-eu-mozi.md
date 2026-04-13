---
title: 'Baby’s First Rust+WebAssembly module: Say hi to JSConf EU! – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2018/06/babys-first-rustwebassembly-module-say-hi-to-jsconf-eu/
author: Lin Clark
published: '2018-06-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A secret project has been brewing for JSConf EU, and this weekend is the big reveal…

The Arch is a larger-than-life experience that uses 30,000 colored LEDs to create a canvas for light animations.

And *you* can [take charge of this space](https://experiencethearch.com/). Using modules, you can create a light animation.

But even though this is JSConf, these animations aren’t just powered by JavaScript modules. In fact, we hope you will try something new… Rust + WebAssembly.

### Why this project?

One of the hardest problems when you’re learning a new programming language is finding a project that can teach you the basics, but that’s still fun enough to keep you learning more. And “Hello World” is only fun your first few times… it has no real world impact.

But what if your Hello World *could* have an impact on the real world? What if it could control a structure like this one?

So let’s get started on baby’s first Rust to WebAssembly module.

And in a way, this the perfect project for your first WebAssembly project… but not because this is the kind of project that you’d use WebAssembly for.

People usually use WebAssembly because they want to supercharge their application and make it run faster. Or because they want to use the same code across both the web and different devices, with their different operating systems.

This project doesn’t do either of those.

The reason this is a good project for getting started with WebAssembly is not because this is what you would use WebAssembly for.

Instead, it’s useful because it gives you a mental model of how JavaScript and WebAssembly work together. So let’s look at what we need to do to take control of this space with WebAssembly. And then I’ll explain why this makes it a good mental model for how WebAssembly and JavaScript work together.

### The space/time continuum as bytes

What we have here is a 3D space. Or really, if you think about it, it’s more like a four dimensional space, because we’re going through time as well.

The computer can’t think in these four dimensions, though. So how do we make these four dimensions make sense to the computer? Let’s start with the fourth dimension and collapse down from there.

You’re probably familiar with the way that we make time the fourth dimension make sense to computers. That’s by using these things called frames.

The screen is kind of like a flipbook. And each frame is like a page in that flip book.

On the web, we talk about having 60 frames per second. That’s what you need to have smooth animations across the screen. What that really means is that you have 60 different snapshots of the screen… of what the animation should look like at each of those 60 points during the second.

In our case, the snapshot is a snapshot of what the lights on the space should look like.

So that brings us down to a sequence of snapshots of the space. A sequence of 3D representations of the space.

Now we want to go from 3D to 2D. And in this case, it is pretty easy. All we need to do is take the space and flatten it out into basically a big sheet of graph paper.

So now we’re down to 2D. We just need to collapse this one more time.

We can do that by taking all the rows and putting them next to each other.

Now we’re down to this line of pixels. And this we can put in memory. Because memory is basically just a line of boxes.

This means we’ve gotten it down to a one-dimensional structure. We still have all of the data that we had in a two-, three- or four-dimensional representation. It’s just being represented in a different way. It’s being represented as a line.

### Why is this a good model for learning WebAssembly? Linear memory.

The reason that this is a good mental model for how WebAssembly and JavaScript work together is because one of the main ways to communicate between WebAssembly and JavaScript is through something called linear memory. It’s basically a line of memory that you use to represent things.

The WebAssembly module and the JavaScript that’s running it both have access to this object.

It’s a JavaScript object called an ArrayBuffer. An array buffer is just an array of bytes, and bytes are just numbers. So to make this animation happen, JavaScript tells the WebAssembly module, “Okay, fill in the animation now.”

It will do this by calling a method on the WebAssembly module.

WebAssembly will go and fill in all of the colors for each pixel in the linear memory.

Then the JavaScript code can pull those colors out and turn them into a JSON array that will get sent to the space.

Let’s look at how you use this data from JS.

### Linear memory, the hard way

If you’re doing everything yourself and not using any libraries, then you’ll be working directly with the linear memory.

This linear memory is just one big line of 1s and 0s. When you want to create meaning from these 1s and 0s, you have to figure out how to split them up. What you do is create a typed array view on the ArrayBuffer.

Basically this just tells JavaScript how to break up the the bits in this ArrayBuffer. It’s basically like drawing boxes around the bits to say which bits belong to which number.

For example, if you were using hexadecimal values, then your numbers would be 24 bits wide. So you’d need a box that can fit 24 bits. And each box would contain a pixel.

The smallest box that would fit is 32 bits. So we would create an `Int32`

view on the buffer. And that would wrap the bits up into boxes. In this case we’d have to add a little padding to fill it out (I’m not showing that, but there would be extra zeros).

In contrast, if we used RGB values, the boxes would only be 8 bits wide. To get one RGB value, you would take every three boxes and use those as your R — G — and B values. This means you would iterate over the boxes and pull out the numbers.

Since we’re doing things the hard way here, you need to write the code to do this. The code will iterate over the linear memory and move the data around into more sensible data structures.

For a project like this, that’s not too bad. Colors map well to numbers, so they are easy to represent in linear memory. And the data structures we’re using (RGB values) aren’t too complex. But when you start getting more complex data structures, having to deal directly with memory can be a big pain.

It would be a lot easier if you could pass a JS object into WebAssembly and just have the WebAssembly manipulate that. And this will be possible in the future with specification work currently happening in the WebAssembly community group.

But that doesn’t mean that you have to wait until it’s in the spec before you can start working with objects. You can pass objects into your WebAssembly and return them to JS today. All you need to do is add one tiny library.

### Linear memory, the easy way

This library is called `wasm-bindgen`

. It wraps the WebAssembly module in a JavaScript wrapper.

This wrapper knows how to take complex JavaScript objects and write them into linear memory. Then, when the WebAssembly function returns a value, the JS wrapper will take the data from linear memory and turn it back into a JS object.

To do this, it looks at the function signatures in your Rust code and figures out exactly what JavaScript is needed. This works for built-in types like strings. It also works for types that you define in your code. wasm-bidgen will take those Rust [structs](https://doc.rust-lang.org/1.15.1/book/structs.html) and turn them into JavaScript classes.

Right now, this tool is specific to Rust. But with the way that it’s architected, we can add support for this kind of higher level interaction for other languages — languages like C/C++.

### In conclusion…

Hopefully you now see how to take control of this space… How you can say Hello World, and hello to the world of WebAssembly.

Before I wrap this up, I do want to give credit to the people that made this project possible.

The seeds of the idea for this project came from a dance party in a space like this I attended in Pittsburgh. But this project was only possible because of the amazing group of people that gathered to make it a reality.

- Sandra Persing — I came to her with a vision and she made that vision real
- Dan Brown and Maciej Pluta, who took that vision and turned it into something even more exciting and engaging than I had imagined
- Till Schneidereit, who helped me figure out how all the pieces fit together
- Josh Marinacci, who created the site and made taking control of the space possible
- Dan Callahan, who jumped in with his development and debugging wizardry to ensure all of the pieces worked together
- Trevor F Smith, who created the virtual space so that everyone can experience the Arch, even if they aren’t at the event
- Michael Bebenita and Yury Delendik, whose work on WebAssembly Studio makes it possible to share WebAssembly with a whole new audience
- Rustaceans: Alex Crichton, Ashley Williams, Sarah Meyers, Jan-Erik Rediger, Florian Gilcher, Steve Klabnik, Fabian, Istvan ‘Flaki’ Szmozsanszky, who worked on WebAssembly Studio’s Rust integration and helped new, aspiring Rust developers level up their skills
- The JSConf EU team for all of their hard work making sure that we could get the project off the ground
- Ian Brill, the artist who’s work inspired this project and who’s hard work ensured we could share it with you

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.