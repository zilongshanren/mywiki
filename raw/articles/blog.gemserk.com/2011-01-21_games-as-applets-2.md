---
title: Games as Applets 2
url: https://blog.gemserk.com/2011/01/21/games-as-applets-2/
published: '2011-01-21'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Talking with [kappaOne](http://ninjacave.com/), one of the [LWJGL](http://lwjgl.org/) developers, he pointed us that our applet solution has one problem. When js is disabled or it has failed to load, then the applet tag is not written, then the game is not loaded.

In order to fix this problem, we adopted part of his solution. He always creates the applet tag for the game and then hides it using js. If for some reason js fails, then the applet starts automatically.

The new html needed looks like this:

**Html:**

<div id="applet" class="applet" align="center"> <applet id="gameApplet" width="800" height="600" code="com.gemserk.games.appletverifier.AppletVerifier" archive="http://www.gemserk.com/appletverifier-0.0.1-SNAPSHOT.jar"> <param name="jnlp_href" value="http://www.gemserk.com/prototipos/zombierockers-webstart-release/launch-applet.jnlp" > </applet> </div>

And this is the modified js with a merge between his solution and ours:

**Javascript:**

var width="800"; var height="600"; var jnlp_href="http://www.gemserk.com/prototipos/zombierockers-webstart-release/launch-applet.jnlp"; var screenshotUrl="/wp-content/uploads/2010/12/zombierockers-screenshot01.jpg"; var appletTag; var requiredVersion = '1.6.0_10+' var attributes = { code:'com.gemserk.games.appletverifier.AppletVerifier', width:width, height:height} ; var parameters = {jnlp_href: jnlp_href}; hideApplet(); function hideApplet(){ var appletbox=document.getElementById('applet'); appletTag = appletbox.innerHTML; if (navigator.appName == 'Microsoft Internet Explorer') { var params = ""; var p = appletbox.getElementsByTagName("PARAM"); for(var i=0; i < p.length; i++) { params += p[i].outerHTML; } appletTag = appletTag.replace("</APPLET>", params+"</APPLET>"); } var isRequiredVersion = deployJava.versionCheck(requiredVersion); var text = "" var callback = "" if (isRequiredVersion) { text = "Click to play" callback = "showApplet()" } else { text = "You don't have java plugin enabled, click to install" callback = "installJava(\'" + requiredVersion + "\')" } // adds the screenshot inside the applet div var screenshotDivHtml = "<div id=\"screenshot\" class=\"play\" onclick=\""+callback+"\" style=\"width:"+width+"px; height:"+height+"px;\">"; screenshotDivHtml += "<span>"+text+"</span>"; screenshotDivHtml += "<img id=\"screenshotImage\" src=\""+screenshotUrl+"\" alt=\""+text+"\" width=\""+width+"px\" height=\""+height+"px\">"+"</img>"; screenshotDivHtml += "</div>"; appletbox.innerHTML=screenshotDivHtml; } function showApplet(){ var appletbox=document.getElementById('applet'); appletbox.innerHTML = appletTag; } function installJava(version) { deployJava.installJRE(version); }

You can see a working example [here](https://blog.gemserk.com/games/floating-islands/play/).

Thats all.