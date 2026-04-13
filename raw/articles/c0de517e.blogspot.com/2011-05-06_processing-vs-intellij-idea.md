---
title: Processing vs IntelliJ IDEA
url: http://c0de517e.blogspot.com/2011/05/edit-and-continue-is-fun.html
published: '2011-05-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Update**: This old article used to describe how to get Processing up and running with Eclipse. That's not so great, so now I'm using IntelliJ's IDEA Community Edition instead.Even if I use Processing for small prototypes and stuff like that, I've always restricted myself to its own sketch IDE, even if it's fairly bad I never made big processing projects, I like its minimal interface and I'm not really the kind of guy that cares too much about his editor.

Also, the popular alternative is Eclipse an IDE that is the de-facto standard in the Java world and its known to be huge, slow and generally a mess. The few times I had to use Java I went with the simple and beautiful DrJava "educational" IDE instead.

Oh just how wrong I was about that. It turns out that Processing in IDEA ~~Eclipse~~ is just amazing, as ~~Eclipse~~ IDEA supports edit-and-continue ("hotswapping" if we don't want to stick to the MS lingo, it's a fairly old


~~Now you won't get anywhere near the awesomeness of something like ~~

[feature of the JVM](http://www.jug.mk/blogs/ipenov/entry/hotswapping_using_jvm)).[Fields](http://createdigitalmotion.com/2009/04/field-digital-movement-and-visual-expression-a-rich-open-source-code-visual-framework/), that was designed from the grounds up as an interactive coding tool, but well, it's 100 times better than the Sketch IDE and it's really enjoyable.

So assuming that you know nothing about IDEA, just like me, here is a step by step guide to coding fun:

**Step.1**

Download the IDEA, at launch, you can disable all plugins, none are relevant to Processing development.

Unfortunately it doesn't seem possible to download a version of IDEA without all that crap, nor uninstall the default plugins, but at least everything can be disabled. Note that more stuff can be removed if you use Configure/Plugins...


Configure/Settings/Keymap also allows to use Visual Studio's default keybindings, if you (like me) prefer that.

Unfortunately it doesn't seem possible to download a version of IDEA without all that crap, nor uninstall the default plugins, but at least everything can be disabled. Note that more stuff can be removed if you use Configure/Plugins...

Configure/Settings/Keymap also allows to use Visual Studio's default keybindings, if you (like me) prefer that.



**Step.2**

IntelliJ IDEA doesn't come with a JDK, and for some reason I can't just point the IDE to the JDK included with processing. You can either install a JDK or I found that PortableApps.com does have a portable version of the JDK, and I used that.

Note that not all directories seem to work for that, IDEA still complained when I had the portable JDK in my downloads folder for some reason, moving it to C:\ fixed the issue.

Note that not all directories seem to work for that, IDEA still complained when I had the portable JDK in my downloads folder for some reason, moving it to C:\ fixed the issue.

**Step.3**

Download

[Processing](http://www.processing.org/)and locate the core.jar library. There might be other jar files alongside it, most probably, you'll need them all... Note the directory where these live.

Now you have to add the Processing jar files. Select the project (view/tool windows/project) and right-click to "Open module settings". Here, under "Libraries" add the path where the Processing core.jar lives.

**Step.4**

IDEA should have created a Main.java file. Edit it with the following sample code:



import processing.core.PApplet;

import java.util.*;


import processing.data.*;


public class Main extends PApplet {


public static void main(String args[]) {

PApplet.main("Main");

}


@Override

public void settings() {

size(512, 512);

}


@Override

public void setup() {

}


@Override

public void draw() {

background(15);

}

}

import java.util.*;

import processing.data.*;

public static void main(String args[]) {

PApplet.main("Main");

}

@Override

public void settings() {

size(512, 512);

}

@Override

public void setup() {

}

@Override

public void draw() {

background(15);

}

}

**In general, converting Processing PDE code to plain java implies mostly sprinkling some "public" keywords in classes, as Processing PDE class members are all public by default (while Java aren't).**


Also, you might need to change double literals (e.g. 0.0) to floats (0.f), another difference between PDE and plain Java, this is actually quite annoying. Lastly Processing "color" type should be changed to a plain "int".



**Step.4**

Launch the debugger. Notice that every time you build the class/project, IDEA will prompt asking if you want to hot-reload, which should just work.


Have fun!



Have fun!

Here are the ooooold instructions, for Eclipse/Processing 2.x, if you prefer that one...

**Step.1**

Download the most tiny, stripped down version of Eclipse possible. This can be quite a challenge as Eclipse comes in many bloated flavors by default.

The tiniest of the prepackaged ones seems to be Eclipse Classic, that just includes all the Eclipse sources plus the CVS versioning plus the plugin development environment...

Luckily, there is a customization service run by Yoxos here:

[https://yoxos.eclipsesource.com/discover.html](https://yoxos.eclipsesource.com/discover.html), just select from the Components tab the "Eclipse Java Development Tools" and that should do the trick. It's "only" 85mb!**Note**: If you're not lazy like me you can read this and learn the

[Eclipse shortcuts](http://www.vogella.de/articles/EclipseShortcuts/article.html). Otherwise, include in the custom download also the C++ development platform. Now the package should be around 120mb, but you'll get the Visual Studio keybindings (preferences/general/keys)



**Step.2**

Download

[Processing](http://www.processing.org/)and locate the core.jar library. There might be other jar files alongside it, most probably, you'll need them all (in the current processing v2.1 you'll need core, jogl-all and jogl-natives-, gluegen-rt and gluegen-rt-natives-) In my case, being on OSX Processing comes packages in a nice .app structure, I used muCommander to extract the files I needed.**Step.3**

Run Eclipse and create a new Java project. Select the package you just created, right-click and select "Build Path/Configure Build Path/Libraries/Add External Jar" and select the Processing jar libraries. Then add a new class, named as the project and type something like this:

import processing.core.PApplet;

public class Test extends PApplet {


public void setup()

{

size(512,512,P3D);

}

public void draw()

{

background(0);

sphere(100);

}

}

public class Test extends PApplet {

public void setup()

{

size(512,512,P3D);

}

public void draw()

{

background(0);

sphere(100);

}

}



**Step.4**

Launch the debugger. Notice that every time you save the class, the processing window automatically refreshes. Have fun!

## 1 comment:

Post a Comment