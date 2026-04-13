---
title: Building User-Extensible Webapps with Local – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/building-user-extensible-webapps-with-local/
author: Paul Frazee
published: '2013-03-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In an interview with Andrew Binstock in 2012, Alan Kay described the browser as “a joke.” If that surprises you, you’ll be glad to know that Mr. Binstock was surprised as well.

Part of the problem Kay pointed out is well-known: feature-set. Browsers are doing today what word-processors and presentation tools have done for decades. But that didn’t seem to be the problem that bothered him most. The real problem? Browser-makers thought they were making an application, when they were really building an OS.

The browser tab is a very small environment. Due to the same-origin policy, the application’s world is limited to what its host reveals. Unfortunately, remote hosts are often closed networks, and users don’t control them. This stops us from doing composition (no pipe in the browser) and configuration (no swapping out backends for your frontend). You can change tabs, but you can’t combine them.

## Built out of IRON

Despite these problems, the Web is successful, and the reasons for that are specific. [In a paper published in 2011, Microsoft, UT, and Penn researchers outlined the necessary qualities (PDF)](http://www.cs.utexas.edu/~mwalfish/papers/zoog-hotnets11.pdf): Isolated, Rich, On-demand, and Networked. Those qualities are why, on the whole, you can click around the Web and do interesting things without worrying a virus will infect your computer. As they point out, if we want to improve the Web, we have to be careful not to soften it.

That research team proposed a less-featured core browser which downloads its high-level capabilities with the page. Their approach could improve richness and security for the Web, but it requires a “radical refactor” first. With a need for something more immediate, I’ve developed [Local](http://grimwire.com/local), an in-browser program architecture which is compatible with HTML5 APIs.

## HTTP over Web Workers

Local uses Web Workers to run its applications. They’re the only suitable choice available, as iframes and object-capabilities tools (like Google’s Caja or Crockford’s ADsafe) share the document’s thread. Workers, however, lack access to the document, making them difficult to use. Local’s solution to this is to treat the Workers like Web hosts and dispatch requests over the `postMessage`

API. The Workers respond in turn with HTML, which the document renders.

This leaves it to the document to make a lot of decisions: traffic permissions, HTML behaviors, which apps to load, and so on. Those decisions make up the page’s “environment,” and they collectively organize the apps into either a host-driven site, a pluggable web app, or a user-driven desktop environment.

One of Local’s fundamental requirements is composition. The Internet’s strength– distributed interconnection– should be reflected in its software. REST is a unified interface to Local’s architecture, a philosophy which is borrowed from the Plan9 file-system. In HTML5 + Local, URIs can represent remote service endpoints, local service endpoints, and encoded chunks of data. The protocol to target javascript (httpl://) allows client regions to link to and target the Workers without event-binding.

This keeps HTML declarative: there’s no application-specific setup. Additional interface primitives can be introduced by the Environment. [Grimwire.com](http://grimwire.com) tries its own take on Web Intents, which produces a drag-and-drop-based UX. For programmatic composition, Local leans on the Link header, and provides the “navigator” prototype to follow those links in a hypermedia-friendly way.

Security is also a fundamental requirement for Local. The Web Worker provides a secure sandbox for untrusted code ([source (PDF)](http://www.cs.utexas.edu/~mwalfish/papers/treehouse-atc12.pdf), [source](http://stackoverflow.com/questions/12209657/how-can-i-sandbox-untrusted-user-submitted-javascript-content)). Content Security Policies allow environments to restrict inline scripts, styling, and embeds (including images). Local then provides a traffic dispatch wrapper for the environment to examine, scrub, route or deny application requests. This makes it possible to set policies (such as “local requests only”) and to intercept Cookie, Auth, and other session headers. The flexibility of those policies vary for each environment.

## Example Environment: a Markdown Viewer

To get an idea of how this works, let’s take a quick tour through a simple environment. These snippets are from [blog.grimwire.com](http://blog.grimwire.com). The page HTML, JS, and markdown are served statically. A Worker application, “markdown.js”, proxies its requests to the hosted blog posts and converts their content to HTML. The environment then renders that HTML into the Content “client region,” which is an area segmented by Local into its own browsing context (like an iframe).

### index.js

The first file we’ll look at is “index.js,” the script which sets up the environment:

```
// The Traffic Mediator
// examines and routes all traffic in the application
// (in our simple blog, we'll permit all requests and log the errors)
Environment.setDispatchWrapper(function(request, origin, dispatch) {
var response = dispatch(request);
// dispatch() responds with a promise which is
// fulfilled on 2xx/3xx and rejected on 4xx/5xx
response.except(console.log.bind(console));
return response;
});
// The Region Post-processor
// called after a response is rendered
// (gives the environment a chance to add plugins or styles to new content)
Environment.setRegionPostProcessor(function(renderTargetEl) {
Prism.highlightAll(); // add syntax highlighting with prismjs
// (http://prismjs.com/)
});
// Application Load
// start a worker and configure it to load our "markdown.js" file
Environment.addServer('markdown.util', new Environment.WorkerServer({
scriptUrl:'/local/apps/util/markdown.js',
// ^^ this tells WorkerServer what app to load
baseUrl:'/posts'
// ^^ this tells markdown.js where to find the markdown files
}));
// Client Regions
// creates browsing regions within the page and populates them with content
var contentRegion = Environment.addClientRegion('content');
contentRegion.dispatchRequest('httpl://markdown.util/frontpage.md');
```

The environment here is very minimal. It makes use of two hooks: the dispatch wrapper and the region post-processor. A more advanced environment might sub-type the `ClientRegion`

and `WorkerServer`

prototypes, but these two hooks should provide a lot of control on their own. The dispatch wrapper is primarily used for security and debugging, while the region post-processor is there to add UI behaviors or styles after new content enters the page.

Once the hooks are defined, the environment loads the markdown proxy and dispatches a request from the content region to load ‘frontpage.md’. Workers load asynchronously, but the WorkerServer buffers requests made during load, so the content region doesn’t have to wait to dispatch its request.

When a link is clicked or a form is submitted within a ClientRegion, Local converts that event into a custom ‘request’ DOM event and fires it off of the region’s element. Another part of Local listens for the ‘request’ event and handles the dispatch and render process. We use `dispatchRequest()`

to programmatically fire our own ‘request’ event at the start. After that, markdown files can link to “httpl://markdown.util/:post_name.md” and the region will work on its own.

### markdown.js

Let’s take a quick look at “markdown.js”:

```
// Load Dependencies
// (these calls are synchronous)
importScripts('linkjs-ext/responder.js');
importScripts('vendor/marked.js'); // https://github.com/chjj/marked
// Configure Marked.js
marked.setOptions({ gfm: true, tables: true });
// Pipe Functions
// used with `Link.Responder.pipe()` to convert the response markdown to html
function headerRewrite(headers) {
headers['content-type'] = 'text/html';
return headers;
}
function bodyRewrite(md) { return (md) ? marked(md) : ''; }
// WorkerServer Request Handler
app.onHttpRequest(function(request, response) {
// request the markdown file
var mdRequest = Link.dispatch({
method : 'get',
url : app.config.baseUrl + request.path,
// ^^ the `baseUrl` given to us by index.js
headers : { accept:'text/plain' }
});
// use helper libraries to pipe and convert the response back
Link.responder(response).pipe(mdRequest, headerRewrite, bodyRewrite);
});
// Inform the environment that we're ready to handle requests
app.postMessage('loaded');
```

This script includes all of the necessary pieces for a Worker application. At minimum, the app must define an HTTP request handler and post the ‘loaded’ message back to the environment. (`postMessage()`

is part of [MyHouse](http://github.com/pfraze/myhouse), the low-level Worker manager which HTTPL is built on.)

Before the application is loaded, Local nulls any APIs which might allow data leaks (such as XMLHttpRequest). When a Worker uses `Link.dispatch`

, the message is transported to the document and given to the dispatch wrapper. This is how security policies are enforced. Local also populates the `app.config`

object with the values given to the `WorkerServer`

constructor, allowing the environment to pass configuration to the instance.

With those two snippets, we’ve seen the basics of how Local works. If we wanted to create a more advanced site or desktop environment, we’d go on to create a layout manager for the client regions, UIs to load and control Workers, security policies to enforce permissions, and so on.

You can find the complete source for the blog at [github.com/pfraze/local-blog](https://github.com/pfraze/local-blog).

## User-Driven Software

Local’s objective is to let users drive the development of the Web. In its ideal future, private data can be configured to save to private hosts, peer-to-peer traffic can go unlogged between in-browser servers with WebRTC, APIs can be mashed up on the fly, and users can choose the interfaces. Rather than fixed websites, I’d like to see hosts provide platforms built around different tasks (blogging, banking, shopping, developing, etc) and competing on services for their user’s apps. Then, services like Mint.com could stop asking for your banking credentials. Instead, they’d just host a JS file.

You can get started with Local by reading its [documentation](http://grimwire.com/local/) and [blog](http://blog.grimwire.com/#blog.md), and by trying out [Grimwire](http://grimwire.com/), a general-purpose deployment in its early stages. The source can be found [on GitHub](https://github.com/pfraze/local) under the MIT license.

## About Paul Frazee

Paul Frazee is an Austin-based web developer with an interest in social computing, virtual reality, and systems architecture. He currently maintains Grimwire.com.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

abyMarch 18th, 2013 at 05:14Robert Nyman [Editor]March 19th, 2013 at 01:09John ThomasMarch 22nd, 2013 at 11:42MacioMarch 26th, 2013 at 06:38