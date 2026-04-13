---
title: Power Polygon – HTML5 slides with theming and much more – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/01/power-polygon-html5-slides-with-theming-and-much-more/
author: Felipe Nascimento de Moura
published: '2013-01-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Since 2007 or so, I’ve been giving talks on my web browser, although browsers did not offer much of the current technology back then! Of course, each talk of mine was based on a new HTML page which isn’t very practical! Power Polygon was then born! And died a few months after that! I kept it working and used it in many of my talks, but I knew it needed some special updates.

In 2012, with [BrazilJS Foundation](http://braziljs.org), which I’m a co-founder, and all the mess with those many presentation tools out there, I decided to reopen the project and BrazilJS became the foster father of the project, which you can find in the [BrazilJS’s projects page](http://braziljs.org/projetos) and on [BrazilJS Foundation’s github](http://github.com/braziljs/power-polygon) page.

This new version of Power Polygon was entirely re-written and was based on statements of some of the best speakers we know of, putting the identified useful tools together!

Want to see it working? First, you can watch a short video with an overview of these features:

Now, you can check on the following demos:

- A presentation showing the
[BrazilJS Conference after event information](http://felipenmoura.org/talks/braziljs-2012/?lang=en). [Demo showing many of the available features](http://felipenmoura.org/talks/meet-ppw/?lang=en)[A demo using the parallax theme](http://felipenmoura.org/talks/demo-parallax/?lang=en)[A slider theme demo](http://felipenmoura.org/talks/yesterday-news/?lang=en)- Using a 3D effect for slide transitions:
[example 1](http://felipenmoura.org/talks/yesterday-news/?lang=en&transition=trans-3d-3#thanks)and[example 2](http://felipenmoura.org/talks/yesterday-news/?lang=en&transition=trans-3d-4#thanks)

## Why Power Polygon?

Well, the first thing is that all the existing presentation tools work by themselves and following their own formats or “fixed” themes and results! The main idea of Power Polygon is to keep it open as the web!

In Power Polygon, there may be addons, themes, transactions and customisations as you need! Even extra JavaScript and CSS or HTML elements can be added.

Your talks in Power Polygon can count on some interesting tools, besides the addons, to help you presenting them, as well as to publish them and making it easier for users to see it afterwards.

Plus, you can change languages of your slides, share it or even profile your talk for different audiences. Once this new version of Power Polygon was born from the knowledge and experience of great speakers and their living situations, you know it is being prepared and maintained to fit such needs!

Power Polygon is open source under MIT license, although, you can create your theme or addon and use its own license, as well as your talks. We believe that being free, means *you* should be able to CHOOSE what you want to keep for free or not! Still, the Power Polygon core is and will be kept Open Source.

## Using it

You can simply load the jquery and power-polygon scripts to your page, and then every section element will become an slide!

All you gotta do is to add, in the end of your HTML code, the following line:

`PPW.init();`

This will set all the default settings to your talk! So, you can easily copy your slides from a tool to another, as well as copying them from one presentation to another! You can pass your own settings to the .init method and change everything!

Another way of using Power Polygon, is to have all your slides saved in individual HTML files…you can even have different directories for each slides and then, put their images inside each respective folder, Power Polygon will load them for you as you define the `slides`

property in your settings, like this:

```
PPW.init({
slides: [
{ id: "myFirstSlide", type: "opening"},
{ id: "anotherSlideOfMine", type: "content"}, // default type, if type is not defined
{ id: "anotherSubject", type: "section"}, // slides of type section look like slide titles
{ id: "anotherSlide", type: "content", notes: ["remember the milk!", "drink water!"]},
{ id: "theLastOne", type: "closing"} // the closing slide is the end of your talk
]
});
```

As you see, your slides may have notes and different types. By defining your slides on the `init`

method, PPW(Power Polygon Web) will look for section elements with the respective IDs in your HTML document, if it is not found, PPW looks for it on a [customisable directory](https://github.com/braziljs/power-polygon/wiki/Create%20your%20talk#wiki-External%20slides).

External slides do not need to have the section element, once PPW will create it for each external slide, giving it the slide id.

You can see more in [the full definition of the available settings](https://github.com/braziljs/power-polygon/wiki/Create%20your%20talk#wiki-Full%20definition), and there’s more info in general in [the wiki documentation](https://github.com/braziljs/power-polygon/wiki).

## Some features

Power Polygon offers all the features we and the many speakers who have helped us building it, realized that would be useful for speakers to use, as well as to the audience to follow. You can easily change the font-size of your slides, the language of your texts(you can create your slides specifying as many different languages as you need), apply new themes, load addons, use CSS3 animations besides the jQuery animations…

Plus, you can see the thumbs of your slides, search into slides and use a group of default shortcuts, or create your own set of shortcuts. You can use some zooming features and add actions to your slides, as well. The presentation tool will let you know about the notes you wrote for each slide, the time left and what slide is next. Also, be alerted as the time passes and you can use the social addon here to see your mentions on twitter during your talk.

You can open your camera to the audience quite easily, so you can show them a device in your hand or anything else, re-sizing, dragging the video, or setting it to full screen. It is also easy for you to test the resolution, colors and font sizes before you start your talk, using the splash screen.

Many other features will be added and you can give us more ideas!

Feel free to submit [new issues on our github repository](https://github.com/braziljs/power-polygon/issues)!

![](../../assets/38b1c33853330ffa.png)


## Actions and animations

Besides the animations you will already be able to do by using jQuery on your talk, you will also be able to use the [PPW.animate()](https://github.com/braziljs/power-polygon/wiki/Create%20your%20slides#wiki-Adding%20richer%20animations) method. The difference here is that the PPW.animate method applies animations using CSS3, instead of JavaScript, and also offers a bunch of different, more complex set of animations, like bouncing or light-effect.

To add actions to a slide, all you gotta do is adding a script INSIDE your slide, either external or not, calling the method [PPW.addAction()](https://github.com/braziljs/power-polygon/wiki/Creating-slides). This will allow you to create a timming action, or to define what and how it is done, and undone.

## Addons and themes

You can also load or create your own addons, so you can add more features to your talk. Among the addons, you can use, for example, the syntax highlight addon, which shows better source codes on your talks, and even allows you to focus on specific lines of code, in case the speaker is a developer.

Another addon can load the mentions you are receiving on twitter, and show them to you on your presentation tool while you are giving your talk! Another example of addon is the [remote-control](https://github.com/braziljs/remote-control), which allows you to control your talk via cellphone or any mobile device, but not only go forward and backward with your slides, but also to show a pointer or a focus spot area on the current slide! You can even draw on the slide using the screen of your mobile device.

Everything that happens in Power Polygon triggers an event that can be listened by using the [PPW.addListener()](https://github.com/braziljs/power-polygon/wiki/API%20-%20Power%20Polygon) method. You can see the list of available events on the [API page](https://github.com/braziljs/power-polygon/wiki/API%20-%20Power%20Polygon).

## What is next?

We want the communities, not only from Brazil, to contribute to Power Polygon, to make it more useful for both speakers and attendees! We want the presentations to be creative and open as the web itself, and by that, I mean your talks should be different, should be creative, should be YOURS!

Therefore, we want to have a talk repository, where you can publish your talks, embed them everywhere, and also have them indexed by search engines. Another huge step we want, is to build a great new interface for you to create your talk, create themes or even addons! Also, feel free to contribute to it, as well!

We will be offering a repository with all the published addons, themes and transitions.

## We need you!

Power Polygon was created to exist as the web! Open, creative and help people to reach their goals! I know we can’t do it alone, so we need you! Power Polygon can be a much more useful tool with your ideas, contributions, and why not, addons, themes or even pull requests on github!

Also, feel free to submit new issues on our [github repository](http://github.com/braziljs/power-polygon)!

By the way, BrazilJS has a bunch of useful, cool projects that may need your initiative! You will be VERY welcome to contribute to our projects and to be at our conference!

I hope you like Power Polygon and look forward to hearing new ideas and feedback from you!

A passionate developer working with Open Source Web Technologies for about 8 years, is nowadays a Senior Development Analyst at the Portal Terra in Brazil. Felipe is also one of the organizers of BrazilJS, the Brazilian JavaScript Conference, and one of the founders of the foundation with the same name. Likes to create new projects, as well as trying new technologies and pushing things to their limits! "Changing the world is the least I expect from myself!"

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Eduard GotwigJanuary 30th, 2013 at 12:40Felipe N. MouraJanuary 30th, 2013 at 14:10