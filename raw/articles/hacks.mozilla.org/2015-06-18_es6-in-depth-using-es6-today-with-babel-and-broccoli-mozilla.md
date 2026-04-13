---
title: 'ES6 In Depth: Using ES6 today with Babel and Broccoli – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/06/es6-in-depth-babel-and-broccoli/
author: Gastón I Silva
published: '2015-06-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

ES6 is here, and people are already talking about ES7, what the future holds, and what shiny features a new standard can offer. As web developers, we wonder how we can make use of it all. More than once, in previous [ES6 In Depth posts](https://hacks.mozilla.org/category/es6-in-depth/), we’ve encouraged you to start coding in ES6, with a little help from some interesting tools. We’ve teased you with the possibility:

If you’d like to use this new syntax on the Web, you can use

[Babel]or[Google’s Traceur]to translate your ES6 code to web-friendly ES5.

Today we’re going to show you step-by-step how it is done. The above-mentioned tools are called *transpilers*. A transpiler is also known as a [source-to-source compiler](https://en.wikipedia.org/wiki/Source-to-source_compiler)—a compiler that translates between programming languages operating at comparable levels of abstraction. Transpilers let us write code using ES6 while also guaranteeing that we’ll be able to execute the code in every browser.

## Transpilation our salvation

A transpiler is very easy to use. You can describe what it does in only two steps:

1. We write code with ES6 syntax.

`<pre>`


let q = 99;

let myVariable = `${q} bottles of beer on the wall, ${q} bottles of beer.`;

</pre>

2. We use the code above as input for the transpiler, which will process it and produce the following output:

`<pre>`


"use strict";

var q = 99;

var myVariable = "" + q + " bottles of beer on the wall, " + q + " bottles of beer."

</pre>

This is the good old JavaScript we know. It can be used in any browser.

The internals of how a transpiler goes from input to output are highly complex and fall out of scope for this article. Just as we can drive a car without knowing all the internal engine mechanics, today we’ll leave the transpiler as a black box that is able to process our code.

### Babel in action

There are a couple of different ways to use Babel in a project. There is a command line tool, which you can use with commands of the form:

`<pre>`


babel script.js --out-file script-compiled.js

</pre>

A browser-ready version is also available. You can include Babel as a regular JS library and then you can place your ES6 code in script tags with the type `"text/babel"`

.

`<pre>`


<script src="node_modules/babel-core/browser.js"></script>

<script type="text/babel">

// Your ES6 code

</script>

</pre>

These methods do not scale when your code base starts to grow and you start splitting everything into multiple files and folders. At that moment, you’ll need a build tool and a way to integrate Babel with a build pipeline.

In the following sections, we’ll integrate Babel into a build tool, [Broccoli.js](http://broccolijs.com/), and we’ll write and execute our first lines of ES6 through a couple of examples. In case you run into trouble, you can review the complete source code here: [broccoli-babel-examples](https://github.com/givanse/broccoli-babel-examples). Inside the repository you’ll find three sample projects:

- es6-fruits
- es6-website
- es6-modules

Each one builds on the previous example. We start with the bare minimum and progress to a general solution, which can be used as the starting point of an ambitious project. In this post, we’ll cover the first two examples in detail. After we are done, you’ll be able to read and understand the code in the third example on your own.

If you are thinking —I’ll just wait for browsers to support the new features— you’ll be left behind. Full compliance, if it ever happens, will take a long time. Transpilers are here to stay; new ECMAScript standards are planned to be released yearly. So, we’ll continue to see new standards released more often than uniform browser platforms. Hop in now and take advantage of the new features.

## Our first Broccoli & Babel project

Broccoli is a tool designed to build projects as quickly as possible. You can uglify and minify files, among many other things, through the use of [Broccoli plugins](https://www.npmjs.com/browse/keyword/broccoli-plugin). It saves us the burden of handling files, directories, and executing commands each time we introduce changes to a project. Think of it as:

Comparable to the Rails asset pipeline in scope, though it runs on Node and is backend-agnostic.


### Project setup

#### Node

As you might have guessed, you’ll have to [install Node 0.11 or later](https://nodejs.org/).

If you are in a unix system, avoid installing from the package manager (apt, yum). That is to avoid using root privileges during installation. It’s best to manually install the binaries, provided at the previous link, with your current user. You can read why using root is not recommended in [Do not sudo npm](http://givan.se/do-not-sudo-npm/). In there you’ll find other [installation alternatives](http://givan.se/do-not-sudo-npm/#install-npm-properly).

#### Broccoli

We’ll set up our Broccoli project first with:

`<pre>`


mkdir es6-fruits

cd es6-fruits

npm init

# Create an empty file called Brocfile.js

touch Brocfile.js

</pre>

Now we install `broccoli`

and `broccoli-cli`


`<pre>`


# the broccoli library

npm install --save-dev broccoli

# command line tool

npm install -g broccoli-cli

</pre>

### Write some ES6

We’ll create a `src`

folder and inside we’ll put a `fruits.js`

file.

`<pre>`


mkdir src

vim src/fruits.js

</pre>

In our new file we’ll write a small script using ES6 syntax.

`<pre>`


let fruits = [

{id: 100, name: 'strawberry'},

{id: 101, name: 'grapefruit'},

{id: 102, name: 'plum'}

];

for (let fruit of fruits) {

let message = `ID: ${fruit.id} Name: ${fruit.name}`;

console.log(message);

}

console.log(`List total: ${fruits.length}`);

</pre>

The code sample above makes use of three ES6 features:

`let`

for local scope declarations (to be discussed in an upcoming blog post)[for-of loops](https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/)[template strings](https://hacks.mozilla.org/2015/05/es6-in-depth-template-strings-2/)

Save the file and try to execute it.

`<pre>`


node src/fruits.js

</pre>

It won’t work yet, but we are about to make it executable by Node and any browser.

`<pre>`


let fruits = [

^^^^^^

SyntaxError: Unexpected identifier

</pre>

### Transpilation time

Now we’ll use Broccoli to load our code and push it through Babel. We’ll edit the file `Brocfile.js`

and add this code to it:

`<pre>`


// import the babel plugin

var babel = require('broccoli-babel-transpiler');

// grab the source and transpile it in 1 step

fruits = babel('src'); // src/*.js

module.exports = fruits;

</pre>

Notice that we require `broccoli-babel-transpiler`

, a Broccoli plugin that wraps around the Babel library, so we must install it with:

`<pre>`


npm install --save-dev broccoli-babel-transpiler

</pre>

Now we can build our project and execute our script with:

`<pre>`


broccoli build dist # compile

node dist/fruits.js # execute ES5

</pre>

The output should look like this:

`<pre>`


ID: 100 Name: strawberry

ID: 101 Name: grapefruit

ID: 102 Name: plum

List total: 3

</pre>

That was easy! You can open `dist/fruits.js`

to see what the transpiled code looks like. A nice feature of the Babel transpiler is that it produces readable code.

## Writing ES6 code for a website

For our second example we’ll take it up a notch. First, exit the `es6-fruits`

folder and create a new directory `es6-website`

using the steps listed under **Project setup** above.

In the `src`

folder we’ll create three files:

`src/index.html`


`<pre>`


<!DOCTYPE html>

<html>

<head>

<title>ES6 Today</title>

</head>

<style>

body {

border: 2px solid #9a9a9a;

border-radius: 10px;

padding: 6px;

font-family: monospace;

text-align: center;

}

.color {

padding: 1rem;

color: #fff;

}

</style>

<body>

<h1>ES6 Today</h1>

<div id="info"></div>

<hr>

<div id="content"></div>

<script src="//code.jquery.com/jquery-2.1.4.min.js"></script>

<script src="js/my-app.js"></script>

</body>

</html>

</pre>

`src/print-info.js`


`<pre>`


function printInfo() {

$('#info')

.append('<p>minimal website example with' +

'Broccoli and Babel</p>');

}

$(printInfo);

</pre>

`src/print-colors.js`


`<pre>`


// ES6 Generator

function* hexRange(start, stop, step) {

for (var i = start; i < stop; i += step) {

yield i;

}

}

function printColors() {

var content$ = $('#content');

// contrived example

for ( var hex of hexRange(900, 999, 10) ) {

var newDiv = $('<div>')

.attr('class', 'color')

.css({ 'background-color': `#${hex}` })

.append(`hex code: #${hex}`);

content$.append(newDiv);

}

}

$(printColors);

</pre>

You might have noticed this bit: `function* hexRange`

— yes, that’s an [ES6 generator](https://hacks.mozilla.org/2015/05/es6-in-depth-generators/). This feature is not currently supported in all browsers. To be able to use it, we’ll need a polyfill. Babel provides this and we’ll put it to use very soon.

The next step is to merge all the JS files and use them within a website. The hardest part is writing our Brocfile. This time we install 4 plugins:

`<pre>`


npm install --save-dev broccoli-babel-transpiler

npm install --save-dev broccoli-funnel

npm install --save-dev broccoli-concat

npm install --save-dev broccoli-merge-trees

</pre>

Let’s put them to use:

`<pre>`


// Babel transpiler

var babel = require('broccoli-babel-transpiler');

// filter trees (subsets of files)

var funnel = require('broccoli-funnel');

// concatenate trees

var concat = require('broccoli-concat');

// merge trees

var mergeTrees = require('broccoli-merge-trees');

// Transpile the source files

var appJs = babel('src');

// Grab the polyfill file provided by the Babel library

var babelPath = require.resolve('broccoli-babel-transpiler');

babelPath = babelPath.replace(/\/index.js$/, '');

babelPath += '/node_modules/babel-core';

var browserPolyfill = funnel(babelPath, {

files: ['browser-polyfill.js']

});

// Add the Babel polyfill to the tree of transpiled files

appJs = mergeTrees([browserPolyfill, appJs]);

// Concatenate all the JS files into a single file

appJs = concat(appJs, {

// we specify a concatenation order

inputFiles: ['browser-polyfill.js', '**/*.js'],

outputFile: '/js/my-app.js'

});

// Grab the index file

var index = funnel('src', {files: ['index.html']});

// Grab all our trees and

// export them as a single and final tree

module.exports = mergeTrees([index, appJs]);

</pre>

Time to build and execute our code.

`<pre>`


broccoli build dist

</pre>

This time you should see the following structure in the `dist`

folder:

`<pre>`


$> tree dist/

dist/

├── index.html

└── js

└── my-app.js

</pre>

That is a static website you can serve with any server to verify that the code is working. For instance:

`<pre>`


cd dist/

python -m SimpleHTTPServer

# visit http://localhost:8000/

</pre>

You should see this:

![simple ES6 website](../../assets/06676560bfc217f0.png)


## More fun with Babel and Broccoli

The second example above gives an idea of how much we can accomplish with Babel. It might be enough to keep you going for a while. If you want to do more with ES6, Babel, and Broccoli, you should check out this repository: [broccoli-babel-boilerplate](https://github.com/jayphelps/broccoli-babel-boilerplate). It is also a Broccoli+Babel setup, that takes it up at least two notches. This boilerplate handles modules, imports, and unit testing.

You can try an example of that configuration in action here: [es6-modules](https://github.com/givanse/broccoli-babel-examples/tree/master/es6-modules). All the magic is in the Brocfile and it’s very similar to what we have done already.

*As you can see, Babel and Broccoli really do make it quite practical to use ES6 features in web sites right now. Thanks to Gastón I. Silva for contributing this week’s post!*

*Next week, ES6 In Depth starts a two-week summer break. This series has covered a lot of ground, but some of ES6’s most powerful features are yet to come. So please join us when we return with new content on July 9.*

*Jason Orendorff*

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) Editor

## About
[
Gastón I. Silva ](http://givan.se)

Software engineer dedicated to web technologies and open source software.

## 8 comments

Grahame BowlandJune 18th, 2015 at 07:20Gastón I. SilvaJune 18th, 2015 at 08:31Chris DeelyJune 19th, 2015 at 11:54Gastón I. SilvaJune 19th, 2015 at 12:17Owen DensmoreJune 19th, 2015 at 20:20Alexander IvantsovJune 23rd, 2015 at 01:35Luis G.June 23rd, 2015 at 18:07BergiJune 23rd, 2015 at 19:58