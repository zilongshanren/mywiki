---
title: Serving Backbone for Robots & Legacy Browsers – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/04/serving-backbone-for-robots-legacy-browsers/
author: Lauri Svan
published: '2013-04-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I like the Single Page Application model and [Backbone.js](http://backbonejs.org/), because I get it. As a former Java developer, I am used to object oriented coding and events for messaging. Within our HTML5 consultancy, SC5, Backbone has become almost a synonym for single page applications, and it is easy to move between projects because everybody gets the same basic development model.

We hate the fact that we need to have server side workarounds for robots. Making applications crawlable is very reasonable business-wise, but ill-suited for the SPA model. Data-driven single page applications typically get only served a HTML page skeleton, and the actual construction of all the visual elements is done in browser. Any other way would easily lead into double code paths (one on a browser, one on a server). Some have even concerned on giving up the SPA model and moving the logic and representation back to the server.

Still, we should not let the tail wag the dog. Why sacrifice the user experience of 99,9% of the users for the sake of the significant 0.1%? Instead, for such low traffic, a better suited solution would be to create a server side workaround.

## Solving the Crawling Problem with an App Proxy

The obvious solution for the problem is running the same application code at the both ends. Like in the digital television transformation, a set-top box would fill in the gap of legacy televisions by crunching the digital signal into analog form. Correspondingly, a proxy would run the application server side and serve the resulting HTML back to the crawlers. Smart browsers would get all the interactive candy, whereas crawlers and legacy browsers would just get the pre-processed HTML document.

![Proxy pattern explained through a TV set metaphor Proxy pattern explained through a TV set metaphor](../../assets/b61703f842fd2afa.png)


Thanks to [node.js](http://nodejs.org/), JavaScript developers have been able to use their favourite language on the both ends for some time already, and proxy-like solutions have become a plausible option.

## Implementing DOM and Browser APIs on the Server

Single page applications typically heavily depend on DOM manipulation. Typical server applications combine several view templates into a page through concatenation, whereas Backbone applications append the views into DOM as new elements. Developer would either need to emulate DOM on the server side, or build an abstraction layer that would permit using DOM on the browser and template concatenation on the server. DOM can either be serialized into a HTML document or vice versa, but these techniques cannot be easily mixed runtime.

A typical Backbone application talks with the browser APIs through several different layers – either by using Backbone or jQuery APIs, or accessing the APIs directly. Backbone itself has only minor dependencies to layers below – [jQuery](http://jquery.com/) is used in DOM manipulation and AJAX requests, and application state handling is done using pushState.

![Sample Backbone layers Sample Backbone layers](../../assets/c4d78fc4edbe6d64.png)


Node.js has ready-made modules for each level of abstraction: [JSDOM](https://github.com/tmpvar/jsdom) offers a full DOM implementation on the server-side, whereas [Cheerio](https://github.com/MatthewMueller/cheerio) provides a jQuery API on top of a fake DOM with a better performance. Some of the other server-side Backbone implementations, like AirBnB [Rendr](http://nerds.airbnb.com/weve-launched-our-first-nodejs-app-to-product) and [Backbone.LayoutManager](http://vimeo.com/46033641), set the abstraction level to the level of Backbone APIs (only), and hide the actual DOM manipulation under a set of conventions. Actually, Backbone.LayoutManager does offer the jQuery API through Cheerio, but the main purpose of the library itself is to ease the juggling between Backbone layouts, and hence promote a higher level of abstraction.

## Introducing backbone-serverside

Still, we went for our own solution. Our team is a pack of old dogs that do not learn new tricks easily. We believe there is no easy way of fully abstracting out the DOM without changing what Backbone applications essentially are. We like our Backbone applications without extra layers, and jQuery has always served us as a good compatibility layer to defend ourselves against browser differences in DOM manipulation. Like Backbone.LayoutManager, we choose Cheerio as our jQuery abstraction. We solved the Backbone browser API dependencies by overriding Backbone.history and Backbone.ajax with API compatible replacements. Actually, in the first draft version, these implementations remain bare minimum stubs.

We are quite happy about the solution we have in the works. If you study the [backbone-serverside example](https://github.com/SC5/backbone-serverside), it looks quite close to what a typical Backbone application might be. We do not enforce working on any particular level of abstraction; you can use either Backbone APIs or the subset of APIs that jQuery offers. If you want to go deeper, nothing stops from implementing server-side version of a browser API. Insuch cases, the actual server side implementation may be a stub. For example, needs touch event handling on the server?

The current solution assumes a node.js server, but it does not necessarily mean drastic changes to an existing server stack. An existing servers for API and static assets can remain as-is, but there should be a proxy to forward the requests of dumb clients to our server. The sample application serves static files, API and the proxy from the same server, but they all could be decoupled with small modifications.

![backbone-serverside as a proxy backbone-serverside as a proxy](../../assets/b14bbc1ac825f551.png)


## Writing Apps That Work on backbone-serverside

Currently the backbone-serverside core is a bare minimum set of adapters to make Backbone run on node.js. Porting your application to run on server may require further modifications.

If the application does not already utilise a module loader, such as [RequireJS](http://requirejs.org/) or [Browserify](http://browserify.org/), you need to figure out on how to load the same modules on the server. In our example below, we use RequireJS and need a bit JavaScript to use Cheerio instead of vanilla jQuery on the server. Otherwise we are pretty able to use the same stack we typically use (jQuery, [Underscore](http://underscorejs.org/)/[Lo-Dash](http://lodash.com/), Backbone and [Handlebars](http://handlebarsjs.com/).When choosing the modules, you may need to limit to the ones that do not play with Browser APIs directly, or be prepared to write a few stubs by yourself.

```
// Compose RequireJS configuration run-time by determining the execution
// context first. We may pass different values to browser and server.
var isBrowser = typeof(window) !== 'undefined';
// Execute this for RequireJS (client or server-side, no matter which)
requirejs.config({
paths: {
text: 'components/requirejs-text/text',
underscore: 'components/lodash/dist/lodash.underscore',
backbone: 'components/backbone/backbone',
handlebars: 'components/handlebars/handlebars',
jquery: isBrowser ? 'components/jquery/jquery' : 'emptyHack'
},
shim: {
'jquery': {
deps: ['module'],
exports: 'jQuery',
init: function (module) {
// Fetch the jQuery adapter parameters for server case
if (module && module.config) {
return module.config().jquery;
}
// Fallback to browser specific thingy
return this.jQuery.noConflict();
}
},
'underscore': {
exports: '_',
init: function () {
return this._.noConflict();
}
},
'backbone': {
deps: ['underscore', 'jquery'],
exports: 'Backbone',
init: function (_, $) {
// Inject adapters when in server
if (!isBrowser) {
var adapters = require('../..');
// Add the adapters we're going to be using
_.extend(this.Backbone.history,
adapters.backbone.history);
this.Backbone.ajax = adapters.backbone.ajax;
Backbone.$ = $;
}
return this.Backbone.noConflict();
}
},
'handlebars': {
exports: 'Handlebars',
init: function() {
return this.Handlebars;
}
}
},
config: {
// The API endpoints can be passed via URLs
'collections/items': {
// TODO Use full path due to our XHR adapter limitations
url: 'http://localhost:8080/api/items'
}
}
});
```

Once the configuration works alright, the application can be bootstrapped normally. In the example, we use Node.js express server stack and pass specific request paths to Backbone Router implementation for handling. When done, we will serialize the DOM into text and send that to the client. Some extra code needs to be added to deal with Backbone asynchronous event model. We will discuss that more thoroughly below.

```
// URL Endpoint for the 'web pages'
server.get(//(items/d+)?$/, function(req, res) {
// Remove preceeding '/'
var path = req.path.substr(1, req.path.length);
console.log('Routing to '%s'', path);
// Initialize a blank document and a handle to its content
//app.router.initialize();
// If we're already on the current path, just serve the 'cached' HTML
if (path === Backbone.history.path) {
console.log('Serving response from cache');
res.send($html.html());
}
// Listen to state change once - then send the response
app.router.once('done', function(router, status) {
// Just a simple workaround in case we timeouted or such
if (res.headersSent) {
console.warn('Could not respond to request in time.');
}
if (status === 'error') {
res.send(500, 'Our framework blew it. Sorry.');
}
if (status === 'ready') {
// Set the bootstrapped attribute to communicate we're done
var $root = $html('#main');
$root.attr('data-bootstrapped', true);
// Send the changed DOM to the client
console.log('Serving response');
res.send($html.html());
}
});
// Then do the trick that would cause the state change
Backbone.history.navigate(path, { trigger: true });
});
```

## Dealing with Application Events and States

Backbone uses an asynchronous, event-driven model for communicating between the models views and other objects. For an object oriented developer, the model is fine, but it causes a few headaches on node.js. After all, Backbone applications are data driven; pulling data from a remote API endpoint may take seconds, and once it eventually arrives, the models will notify views to repaint themselves. There is no easy way to know when all the application DOM manipulation is finished, so we needed to invent our own mechanism.

In our example we utilise simple state machines to solve the problem. Since the simplified example does not have a separate application singleton class, we use a router object as the single point of control. Router listens for changes in states of each view, and only notifies the express server about readiness to render when all the views are ready. In the beginning of the request, router resets the view states to pending and does not notify the browser or server until it knows all the views are done. Correspondingly, the views do not claim to be done until they know they are fed with valid data from their corresponding model/collection. The state machine is simple and can be consistently applied throughout the different Backbone objects.

![Activity diagram of a Backbone app event flow Activity diagram of a Backbone app event flow](../../assets/5c78669494d09895.png)


## Beyond the Experimental Hack

The current version is still experimental work, but it proves Backbone applications can happily live on the server without breaking Backbone APIs or introducing too many new conventions. Currently in SC5 we have a few projects starting that could utilise the this implementation, so we will

continue the effort.

We believe the web stack community benefits from this effort, thus we have [published the work in GitHub](https://github.com/SC5/backbone-serverside). It is far from being finished and we would appreciate all community continueributions in the forms of ideas and code. Share the love, criticism and all in between: [@sc5io #backboneserverside](https://twitter.com/intent/tweet?url=https://github.com/SC5/backbone-serverside&text=@sc5io&hashtags=backboneserverside).

Particularly,we plan to change and hope to get contributions for the following:

- The current example will likely misbehave on concurrent requests. It shares a single DOM representation for all the ongoing requests, which can easily mess up each other.
- The state machine implementation is just one idea on how to determine when to serialize the DOM back to the client. It likely can be drastically simplified for most use cases, and it is quite possible to find a better generic solution.
- The server-side route handling is naive. To emphasize that only the crawlers and legacy browsers might need server-side rendering, the sample could use projects like express-device to detect if we are serving a legacy browser or a server.
- The sample application is a very rudimentary master-details view application and will not likely cause any wow effect. It needs a little bit of love.

We encourage you to fork the repository and start from modifying the example for your needs. Happy Hacking!

## About Lauri Svan

Lauri ([@laurisvan](https://twitter.com/laurisvan)) is an architect at [SC5](http://sc5.io/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

Lauri SvanApril 2nd, 2013 at 09:20Amy VargaApril 3rd, 2013 at 04:11AndrewApril 9th, 2013 at 03:43Lauri SvanApril 9th, 2013 at 07:20Paul GrillApril 9th, 2013 at 09:56