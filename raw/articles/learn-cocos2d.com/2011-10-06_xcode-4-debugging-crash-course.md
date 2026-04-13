---
title: Xcode 4 Debugging Crash-Course
url: http://www.learn-cocos2d.com/2011/10/xcode-4-debugging-crashcourse/
author: Josh Jones says
published: '2011-10-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

What do you do if your app doesn’t behave as it should, or even crashes?

**Answer A: **Post your problem in just about every programming forum.

**Answer B: **Use the Xcode Debugger to analyze what’s going wrong.

Since most of you already know how to do **A** I’ll focus on **B** in this Xcode 4 Debugging Crash-Course. It’s kind of aimed at beginning Xcode developers but that’s just because I hope - against better knowledge - that experienced developers already know that … thing … that debugger stuff. Ya know?


### A very bad program. Bad, bad program!

Here’s a very simple program with a nasty bug. It’s written with Cocos2D but don’t let that scare you off, what you’ll learn is applicable to any Xcode app and any 3rd party frameworks you may be using.

The goal is to have the "Moving Upward" label continuously move upwards starting at the very bottom. However, the label is not moving at all, and it is positioned strangely about one third of the way up. What’s going on? Can you spot the bug right away?

-(id) init

{

if ((self = [super init]))

{

glClearColor(0.1f, 0.4f, 0.2f, 1.0f);

label = [CCLabelTTF labelWithString:@”Moving Upward”

fontName:@”Marker Felt” fontSize:48];

CGSize size = [[CCDirector sharedDirector] winSize];

label.position = CGPointMake(size.width / 2, 0);

[self addChild:label];

[self scheduleUpdate];

}

return self;

}

-(void) addLabelOffset:(CGPoint)offset

{

label.position = CGPointMake(label.position.x + offset.x,

label.position.x + offset.y);

}

-(void) update:(ccTime)delta

{

CGPoint offset = CGPointMake(0, 1);

[self addLabelOffset:offset];

}

[/cc]

Here’s the output, instead of a moving label we get one that’s forever stuck at a position we very certainly didn’t set (y position was set to 0). How can this be? So many questions …

![wpid3618-media_1317761205745.png](../../../wordpress/wp-content/uploads/wpid3618-media_1317761205745.png)

You could just stare at the code for hours, and run and re-run it. Maybe make some random changes that you think might bring about the solution. It hardly ever works that way.

You can also blame others, but that’s not going to help anyone, even though it may be your first reaction. It’s quite normal even, because you want to do one thing (move the label) and get something else (a bug). You have to come to terms that programming is a lot about making mistakes and learning from them.

You might also give it a shot and ask about this bug in a forum, but the usual support places are riddled with questions that scream "please do your due diligence first, thank you". Meaning there are a lot of code bug related questions on the Internet that are asked solely because the programmer didn’t know the basics of debugging.

A lot more people are becoming programmers these days, and no one really wants to be bothered with the "techy stuff" like debugging it seems. Debugging code sounds like fancy-pantsy geeky stuff only experts can do, right? Wrong!

### One step closer: Set a Breakpoint!

![wpid3619-media_1317762871211.png](../../../wordpress/wp-content/uploads/wpid3619-media_1317762871211.png)

The first order of business is setting breakpoints. A breakpoint is a little stop sign for the debugger that tells it to stop the execution of the running app in order for you to be able to analyze the code while it is running, with your normal human pace.

You can set a breakpoint in Xcode by clicking on the bar to the left of the text editor view. A blue bar indicates that execution will stop at this line. You can set a breakpoint before running the app or even when it is already running. You will also frequently add and remove breakpoints as you step through your code and learn more about what’s going on.

If you click the blue bar again you’ll notice it will become transparent, indicating that the breakpoint is currently disabled. You can see a list of all breakpoints in the **Breakpoint Navigator** pane (View -> Navigators -> Show Breakpoint Navigator, Hotkey: Command+6).

### Breakpoint not hit?

If your breakpoint doesn’t cause the app to stop execution (in geek terms the "breakpoint wasn’t hit"), it means that the code with your breakpoint is not executed (geek term: "never reached"). A lot of bugs result in methods not being called, and setting a breakpoint in the method is a very simple and sure way of finding out whether the method is called or not.

If your app doesn’t stop despite the breakpoint being set at the correct place … well:

What you do if your breakpoint isn’t hit is to look at the code calling the method. Set a breakpoint there and see if that gets hit. From there you can progress with the instructions below.

### Break! Halt! Stop! Or I’ll shoot!

![media_1317769887651.png](../../../wordpress/wp-content/uploads/media_1317769887651.png)

Luckily for us, in the above screenshot the pale green line indicates that execution halted at the breakpoint. Now what?

### Single-Stepping Through Code

![media_1317770011425.png](../../../wordpress/wp-content/uploads/media_1317770011425.png)

Notice the floating numbers 1-4 below the icons in the screenshot above? They are the execution controls:

1) **Continue** (pause) program execution

2) **Step Over** (Hotkey: F6)

3) **Step Into** (Hotkey: F7)

4) **Step Out** (Hotkey: F8)

These four buttons allow you to control how the program continues execution after it hit a breakpoint.

If you press **Continue** (1), the program will run again until it hits another (or the same) breakpoint. You normally use that to quickly advance to the next breakpoint, or end your debugging-with-breakpoints session. While the program is running, it’s a **Pause** button that allows you to halt the execution at any time. **Pause** is rarely needed and mostly only useful to halt the app to inspect the contents of the screen, rather than looking at the code.

With **Step Over** (2) you can continue execution line-by-line. Let’s try that.

### Step Over

![wpid3620-media_1317763163346.png](../../../wordpress/wp-content/uploads/wpid3620-media_1317763163346.png)

After pressing **Step Over** (2) the current line indicator moved one line. The CGPoint offset was assigned the values of the call to CGPointMake.

Now if you would press **Step Over** again, the code in **addLabelOffset** will be executed but you don’t get to follow the execution inside the **addLabelOffset** method.

That is what the **Step Into** (3) button is for: it allows you to "step into" the execution of the next method/function. Press **Step Into** now and the line of execution will be in the **addLabelOffset** method:

### Step Into

![wpid3621-media_1317763304038.png](../../../wordpress/wp-content/uploads/wpid3621-media_1317763304038.png)

Great!

If you ever wanted to leave a method, even though there’s still a lot of code ahead, you can always press **Step Out** (4) to leave the method the execution pointer is currently in and continue at the next line from where the current method was called. We don’t need that right now but its handy if you accidentally stepped into the wrong method, or find that the current method isn’t holding the key to revealing the bug you’re trying to nail down.

Now that we’re at the place where the label’s position is clearly updated. But how do we find out what’s going wrong?

### The Debug View

![media_1317770600530.png](../../../wordpress/wp-content/uploads/media_1317770600530.png)

Whenever Xcode halts execution due to a breakpoint (or other execution-halting events), it will open the Debug View at the bottom.

The Debug View hosts the variables view and the debug output view (known as the Debug Console). With the three controls in the top right corner you can toggle the individual views on or off. Right now it is set to show both panes in a split view.

The debug output is where the output of the CCLOG(..) and NSLog(..) functions is shown. Many times, in particular if exceptions or assertions occur you’ll be able to find hints as to what caused the error at the end of the debug output.

Note that exceptions and assertions are commonly but incorrectly referred to as crashes. From the perspective of a programmer a crash is an unhandled error that forced the app to stop running, for example when the memory of an object was overwritten by a buffer overflow. Exceptions and assertions are not crashes in the same sense because the programmer willfully stated that if a certain condition occurs, the app should stop running, and do so gracefully. Although admittedly the latter part can be quite subjective.

Right now we’re more interested in finding out what actually happens to the label’s position. The Debug View to inspect variables is to the left, so let’s have a look what we can find there.

### Inspecting Variables

![wpid3622-media_1317764373553.png](../../../wordpress/wp-content/uploads/wpid3622-media_1317764373553.png)

The left half of the debug view (red box in the screenshot) contains a list of variables, including **self**. Since **label** is an instance variable of the current class, it should be in **self**. Click the arrow to expand **self**.

![wpid3623-media_1317764667619.png](../../../wordpress/wp-content/uploads/wpid3623-media_1317764667619.png)

So there’s the **label**! But I don’t see a position, just a bunch of font related properties…

In cases like these you’ll have to dig deeper. The label variable is an instance of the **CCLabelTTF** class, which inherits from **CCSprite** which in turn inherits from **CCNode** and finally **NSObject**.

You’ll notice that the label variable contains a reference to CCSprite as the first entry. This is where the super classes are listed, and you’ll just have to open them until you find the property you’re looking for.

![wpid3624-media_1317765064697.png](../../../wordpress/wp-content/uploads/wpid3624-media_1317765064697.png)

There we go! Position is a property of the CCNode class. Notice that it’s called **position_** with an underscore at the end. This is just the internal name of the property, a lot of the Cocos2D code [suffixes internal variable names with an underscore](http://stackoverflow.com/questions/5679775/preferred-way-to-name-instance-variable-in-objective-c) while the public property is named position.

Note that the underscore thing is just a naming convention that Cocos2D follows. Other frameworks will follow other guidelines, ie. I prefer not to use any prefixes in [Kobold2D](http://www.kobold2d.com/) for class instance variables. Mostly because you end up code-completing the wrong name because the variabe suffixed with an underscore is identical to the last character, and you don’t have to deal with two different names for the same variable.

As you can see in the screenshot, the initial position of the label is (160, 0). This is the position we assigned in the init method:

**label**.position = CGPointMake(size.width / 2, 0);

So that seems to be correct. Let’s see what happens when we **Step Over** (Hotkey: F6).

![wpid3625-media_1317765171219.png](../../../wordpress/wp-content/uploads/wpid3625-media_1317765171219.png)

Notice how the **position.y** value has been highlighted in blue. This indicates that the value has changed since the last time you used **Step Over**. Since the offset (0, 1) we were adding added zero to the x position, it remained unchanged.

The question is: why did the y position change from 0 to 161 when all we did was add 1? This can only happen if the value we add 1 to is already 160 to begin with … hey, wait a minute …

![wpid3626-media_1317765377680.png](../../../wordpress/wp-content/uploads/wpid3626-media_1317765377680.png)

Stupid typo! We were adding **label.position.x **instead of **label.position.y**. This is easily fixed, the debugger just saved your soul and sanity!

### Don’t hesitate to Step Into!

Here’s another great tip if you’re using an open source framework such as Cocos2D.

For example, if you create a sprite with an image file and it won’t display on screen, it might make sense to step into the CCSprite code that creates a sprite, and inspect both the flow of execution and the variables there.

By going through code line by line it’s not only easier to understand, you’ll also learn more about its inner secrets, which give you clues as to why your code isn’t working the way it’s supposed to be. For example, you might find out that the image file name apparently doesn’t exist in your bundle, so the texture wasn’t created and the sprite ended up returning nil.

### Debugging EXC_BAD_ACCESS

Assume it’s 4 am in the morning. You’re still coding, making the final tweak to your awesome app. Of course you are sleep deprived, ignored all the warnings (literally) and just wrote the stupidest line of code ever. You just don’t know it yet, only after you woke up in the morning (ahem, evening) and re-ran your app it …

**BOOM - it crashes!! All the time!!! With EXC_BAD_ACCESS - the worst kind of crash! OMG?? WTF?!?!?**

![wpid3627-media_1317766056587.png](../../../wordpress/wp-content/uploads/wpid3627-media_1317766056587.png)

**No, no, no, no, no, no, nooooo!!! This worked yesterday, why does it crash now???**

Calm down! Really, seriously, I mean it. Whenever your app crashes, and I know it’s frustrating as hell, get your emotions under control!

The more frustrated and angered you are, the longer it takes to actually find and fix a bug! Trust me, this is something you’ll (hopefully don’t have to) learn from experience. But it’s a long way until you reach a Zen-like state where not even the worst, unexplicable, most badly timed crash can affect your cool. I bet that 99.9997% of all programmers never reach that state. But you should aim to get above the 80% level.

**Tip:** 99% of the bugs you’ll encounter in your life as programmer are caused by you. There’s a [humbling lesson to be learned](http://www.codinghorror.com/blog/2004/08/why-im-the-best-programmer-in-the-world.html)!

So what are our options here?

Clearly EXC_BAD_ACCESS means there’s something horribly wrong. In almost all cases this means that you’re trying to call a method or access a property of an object which has gone out of scope, which was released, or whose memory was otherwise mangled. And the Debug Console is no help either - usually there’s some kind of error message printed in the last couple lines of the log, but not so when there’s an EXC_BAD_ACCESS due to pointer corruption.

Let’s see if variable inspection is able to tells us more …

![wpid3628-media_1317766298106.png](../../../wordpress/wp-content/uploads/wpid3628-media_1317766298106.png)

Ouch! What happened to the label’s properties? They don’t have any value at all, the CGPoints seemingly being empty. Strange.

![wpid3629-media_1317766441007.png](../../../wordpress/wp-content/uploads/wpid3629-media_1317766441007.png)

Very odd is the memory address, which is 0x64 hexadecimal. That equals 100 in decimal. That’s not a valid object pointer!

The hex number printed after objects is their memory address, where they store the data contained in the object. You know the pointer is invalid whenever you see a number that’s not even closely resembling a valid pointer address. Like the nil pointer (0x0), an obvious pattern (0xdededede) or merely a value that’s too small to be a valid pointer memory address (0x64 - in general any value that doesn’t have at least 6 hex digits).

**Tip:** setting the environment variable [NSZombieEnabled](http://stackoverflow.com/questions/1211923/how-to-use-nszombie-in-xcode) is particularly useful to hunt down persistent EXC_BAD_ACCESS.

### The Callstack

Let’s assume for a second that we’re in no position to judge where the hell the label pointer could have been mangled with, even though there’s only two methods in this project.

In cases like these, we need to have a look at the callstack. The callstack is simply a list of function calls that were made to get to the current line of code. Every time a method is called, it is pushed onto the callstack. Every time a method finishes execution and returns, it is popped from the call stack.

The callstack is the footprint of how execution arrived at the point where it is now. You can see the callstack in the **Debug Navigator **pane (View -> Navigators -> Show Debug Navigator, Hotkey: Command + 5). Normally Xcode will open the **Debug Navigator** pane automatically when a breakpoint is hit or the program aborted, as in this case.

![wpid3630-media_1317766902570.png](../../../wordpress/wp-content/uploads/wpid3630-media_1317766902570.png)

The highlighted line is where execution stopped. The methods at level 2 and lower represent the flow of execution. The **CCDirectorIOS drawScene** method called **CCScheduler tick** which in turn called **HelloWorldLayer update** and that, as we know, calls **HelloWorldLayer addLabelOffset**. So far so good.

You can click on any of the methods in the callstack to see its source code, if available. If an entry in the callstack is displayed in gray, then there’s no source code for this method available, you’ll only see the machine code instructions (assembler). Let’s not go there, in fact you can fix about any code problem without ever having to step into assembler code - unless you want to be a pirate. Arrrrr!

Just for kicks click on the HelloWorldLayer update method to reveal its code:

![wpid3631-media_1317767190324.png](../../../wordpress/wp-content/uploads/wpid3631-media_1317767190324.png)

Clicking through the callstack to see where you’re coming from can be helpful to analyse the flow of execution. In many cases the problem isn’t in the method that crashes, it’s one of the enclosing methods further down in the callstack. In this case I made it simple enough to see the problem.

Hint: there’s a warning …

![wpid3632-media_1317767339719.png](../../../wordpress/wp-content/uploads/wpid3632-media_1317767339719.png)

Oh my, how could … ???

In your sleep deprived state you created a variable "nils" which is suspiciously similarly named to "nil". Alas, you assigned nils to the label and blatantly ignored the warning. Let alone the statement makes no sense.

**Pro Tip:** don’t code when sleep deprived, drunk, preoccupied, distracted or otherwise not fully focused on the task at hand. Also, disregard what I’m saying, I have no idea what I’m talking about! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)



### Tip: Write Readable Code

Quite frankly weird bugs like the one above is just something that happens occassionally. No one can be 100% focused on the programming task all the time. That’s why we write buggy apps. That’s why we have compilers and debuggers to help us fix our own occassional incompetence.

But most importantly we can make our lives easier by [writing readable code for people](http://www.fileinview.com/chms/Code%20Complete,%202nd%20Edition/0735619670/ch34lev1sec3.html) (even if those people remain largely imaginary). It does help debugging. In particular I try to avoid cramming multiple method calls into a single line like this:

**BOOL result = [self checkThatWithString:[self getStringFromValue:[object getValue]] location:[touch locationInView:[CCDirector sharedDirector].openGLView]];**

Instead, it is much more readable, requires only little more writing, and doesn’t slow down anything because the compiler does exactly this stuff behind the scenes anyway:

**NSString* string = [self getStringFromValue:[object getValue]];**

**CGPoint location = [touch locationInView:[CCDirector sharedDirector].openGLView];**

**BOOL result = [self checkThatWithString:string location:location];**

### Tip: Write Warning-Free Code

![wpid3633-media_1317767557320.png](../../../wordpress/wp-content/uploads/wpid3633-media_1317767557320.png)

There’s a good reasons why warnings exist: they remind you of potentially dangerous code. They’re not obnoxious yellow banners to be ignored. Writing warning-free code is a [highly recommended best practice](http://www.artima.com/cppsource/codestandards.html), and while it can be a little annoying at times it can save you a lot of trouble down the road by actually forcing you to fix the warnings.

The previous crash wouldn’t have happened if you had actually looked at the warning, understood what it meant, and fixed it. It could have saved you the time to debug the problem, let alone the anger and frustration it caused just because your app was acting up rather unexpectedly.

By turning all warnings into errors you’re forced to learn why these warnings exist in the first place, because you need to understand them to be able to fix them. Once you know what causes a warning, it becomes second nature to write the correct code in the first place.

Writing warning free code is an essential part of learning to program. Warnings are like little reminders: hey, learn why I exist or else I’ll kick you in the rear when you’ll least expect it: there **will** be a test!

### Summary

I hope you enjoyed this introduction to debugging with Xcode 4! There’s a lot more to debugging but armed with this basic knowledge you’ll be able to get to the bottom of most issues. In fact, I rarely use any other debugging techniques than those described above: setting breakpoints, stepping through code, analyzing variables, skimming through the debug output, walking the callstack up and down.

The only thing that’s not so easy is finding the right places to set breakpoints, when to use logging and when to step through the code. This only comes with experience. So you’d better start using that Xcode debugger now! Have fun!

If you liked this article or think it will be useful for your friends please don’t hesitate to tweet, like or plus-one it. Thank you!


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Great post, and also very detailed!

I expect this to be a item to be searched for in the not too distant future. Also, “treat warnings as errors” has saved my butt more times than I can count!

Only wanna say that this is a very useful and interesting post, man, detailed and even funny, jaja! I think I’ll start using variable names like “whiles”, “fors”, “breaks”, etc.

Excellent!!! Has a lot of good information and answered some some questions I had.

Is the sample app (with bugs) on the githubs anywhere? would be great to load into Xcode and play along with the article?

Apparently I forgot that. The project is now linked at the end of the article.

Thanks for this useful informations

A french developer

One tip I recently figured out is that if you are writing a static library and your main app and you want to break on code in the static library you can use the brackpoints view in Xcode while looking at the static library. Right-click on the breakpoint in the static library and say “move to” and select “User” and it will then apply when running the application.

Just plain simple awesomeness. Thanks for saving me a million headaches. -jc

Thanks Dad. Very useful info!