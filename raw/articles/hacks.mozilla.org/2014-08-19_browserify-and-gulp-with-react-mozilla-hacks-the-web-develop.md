---
title: Browserify and Gulp with React – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/08/browserify-and-gulp-with-react/
author: Kevin Ngo
published: '2014-08-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The JS world moves quickly, and nowadays, there’re some new kids around the block. Today, we’ll explore Browserify, Gulp, and React and see whether they’d sound suitable for our projects. You might have heard of them but not have had the time to check them out. So we’ll look at the advantages and disadvantages of using Browserify, using Gulp, using React. Because it certainly doesn’t hurt to know our options.

## Browserify: Bundling Node Modules for the Browser

[Browserify](http://browserify.org/) is a development tool lets us write Node-style modules in the browser or include actual Node modules from [npm](https://www.npmjs.org/). Modules are written in separate files, things can be `export`

ed, and modules pull in other modules through `require`

. Browserify can then parse our main JS module, building a dependency tree, to bundle everything together.

One great thing is that the tens of thousands of modules on NPM are now available for our projects. Dependencies are defined in `package.json`

, and if our project `requires`

them, Browserify will bundle these dependencies with our JS. Take this `package.json`

for example:

```
/* package.json */
{
"name": "hipApp",
"description": "Showing off hip stuff",
"dependencies": {
"browserify": "~3.44.x",
"gulp": "3.8.x",
"react": "0.11.x",
"underscore": "*"
}
}
```

Once we run `npm install`

, we’ll have modules like React and Underscore available to use in our project. Now we just `require`

them in our project:

```
/* app.js */
var React = require('react');
var myModule = require('./myModule');
// ...
```

Then we invoke Browserify:

browserify --debug app.js > bundle.js

And Browserify will include React from npm for us. Notice that it will even figure out which local modules to include. We included `./myModule`

which is another module in the same folder as `app.js`

.

Let’s compare this style of dependency loading with technologies such as AMD ,which is prominently implemented by [RequireJS](http://requirejs.org/). They are both JS module definition APIs but with different implementations. Browserify falls in line with CommonJS which is suited for the server, and RequireJS falls in line with AMD which is suited for the browser. However, either can be used in either environment.

What’s awesome about Browserify is that all NPM modules are available for our project, 86K and counting. Its modules also do not need to be wrapped in a `define`

call.

Though Browserify requires all the modules up front, which means needing a build step. AMD is asynchronous so modules can be lazily-loaded, and all that is needed is a page refresh. Though we can automate the Browserify build step with Gulp.

## Gulp: The Streaming Build System

[Gulp](http://gulpjs.com) is a JS build system, like [Grunt](http://gruntjs.com), that makes use of “streams”, or pipelining, and focuses on code-over-configuration. Build systems are usually set up to watch for changes to projects, and then automatically handling common build steps such as bundling, pre-compilation, or minification. Both Gulp and Grunt have tons of plugins to help with these things. Browserify is one such plugin.

Let’s take a look at an example Gulpfile. It includes some facilities for React JSX files which we haven’t looked at yet, but it’ll come in handy later. Read the comments in the Gulpfile to follow along:

```
/* gulpfile.js */
// Load some modules which are installed through NPM.
var gulp = require('gulp');
var browserify = require('browserify'); // Bundles JS.
var del = require('del'); // Deletes files.
var reactify = require('reactify'); // Transforms React JSX to JS.
var source = require('vinyl-source-stream');
var stylus = require('gulp-stylus'); // To compile Stylus CSS.
// Define some paths.
var paths = {
css: ['src/css/**/*.styl'],
app_js: ['./src/js/app.jsx'],
js: ['src/js/*.js'],
};
// An example of a dependency task, it will be run before the css/js tasks.
// Dependency tasks should call the callback to tell the parent task that
// they're done.
gulp.task('clean', function(done) {
del(['build'], done);
});
// Our CSS task. It finds all our Stylus files and compiles them.
gulp.task('css', ['clean'], function() {
return gulp.src(paths.css)
.pipe(stylus())
.pipe(gulp.dest('./src/css'));
});
// Our JS task. It will Browserify our code and compile React JSX files.
gulp.task('js', ['clean'], function() {
// Browserify/bundle the JS.
browserify(paths.app_js)
.transform(reactify)
.bundle()
.pipe(source('bundle.js'))
.pipe(gulp.dest('./src/'));
});
// Rerun tasks whenever a file changes.
gulp.task('watch', function() {
gulp.watch(paths.css, ['css']);
gulp.watch(paths.js, ['js']);
});
// The default task (called when we run `gulp` from cli)
gulp.task('default', ['watch', 'css', 'js']);
```

Just install the NPM dependencies, run `./node_modules/.bin/gulp`

, and it handles everything for us in the background. Our files are watched with `gulp.watch`

, tasks are automatically run, and things are cleanly accomplished in streams and pipelines. Whenever we modify any JS/CSS, we can can refresh in the browser just as if we were using AMD.

Whether to use Grunt or Gulp is a matter of preference. Both have tons of modules available, though Gulp is a bit newer. Grunt is done more through configuration whereas Gulp is done more through code and streams. Though Gulp can be a bit faster as it does not require intermediary files to accomplish its tasks. So with our build system in place, let’s head to the big show: React.

## React: Declarative and Reactive Components

[React](http://facebook.github.io/react/) is a JS library from Facebook for building reusuable web components. It’s not a full MVC framework like [AngularJS](https://angularjs.org/); React focuses on view rendering of components making no assumptions about framework, and it can plug in to most projects smoothly.

[Facebook says](http://facebook.github.io/react/docs/why-react.html) React was made to *build large applications with data that changes over time*. Facebook wanted something that didn’t take over the whole application. They could mix in components that could be integrated with legacy components. If you’d like some convincing, Pete Hunt, one of the authors of React, wrote some [arguments for React](http://www.quora.com/Pete-Hunt/Posts/React-Convincing-the-Boss) on Quora.

Rather than imperative one-way data binding as in traditional applications or two-way data binding as in Angular, React implements a **one-way reactive data flow**. Rather than manually registering listeners and handlers to update the DOM, or having to set up linking functions and data bindings, React’s components are **declaratively** defined and automatically re-render when its data changes. Like a function, data goes in, components come out.

For convenience, let’s take a look at an example based off of React’s homepage, which simply displays a name:

```
/** @jsx React.DOM */
var React = require('react'); // Browserify!
var HelloMessage = React.createClass({ // Create a component, HelloMessage.
render: function() {
return Hello {this.props.name}; // Display a property.
}
});
React.renderComponent( // Render HelloMessage component at #name.
``` ,
document.getElementById('name'));

You may have noticed, there’s some mark-up in our Javascript. React features syntatical sugar called JSX. It needs to be compiled into JS, which’ll automatically be done with our Gulpfile from earlier through the Reactify plugin. Though React also has a [JSX compiler](http://facebook.github.io/react/jsx-compiler.html) if we wanted it. Note that JSX is not required; React has normal JS APIs, but where’s the fun in that?

Components are created with `createClass`

. Like functions, components can take in arguments during rendering in the form of `props`

. In the above example `name="John"`

is passed into the component and is then referenced by `{this.props.name}`

. Note that components can be made up of only one Node. If we wish to have multiple DOM nodes, they must all be wrapped under a single root node.

Along with taking input data through `props`

, a component can have an internal and mutable state as accessed through `this.state`

. Here’s another example, this time of a timer, based off of React’s homepage:

```
/** @jsx React.DOM */
var React = require('react');
var Timer = React.createClass({
getInitialState: function() { // Like an initial constructor.
return {
seconds: 0
};
},
incrementTimer: function() { // A helper method for our Timer.
this.setState({ // Use setState to modify state.
seconds: this.state.seconds + 1 // Never modify state directly!
});
},
componentDidMount: function() { // A method run on initial rendering.
setInterval(this.incrementTimer, 1000);
},
render: function() {
return (
Seconds Elapsed: {this.state.seconds}
);
}
});
React.renderComponent(
``` , document.getElementById('timer'));

We have a `setInterval`

modifying our component’s state which triggers a refresh every 1000ms. Though in more practical applications, the state more likely be modified through user input or through data coming in via XHR rather than through a simple interval.

And those are some of the basics of React. If reusuable declarative components and reactive rendering hits you as something that would sound perfect in your project, you can head to [Getting Started with React](http://facebook.github.io/react/docs/getting-started.html). Best of luck to your development. Whether you decide to use these tools or not, it is always advantageous to know your options.

## About
[
Kevin Ngo ](http://ngokevin.com)

Kevin is a virtual reality developer at Mozilla and a core developer on A-Frame, an open-source WebVR framework. He is @ngokevin_ on Twitter.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

Victor BjelkholmAugust 22nd, 2014 at 08:50Robert Nyman [Editor]August 25th, 2014 at 00:21Pete DohertyAugust 27th, 2014 at 09:41Victor BjelkholmAugust 27th, 2014 at 11:36Eric NjangaAugust 27th, 2014 at 10:10Josh HabdasAugust 28th, 2014 at 14:23BrunoSeptember 5th, 2014 at 12:25BrunoSeptember 5th, 2014 at 13:17PalmerSeptember 15th, 2014 at 17:07