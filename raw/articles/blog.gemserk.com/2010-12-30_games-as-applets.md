---
title: Games as Applets
url: https://blog.gemserk.com/2010/12/30/game-as-applets/
published: '2010-12-30'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As you may know, we are publishing our games in two formats, Applets and Webstart. Applets works in a similar fashion as a Unity or Flash applications does, you open the web page and the game loads inside it. Webstart applications starts as a desktop application, outside the browser.

In this post we will explain how we deal with Java Applets. One thing we didn’t like about applets is that they starts as soon as you visit the page, sometimes you want to visit a game page only to see some information or read comments, etc.

We created a workaround for that, it consists in showing a game’s screenshot with a text “click to play” and whenever a player clicks on it, the game is started.

**Implementation**

Our solution consist in a css with the styles to show the screenshot with the text and a javascript with the logic to change the screenshot with the Java Applet.

First we have styles to show the text over the screenshot and highlight it whenever the user moves the mouse over it.

**Style:**

.play { display:block; position:relative; -moz-opacity:0.80; opacity:0.80; } .play span { -moz-opacity:0.60; opacity:0.60; display:block; position:absolute; top:225px; z-index:100; width:100%; color: white; font-size: 80px; text-align: center; } .play:hover span { -moz-opacity:1; opacity:1; display:block; position:absolute; top:225px; z-index:100; width:100%; color: white; text-align: center; }

Then, we have some javascript to create the screenshot div dynamically, and to replace it with the applet tag when the user clicks on it, or send the user to install the needed version of Java if he hasn’t installed yet.

**Javascript:**

var requiredVersion = '1.6.0_10+' var width = "640" var height = "480" var screenshotUrl = "floatingislands03.jpg" var url = "launch-applet.jnlp"; var attributes = { code:'org.newdawn.slick.AppletGameContainer', width:width, height:height} ; var parameters = {jnlp_href: url}; var isRequiredVersion = deployJava.versionCheck(requiredVersion); var text = "" var callback = "" if (isRequiredVersion) { text = "Click to play" callback = "startGame()" } else { text = "Click to install Java" callback = "installJava()" } var screenshotDivHtml = "<div id=\"screenshot\" class=\"play\" onclick=\""+callback+"\" style=\"width:"+width+"px; height:"+height+"px; background-color:white;\">"; screenshotDivHtml += "<span style=\"color:black;\">"+text+"</span>"; screenshotDivHtml += "<img id=\"screenshotImage\" src=\""+screenshotUrl+"\" alt=\""+text+"\">"+"</img>"; screenshotDivHtml += "</div>"; var appletElement = document.getElementById('applet'); appletElement.innerHTML += screenshotDivHtml; function startGame() { var screenshotElement = document.getElementById('screenshot'); var appletElement = document.getElementById('applet'); appletElement.removeChild(screenshotElement); var oldwrite = document.write; var newHtml = ''; document.write = function (str) { newHtml += str; } deployJava.writeAppletTag(attributes, parameters); document.write = oldwrite; var realAppletElement = document.getElementById('realApplet') realAppletElement.innerHTML = newHtml } function installJava() { deployJava.installJRE(requiredVersion); }

Also, we will need to add two divs to the html to make the javascript to work.

**Html:**

That’s all, if you want to take a look at a working example, click [here](https://blog.gemserk.com/games/floating-islands/play/).