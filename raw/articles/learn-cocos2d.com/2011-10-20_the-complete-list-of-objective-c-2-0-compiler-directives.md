---
title: The Complete List of Objective-C 2.0 @ Compiler Directives
url: http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/
author: 那些被遗漏的Objective-C保留字; 我的Ios支持平台 Says
published: '2011-10-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I haven’t been able to find a list of all Objective-C **@** compiler directives in one place. We all know the keywords like **@interface** and **@implementation** but others like **@dynamic** and **@encode** are lesser known, and possibly even much less understood.

Although I know most of them already, I couldn’t shake the feeling that I may be missing a hidden gem. So I made an effort to document all the Objective-C @ compiler directives in one place.

[@class](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#class)[@defs](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#defs)[@protocol @required @optional @end](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#protocol)[@interface @public @package @protected @private @property @end](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#interface)[@implementation @synthesize @dynamic @end](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#implementation)[@throw @try @catch @finally](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#throw)[@synchronized](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#synchronized)[@autoreleasepool](http://www.learn-cocos2d.com#autoreleasepool)[@selector](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#selector)[@encode](http://www.learn-cocos2d.com#encode)[@compatibility_alias](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#compatibility_alias)[@”string”](http://www.learn-cocos2d.com/2011/10/complete-list-objectivec-20-compiler-directives/#string)


##### @class

Used for [class forward declarations](http://stackoverflow.com/questions/5191487/objective-c-forward-class-declaration). Declares class as known without having to import the class’ header file.

[cc lang=”c”]

@class ClassName;

[/cc]

Note, unlike with [ @protocol](http://www.learn-cocos2d.com#protocol) and

[you can](http://www.learn-cocos2d.com#selector)

**@selector***not*write the following to get the Class object by name:

[cc lang=”cpp”]

// ERROR: this doesn’t work!

Class c = @class(ClassName);[/cc]

Instead use: [cc lang=”cpp”]Class c = [ClassName class];[/cc]

##### @defs

The @defs directive returns the layout of an Objective-C class, it allows you to create a C struct with the same layout as the Objective-C class. If you don’t know yet, Objective-C classes are basically just C structs with additional methods. Makes sense if you consider that Objective-C is merely a set of extensions to the C language.

[cc lang=”c”]

struct { @defs( NSObject) }

[/cc]

You will only ever need @defs for some hardcore, low-level Objective-C operations or optimizations, [as in this article which speeds up Objective-C message sends](http://www.mulle-kybernetik.com/artikel/Optimization/opti-3-imp-deluxe.html).

##### @protocol @required @optional @end

Marks the start of a protocol declaration. A **@protocol** can optionally declare that it must conform to other protocols.

[cc lang=”c”]

@protocol ProtocolName

@required

// method declarations

@optional

// method declarations

@end

[/cc]

Like with [ @selector](http://www.learn-cocos2d.com#selector) you can use

**@protocol**to get a protocol object by name:

[cc lang=”c”]

-(void) aMethod

{

Protocol *aProtocol = @protocol(ProtocolName);

}

[/cc]

**Dependent Directives:**

**@required**(default) - Declares the methods following the**@required**directive as required (default).**@optional**- Declares the methods following the**@optional**directive as optional. Classes implementing this protocol can decide whether to implement an optional method or not. Classes making use of the protocol must test optional protocol methods for existence. For example: [cc lang=”c”][object respondsToSelector:@selector(optionalProtocolMethod)];[/cc]**@end**- Marks the end of the protocol declaration.

##### @interface @public @package @protected @private @property @end

Marks the start of a class or category declaration.

**Class declaration:**

While SuperClassName is optional, Objective-C classes should derive from [NSObject](http://developer.apple.com/library/ios/#documentation/Cocoa/Reference/Foundation/Classes/NSObject_Class/Reference/Reference.html) either directly or indirectly. The **@interface** for a class declaration can optionally declare that it conforms to other protocols.

[cc lang=”c”]

@interface ClassName : SuperClassName

{

@public

// instance variables

@package

// instance variables

@protected

// instance variables

@private

// instance variables

}

// property declarations

@property (atomic, readwrite, assign) id aProperty;

// public instance and/or class method declarations

@end

[/cc]

**Category declaration:**

The **@interface** of a Objective-C category can not add instance variables. But it can optionally declare to conform to (additional) protocols. [CategoryName can be omitted](http://stackoverflow.com/questions/172598/best-way-to-define-private-methods-for-a-class-in-objective-c/651852#651852) (leaving only the empty brackets) if the category is added to the implementation file of the class that it extends, in order to declare methods as “private”.

[cc lang=”c”]

@interface ClassName (CategoryName)

// property declarations

@property (atomic, readwrite, assign) id aProperty;

// method declarations

@end

[/cc]

**Dependent Directives:**

**@public**- Declares the instance variables following the**@public**directive as publicly accessible. Public instance variables can be read and modified with pointer notation: [cc lang=”cpp”]someObject->aPublicVariable = 10;[/cc]**@package**- Declares the instance variables following the**@package**directive as[public inside the framework that defined the class, but private outside the framework](http://developer.apple.com/library/mac/#releasenotes/Cocoa/RN-ObjectiveC/_index.html#//apple_ref/doc/uid/TP40004309-CH1-DontLinkElementID_7). This applies only to 64-bit systems, on 32-bit systems**@package**has the same meaning as**@public**.**@protected**(default) - Declares the instance variables following the**@protected**directive as accessible only to the class and its derived classes.**@private**- Declares the instance variables following the**@private**directive as private to the class. Not even derived classes can access private instance variables.**@property**- Declares a property which can be accessed with dot notation. The**@property**can be followed by optional brackets within which special keywords (property modifiers) specify the exact behavior of the property. The property modifiers are:**readwrite**(default),**readonly**- Generate both setter & getter methods (readwrite), or only the getter method (readonly).**assign**(default),**retain**,**copy**- Only applicable for properties that can be safely cast to**id**. Assign simply assigns the passed value - retain sends**release**to the existing instance variable, sends**retain**to the new object, assigns the retained object to the instance variable - copy sends**release**to the existing instance variable, sends**copy**to the new object, assigns the copied object to the instance variable. In the latter two cases[you are still responsible for sending release](http://stackoverflow.com/questions/1820584/releasing-propertycopy-instance-variables)(or assigning**nil**) to the property on dealloc.**atomic**(default),**nonatomic**- Atomic properties are thread-safe, nonatomic properties are prone to synchronization issues if accessed from multiple threads. Nonatomic property access is faster than atomic and often used in single-threaded apps, or in cases where you’re absolutely sure the property will only be accessed from one thread.**weak**(default),**strong**- Available if[automatic reference counting](http://developer.apple.com/library/ios/#releasenotes/ObjectiveC/RN-TransitioningToARC/_index.html)(ARC) is enabled. The keyword**strong**is synonymous to**retain**, while**weak**is synonymous to**assign**, except that a**weak**property is automatically set to nil should the instance be deallocated. Note that**weak**is only available in iOS 5 or newer and Mac OS X 10.7 (Lion) or newer.**@end**- Marks the end of the interface declaration.

##### @implementation @synthesize @dynamic @end

Marks the start of a class’ or category implementation.

**Class implementation:**

[cc lang=”c”]

@implementation ClassName

@synthesize aProperty, bProperty;

@synthesize cProperty=instanceVariableName;

@dynamic anotherProperty;

// method implementations

@end

[/cc]

**Category implementation:**

[cc lang=”c”]

@implementation ClassName (CategoryName)

@synthesize aProperty, bProperty;

@synthesize cProperty=instanceVariableName;

@dynamic anotherProperty, bnotherProperty;

// method implementations

@end

[/cc]

**Dependent Directives:**

**@synthesize**- Instruct compiler to automatically generate property setter and getter methods for the given (comma seperated list of) properties. The setter and getter methods are generated according to the property modifiers. If the instance variable is not named exactly like the**@property**, you can specify the instance variable name following the equals sign.**@dynamic**- Tells the compiler that the necessary setter and getter methods for the given (comma seperated list of) properties will be implemented manually, or dynamically at runtime. Accessing a dynamic property will not generate a compiler warning, even if the getter/setter is not (yet) implemented. You will want to use**@dynamic**in cases where property getter and setter methods need to perform custom code.**@end**- Marks the end of the implementation of the class.

##### @throw @try @catch @finally

Used for [handling and throwing exceptions](http://developer.apple.com/library/mac/#documentation/cocoa/conceptual/ObjectiveC/Chapters/ocExceptionHandling.html).

**Throwing and Handling exceptions:**

[cc lang=”c”]

@try

{

// code that might throw an exception … like this one:

NSException *exception =

[NSException exceptionWithName:@”ExampleException”

reason:@”In your face!”

userInfo:nil];

@throw exception;

}

@catch (CustomException *ce)

{

// CustomException-specific handling …

}

@catch (NSException *ne)

{

// generic NSException handling …

// to simply re-throw the caught exception in a catch block:

@throw;

}

@finally

{

// code that runs whether an exception occurred or not …

}

[/cc]

##### @synchronized

Encapsulates code in a [mutex lock](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/Multithreading/ThreadSafety/ThreadSafety.html#//apple_ref/doc/uid/10000057i-CH8-SW3). It ensures that the block of code and the locked object can only be accessed by one thread at a time. See [mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion).

[cc lang=”c”]

-(void) aMethodWithObject:(id)object

{

@synchronized(object)

{

// code that works with locked object

}

}

[/cc]

##### @autoreleasepool

In an app that has ARC ([automatic reference counting](http://www.mikeash.com/pyblog/friday-qa-2011-09-30-automatic-reference-counting.html)) enabled, you must use @autoreleasepool as a replacement for the NSAutoreleasePool class. The [@autoreleasepool is about six times faster than using NSAutoreleasePool](http://developer.apple.com/library/ios/releasenotes/ObjectiveC/RN-TransitioningToARC/_index.html#//apple_ref/doc/uid/TP40011226-CH1-DontLinkElementID_6), therefore Apple recommends its use even for non-ARC projects.

You should not declare a variable inside the @autoreleasepool block and continue to use the variable after the @autoreleasepool block. Such code should be avoided or refactored.

[cc lang=”c”]

-(void) aMethod

{

@autoreleasepool

{

// code that creates a large number of temporary objects

}

}

[/cc]

##### @selector

Returns the [selector type SEL](http://stackoverflow.com/questions/297680/how-do-sel-and-selector-work-in-iphone-sdk) of the given Objective-C method. Generates compiler warning if the method isn’t declared or doesn’t exist.

[cc lang=”c”]

-(void) aMethod

{

SEL aMethodSelector = @selector(aMethod);

[self performSelector:aMethodSelector];

}

[/cc]

##### @encode

Returns the [character string encoding](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html) of a type.

[cc lang=”c”]

-(void) aMethod

{

char *enc1 = @encode(int); // enc1 = “i”

char *enc2 = @encode(id); // enc2 = “@”

char *enc3 = @encode(@selector(aMethod)); // enc3 = “:”

// practical example:

CGRect rect = CGRectMake(0, 0, 100, 100);

NSValue *v = [NSValue value:&rect withObjCType:@encode(CGRect)];

}

[/cc]

##### @compatibility_alias

Allows you to define an alias name for an existing class. The first parameter is the alias for a class name, a class with this name must not exist. The second parameter is the name of an existing class that the alias refers to.

[cc lang=”c”]

@compatibility_alias AliasClassName ExistingClassName

[/cc]

From then on you can use AliasClassName in place of ExistingClassName. This can be useful after refactoring a class’ name without modifying its behavior, you can use @compatibility_alias to allow existing code using the refactored class to continue to work without refactoring.

##### @”string”

Declares a constant NSString object. Such strings do not need to be retained or released.

[cc lang=”c”]

-(void) aMethod

{

NSString* str = @”This is a constant string.”;

NSUInteger strLength = [@”This is legal!” length];

}

[/cc]

#### Summary

I hope you enjoyed this list and hopefully learned something from it. If you know there’s a directive missing from the list, please add a comment and I will update the post!

**UPDATE:** Johann Dowa from [maniacdev.com](http://maniacdev.com/2011/10/the-objective-c-2-0-compiler-directives-cheat-sheet/) has compiled the [Objective-C 2.0 @ Compiler Directives Cheat Sheet](http://maniacdev.com/cheatsheetobjccd.pdf) in PDF format.

If you liked this list please tweet, like or plus-one it, thank you!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] Steffen Itterheim在他的博客中总结了 Objective-C 2.0 所有的编译器保留字，并且对这些保留字做了介绍和使用示例。这些保留字如下： @class @defs @protocol @required @optional @end @interface @public @package @protected @private @property @end @implementation @synthesize @dynamic @end @throw @try @catch @finally @synchronized @autoreleasepool @selector @encode @compatibility_alias @”string” […]

Thank you for detail description!

For the @property directive, “strong” is the default attribute. Also, “weak” is the same as “unsafe_unretained”, not “assign”.