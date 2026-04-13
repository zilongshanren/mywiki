---
title: 'The Web Developer Toolbox: Backbone – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/10/the-web-developer-toolbox-backbone/
author: Jeremie Patonnier
published: '2012-10-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is [the fourth in a series of articles](https://hacks.mozilla.org/category/web-developer-toolbox/) dedicated to useful libraries that all web developers should have in their toolbox. The intent is to show you what those libraries can do and help you to use them at their best. This fourth article is dedicated to the Backbone library.

## Introduction

[Backbone](http://backbonejs.org/) is a library originally written by [Jeremy Ashkenas](http://ashkenas.com/) (also famous for having created [CoffeeScript](http://coffeescript.org/)).

Backbone is an implementation of the MVC design pattern in JavaScript. It allows you to build applications easier to maintain by strongly dividing responsibility of each application component. Actually due to it’s high flexibility, Backbone is more something like a super controller in the MVC design pattern than a true MVC implementation. It gives you freedom to choose your own model or view system as long as you make sure they are compatible with its API.

## Basic usage

Backbone is made of 4 core objects that will be used to drive your application: `Collection`

, `Model`

, `View`

, `Router`

. To make things a little clearer here is a quick schema of their interaction:

### The `Model`

objects

Those kind of objects are the heart of your application. They will contain the whole logic of your application and they will dispatch events each time they are updated. That way, you can easily bind a View object to a model in order to react to any change. Those objects are actually wrappers around your own application business logic (Functions, Objects, Libraries, whatever).

### The `Collection`

objects

As stated by its name, this type of object is a collection of `Model`

objects with their own logic to sort them, filter them, etc. This object is a convenient way to make the glue between the model and the view because it is some sort of a super Model object. Any change send by a Model object in a collection is also sent by the collection so it makes easy to bind a view to several Model objects.

### The `View`

objects

Backbone views are almost more convention than code — they don’t determine anything about your HTML or CSS for you, you’re free to use any JavaScript templating library such as [Mustache](http://mustache.github.com/), [haml-js](https://github.com/creationix/haml-js), etc. The idea is to organize your interface into logical views, backed by models, each of which can be updated independently when the model changes, without having to redraw the page. Instead of digging into a JSON object, looking up an element in the DOM, and updating the HTML by hand, you can bind your view’s render function to the model’s “`change`

” event — and thanks to that everywhere that model data is displayed in the UI, it’s immediately updated.

### The `Router`

objects

Those objects provides methods for routing URLs, and connecting them to actions and events on Model objects. It relies on the History API to nicely handle the URLs. For browsers which don’t yet support the History API, it handles graceful fallback and transparent translation to a hash fragments’ URL.

So as you can see it’s not necessarily a canonical implementation of the MVC design pattern but it allows you to work that way with high flexibility.

## Getting started or Digging into it

Digging into Backbone is not that simple. As you can see, I haven’t tried to provide some code sample in this article. Even if the documentation is well written it’s sometimes a bit difficult to understand how to use the full API. Fortunately, there is some very good tutorials and projects out there and I recommend the following:

- The famous
[Backbone Tutorial](http://backbonetutorials.com/)by Thomas Davis - The
[Hello Backbone](http://arturadib.com/hello-backbonejs/)tutorial by Artur Adib, which is a very thoughtful progressive list of commented code samples and examples [The TodoMVC project](http://todomvc.com/)which builds the same basic Todo list application with different JavaScript MVC libraries. Of course,[Backbone is one of them](http://todomvc.com/architecture-examples/backbone/).

If you know some other good resources, feel free to add it through the comments ;)

## Limits and precautions

One of the biggest limitations of backbone is its dependency of two other libraries: [Underscore](http://underscorejs.org/) and [jQuery](http://jquery.com/) (or jQuery like library such as [Zepto](http://zeptojs.com/)). The former provide some very useful (and missing) features to JavaScript, the latter is conveniently used to access and manipulate the DOM easily as well as dealing with DOM Events.

Another point you should take care of is that backbone remains a very low level library that can be hard to deploy and to use easily. This is mainly due to the fact that it’s just a library rather than a full framework with coding conventions. Some aside projects try to make it more user friendly. One of the best known is the [Chaplin](https://github.com/chaplinjs/chaplin/) project.

## Conclusion

Backbone is one of the best libraries to help you build powerful applications. Even if its MVC implementation is somewhat unconventional, it’s a very good way to structure your code and being able to make your code base grow without too much trouble. Of course there are other libraries that do similar things such as [Ember](http://emberjs.com/) or [Knockout](http://knockoutjs.com/). If you plan to work on a large application, you really should consider using one of them.

## About
[
Jeremie Patonnier ](https://developer.mozilla.org)

Jeremie is a long time contributor/employee to the Mozilla Developer Network, and a professional web developer since 2000. He's advocating web standards, writing documentation and creating all sort of content about web technologies with the will to make them accessible to everybody.

## One comment

Allan JosephNovember 28th, 2012 at 05:16