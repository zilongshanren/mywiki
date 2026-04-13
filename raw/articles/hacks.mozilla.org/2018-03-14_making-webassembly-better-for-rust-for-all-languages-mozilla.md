---
title: Making WebAssembly better for Rust & for all languages – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/
author: Lin Clark
published: '2018-03-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One big 2018 goal for the Rust community is to become a web language. By targeting WebAssembly, Rust can run on the web just like JavaScript. But what does this mean? Does it mean that Rust is trying to replace JavaScript?

The answer to that question is no. We don’t expect Rust WebAssembly apps to be written completely in Rust. In fact, we expect the bulk of application code will still be JS, even in most Rust WebAssembly applications.

This is because JS is a good choice for most things. It’s quick and easy to get up and running with JavaScript. On top of that, there’s a vibrant ecosystem full of JavaScript developers who have created incredibly innovative approaches to different problems on the web.

But sometimes for specific parts of an application, Rust+WebAssembly is the right tool for the job… like when you’re [parsing source maps](https://hacks.mozilla.org/2018/01/oxidizing-source-maps-with-rust-and-webassembly/), or figuring out what changes to make to the DOM, like [Ember](https://www.youtube.com/watch?v=qfnkDyHVJzs&feature=youtu.be&t=5880).

So for Rust+WebAssembly, the path forward doesn’t stop at compiling Rust to WebAssembly. We need to make sure that WebAssembly fits into the JavaScript ecosystem. Web developers need to be able to use WebAssembly as if it were JavaScript.

But WebAssembly isn’t there yet. To make this happen, we need to build tools to make WebAssembly easier to load, and easier to interact with from JS. This work will help Rust. But it will also help all other languages that target WebAssembly.

What WebAssembly usability challenges are we tackling? Here are a few:

- How do you make it easy to pass objects between WebAssembly and JS?
- How do you package it all up for
[npm](https://www.npmjs.com/)? - How do developers easily combine JS and WASM packages, whether in bundlers or browsers?

But first, what are we making possible in Rust?

Rust will be able to call JavaScript functions. JavaScript will be able to call Rust functions. Rust will be able to call functions from the host platform, like `alert`

. Rust crates will be able to have dependencies on npm packages. And throughout all of this, Rust and JavaScript will be passing objects around in a way that makes sense to both of them.

So that’s what we are making possible in Rust. Now let’s look at the WebAssembly usability challenges that we need to tackle.

### Q. How do you make it easy to pass objects between WebAssembly and JS?

A. `<a href="https://github.com/alexcrichton/wasm-bindgen">wasm-bindgen</a>`


One of the hardest parts of working with WebAssembly is getting different kinds of values into and out of functions. That’s because WebAssembly currently only has two types: integers and floating point numbers.

This means you can’t just pass a string into a WebAssembly function. Instead, you have to go through a bunch of steps:

- On the JS side, encode the string into numbers (using something like the TextEncoder API)

![Encoder ring encoding Hello into number equivalent](../../assets/64b145131d922717.png)

- Put those numbers into WebAssembly’s memory, which is basically an array of numbers

![JS putting numbers into WebAssembly's memory](../../assets/759c46b60caf74ab.png)

- Pass the array index for the first letter of the string to the WebAssembly function

![](../../assets/75f17d6145717e6f.png)

- On the WebAssembly side, use that integer as a pointer to pull out the numbers

![](../../assets/a170d49c21da441b.png)


And that’s only what’s required for strings. If you have more complex types, then you’re going to have a more convoluted process to get the data back and forth.

If you’re using a lot of WebAssembly code, you’ll probably abstract this kind of glue code out into a library. Wouldn’t it be nice if you didn’t have to write all that glue code, though? If you could just pass complex values across the language boundary and have them magically work?

That’s what `wasm-bindgen`

does. If you add a few annotations to your Rust code, it will automatically create the code that’s needed (on both sides) to make more complex types work.

This means calling JS functions from Rust using whatever types those functions expect:

#[wasm_bindgen] extern { type console; #[wasm_bindgen(static = console)] fn log(s: &str); }

#[wasm_bindgen] pub fn foo() { console::log("hello!"); }

… Or using structs in Rust and having them work as classes in JS:

// Rust #[wasm_bindgen] pub struct Foo { contents: u32, } #[wasm_bindgen] impl Foo { pub fn new() -> Foo { Foo { contents: 0 } }

pub fn add(&mut self, amt: u32) -> u32 { self.contents += amt; return self.contents } }

// JS import { Foo } from "./js_hello_world";

let foo = Foo.new(); assertEq(foo.add(10), 10); foo.free();

… Or many other niceties.

Under the hood, `wasm-bindgen`

is designed to be language-independent. This means that as the tool stabilizes it should be possible to expand support for constructs in other languages, like C/C++.

Alex Crichton will be writing more about `wasm-bindgen`

in a couple of weeks, so watch for that post.

### Q. How do you package it all up for npm?

A. `<a href="https://github.com/ashleygwilliams/wasm-pack/">wasm-pack</a>`


Once we put it all together, we have a bunch of files. There’s the compiled WebAssembly file. Then there’s all of the JavaScript — both dependencies and the JS generated by `wasm-bindgen`

. We need a way to package them all up. Plus, if we’ve added any npm dependencies, we need to put those into the `package.json`

manifest file.

Again, it would be nice if this could be done for us. And that’s what `wasm-pack`

does. It is a one-stop shop for going from a compiled WebAsssembly file to an npm package.

It will run `wasm-bindgen`

for you. Then, it will take all of the files and package them up. It will pop a `package.json`

on top, filling in all of the npm dependencies from your Rust code. Then, all *you* need to do is `npm publish`

.

Again, the foundations of this tool are language-independent, so we expect it to support multiple language ecosystems.

Ashley Williams will be writing more about `wasm-pack`

next month, so that’s another post to watch for.

### Q. How do developers easily combine JS and WASM, whether in bundlers, browsers, or Node?

A. ES modules

Now that we’ve published our WebAssembly to npm, how do we make it easy to use that WebAssembly in a JS application?

Make it easy to add the WebAssembly package as a dependency… to include it in JS module dependency graphs.

Currently, WebAssembly has an imperative JS API for creating modules. You have to write code to do every step, from fetching the file to preparing the dependencies. It’s hard work.

But now that native module support is in browsers, we can add a declarative API. Specifically, we can use the ES module API. With this, working with WebAssembly modules should be as easy as importing them.

We’re working with TC39 and the WebAssembly community group to standardize this.

But we don’t just need to standardize ES module support. Even once browsers and Node support ES modules, developers will still likely use bundlers. That’s because bundlers reduce the number of requests that you have to make for module files, which means it takes less time to download your code.

Bundlers do this by combining a bunch of modules from different files into a single file, and then adding a little bit of a runtime to the top to load them.

Bundlers will still need to use the JS API to create the modules, at least in the short term. But users will be authoring with ES module syntax. Those users will expect their modules to act as if they were ES modules. We’ll need to add some features to WebAssembly to make it easier for bundlers to emulate ES modules.

I will be writing more about the effort to add ES module integration to the WebAssembly spec. I’ll also be diving into bundlers and their support for WebAssembly over the coming months.

### Conclusion

To be a useful as a web language, Rust needs to work well with the JavaScript ecosystem. We have some work to do to get there, and fortunately that work will help other languages, too. Do you want to help make WebAssembly better for every language? Join us! We’re happy to [help you get started](http://fitzgeraldnick.com/2018/02/27/wasm-domain-working-group.html) :)


## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 10 comments

Ray ScottMarch 14th, 2018 at 09:51Pablo ValdesMarch 14th, 2018 at 11:54Jack BlevinsMarch 15th, 2018 at 08:11Tom OMarch 15th, 2018 at 08:47Todd L NordbyMarch 15th, 2018 at 23:21SerhiiMarch 16th, 2018 at 02:07Artem RudenkoMarch 18th, 2018 at 16:46Lin ClarkMarch 22nd, 2018 at 17:25Christian GaetanoMarch 20th, 2018 at 10:47Lin ClarkMarch 22nd, 2018 at 17:27