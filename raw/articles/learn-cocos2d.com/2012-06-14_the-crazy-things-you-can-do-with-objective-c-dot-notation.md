---
title: The Crazy Things you can do with Objective-C Dot Notation
url: http://www.learn-cocos2d.com/2012/06/crazy-objectivec-dot-notation/
author: Kyle says
published: '2012-06-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Have a look at the following code example:

|
1 2 3 |
NSString* str1 = NSString.alloc.init; NSString* str2 = str1.copy; NSLog(@"str1: %@, str2: %@", str1.capitalizedString, str2.description); |

Did you find it strange somehow? Odd perhaps? Then you may be surprised to learn that this is perfectly valid Objective-C code. Go ahead and try it in your project. As long as the project is set to use the Apple LLVM Compiler this will work.


#### How dot notation works

The dot notation of the above example is equivalent to this code:

|
1 2 3 |
NSString* str1 = [[NSString alloc] init]; NSString* str2 = [str1 copy]; NSLog(@"str1: %@, str2: %@", [str1 capitalizedString], [str2 description]); |

As you can see, you can write any message sent to an object (ie init) and any message sent to a class (ie alloc) with dot notation, effectively treating the method like a readonly property. This is a feature of the Apple LLVM Compiler.

I’m not sure if this behavior it is documented or not, but it’s definitely a side-effect of Objective-C properties that are implemented more generically in the Apple LLVM compiler than they were in the LLVM GCC compiler. We’re now allowed to use dot notation for many methods. There are only two rules to consider.

The first rule is that dot notation does not generally work for all methods that receive parameters. For example you can’t use dot notation with initWithString: - that wouldn’t even work syntactically:

|
1 |
NSString* str1 = NSString.alloc.initWithString:@""; // Err, what? Bad Syntax. |

The second rule is that there are methods with parameters that are allowed to be used with dot notation - if that method is defined like a property setters and begins with “set” and the capitalized name of the property. That means the setter of “number” would have to be “setNumber” in order for you to assign a value to number using dot notation.

So if you have a class that defines this setNumber: method but number is not a @property of the class (nor @synthesize’d nor @dynamic), you can still use dot notation to assign a number:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
@interface MyClass : NSObject -(void) setNumber:(int)number; @end @implementation MyClass -(void) setNumber:(int)number { NSLog(@"number is: %i", number); } @end // in some other class MyClass* myClass = [[MyClass alloc] init]; myClass.number = 10; // allowed, even though number is not a property int number = myClass.number; // ERROR, no getter method for number in MyClass |

Effectively this makes number a write-only property of MyClass. That’s something that you can’t normally do with Objective-C properties. For good reason I might add, since if you can store a value in an object anyone would rightfully assume that it is valid to read the value as well.

#### Where dot notation fails unexpectedly

One case I mentioned just above, although I haven’t encountered one yet there’s a slim chance you might run into the occasional write-only property. The compiler will give you a “Expected getter method not found on object of type …” error in that case.

There are also some rare exceptions that really should work, but don’t. For example this is one I encountered:

|
1 2 |
Class c1 = str1.class; // ERROR Class c2 = str1.superclass; // works fine |

For some reason using dot notation with the class message spits out a “Expected unqualified-id” error. This is likely because class is a reserved keyword, and Xcode actually highlights class in the same color as @interface, return, self or super.

My guess is that technically it would work on the compiler-level, but the parser says “no, no, that can’t be right, class is a reserved keyword”.

#### When to use dot notation

I’m not suggesting that you use dot notation everywhere you can. I’m aware this is a highly subjective issue, since at the machine code level both [str1 copy] and str1.copy will generate the exact same instructions. They’re virtually identical, so it boils down to a matter of preference regarding code style.

My recommendation is to use dot notation wherever the message name indicates that it is some kind of a passive property of the object rather than running complex code. Methods like capitalizedString, length, count, intValue, hash, description, lastPathComponent, isAbsolutePath are all great examples of should-be-properties.

I do agree with you if you find the following rather odd:

|
1 |
NSString* str = NSString.alloc.init; // odd, avoid doing this |

I could get used to it but I wouldn’t recommend using dot notation for object allocation and init because in many cases you will be using some variant of initWithXXX. So then that would become a mixture of dot notation and old-school messaging:

|
1 |
NSString* str = [NSString.alloc initWithString:@"x"]; // YIKES! |

Where I can recommend to use dot notation indiscriminately is with singletons. Consider this:

|
1 2 3 4 5 |
CCDirector* director = [CCDirector sharedDirector]; CCDirector* director = CCDirector.sharedDirector; NSFileManager* fm = [NSFileManager defaultManager]; NSFileManager* fm = NSFileManager.defaultManager; |

Dot notation makes working with singletons less brackety and I think more natural, too:

|
1 2 3 4 |
CCDirector.sharedDirector.animationInterval = 1.0 / 60.0; CCDirector.sharedDirector.displayStats = YES; if (KKInput.sharedInput.touchesAvailable) {..} NSLog(@"%@", UIDevice.currentDevice.name); |

#### Why dot notation is preferable

Unless you’ve been programming objectively for many years, it shouldn’t be too hard to let go of some of those square brackets. Personally after 3 years of working with Objective-C I’ve totally become accustomed to using square brackets. However they do get in the way frequently, especially when Xcode messes things up.

A typical example revolves around writing a line of code, adding a square bracket at the end, only to realize that Xcode added the opening bracket to the wrong statement. Typically Xcode adds brackets at the beginning of the line:

|
1 2 3 4 5 6 7 8 9 10 11 |
// what I wrote: [label setString:message capitalizedString]; // what Xcode thinks I wanted after adding a second square bracket at the end: [[label setString:message capitalizedString] ]; // what I really wanted: [label setString:[message capitalizedString]]; // how dot notation makes ugly crap like this totally natural: label.string = message.capitalizedString; |

#### How dot notation can make your code more readable

In some cases dot notation can make previously mixed dot notation and bracketed lines of code to uniformly dot notated code, which I think is a lot better to the eyes:

|
1 2 3 4 5 6 7 8 9 |
// previously on We Love Brackets: int width = [node.parent texture].contentSize.width; // or some variation thereof, like: int width = [[node.parent texture] contentSize].width; int width = [[node parent] texture].contentSize.width; int width = [[[node parent] texture] contentSize].width; // … and now the conclusion: int width = node.parent.texture.contentSize.width; |

Ah, what a relief! Go ahead and try it yourself. Dot-notate the crap out of Objective-C, I dare you!

#### Dot notation for non-properties considered a blessing!

Dot notation is shorter, less noisy on the eyes, and can be applied more consistently if you’re working with C structs frequently (ie CGPoint, CGSize, etc.).

Moreover - at least for european users - the dot is a single key on the keyboard whereas either square bracket requires to hold down a modifier key while typing it. And if you’re anything like me (ie human), then you’ll know the pain associated with accidentally typing { and Xcode autocompleting that with a closing } or some other autocompletion “Not no, dammit!” insults.

I definitely see a great appeal to this for programmers new to Objective-C (specifically with C# or Java backgrounds), as they don’t need to expose themselves to “weird square brackets” just as often as has been the case in the past years. This should make transitioning easier.

What do you think about dot notation? Are you going to adopt it, or stick with square brackets?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Awesome article, very enlightening!

I was actually doing some of this for singletons without realizing it, although I made the mistake of blending old and dot notations such as:

[MyObject sharedInstance].property

I’m not sure why I never put it together that you could do the whole thing in dots.

For me, there’s a big difference between the dot notation and square brackets!

Dot notation is for accessing a value or a method while square brackets are specific in Obj-C for sending messages.

If you start using dot notation everywhere, you’ll start mixing between calling functions and settings values. Please correct me if I’m wrong 😉

Will do. You’re wrong. 😉

int i = object.property;

is the same as

int i = [object property];

Accessing a property sends a message to the property getter. And assigning a value sends a message to the property setter:

object.property = 10;

is equivalent to

[object setProperty:10];

The only difference between the two variants is syntactical. Technically they both do the exact same thing. The interesting part is that for dot notation to work you no longer have to have declared the getter and setter as a @property.

I could understand you if you followed the unspoken rule of never having side effects in property accessors. I.e. if your properties never contain any more code than “return i-var” and “if (ivar != argument) ivar = argument”, effectively.

With following that rule, you could then use the dot notation only for accessing such properties, and it would help documenting your code in the way: “this invocation only sets or read an i-var, nothing more”. Then, yes, your argument is valid.

However, most code I’ve seen doesn’t follow this rather clear rule and employs side effects in properties freely. Then your distinction isn’t helpful any more, since the property accessors behave like any other custom-written method, and so there’s no use in using dot notation for one and messaging for the other type.

After the first few lines I thought: Boooring! Been there, done that.

But the further I looked down the more I liked your article.

You discuss all the various possibilities well, and it opened my eyes to a few cases that I had not considered before.

Danke, Steffen!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Great article. I did not realized such thing can be done in Obj-C

Why I don’t use dot for singletons — it breaks intellisense, and auto-complete is a must for me. At least this is true for Xcode 4.2, have they fixed it since?

Never knew you have to type square brackets with a modifier key. I type in US keyboard exclusively and don’t have this issue. If I switch to Russian keyboard then I do not have square brackets at all!

Good point. I just tried it with Xcode 4.3.3 and typing CCDirector.sharedDirector does not offer sharedDirector in autocompletion. But once you’ve typed that it does offer the director properties for autocompletion, like displayStats or animationInterval.

On most european keyboards the square brackets are on the 8 and 9 keys, and you have to hold down Control or Alt (not sure which is which because I’m using a windows keyboard with remapped Cmd, Alt, Ctrl buttons). On Windows systems you have to press AltGr+8 and AltGr+9. Interestingly on a german wireless Mac keyboard the [ and ] characters aren’t even printed on the keys.

Wow, this really different!

I’m a little afraid of the C++ look of it. I’ve spent time learning Objective C and never really liked the bracket syntax. Years of C and C++ make the brackets look wrong to me. Now I fear I’ll start doing this and mis-use the language. I’ll be very interested to hear of any long term pitfalls that may come to light

Dot notation is meant for properties. So it’s perfectly fine to use it as a shortcut to a method that returns a property (a noun). However, never use it for a method that describes an action (a verb). I think this is what you meant when you referred to the do’s and don’ts. It’s not a matter of underlying complexity, but a matter of semantics. Design deals with semantics. It doesn’t care about computing complexity.

In short:

alloc = a verb -> no no

init = a verb -> no no

copy = a verb -> no no

capitalizedString = a noun -> yeah!

description = a noun -> yeah!

Good point!

While I am very inclined to agree with you also, alloc and init feels pretty good in practice compared to the nested brackets approach typically recommended.

Since both return a Related Return Type (instanceType), we could assume them to return a “noun” of sorts. Ok I’m pushing I know but I like the idea of Class.alloc.init returning a standard object and saving the extra brackets in a call to [Class.alloc initWithGoodies:goodStuff]. Looks cleaner than [[Class alloc] initWithGoodies:goodStuff] to me.

I love objective c but I have to add that I have no Smalltalk experience, so maybe I’ve been tainted by the Java and C# approach over the years. I’m pretty satisfied though with brackets and have fully adjusted to this style of messaging.

I would venture to go further with this! How about instances where we may use convienience constructors as in:

NSString* text = NSString.string;

Is this a terrible idea?

One other crazy thing you could (but not want to) do is using block properties instead of methods declaration / implementation. F.e. having a block property and assign it like this:

self.sum = ^(int a, int b) { return a + b; };

Then I’m able to use dot-notation:

int res = self.sum(1, 2);

and getting rid of square brackets syntax. Terrible, isn’t it?

That is![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


crazy!Evil genius.

My God, tons of unreadable code will appear very soon.

Valeriy, this should make for more readable code, as it is an increase in self documenting.

[[myObject randomName] somethingSomething];

vs

[myObject.randomName somethingSomething];

The latter distinguishes in code the difference in concept between the two methods. The former gives no distinction, and relies on you already knowing what the distinction is.

One counterargument is that there should be no conceptual difference between the two methods from the perspective of a caller. In other words, one shouldn’t know or care whether or not -randomName is just a getter that returns an internal variable, because that’s an implementation detail of the class.

I have mixed feelings about dot syntax because of that exposure of class details.