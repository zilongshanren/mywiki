---
title: Hello wasm-pack! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/04/hello-wasm-pack/
author: Ashley Williams
published: '2018-04-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![2 panels, one showing ferris the crab with assorted rust and wasm packages and one with the npm wombat with assorted js wasm and css/html packages. the crab is throwing a package over towards the wombat](../../assets/470ba705d99aac5b.png)


As [Lin Clark emphasizes in her article about Rust and WebAssembly](https://hacks.mozilla.org/2018/03/making-webassembly-better-for-rust-for-all-languages/): the goal of WebAssembly is not to replace JavaScript, but to be an awesome tool to use **with JavaScript**. Lots of amazing work has been done to simplify crossing the language boundary between JavaScript and WebAssembly, and you can read all about that in [Alex Crichton’s post on wasm-bindgen](https://hacks.mozilla.org/2018/04/javascript-to-rust-and-back-again-a-wasm-bindgen-tale/). This post focuses on a different type of JavaScript/Rust integration: package ecosystem and developer workflows.

Both Rust and JavaScript have vibrant package ecosystems. Rust has [cargo](https://github.com/rust-lang/cargo) and [crates.io](https://crates.io/). JavaScript has [several](https://yarnpkg.com/en/) [CLI](https://github.com/pnpm/pnpm) [tools](https://github.com/cnpm/cnpm), including the [npm CLI](https://github.com/npm/npm), that interface with the [npm registry](https://www.npmjs.com/). In order for WebAssembly to be successful, we need these two systems to work well together, specifically:

- Rust developers should be able to produce WebAssembly packages for use in JavaScript
**without**requiring a Node.js development environment - JavaScript developers should be able to use WebAssembly
**without**requiring a Rust development environment

✨📦 Enter: `wasm-pack`

.

`wasm-pack`

**is a tool for assembling and packaging Rust crates that target WebAssembly. These packages can be published to the npm Registry and used alongside other packages. This means you can use them side-by-side with JS and other packages, and in many kind of applications**, be it a Node.js server side app, a client-side application bundled by Webpack, or any other sort of application that uses npm dependencies. You can find `wasm-pack`

on [crates.io](https://crates.io/crates/wasm-pack) and [GitHub](https://github.com/ashleygwilliams/wasm-pack).

Development of this tooling has just begun and we’re excited to get more developers from both the Rust and JavaScript worlds involved. Both the JavaScript and Rust ecosystems are focused on developer experience. We know first hand that the key to a productive and happy ecosystem is good tools that automate the boring tasks and get out of the developer’s way. In this article, I’ll talk about where we are, where we’re headed, how to get started using the tooling now, and how to get involved in shaping its future.

## 💁 What it does today

![ferris stands between 2 open packages, one labelled rust, one labelled npm. there is a flow from the Rust package to the npm package with 4 stages. first stage: a lib.rs and cargo.toml file, then a .wasm file, then a .wasm and a .js file, then a .wasm, .js, package.json and a readme](../../assets/0884910fb39d7916.png)


Today, `wasm-pack`

walks you through four basic steps to prepare your Rust code to be published as a WebAssembly package to the npm registry:

### 1. Compile to WebAssembly

`wasm-pack`

will add the appropriate WebAssembly compilation target using [ rustup](https://rustup.rs/) and will compile your Rust to Web Assembly in release mode.

To do this, `wasm-pack`

will:

- Add the
`wasm32-unknown-unknown`

compilation target, if needed - Compile your Rust project for release using the wasm target

### 2. Run `wasm-bindgen`


`wasm-pack`

wraps the CLI portion of the `wasm-bindgen`

tool and runs it for you! This does things like wrapping your WebAssembly module in JS wrappers which make it easier for people to interact with your module. `wasm-bindgen`

supports both ES6 modules and CommonJS and you can use `wasm-pack`

to produce either type of package!

To do this, `wasm-pack`

will:

- If needed, install and/or update
`wasm-bindgen`

- Run
`wasm-bindgen`

, generating a new`.wasm`

file and a`.js`

file - Moves the generated files to a new
`pkg`

directory

### 3. Generate `package.json`


`wasm-pack`

reads your `Cargo.toml`

and generates the [ package.json](https://docs.npmjs.com/files/package.json) file necessary to publish your package to the npm registry. It will:

To do this, `wasm-pack`

will:

- Copy over your project
and`name`

`description`

- Link to your Rust project’s
`repository`

- List the generated JavaScript files in the
key. This ensures that those files, and only those files, are included in your npm package. This is particularly important for ensuring good performance if you intend to use this package, or a bundle including this package, in the browser!`files`


### 4. Documentation

`wasm-pack`

will copy your Rust project’s `README.md`

to the npm package it produces. We’ve got a lot of great ideas about extending this further to support the Rust ecosystem’s documentation feature, `rustdoc`

– more on the in the next section!

## 🔮 Future Plans

### Integrate with `rustdoc`


The crates.io team [survey](http://rust-lang.github.io/rfcs/1824-crates.io-default-ranking.html#factors-considered-when-ranking-crates)ed developers, and learned that [good documentation](http://rust-lang.github.io/rfcs/1824-crates.io-default-ranking.html#easy-to-use) was the number one feature that developers looked for when evaluating the use of crate. Contributor [Yoshua Wuyts](https://github.com/yoshuawuyts) introduced the brilliant idea of generating further `README.md`

content by integrating `wasm-pack`

with the Rust API documentation tool, `rustdoc`

. The Rust-wasm team is committed to making Rust a first class way to write WebAssembly. Offering documentation for Rust-generated WebAssembly packages that’s both easy to write and easy to discover aligns neatly with our goals. Read more about the team’s thoughts in [this issue](https://github.com/ashleygwilliams/wasm-pack/issues/7#issuecomment-368551714) and join in the discussion!

### Manage and Optimize your Rust and JS dependency graphs

The next large piece of development work on `wasm-pack`

will focus on using custom segments in compiled WebAssembly to declare dependencies on local Javascript files or other npm packages.

The preliminary work for this feature has [already landed](https://github.com/rustwasm/wasm-bindgen/issues/23) in `wasm-bindgen`

, so the next step will be integrating it into `wasm-pack`

. The naive integration won’t be too tricky- but we’re excited to explore the opportunities we have to streamline and optimize Rust dependency trees that contain npm dependencies on several levels! This work will be similar to the optimizations that bundlers like webpack deliver, but on the level of Rust dependencies.

There’s a lot of questions we still have to answer and there’s going be a lot of neat engineering work to do. In a few weeks there will be a full post on this topic, so keep an eye out!

![ferris is sitting in a package on a scale, in the distance several interconnected and dependent packages are linked with lines flowing into the package. the scale says "heavy"](../../assets/55a929a260d2ea4b.png)


### Grow Node.js toolchain in Rust

The largest and most ambitious goal of this project is to rewrite the required `npm login`

, `npm pack`

and `npm publish`

steps in Rust so that the required dependency on a Node.js development environment becomes optional for those who don’t currently use Node.js in their workflow. As we’ve said before, we want to ensure that both WebAssembly package producers and users can remain in their familiar workflows. Currently, that is true for JavaScript developers- they do not need to have a Rust development environment or any knowledge of Rust to get started using a Rust-generated WebAssembly module that’s been published with `wasm-pack`

. However, Rust developers still need to install Node.js and npm to publish with `wasm-pack`

, we’re excited to change that by writing a npm package publisher in Rust- and who knows, perhaps we can eventually integrate some Rust elements (perhaps compiled to WebAssembly!) into the npm client!

### Further collaboration with npm and bundlers

We’re always communicating with the npm CLI team members [Kat Marchan](https://github.com/zkat) and [Rebecca Turner](https://github.com/iarna), as well as the folks who work on [webpack](https://webpack.js.org/) and [Parcel](https://parceljs.org/)– we’re excited to keep working with them to make it easy for developers to release and use WebAssembly code!

## 🛠 Start using it today!

`wasm-pack`

is currently a command line tool distributed via Cargo. To install it, [setup a Rust development environment](https://www.rust-lang.org/en-US/install.html), and then run:

```
cargo install wasm-pack
```


If you aren’t sure where to start, we have a tutorial for you! [This tutorial](https://rust-lang-nursery.github.io/rust-wasm/wasm-pack/introduction.html), by [Michael Gattozzi](https://github.com/mgattozzi) and the Rust-wasm working group, walks you through:

- writing a small Rust library
- compiling it to WebAssembly, packaging, and publishing with
`wasm-pack`

- bundling with
[webpack](https://webpack.js.org/)to produce a small website

![a gif of the wasm pack CLI tool. first we ls a directory with a rust crate, then we run wasm pack. it completes in one minute, then we ls the target directory to see that a wasm binary was compiled, then we ls the pkg directory to see that an npm package was created](https://d2mxuefqeaa7sj.cloudfront.net/s_A9A8C3816B05444A18E82A6772DDBA985038B68FF6B90B7266556F8069E039E0_1524011130215_demo.gif)


## 👯♀️Contribute

The key to all excellent developer tooling is a short feedback cycle between developers of the tool and developers using the tool in their day to day workflows. In order to be successful with `wasm-pack`

, and all of our WebAssembly developer tooling, we need developers of all skill levels and backgrounds to get involved!

Take a look at our [Contributor Guidelines](https://github.com/ashleygwilliams/wasm-pack/blob/master/CONTRIBUTING.md) and our [Issue Tracker](https://github.com/ashleygwilliams/wasm-pack/issues) (we regularly label things as “[good first issue](https://github.com/ashleygwilliams/wasm-pack/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)” and provide mentors and mentoring instructions!)- we’re excited to work with you!

## About
[
Ashley Williams ](https://github.com/ashleygwilliams)

Ashley Williams is an engineer at Integer32, contracting for Mozilla on the Rust Programming Language. She is a member of the Rust Core team, leads the Rust Community Team, and helps maintain Rust's package registry, crates.io. Previously, she worked as an engineer at npm, the package manager for Javascript, and currently is the Individual Membership Director on the Node.js Foundation Board of Directors. A long time teacher, Ashley has focused much of her energies on education programs for open source projects, founding NodeTogether in 2016 and currently leading the RustBridge initiative. She has represented teachers' perspectives at TC39 meetings to influence the growth of JavaScript and continues to be passionate about growing the web through her work on Web Assembly.