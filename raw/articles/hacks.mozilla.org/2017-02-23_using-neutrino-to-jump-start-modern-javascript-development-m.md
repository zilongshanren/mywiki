---
title: Using Neutrino to jump-start modern JavaScript development – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2017/02/using-neutrino-for-modern-javascript-development/
author: Eli Perelman
published: '2017-02-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Neutrino](https://neutrino.js.org) is a tool which brings together the best parts of the modern JavaScript toolchain with the ease of zero upfront configuration. Embarking on the adventure that is JavaScript development can be daunting.

Working with the latest tools and cutting edge libraries is fun, but oftentimes results in a significant amount of setup overhead before sitting down to write an app. Facing analysis paralysis is a common threat, and the time necessary to complete a comprehensive tooling pipeline has given rise to stigmas like “JavaScript fatigue”. Neutrino was built to let you hit the ground running.

Neutrino combines the power of [Webpack](https://webpack.github.io/) with the simplicity of presets to build web and Node.js projects. By encapsulating the common use cases of Webpack configuration into shareable presets, it is possible to create an application without ever needing to touch a configuration file. At present, there are presets available for creating applications for the web, React, and even Node.js. Adding testing or linting is also only a preset away. Let’s take a look at how quickly we can start a React application.

## React quickstart

*Throughout this guide I’ll be using the Yarn client for working with dependencies and running commands. This is merely a personal preference; you can also use the npm client if you desire.*

First up, we need a space to create our React application. In your terminal, create a new directory and change it into:

```
❯ mkdir hacks-react
❯ cd hacks-react
```


Next, let’s add Neutrino and the React preset for building the app, and some other dependencies for actually developing with React:

```
❯ yarn add --dev neutrino neutrino-preset-react
❯ yarn add react react-dom
```


The React preset has a few conventions:

- Source code lives in
`src`

- The entry point to the app is
`src/index.js`

- You can mount your application to an element with an ID of “root”

Let’s create the entry file at `src/index.js`

, edit it with some simple content, and render it:

```
import React from 'react';
import { render } from 'react-dom';
render(<h1>Hacks: React!</h1>, document.getElementById('root'));
```


In order to run our preview app and build it, add a couple scripts to your package.json:

```
{
"scripts": {
"start": "neutrino start --presets neutrino-preset-react",
"build": "neutrino build --presets neutrino-preset-react"
},
"devDependencies": {
"neutrino": "^4.0.0",
"neutrino-preset-react": "^4.0.0"
},
"dependencies": {
"react": "^15.4.2",
"react-dom": "^15.4.2",
"react-hot-loader": "next"
}
}
```


Run the command to start it in your console, and open the URL given:

```
❯ yarn start
✔ Development server running on: http://localhost:5000
✔ Build completed
```


![Screen Shot 2017-02-17 at 12.55.05 AM](../../assets/b1f1843a4b99a681.png)


In less than 5 minutes, we have a working start to a React app! What’s more, our Neutrino preset comes with quite a bit out of the box:

- Zero upfront configuration necessary to start developing and building a React web app.
- Modern
[Babel](https://babeljs.io/)compilation adding JSX, ES modules, last 2 major browser versions, async functions, and object rest spread syntax. - Support for React Hot Loader with hot module replacement.
- Extends from
`neutrino-preset-web`

. - Webpack loaders for importing HTML, CSS, images, icons, and fonts directly from JavaScript.
- Webpack Dev Server during development.
- Automatic creation of static HTML pages, no templating necessary.
- Production-optimized bundles with
[Babili minification](https://babeljs.io/blog/2016/08/30/babili)and easy chunking. - Easily extensible to customize your project as needed, no blackboxes or ejecting required.

## Code quality

It’s just as easy to add linting. Let’s use the [Airbnb style guide](https://github.com/airbnb/javascript) as an example. By adding the Airbnb preset, we can lint our source code according to the Airbnb style guide:

```
❯ yarn add --dev neutrino-preset-airbnb-base
```


Now let’s add our preset to our Neutrino commands, but let’s move it to “presets” and out of “scripts” so it’s not so unwieldy and we reduce repetition. Also, the Airbnb preset needs to load before our build preset:

```
{
"config": {
"presets": [
"neutrino-preset-airbnb-base",
"neutrino-preset-react"
]
},
"scripts": {
"start": "neutrino start",
"build": "neutrino build"
}
}
```


If we start the app again, but this time introduce something that goes against the Airbnb style guide, we can see the problems right in the console:

```
❯ yarn start
✔ Development server running on: http://localhost:5000
✔ Build completed
ERROR in ./src/index.js
/Users/eli/code/hacks-react/src/index.js
5:13 error Strings must use singlequote quotes
✖ 1 problem (1 error, 0 warnings)
```


Keeping your code quality high is as simple as adding presets and following conventions. You can follow the same guidelines to add testing to the project. Just choose a testing preset and you are on your way.

## With great power…

There may come a point where something in the build process needs to change to support your specific use cases. Fortunately, customizing and overriding the build process is straightforward. Neutrino does not force you to maintain the entire build configuration if you need changes, nor does it eject all its dependencies into your project. Each Neutrino preset has well-defined mechanisms for augmenting the build with a minimal but intuitive API. Creating your own presets is also a good way to unify configuration across many projects and reduce duplicating common changes. Simply publish to npm or GitHub, add as another dependency, and continue developing.

## Our motivation

We created Neutrino to solve problems we faced creating front-end applications across teams within Mozilla’s Release & Productivity organization. Neutrino is currently in use by several Mozilla projects including [TaskCluster](https://github.com/taskcluster/mozilla-taskcluster), [Treeherder](https://wiki.mozilla.org/EngineeringProductivity/Projects/Treeherder), and Unified Logviewer. We maintain and support Neutrino because it is something we ourselves need and use, and we hope that everyone who uses it will also benefit.

## Go forth and create

By bringing together great tools, Neutrino and its presets foster an environment for rapid development while eliminating some of the barriers in the way of writing applications. I encourage you to read through the comprehensive [Neutrino documentation](https://neutrino.js.org) and try it out in your next project. All the source code is licensed MPL v2 and is available on [GitHub](https://github.com/mozilla-neutrino/neutrino-dev). Enjoy!

## 14 comments

batFebruary 23rd, 2017 at 14:32Eli PerelmanFebruary 23rd, 2017 at 14:48batFebruary 23rd, 2017 at 18:02Eli PerelmanFebruary 23rd, 2017 at 20:02Philip ManderFebruary 24th, 2017 at 05:24Eli PerelmanFebruary 24th, 2017 at 10:03Jorge AntunesFebruary 24th, 2017 at 09:27Eli PerelmanFebruary 24th, 2017 at 10:04KZFebruary 26th, 2017 at 01:15Eli PerelmanFebruary 26th, 2017 at 07:27AlexanderMarch 3rd, 2017 at 02:50Eli PerelmanMarch 3rd, 2017 at 05:36DamiMarch 10th, 2017 at 10:10Eli PerelmanMarch 10th, 2017 at 10:16