---
title: The perfect logging system for C++ apps
url: https://anki3d.org/the-perfect-logging-system-for-c-apps/
author: Panagiotis Christopoulos Charitos
published: '2011-01-03'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

Ok, the title sounds a little bit pompous and promises allot, many fellow programmers will disagree with the described methodology and others may find it useful. After many changes and rewrites of the AnKi logging system we’ve gained some experience of how a proper logger should be designed and work. The purpose of this article is to pass this knowledge to anyone who is interested.


First of all lets see what logging is. Logger is a subsystem responsible of keeping a record of the various engine events, to inform about problems and eventually help us (the programmers) diagnose them.

A simple logging method is to use the printf function for writing in the standard output:

// Report an error printf("Error: %s\n", "Something went wrong"); // ...or inform the user of a certain event: printf("Renderer initialized successfully!\n");

The simple printf is more than inadequate. A proper logger should have the following attributes:

- Data abstraction
- Minimal dependences
- Only one instance & self sustained
- Multiple outputs
**(VERY VERY INTERESTING)** - Error tolerant

### Data abstraction

The logger should be able to take as input various data types and be able to process them without much trouble from our side. The std::cout is a perfect example. cout can output C strings, STL strings, floats, ints and other standard data types. So a its a good idea for a logger to have the same functionality as the STL ostream.

// Bad and slow (thanks to boost::lexical_cast) Logger::getInstance().write("The current line is: " + boost::lexical_cast<std::string>(__LINE__)); // Good Logger::getInstance() << "The current line is: " << __LINE__ << endl;

Also note that the ostream’s way is much faster because we can use a preallocated buffer instead of invoking malloc to concatenate the STL strings all the time.

### Minimal dependences

The logger is an essential subsystem that practically every other subsystem uses. It’s a very bad idea for the logger to depend on other engine subsystems like the renderer or some global variables. The cross dependencies across subsystems should be avoided when possible and especially for logging.

### Only one instance & self sustained

In an application only one logger should exist. To ensure the uniqueness we can use the [singleton pattern](http://en.wikipedia.org/wiki/Singleton_pattern) or create a global instance. As we all know globals should be avoided when possible and for that reason the AnKi logger is a singleton class. Also the logger cannot be part of any other subsystem because this makes the unit testing difficult.

In the previous version the logger was member of the global application class and it was initialized by the application. For testing, if a subsystem wanted to use only the logger it had to initialize the whole application. Thats a bad practice for our simple unit tests because it renders the code pretty untestable. For unit testing the preferable practice is to have many independent subsystems with very little dependences with each other.

### Multiple outputs

In a game engine the logs should be outputted in various locations. The output can be the standard output (or standard error), the in-game console (eg quake console), a pop-up message box, in a log file(s) or in all of these at the same time. As we already mentioned before the logger should not have any dependencies so a question is how to write to the in-game console, for example, without invoking the renderer? The answer is to use the [observer pattern](http://en.wikipedia.org/wiki/Observer_pattern). For those who have worked with a signal/slot framework (eg Qt) this introduction is pointless but for those who haven’t lets explain how AnKi uses it.

The logger has a signal data member, if another subsystem wants to know the logger’s output it can simply “connect” to this signal. When the logger is ready output a message (eg when it flushes) it emits the signal with the message as a parameter. The subsystems that are “connected” to this signal will get the message and handle it according to their needs.

// Connect the signal with a method... Logger::getInstance().getSignal().connect(boost::bind(&App::handleMessageHanlderMsgs, this, _1, _2, _3, _4)); // ... and the method just outputs to the stdout void App::handleMessageHanlderMsgs(const char* file, int line, const char* func, const std::string& msg) { std::cout << "(" << file << ":" << line << " "<< func << ") " << msg << std::endl; }

### Error tolerant

The logger provides the means for error reporting but what happens if the logger itself needs to report an internal error? Its very stupid for the logger to use itself to for reporting, the reason is pretty obvious I guess. The only solution is to be fault tolerant or use assertions. For example, in AnKi when we have a buffer overflow we flush the already filled buffer and continue from the top. In another case when the logger’s input is very big and exceeds the logger’s internal buffer (more than 512 bytes!!??) we simply ignore the message.

### Conclusion & references

The logger in AnKi is very clean and abstract. One of the disadvantages it that the signals and slots add a certain overhead but the messages in the main loop should be kept to minimum either way.