---
title: Xcode 4 Template Docs
url: http://www.learn-cocos2d.com/store/xcode4-template-documentation/
author: My Xcode ; Learn; Master Cocos
published: '2011-04-21'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# Xcode 4 Template Docs

### What you’ll get in bulletpoints:

- Five tutorials on how to create File and Project templates
- Extensive reference for all known TemplateInfo.plist items (keys) and settings
- Explanation of the placeholders (eg ___FILENAME___) and variables (eg ___*___)
- Frequently Asked Questions answered
- Many tips and tricks
- Total of 70 pages of documentation (PDF) from 70+ hours of experimentation
- File and Project Template example files

### Synopsis

This unofficial but comprehensive Xcode 4 Template documentation explains how to create File and Project Templates for Xcode 4. Xcode 4 uses a template format significantly different from the one used in Xcode 3, which renders all previous information on Template creation useless. The new format is also much more complex and allows for greater flexibility, for example a template can now consist of multiple inherited templates.

This Xcode 4 Template documentation first gives you a quick overview what File and Project templates are. Step-by-step tutorials show you how to create your own File and Project Templates. In the reference section the format of the TemplateInfo.plist and related files are meticulously documented. Finally there’s the Frequently Asked Questions (FAQ) section with answers to common questions. The documentation is fully hyperlinked so that you can quickly look up keywords in the reference section. Several example files for File and Project Templates help you get started and can be used as the basis for your own templates.

### Available for free

The documentation is now **available for free**:

### Disclaimers

This is not official documentation. I can not guarantee that the documentation is 100% correct, much of the information was found out through lots of trial and error. Nevertheless this documentation contains a lot more information than what is currently available on the Internet.

THE DOCUMENTATION IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DOCUMENTATION OR THE USE OR OTHER DEALINGS IN THE DOCUMENTATION.

[…] Xcode 4 Template Documentation […]

[…] Xcode 4 Template Documentation […]

Hi, i’m interessed in the book, but i have a question: mi problem is how to create a template to generate a project with links to mi already existent static libraries. Does it include any sample about it? Thanks.

No, that’s one of the things that doesn’t seem to be possible with Xcode 4 templates.

Hi,![:)](../../wordpress/wp-includes/images/smilies/simple-smile.png)


I would love to start to program with Xcode 4, but I am a real noob at it. No experiences at all except on database like 4dimension

I just would like to know that if your template/book, would help a newbie or should I try to find first a “Book for the dumb” ? (in french we do have a book’s collection called “pourlesnuls” (forthedumbs) to help for the really first step…![:)](../../wordpress/wp-includes/images/smilies/simple-smile.png)


Best Regards,

Charles

In english there’s a book series “for Dummies” which is quite popular and yes, there’s a Objective-C for Dummies.

Personally, I learned Objective-C from Learn Objective-C on the Mac from Apress.

You don’t need to know much of Xcode to start working with it, respectively what you need to know you can research via google whenever you need some help. I think the crucial parts are usually explained in good Objective-C books.

You can also preview my Learn Cocos2D book on google to see if it matches with your level of experience.

BRILLIANT, with this resource in front of me creating file projects seemed really simple.Thanks!

karl

Does this include the features or capabilities described in your “My professional cocos2d Xcode Project Template”? (http://www.indiepinion.com/steffenj/my-professional-cocos2d-xcode-project-template/)

I’m not sure what exactly you’re referring to but I would say no. Basically because this doc is for the new Xcode 4 template format, the tutorial describes how to setup cocos2d as external reference in an Xcode 3 project. Unfortunately, adding external .xcodeproj files is one of the few things the Xcode 4 Template format does not support in a satisfactory way (there are manual steps required to make externally references projects work in Xcode 4 project templates).

The earlier “professional cocos2d Xcode Project Template” appears to focus on results, leveraging Xcode 3 capabilities to get things done. That blog post includes a bulleted feature list for that template.

The newer “Docs: Xcode 4 Templates” appears to be the “missing manual” detailing all Xcode 4 capabilities. But does it also provide a finished template with all or most of the capabilities of the earlier template? Or is creating an Xcode 4 template with those same capabilities left as an exercise for the reader?

I’m ready to transition from “can I really do this” initial development, to “time to get serious about releasing a product” development. I’m hoping to adopt a suitable Xcode template to assist me in doing that.

I should mention I bought your book, it’s been *tremendously* helpful, as have the many other resources you’ve provided. Thanks!

There are example templates in the Xcode 4 Template documentation (product on this page). However, they are not cocos2d project templates.

Moreover, the older Xcode 3 Template Tutorial for Cocos2D is labelled a bit misleading as “template”, it’s not a template that you can create via File -> New Project in Xcode - it’s a project that I used as template for my own projects by copying the entire folder.

Hello Steffen, Thx a lot for this document

I have just one question, i bought with paypal your doc but after the confirm how i download the doc ??? i don’t have seen any links and nothing in my email box just the paypal ticket maybe you will send me after verification ???

have a good day

(My english level is not perfect i hope you will understand me) bye

Oooops I’m too impatient, Don’t forget Always verify the Spam Box

thx !!!

No problem. Also sometimes Paypal payments can take several days to go through. It depends on the chosen payment method. Credit card and direct debit clear immediately, other options may take longer.

This is a great resource, but there’s one thing that I can’t seem to make work - groups.

It seems that groups are created automatically when you include definitions for files and specify that they are in groups. That’s useful, but I want to be able to specify the path of a group.

You can do this in Xcode and the result is that new files created within that group are automatically placed in the right subdirectory on disk. It’s great for keeping things organised.

In other words, I want the on-disk layout to be Foo/Bar/Baz.txt, and I want matching groups:

Foo should have a path of Foo, relative to its enclosing group.

Bar should have a path of Bar, relative to its enclosing group, with its parent being Foo.

Baz.txt should have a path of Baz.txt, relative to its enclosing group, with its parent being Bar.

However because the groups are created automatically, there’s no opportunity to supply a Path entry. If I only define Baz.txt, then Foo and Bar are created, but their paths are blank.

I tried to specify the groups manually by giving them definitions and nodes, but that has the result of trying to copy them as directories instead, meaning that the files and directories within are copied twice and all kinds of weirdness ensues.

This is also a problem when trying to create empty groups.

It’s not clear from your documentation whether this is possible or not. Have you solved this problem?

Groups in the Xcode 4 templates are sketchy at best. What you can do is use the “Group” in “Definitions” but change it from string to array. From the documentation (p35): “If Group is an array, you can specify subgroups by creating an array item for each group. For example, to put a file into the group path /Classes/MyCode/Tests/ you would add in the same order three array items: Classes, MyCode and Tests without the slashes.”

What I believe you can’t do is to have files in one folder but in a differently named group or group path in Xcode.

Yeah, I got that. Creating nested groups I can do no problem. It’s setting the path for the groups that’s the issue. I experimented with putting dictionaries into the array instead of strings, but didn’t find anything that wasn’t ignored. I checked the official templates, and none of the groups in them have paths set, so I reckon it’s an inherent limitation of the template system unfortunately.

It works with

Assets

Path

Assets

TargetIndices

and an entry in the Nodes array

Nodes

…

Assets

…

Oooold thread, but for other people seeking this info:

If the name of the entry in the Definitions dict, as well as the matching name in the Nodes array contains the full relative path starting with”./”, the file will be placed in accordingly on the disk.

Has anyone figured out how to add headers to the Copy Headers build phase in a template? This is the last piece of the puzzle for my own template.

Regarding the CopyFiles build phase:

I have figured out that the DstSubfolderSpec is the 1-based index of the selected item in the Destination popup menu. The items in the menu for Xcode 4.0.1 are:

1 Absolute Path

2 Separator

3 Product Directory

4 Separator

5 Wrapper

6 Executable

7 Resources

8 Java Resources

9 Frameworks

10 Shared Frameworks

11 Shared Support

12 PlugIns

If you open a project and manually create a CopyFiles phase, set the Destination to Resources and add file to be copied, close the project, then open the project.pbxproj file in a text editor, you’ll see a CopyFiles section that looks like:

/* Begin PBXCopyFilesBuildPhase section */

082486231469AFBE0019A165 /* CopyFiles */ = {

isa = PBXCopyFilesBuildPhase;

buildActionMask = 2147483647;

dstSubfolderSpec = 7;

files = (

082486451469B1150019A165 /* my_file_to_copy.txt in CopyFiles */,

);

runOnlyForDeploymentPostprocessing = 0;

};

/* End PBXCopyFilesBuildPhase section */

Note that dstSubfolderSpec == 7 and that there is a “files” array.

In a project template, adding a CopyFiles build phase and setting DstSubfolderSpec to 7 gives the same result EXCEPT that there does not seem to be any way to specify the “files” array. I’ve tried every way I can think of (around 100 different combinations including using Definitions and Nodes, arrays named “files” and “Files”, etc.), but the files array in the resulting project is always empty.

Note that Apple’s single example that uses a CopyFiles build phase (the Mac Command Line Tool template) has the same result: a PBXCopyFilesBuildPhase section is created but the files array is empty.

Hello Steffen. Could you please help me?

1) Are there an information about adding more then one target to project in this documentation?

2) Can I add some file only for one target (e.g. create two targets, one regular and second for unit tests, and add tests source only into second target for compilation)?

Thanks in advance!

I’m interested in doing the same. Could you please clarify if the doc talks about this, Steffen?

Thanks.

Multiple targets was one of the issues why I chose to write a separate template tool for Kobold2D because it doesn’t seem possible to add multiple targets in an Xcode template. At least I couldn’t figure out a way to do it.

If I remember correctly there was exactly one Xcode template project provided by Apple that magically had two targets (I think Quartz plugin or some plugin template). It looked like this was hardcoded in Xcode and not configurable via templates.

I found a way to do it!

“MacRuby” library has a project template with 2 targets. You can have a look at it: https://github.com/MacRuby/MacRuby

Hi Steffen

I read your xcode 4 template documentation. It was worth the reading and was able to create my own templates. i had one question do we have to follow similar steps for creating templates for xcode 4.2.

As far as I know the template format hasn’t changed since the release of Xcode 4.0, so it’s the same for Xcode 4.2.

Hi Steffen,

Great job with the doc. It’s really helped with getting over the main hump. But I’ve hit a couple of problems (this is under Xcode 4.2.1). Perhaps you can point me in the right direction:

1. How do you add a dylib (like libxml2.2.7.3.dylib or libicucore.dylib)?

The “Frameworks” section works fine for adding known frameworks, but these are dylibs in /usr/lib. Just adding them in manually doesn’t work because it assumes they’re resident in the current directory and the path is all wrong. Adding them into the Frameworks section automatically appends a .framework to the name.

2. On a related note, how does one go about adding a custom framework, i.e. one made by a third-party installed in a non-shared directory, perhaps with the path defined in an environment variable?

Maybe you’ve already described it in the Template Doc book and I’ve just missed it.

Any tips (or pointers to examples) appreciated.

1) I believe that’s not possible, at least I don’t know a way to do this.

2) Same for custom frameworks or static libraries (.a).

Because of these issues I ended up not using Xcode 4 project templates for Kobold2D, and instead devised my own mechanism and a tool to provide template projects. It has the positive side-effect that it makes creating additional template projects dead easy, it’s just a regular project with a specific name and folder location.

Regarding (1) this seems to work for me:

libsqlite3.dylib

PathType

DeveloperDir

Path

/usr/lib/libsqlite3.dylib

FileType

wrapper.framework

how do I pay for this with paypal?Thanks.

To my knowledge Plimus is currently working on their Paypal integration, so Paypal may not be available to all customers. Hopefully this will be resolved soon.

I think this may be a quick question, but it’s totally baffling me. I just got interested in Xcode 4 templates, so I bought your documentation.

I pretty much have the file templates figured out (as you say they’re pretty easy.) Only problem I had was that I wanted to use a combo box for an option, and, as you say, it doesn’t work for file templates. (:

So, on to project templates. I started to do the Basic Project Template Tutorial and that’s where I ran into trouble. I’m using Xcode 4.4.1. Maybe Apple changed something. I tried copying the Core Data Spotlight Application template, but it doesn’t show up (after moving renaming, changing identifier, etc) because it’s not concrete.The only applicable one in that Mac directory in the Xcode package that is concrete is Cocoa Application. After copying that one and doing all the necessary fixup, it does show up and does create a new project. However, it doesn’t have all the options that the “standard” Apple Cocoa application project does.

I checked the ancestors and sure enough it doesn’t include the core data or cocoa document-based, etc templates, so I understand why those options don’t show up in my version. However, my biggest question is rather why they do show up when I pick the Apple version from the Xcode package? It’s been driving me crazy for several hours now. That’s the only template that’s concrete and it also doesn’t have the ancestors I would expect, but the options still show up. Do you have any thoughts on this? I can’t explain how Apple’s template shows the options it does.

I too found it very confusing how Apple set up their templates. The issue you describe sounds like a missing reference to one of the template files. One thing you can do to debug this is to traverse all the references from both ends. Sometimes in-between templates include other common template files. It’s not always strictly hierarchical, and in some cases templates are replaced (overridden) by child templates if I remember correctly. I can’t rule out though that Xcode 4.4 has introduced some changes.

Something else you could try is to copy *all* the original templates to the user templates folder, and start manipulating them there, perhaps removing the template files and folders that should not be needed. Check frequently in Xcode to see if the template you’re interested in still works.

Thanks for the reply. I have considered, but not yet tried, just the strategy you suggest. I don’t know if you are planning any update to your documentation, but as it currently exists, anyone following the instructions will fail on the first part of the Basic Project Template Tutorial because of the same issues I had. If it were my product, I would be considering an update. Of course, it’s not my product and I understand it’s just a small side project you did at one time.

Thanks,

Ward

I’ll check if there’s a breaking change.

Hi!

Thank you for the nice tutorial on Xcode 4 templates worth the €10.

When using an External Build System, Xcode shows on the Info pane three parameters: Build Tool, Arguments, Directory.

On the project template, the keyword for Build Tool and Arguments are defined, but not for Directory.

Any clue? Thanks.

Hmmm not from the top of my head. If I remember correctly there are constants for various directory locations but not one where you can specify a custom directory.

Hey Steffen! Is there anything in this book about adding key/values to the existing Info.plist file? Thanks!

You simply provide a Info.plist file in the template that has the desired keys set. If you need different versions of the Info.plist you can include different plist files based on template variables.

Since Info.plist is a text file the regular text substitution will also work with plists. Meaning you can create a placeholder name and then add a specific Info.plist key depending on user settings in the template dialog. Plus Info.plist itself recognizes special variables, for example the app’s name via ${PRODUCT_NAME}. These identifiers are described in the Xcode documentation, I believe in the section about enviroment variables.

Hi Steffen,

Thanks for putting all this together, it must have been a lot of work.

I was wondering if you know of a way to get Build Rules into a template.

My problem is that I have created a custom compiler spec for sourcecode.c.c files. However, when I try to use it Xcode issues warnings like:

“Warning: no rule to process file ‘$(PROJECT_DIR)/HW4/main.c’ of type sourcecode.c.c for architecture Darwin-x86_64”.

To fix this I can add a Target Build Rule to process source c files with my compiler. When I do this it inserts code like the following into my project file:

/* Begin PBXBuildRule section */

1FB2A6C31795A65300E37260 /* PBXBuildRule */ = {

isa = PBXBuildRule;

compilerSpec = com.apple.compilers.gcc.4_7;

fileType = sourcecode.c;

isEditable = 1;

outputFiles = (

);

script = “# \n”;

};

1FE492271795B94200B0BB9A /* PBXBuildRule */ = {

isa = PBXBuildRule;

compilerSpec = com.apple.compilers.gcc.4_7;

fileType = sourcecode.c;

isEditable = 1;

outputFiles = (

);

};

/* End PBXBuildRule section */

I was wondering if you know of a way to add build rules to my target templates. Or better yet, to get Xcode to realize that my compiler spec processes sourcecode.c.c. files. I have this information in my xcspec:

Identifier = “com.apple.compilers.gcc.4_7”;

Type = Compiler;

Class = “PBXCompilerSpecificationGcc3_3”;

Name = “GCC 4.7”;

Description = “GNU C/C++ Compiler 4.7”;

Vendor = Apple;

Version = “4.7”;

FileTypes = (

“sourcecode.c.c”,

“sourcecode.c.objc”,

“sourcecode.cpp.cpp”,

“sourcecode.cpp.objcpp”,

“sourcecode.asm”,

);

Architectures = (

“Darwin-i386”,

“Darwin-x86_64”,

“MinGW-x86_64”,

“Linux-x86_64”,

);

But it does not seem to help.

By the way, once I add the build rule, everything compiles nicely and I can run the executables under windows, mac os x, and linux. So the cross-compiling works properly.

Thanks in advance,

Kevin

Hi Steffen…

Excellent document !!

Thanks for going to the trouble of digging into the guts of Xcode templates, and pulling it all together into this well-researched, and well-written document !

…Bill