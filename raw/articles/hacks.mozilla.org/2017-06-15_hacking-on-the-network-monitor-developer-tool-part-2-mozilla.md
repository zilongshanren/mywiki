---
title: Hacking on the Network Monitor Developer Tool (Part 2) – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2017/06/hacking-on-the-network-monitor-developer-tool/
author: Jan Honza Odvarko
published: '2017-06-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the previous post, [Network Monitor Reloaded](https://hacks.mozilla.org/2017/06/network-monitor-reloaded), we walked through the reasoning for refactoring the Network Monitor tool. We also learned that using web standards for building Dev Tools enables us to running them in different environments – loaded either within the Firefox Developer Toolbox or within a browser tab as a standard web application.

In this companion article, we’ll show you how to try these things and see the Network Monitor in action.

## Get to the Source

The Firefox Developer Tools code base is currently part of the Firefox source repository, and so, downloading it requires downloading the entire repo. There are several ways how to get the source code and work on the code. You might want to start with our [Github docs](http://docs.firefox-dev.tools/getting-started/build.html) for detailed instructions.

One option is to use [Mercurial](https://developer.mozilla.org/en/Mercurial) and clone the mozilla-central repository to get a local copy.

```
# This may take a while...
hg clone https://hg.mozilla.org/mozilla-central
cd mozilla-central
```


Part of our strategy to *use web standards to build tools for the web* also involves moving our code base from Mercurial to Git (on github.com). So, ultimately, the way to get the source code will change permanently, and it will be easier and faster to clone and work with.

## Run Developer Toolbox

For now, if you want to build the Network Monitor and run it inside the Firefox Developer Toolbox, follow these detailed [instructions](http://docs.firefox-dev.tools/getting-started/build.html#building-and-running-locally).

Essentially, all you need to do is use the `mach`

command.

```
cd mozilla-central
./mach build
```


After the build is complete, start the compiled binary and open the Developer Toolbox (*Tools -> Web Developer -> Toggle Tools*).

You can rebuild quickly after making changes to the source code as follows:

`./mach build faster`


## Run Development Server

In order to run Net Monitor inside a web page (experimental) you’ll need to install the following packages:

[Node](https://nodejs.org/)[NPM](https://www.npmjs.com/)[Yarn](https://yarnpkg.com/en/)- Firefox (either the
[released version](https://www.mozilla.org/en-US/firefox/new/)or the build from source code)

We’ve developed a simple container that allows running Firefox Dev Tools (not only the Network Monitor) inside a web page. This is called [Launchpad](https://github.com/firefox-devtools/devtools-core/tree/master/packages/devtools-launchpad#readme). The Launchpad is responsible for making a connection to the instance of Firefox being debugged and loading our Network Monitor tool.

The following diagram depicts the entire concept:

- The Net Monitor tool (client) is running inside a Browser tab just like any other standard web application.
- The app is served by the development server (server) through
`localhost:8000`

- The Net Monitor tool (client) is connecting to the target (debugged) Firefox instance through a WebSocket.
- The target Firefox instance needs to listen on port 6080 to allow the WebSocket connection to be created.
- The development server is started using yarn start

Let’s take a closer look at how to set up the development environment.

First we need to install dependencies for our development server:

```
cd mozilla-central
cd devtools/client/netmonitor
yarn install
```


Now we can run it:

`yarn start`


If all is ok, you should see the following message:

`Development Server Listening at http://localhost:8000`


Next, we need to listen for incoming connection in the target Firefox browser we want to debug. Open Developer Toolbar (*Tools -> Web Developer -> Developer Toolbar*) and type the following command into it. This will start listening so tools can connect to this browser.

`listen 6080`


The Developer Toolbar UI should be opened at the bottom of the browser window.

Finally, you can load `localhost:8000`


You should see the Launchpad user interface now. It lists the opened browser tabs in the target Firefox browser. You should also see that one of these tabs is the Launchpad itself (the last net monitor tab running from localhost:8000).

All you need to do is to click one of the tabs you want to debug. As soon as the Launchpad and Network monitor tools connect to the selected browser tab, you can reload the connected tab and see a list of HTTP requests.

If you change the underlying source code and refresh the page you’ll see your changes immediately.

Check out the following screencast for a detailed walk-through of running the Network monitor tool on top of the Launchpad and utilizing the hot-reload feature to see code changes instantly.

You might also want to read [mozilla-central/devtools/client/netmonitor/README.md](https://github.com/mozilla/gecko-dev/blob/master/devtools/client/netmonitor/README.md) for more detailed info about how to build and run the Network Monitor tool.

## Future Plans

We believe that building tools for the web using standard web technologies is the right way to go! Our tools are for web developers. We’d like you to be able to work with our tools using the same skills and knowledge that you already apply when developing web apps and services.

We are planning many more powerful features for Firefox Dev Tools, and we believe that the future holds a lot of exciting things. Here’s a teaser for what’s ahead on the roadmap.

- Connecting to Chrome
- Connecting to NodeJS
- Integration with existing IDEs

Stay tuned!

Jan ‘Honza’ Odvarko

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 6 comments

Damien JubeauJune 15th, 2017 at 09:57Towkir AhmedJune 15th, 2017 at 22:16BoryslavJune 16th, 2017 at 00:11VaelorJune 16th, 2017 at 00:54Towkir AhmedJune 16th, 2017 at 13:02Havi Hoffman [Editor]June 16th, 2017 at 13:35