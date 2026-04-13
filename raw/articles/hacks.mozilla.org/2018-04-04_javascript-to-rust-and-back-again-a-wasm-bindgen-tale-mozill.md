---
title: 'JavaScript to Rust and Back Again: A wasm-bindgen Tale – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2018/04/javascript-to-rust-and-back-again-a-wasm-bindgen-tale/
author: Alex Crichton
published: '2018-04-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Recently we’ve seen how WebAssembly is [incredibly fast to compile](https://hacks.mozilla.org/2018/01/making-webassembly-even-faster-firefoxs-new-streaming-and-tiering-compiler/), [speeding up JS libraries](https://hacks.mozilla.org/2018/01/oxidizing-source-maps-with-rust-and-webassembly/), and [generating even smaller binaries](https://hacks.mozilla.org/2018/01/shrinking-webassembly-and-javascript-code-sizes-in-emscripten/). We’ve even [got a high-level plan](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/) for better interoperability between the Rust and JavaScript communities, as well as other web programming languages. As alluded to in that [previous post](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/), I’d like to dive into more detail about a specific component, [ wasm-bindgen](https://github.com/alexcrichton/wasm-bindgen).

Today the [WebAssembly specification](https://webassembly.github.io/spec/) only defines four types: two integer types and two floating-point types. Most of the time, however, JS and Rust developers are working with much richer types! For example, JS developers often interact with [ document](https://developer.mozilla.org/en-US/docs/Web/API/Document) to add or modify HTML nodes, while Rust developers work with types like

[for error handling, and almost all programmers work with strings.](https://doc.rust-lang.org/std/result/enum.Result.html)

`Result`

Being limited only to the types that WebAssembly provides today would be far too restrictive, and this is where `wasm-bindgen`

comes into the picture. The goal of `wasm-bindgen`

is to provide a bridge between the types of JS and Rust. It allows JS to call a Rust API with a string, or a Rust function to catch a JS exception. `wasm-bindgen`

erases the impedance mismatch between WebAssembly and JavaScript, ensuring that JavaScript can invoke WebAssembly functions efficiently and without boilerplate, and that WebAssembly can do the same with JavaScript functions.

The `wasm-bindgen`

project has some more description in its [README](https://github.com/alexcrichton/wasm-bindgen/blob/master/README.md). To get started here, let’s dive into an example of using `wasm-bindgen`

and then explore what else it has to offer.

## Hello, World!

Always a classic, one of the best ways to learn a new tool is to explore its equivalent of printing “Hello, World!” In this case we’ll explore an [example](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples/hello_world) that does just that — alert “Hello, World!” to the page.

The goal here is simple, we’d like to define a Rust function that, given a name, will create a dialog on the page saying `Hello, ${name}!`

. In JavaScript we might define this function as:

```
export function greet(name) {
alert(`Hello, ${name}!`);
}
```


The caveat for this example, though, is that we’d like to write it in Rust. Already there’s a number of pieces happening here that we’ll have to work with:

- JavaScript is going to call into a WebAssembly module, namely the
`greet`

export. - The Rust function will take a string as an input, the
`name`

that we’re greeting. - Internally Rust will create a new string with the name interpolated inside.
- And finally Rust will invoke the JavaScript
function with the string that it has created.`alert`


To get started, we create a fresh new Rust project:

```
$ cargo new wasm-greet --lib
```


This initializes a new `wasm-greet`

folder, which we work inside of. Next up we modify our `Cargo.toml`

(the equivalent of `package.json`

for Rust) with the following information:

```
[lib]
crate-type = ["cdylib"]
[dependencies]
wasm-bindgen = "0.2"
```


We ignore the `[lib]`

business for now, but the next part declares a dependency on the [ wasm-bindgen crate](https://crates.io/crates/wasm-bindgen). The crate here contains all the support we need to use

`wasm-bindgen`

in Rust.Next up, it’s time to write some code! We replace the auto-created `src/lib.rs`

with these contents:

```
#![feature(proc_macro, wasm_custom_section, wasm_import_module)]
extern crate wasm_bindgen;
use wasm_bindgen::prelude::*;
#[wasm_bindgen]
extern {
fn alert(s: &str);
}
#[wasm_bindgen]
pub fn greet(name: &str) {
alert(&format!("Hello, {}!", name));
}
```


If you’re unfamiliar with Rust this may seem a bit wordy, but fear not! The `wasm-bindgen`

project is continually improving over time, and it’s certain that all this won’t always be necessary. The most important piece to notice is the `#[wasm_bindgen]`

*attribute*, an annotation in Rust code which here means *“please process this with a wrapper as necessary”*. Both our import of the `alert`

function and export of the `greet`

function are annotated with this attribute. In a moment, we’ll see what’s happening under the hood.

But first, we cut to the chase and open this up in a browser! Let’s compile our wasm code:

```
$ rustup target add wasm32-unknown-unknown --toolchain nightly # only needed once
$ cargo +nightly build --target wasm32-unknown-unknown
```


This gives us a wasm file at `target/wasm32-unknown-unknown/debug/wasm_greet.wasm`

. If we look inside this wasm file using tools like [ wasm2wat](https://github.com/WebAssembly/wabt) it might be a bit scary. It turns out this wasm file isn’t actually ready to be consumed just yet by JS! Instead we need one more step to make it usable:

```
$ cargo install wasm-bindgen-cli # only needed once
$ wasm-bindgen target/wasm32-unknown-unknown/debug/wasm_greet.wasm --out-dir .
```


This step is where a lot of the magic happens: the `wasm-bindgen`

CLI tool postprocesses the input `wasm`

file, making it suitable to use. We’ll see a bit later what “suitable” means, for now it suffices to say that if we import the freshly created `wasm_greet.js`

file (created by the `wasm-bindgen`

tool) we’ve got the `greet`

function that we defined in Rust.

Finally, all we’ve got to do is package it up with a bundler, and create an HTML page to run our code. At the time of this writing, only [Webpack’s 4.0 release](https://medium.com/webpack/webpack-4-released-today-6cdb994702d4) has enough WebAssembly support to work out-of-the box (although it also has a [Chrome caveat](https://github.com/alexcrichton/wasm-bindgen/blob/master/examples/hello_world/README.md#caveat-for-chrome-users) for the time being). In time, more bundlers will surely follow. I’ll skip the details here, but you can follow the [example](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples/hello_world) configuration in the Github repo. If we look inside though, our JS for the page looks like:

```
const rust = import("./wasm_greet");
rust.then(m => m.greet("World!"));
```


…and that’s it! Opening up our webpage should now show a nice “Hello, World!” dialog, driven by Rust.

## How `wasm-bindgen`

works

Phew, that was a bit of a hefty “Hello, World!” Let’s dive into a bit more detail as to what’s happening under the hood and how the tooling works.

One of the most important aspects of `wasm-bindgen`

is that its integration is fundamentally built on the concept that a wasm module is just another kind of ES module. For example, above we *wanted* an ES module with a signature (in Typescript) that looks like:

```
export function greet(s: string);
```


WebAssembly has no way to natively do this (remember that it only supports numbers today), so we’re relying on `wasm-bindgen`

to fill in the gaps. In our final step above, when we ran the `wasm-bindgen`

tool you’ll notice that a `wasm_greet.js`

file was emitted alongside a `wasm_greet_bg.wasm`

file. The former is the actual JS interface we’d like, performing any necessary glue to call Rust. The `*_bg.wasm`

file contains the actual implementation and all our compiled code.

When we import the `./wasm_greet`

module we get what the Rust code *wanted* to expose but couldn’t quite do so natively today. Now that we’ve seen how the integration works, let’s follow the execution of our script to see what happens. First up, our example ran:

```
const rust = import("./wasm_greet");
rust.then(m => m.greet("World!"));
```


Here we’re asynchronously importing the interface we wanted, waiting for it to be resolved (by downloading and compiling the wasm). Then we call the `greet`

function on the module.


Note: The asynchronous loading here is[required today with Webpack], but this will likely not always be the case and may not be a requirement for other bundlers.

If we take a look inside the `wasm_greet.js`

file that the `wasm-bindgen`

tool generated we’ll see something that looks like:

```
import * as wasm from './wasm_greet_bg';
// ...
export function greet(arg0) {
const [ptr0, len0] = passStringToWasm(arg0);
try {
const ret = wasm.greet(ptr0, len0);
return ret;
} finally {
wasm.__wbindgen_free(ptr0, len0);
}
}
export function __wbg_f_alert_alert_n(ptr0, len0) {
// ...
}
```



Note: Keep in mind this is unoptimized and generated code, it may not be pretty or small! When compiled with LTO (Link Time Optimization) and a release build in Rust, and after going through JS bundler pipelines (minification) this should be much smaller.

Here we can see how the `greet`

function is being generated for us by `wasm-bindgen`

. Under the hood it’s still calling the wasm’s `greet`

function, but it is called with a pointer and a length rather than a string. For more detail about `passStringToWasm`

you can see [Lin Clark’s previous post](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/). This is all boilerplate *you’d otherwise have to write* except the `wasm-bindgen`

tool is taking care of it for us! We’ll get to the `__wbg_f_alert_alert_n`

function in a moment.

Moving a level deeper, the next item of interest is the `greet`

function in WebAssembly. To look at that, let’s see what code the Rust compiler sees. Note that like the JS wrapper generated above, you’re not writing the `greet`

exported symbol here, but rather the `#[wasm_bindgen]`

attribute is generating a shim, which does the translation for you, namely:

```
pub fn greet(name: &str) {
alert(&format!("Hello, {}!", name));
}
#[export_name = "greet"]
pub extern fn __wasm_bindgen_generated_greet(arg0_ptr: *mut u8, arg0_len: usize) {
let arg0 = unsafe { ::std::slice::from_raw_parts(arg0_ptr as *const u8, arg0_len) }
let arg0 = unsafe { ::std::str::from_utf8_unchecked(arg0) };
greet(arg0);
}
```


Here we can see our original code, `greet`

, but the `#[wasm_bingen]`

attribute inserted this funny looking function `__wasm_bindgen_generated_greet`

. This is an exported function (specified with `#[export_name]`

and the `extern`

keyword) and takes the pointer/length pair the JS passed in. Internally it then converts the pointer/length to a [ &str](https://doc.rust-lang.org/std/primitive.str.html) (a String in Rust) and forwards to the

`greet`

function we defined.Put a different way, the `#[wasm_bindgen]`

attribute is generating two wrappers: One in JavaScript which takes JS types to convert to wasm, and one in Rust which receives wasm types and converts to Rust types.

Ok let’s look at one last set of wrappers, the `alert`

function. The `greet`

function in Rust uses the standard [ format!](https://doc.rust-lang.org/std/macro.format.html) macro to create a new string and then passes it to

`alert`

. Recall though that when we declared the `alert`

function we declared it with `#[wasm_bindgen]`

, so let’s see what rustc sees for this function:```
fn alert(s: &str) {
#[wasm_import_module = "__wbindgen_placeholder__"]
extern {
fn __wbg_f_alert_alert_n(s_ptr: *const u8, s_len: usize);
}
unsafe {
let s_ptr = s.as_ptr();
let s_len = s.len();
__wbg_f_alert_alert_n(s_ptr, s_len);
}
}
```


Now that’s not quite what we wrote, but we can sort of see how this is coming together. The `alert`

function is actually a thin wrapper which takes the Rust [ &str](https://doc.rust-lang.org/std/primitive.str.html) and then converts it to wasm types (numbers). This calls our

`__wbg_f_alert_alert_n`

funny-looking function we saw above, but a curious aspect of this is the `#[wasm_import_module]`

attribute.All imports of function in WebAssembly have a module that they come from, and since `wasm-bindgen`

is built on ES modules, this too will be interpreted as an ES module import! Now the `__wbindgen_placeholder__`

module doesn’t actually exist, but it indicates that this import will be rewritten by the `wasm-bindgen`

tool to import from the JS file we generated as well.

And finally, for the last piece of the puzzle, we’ve got our generated JS file which contains:

```
export function __wbg_f_alert_alert_n(ptr0, len0) {
let arg0 = getStringFromWasm(ptr0, len0);
alert(arg0)
}
```


Wow! It turns out that quite a bit is happening under the hood here and we’ve got a relatively long chain from `greet`

in JS to `alert`

in the browser. Fear not though, the key aspect of `wasm-bindgen`

is that all this infrastructure is hidden! You only need to write Rust code with a few `#[wasm_bindgen]`

here and there. Then your JS can use Rust just as if it were another JS package or module.

### What else can `wasm-bindgen`

do?

The `wasm-bindgen`

project is ambitious in scope and we don’t quite have the time to go into all the details here. A great way to explore the functionality in `wasm-bindgen`

is to explore the [examples directory](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples) which range from [Hello, World!](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples/hello_world) like we saw above to [manipulating DOM nodes](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples/dom) entirely in Rust.

At a high-level the features of `wasm-bindgen`

are:

- Importing JS structs, functions, objects, etc., to call in wasm. You can call JS methods on a struct and access properties, giving a bit of a “native” feel to the Rust you write once the
`#[wasm_bindgen]`

annotations are all hooked up. -
Exporting Rust structures and functions to JS. Instead of having JS only work with numbers you can export a Rust

`struct`

which turns into a`class`

in JS. Then you can pass structs around instead of only having to pass integers around. The[smorgasboard](https://github.com/alexcrichton/wasm-bindgen/tree/master/examples/smorgasboard)example gives a good taste of the interop supported. -
Allowing other miscellaneous features such as importing from the global scope (aka the

`alert`

function), catching JS exceptions using a`Result`

in Rust, and a generic way to simulate storing JS values in a Rust program.

If you’re curious to see more functionality, stay tuned especially with the [issue tracker](https://github.com/alexcrichton/wasm-bindgen/issues)!

## What’s next for `wasm-bindgen`

?

Before we close out I’d like to take a moment and describe the future vision for `wasm-bindgen`

because I think it’s one of the most exciting aspects of the project today.

### Supporting more than just Rust

From day 1, the `wasm-bindgen`

CLI tool was designed with multiple language support in mind. While Rust is the only supported language today, the tool is designed to plug in C or C++ as well. The `#[wasm_bindgen]`

attribute creates a custom section of the output `*.wasm`

file which the `wasm-bindgen`

tool parses and later removes. This section describes what JS bindings to generate and what their interface is. There’s nothing Rust-specific about this description, so a C++ compiler plugin could just as easily create the section and get processed by the `wasm-bindgen`

tool.

I find this aspect especially exciting because I believe it enables tooling like `wasm-bindgen`

to become a standard practice for integration of WebAssembly and JS. Hopefully, it is beneficial to *all* languages compiling to WebAssembly and recognized automatically by bundlers, to avoid almost all of the configuration and build tooling needed above.

### Automatically binding the JS ecosystem

One of the downsides today when importing functionality with the `#[wasm_bindgen]`

macro is that you have to write everything out and make sure you haven’t made any mistakes. This can sometimes be a tedious (and error-prone) process that is ripe for automation.

All web APIs are specified with [WebIDL](https://heycam.github.io/webidl/) and it should be quite feasible to [generate #[wasm_bindgen] annotations from WebIDL](https://github.com/alexcrichton/wasm-bindgen/issues/42). This would mean you wouldn’t need to define the

`alert`

function like we did above, instead you’d just need to write something like:```
#[wasm_bindgen]
pub fn greet(s: &str) {
webapi::alert(&format!("Hello, {}!", s));
}
```


In this case, the `webapi`

crate could automatically be generated entirely from the WebIDL descriptions of web APIs, guaranteeing no errors.

We can even take this a step further and leverage the awesome work of the TypeScript community and [generate #[wasm_bindgen] from TypeScript as well](https://github.com/alexcrichton/wasm-bindgen/issues/18). This would allow automatic binding of any package with TypeScript available on npm for free!

### Faster-than-JS DOM performance

And last, but not least, on the `wasm-bindgen`

horizon: ultra-fast DOM manipulation — the holy grail of many JS frameworks. Today calls into DOM functions have to go through costly shims as they transition from JavaScript to C++ engine implementations. With WebAssembly, however, these shims will not be necessary. WebAssembly is known to be well typed… and, well, has types!

The `wasm-bindgen`

code generation has been designed with the future [host bindings proposal](https://github.com/WebAssembly/host-bindings) in mind from day 1. As soon as that’s a feature available in WebAssembly, we’ll be able to directly invoke imported functions without any of `wasm-bindgen`

‘s JS shims. Furthermore, this will allow JS engines to aggressively optimize WebAssembly manipulating the DOM as invocations are well-typed and no longer need the argument validation checks that calls from JS need. At that point `wasm-bindgen`

will not only make it easy to work with richer types like strings, but it will also provide best-in-class DOM manipulation performance.

## Wrapping up

I’ve personally found that WebAssembly is incredibly exciting to work with not only because of the community but also the leaps and bounds of progress being made so quickly. The `wasm-bindgen`

tool has a bright future ahead. It’s making interoperability between JS and languages like Rust a first-class experience while also providing long-term benefits as WebAssembly continues to evolve.

Try giving [ wasm-bindgen](https://github.com/alexcrichton/wasm-bindgen) a spin,

[open an issue](https://github.com/alexcrichton/wasm-bindgen/issues)for feature requests, and otherwise

[stay involved](http://fitzgeraldnick.com/2018/02/27/wasm-domain-working-group.html)with Rust and WebAssembly!

## About Alex Crichton

Alex is a member of the Rust core team and has been working on Rust since late 2012. Nowadays he's helping the helping the WebAssembly Rust Working Group make Rust+Wasm the best possible experience. Alex also helps to maintain Cargo (Rust's package manager), the Rust standard library, and Rust's infrastructure for releases and CI.

## 4 comments

Jim DueyApril 10th, 2018 at 01:49KyuWoo ChoiApril 11th, 2018 at 03:55HongheApril 18th, 2018 at 19:38SerhiiApril 21st, 2018 at 06:57