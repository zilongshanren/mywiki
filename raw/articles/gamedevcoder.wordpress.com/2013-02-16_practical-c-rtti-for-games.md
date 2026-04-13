---
title: Practical C++ RTTI for games
url: https://gamedevcoder.wordpress.com/2013/02/16/c-plus-plus-rtti-for-games/
published: '2013-02-16'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

There’s at least few popular approaches to C++ based [RTTI](http://en.wikipedia.org/wiki/Run-time_type_information) (aka Run-Time Type Information) implementation in games. The goal of this post is to discuss strengths and weaknesses of major ones.

But before that let’s have a look at some of the most common uses of RTTI in games. In fact they are not much, if at all, different from any other, non-game related, project.

**(a) Run-time type checking and instancing.**

Being able to check what’s the actual class of an object is often useful functionality for gameplay programmers:

bool Object::InstanceOf(Class* _class) const;

Another useful feature is ability to instantiate an object knowing its class name:

Class* ClassManager::FindClassByName(const char* className); Object* Class::CreateInstance();

To implement above basic RTTI functionality, we’re usually required to derive all of our game classes from some base *Object* class. Supporting multi-inheritance is possible but typically avoided because in most cases it’s just not needed but would make things a lot more complex otherwise.

[Reality Prime’s dev blog](http://www.realityprime.com/blog/2007/03/the-audience/) shows basic implementation of such RTTI system.

**(b) Automatic serialization of objects and their attributes.**

Instead of implementing custom *Read() / Write()* methods for each class where every property is manually processed, we can now (with RTTI system in place) implement generic *Read()* and *Write()* methods that will work for all classes. Alternatively we can write single *Serialize(Serializer&)* method that would either read or write (or do other things) depending on implementation of *Serializer*.

But while this feature sounds great it has one serious downside – very limited support for data versioning. Imagine one day you decide to change some ‘*int m_Name*‘ attribute into ‘*String m_Name*‘ attribute. How would you want your game to load the old data and convert into new format? Would you want to perform some kind of ‘offline’ conversion by running hacked version of the game over all of the data? If so, you’d have to do so for all of the relevant game data files at once. In a big team working on a game that is obviously a challenge because the person performing conversion must assure no one else has got any important local changes on their PC.

Or even worse, suppose your game has already been released and there’s tons of content (e.g. levels, quests, puzzles) created by the community. Simply changing the format of the data expected by an updated game executable would break all of that content unless you provide way to convert from the old format into new one.

To some extent this upgrade process can be automated as demonstrated by [Insomniacs](http://www.insomniacgames.com/new-generation-of-insomniacgames-tools-as-webapp/) (unfortunately, to my knowledge, the actual explanation of that can only be found in GDC slides or articles in paid magazines). Their system of lazy upgrade script evaluation assures that every asset you get from asset database is always in latest format.

Having said all that I should point out that some projects don’t need robust data versioning at all and therefore may well benefit from automatic serialization. This is especially true for small projects without support for community created content.

**(c) Game editor integration**

Another great benefit of RTTI is that it allows class attributes to be automatically exposed for editing within some kind of visual editor. This feature may require additional editor specific attributes to control how each particular type shall be edited. For example you may want to have nice color selection control instead of having to manually type in individual RGB values; or you may want to limit min and max values of fog intensity by 0..1 range, etc.

This best works with [WYSIWYG](http://en.wikipedia.org/wiki/Wysiwyg) game editors which for the purpose of editing use the same C++ classes as the ones used in the game. There’s no need for intermediate communication layer and every editing action changes the game object directly. As with anything, this has some advantages (mainly easier and cleaner implementation) as well as disadvantages (less efficient and editor-polluted run-time code).

**Manual serialization**

A well known example of an engine that supports features listed in all above points is Unreal Engine 3. As for the automatic serialization, it only does so for Unreal Script classes. For their C++ classes they use more “manual” method which does make a lot of sense because it allows for a flexible data format versioning. Here’s sample code that demonstrates mentioned “manual” method:

// Deserializes instance of Dog class void Dog::Read(Reader& reader) { // Deserializes all base class attributes Super::Read(reader); // Read name value reader >> m_Name; // Read color value; only if data has it (old version didn't) if (reader.GetDataVersion() >= ENGINE_VER_DOG_ADDED_COLOR) reader >> m_Color; // Read height value; only if data has it (old version didn't) if (reader.GetDataVersion() >= ENGINE_VER_DOG_ADDED_HEIGHT) reader >> m_Height; }

Implementing automatic serialization that would handle all kinds of data versioning correctly is not possible simply because it’s only programmers who know how data changes between versions. The major limitations of the automatic serialization are as follows:

- only simple type conversion handled correctly (e.g. int into float)
- name changes cause new property to be added and the old one to be removed (thus losing the data)

On the other hand, by manually handling data upgrades, one has full control over data conversion.

**Type information generation methods.**

We now know why RTTI might be useful. But how do we create it? Again, there’s at least a couple of ways – from manual intrusive macro/template based ones to automatic offline ones.

**(a) Manual intrusive macro/template based method.**

One very popular way of creating RTTI in C++ is by adding a couple of special macros and functions to every class. This may look something like this:

*Header file:*

// Sample Dog class class Dog : public Animal { // Tells RTTI that Dog inherits from Animal // Also defines some helper functions RTTI_DECLARE_CLASS(Dog, Animal) private: int m_Height; // Dog height String m_Name; // Dog name };

*Source file:*

// Function declared in RTTI_DECLARE_CLASS macro // Adds all attributes to class RTTI void Dog::RTTI_InitAttributes() { // Initializes m_Height attribute; figures out type using templates RTTI_INIT_ATTRIBUTE(m_Height); // Initializes m_Name attribute; figures out type using templates RTTI_INIT_ATTRIBUTE(m_Name); }

The actual initialization of each class is best done manually – something like this:

void InitMyClasses() { Object::RTTI_Init(); Animal::RTTI_Init(); Dog::RTTI_Init(); Cat::RTTI_Init(); [...] }

To keep things short I’m going to skip implementation of *RTTI_DECLARE_CLASS* and *RTTI_INIT_ATTRIBUTE* macros. The nice thing about attribute registration is that using C++ template specialization it’s totally possible to automatically deduce type from a variable – this is useful because it means you can initialize all attributes with call to the same RTTI_INIT_ATTRIBUTE macro.

The major downside of this approach is that the programmer needs to maintain an up-to-date RTTI initialization code. With the help of automatic attribute type deduction and some C++ macro magic, this can be made safe and less inconvenient but it’s still not perfect.

**(b) Automatic – parser based.**

One totally different approach to building RTTI information is by generating it offline and storing it in a file which is then loaded by run-time. There’s plenty of C++ code parsers available (e.g. [Wave](http://boost-spirit.com/repository/applications/wave.html) or [GCCXML](http://www.gccxml.org/HTML/Index.html)) available which you could use but there’s still some coding required in order to extract selected types for RTTI purposes. You’d also need to integrate C++ parsing step with your project building, so it wouldn’t need to be done manually.

One issue with this approach is that the RTTI data generated during preprocessing step might potentially differ between project configurations / platforms. But since gameplay code is typically platform and configuration independent this is probably a very minor issue.

The nice thing about this approach is that, provided parser can extract comments attached to particular class or attribute, it’s possible to use comment based custom annotation language on a per class or attribute basis. This can be useful in a couple of different scenarios including when you want to mark some attributes as serializable or when you’d like RTTI for a specific C++ class not to be generated at all. Annotation technique is something that is widely used in other languages such as [Java](http://docs.oracle.com/javase/1.5.0/docs/guide/language/annotations.html) or [C#](http://msdn.microsoft.com/en-au/library/dd901590(v=vs.95).aspx).

**(c) Automatic – debug info based.**

Yet another approach to building RTTI information is by extracting it straight from debugging information files such PDB on Windows as described on [Maciej Sinilo’s dev blog](http://msinilo.pl/blog/?p=517). It is a very similar method to the one presented before but one small advantage of it is one doesn’t need to implement an additional parsing step themself which, depending on how easy parses integration is, might save a lot of work.

**Summary**

As it often happens, there’s no best solution that would fit all projects. Every game is different and there’s games that don’t need RTTI at all.

For larger game projects with heaps of gameplay editing involved I’m leaning towards Unreal Engine 3 approach i.e. manual RTTI including manual serialization on the C++ side and automatic RTTI with automatic serialization on the scripting side (assuming there is one). Many popular scripting languages already have full [reflection](http://en.wikipedia.org/wiki/Reflection_(computer_programming)) support in place which makes things easier there.

For projects where WYSIWYG editing isn’t priority, full blown RTTI system with attribute level information may not be necessary at all. Even more so with projects where in-place serialization (one block of memory used for multiple objects) is being done making it mostly redundant to maintain any kind of attribute information at run-time.

Another option is to generate the C++ class from some other data description. I like this because of its simplicity and robustness. You can easily do serialization, deserialization, inspection and all sorts of debugging stuff because all you need to do is generate plain old code to do this based on the data description.

Generating code is easier than parsing. If anything ever crashes or doesn’t work right, it’s just really simple code to step through. It’s not generic, or template, or using any kind of runtime void-pointers or anything like that. All the code you’re ever looking at is special-cased for that specific type and as dumb as you could possible imagine.

Also, your source format can be as limited as you want – no need to worry about some obscure corner of the C++ language being added to a class.

This does assume that only a subset of your classes need RTTI (you really don’t want *every single class* to be defined in some weirdo JSON-like asset format), which is generally true.

You’d also want some simple “escape hatch” mechanism where the “managed” object type simply has a pointer to runtime data that gets loaded through some custom mechanism (i.e. associate the field with an “asset identifier” that gets loaded through custom code). This would be for things where the format of the data matters (like precompiled shaders, or vertex buffers) and it’s easier to just store them as binary blobs and do the patch up on a type-by-type basis.

Thanks Sebastian for your input.

Yeah, it’s definitely worth looking at. I’ve heard about this method but didn’t mention it because my impression was it wasn’t very popular. Do you recommend any particular tools or did you roll out your own implementation?

We just rolled our own. It was based on xml and a gui editor, but I’d probably use something more readable and just use text specification if I were to do it again. You get a lot of mileage from having “blessed” types too. Common types that occur all over the place that you write special code to handle instead of using the data description language to “all the way down” to ints and floats. This way e.g. a 4×4 matrix is a single data member to load/save/visit not 16, which gives a huge constant factor reduction in schema processing and generated code density.

Oh, and it’s worth noting that this isn’t a million miles away from what Unreal does for “native” unrealscript classes. So at least the practice of generating code for game objects is pretty common.