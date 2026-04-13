---
title: 'Build systems: Make'
url: https://anteru.net/blog/2017/build-systems-make
published: '2017-04-17'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

As mentioned last week, we’re going to cover [Make](https://www.gnu.org/software/make/) today, one of the most widely used tools to build software. Make is a good example what I mentioned in the [the intro](https://anteru.net/blog/2017/build-systems-intro) as the core of a build system: A rule based system which transforms data and takes care of dependencies. Because Make is conceptually very simple, I’m going to cover the inner workings in more detail before diving into the sample project.

Short aside: I’ll be covering Linux only. Make itself doesn’t care much about the platform, but for C++, it’s much easier to explain things on Linux where a simple `g++ foo.c`

produces a binary without having to deal with SDK paths and so on.

The prototypical build file for Make is called a *Makefile*, which contains all the targets and rules for a given project. Here’s an example:

```
file.o : file.cpp file.h
g++ -c file.o file.cpp
```


This describes a very simple rule which produces `file.o`

if `file.cpp`

or `file.h`

changes. It uses the command `g++ -c file.o file.cpp`

to generate `file.o`

. We can test that this works as expected:

```
$ touch file.cpp file.h
$ cat > Makefile <<EOL
file.o : file.cpp file.h
g++ -c file.cpp
EOL
$ make
g++ -c file.cpp
```


If we run Make again, it’ll notice there’s nothing to do, because both dependencies are the same.

```
$ make
make: 'file.o' is up to date.
```


Let’s touch the header file – notice both files are empty, so the contents don’t change, but as Make is filestamp based, it will consider the dependency out of date:

```
$ touch file.h
$ make
g++ -c file.cpp
```


This dependency checking means that Make needs to run `stat`

on every file. We can verify this easily by using `strace make 2>&1 | grep stat | grep '"file'`

, which yields:

```
stat("file.o", {st_mode=S_IFREG|0664, st_size=936, ...}) = 0
stat("file.cpp", {st_mode=S_IFREG|0664, st_size=0, ...}) = 0
stat("file.h", {st_mode=S_IFREG|0664, st_size=0, ...}) = 0
```


Here we can see that Make starts at the target, then it checks the inputs, and if one of them is newer, it’ll go ahead and execute the build rule. That’s really all there is to Make. You get a couple of goodies on top – fancy way to write rules, variables, and so on – but the end result will be always an output, one or more inputs, and rules to transform the inputs into the output.

## Sample project build

Now that we know how Make works, how does it help us to build our sample project? The answer is unfortunately not much. Make doesn’t know about C++ libraries, header files and such. The only part of make we can use directly are the [built-in rules](https://www.gnu.org/software/make/manual/make.html#Catalogue-of-Rules) which allow us to skip writing our own rules to transform `.cpp`

into `.o`

files, and a few pre-configured variables like `CFLAGS`

. You can see those variables at work in the `DynamicLibrary`

project, where it sets the `#define`

as well as the linking through variables:

```
LDFLAGS += -shared -L../statlib -lStaticLibrary
CPPFLAGS += -I../statlib -DDBUILD_DYNAMIC_LIBRARY=1
```


The `+=`

specifies we’re appending to those variables. That’s important as someone might want to use custom `CPPFLAGS`

– let’s say, `-Os`

– and we don’t want to override those. Everything is left to the user. I’ve set up the project with four Makefiles total. One for each binary, and a global Makefile to glue everything together. The individual project files are very similar and follow the same template. Let’s walk through the static library as an example:

```
CPPFLAGS += -fPIC
```


Just as mentioned above, we’re adding some options to a variable. As
mentioned in the [intro](https://anteru.net/blog/2017/build-systems-intro) the `-fPIC`

option is the tricky one and must be set for a
static library which will be linked into a dynamic library. Given that
Make doesn’t know anything about C++ projects, nor that the dynamic
library even exists, we have to specify it manually here.

```
OBJ = StaticLibrarySource.o table.o
TARGET = libStaticLibrary.a
.DEFAULT_GOAL := $(TARGET)
```


We set up a couple of variables to reduce repetition. `OBJ`

contains all object files, the corresponding `.cpp`

files are automatically picked up through the built-in rule. We’re also setting a system variable `.DEFAULT_GOAL`

to indicate what to build if invoked without any parameters. By default, Make picks the first rule, which is not the one we want here.

```
table.cpp : tablegen.py
python3 tablegen.py > table.cpp
```


This is our code generator. Notice that there’s really nothing to it, a file `table.cpp`

is generated from a dependency `tablegen.py`

by executing `python3 tablegen.py > table.cpp`

. We could use [automatic variables](https://www.gnu.org/software/make/manual/make.html#Automatic-Variables) here to avoid repeating the dependency and output name if we wanted to. This would change the rule to `python3 $@ > $<`

. The automatic variable `$@`

references the target of the rule and `$<`

references the first pre-requisite. This is mostly useful when writing implicit rules, and for clarity, I’ve just skipped it here.

Note that I’ve hardcoded the path to Python. Make also doesn’t have a way to find existing libraries or programs. The usual method – short of generating the Makefiles from other tools – is to specify environment variables or have a special settings file which is included into all Makefiles.

```
$(TARGET) : $(OBJ)
ar rcs $(TARGET) $(OBJ)
all : $(TARGET)
```


These are the main rules. `$(TARGET)`

builds the library by invoking `ar`

, which builds a static library from the object files.

```
clean :
rm -f table.cpp $(OBJ) $(TARGET)
.PHONY : clean all
```


Finally, the cleanup rule. We need to repeat everything here, as Make doesn’t know what files it generated, and what side effects may have occurred, so we just spell it out. We also use the special `.PHONY`

dependency to indicate that those targets [don’t produce a file](https://www.gnu.org/software/make/manual/make.html#Phony-Targets).

The other targets look virtually the same, so the only interesting file left is the global driver file which glues together the remaining projects. The way it works is it calls Make recursively for each directory, in the right order. As recursive Make is [complicated](http://aegis.sourceforge.net/auug97.pdf) I’m not even striving to set up everything optimally. Rather, I’m using the [simplest setup I could find](http://lackof.org/taggart/hacking/make-example/) which shows the basic idea. We set up new targets for every directory, and provide a rule which invokes Make for that target. Similarly, a new target is specified for cleaning, which just invokes Make and passes `clean`

to it.

Any inter-project dependencies need to be expressed at a global scope, and I’ve hard-coded all include directories into the respective projects. With a lot of work, you can make everything variable and [pass those around to recursive invocations](https://www.gnu.org/software/make/manual/make.html#Variables_002fRecursion). At this point, it should become obvious that you probably should generate the files from some other, higher-level build system which can express all those cross-project dependencies. Make is a low-level tool which executes rules, and in good Unix tradition, that’s all it does – and it does it well.

As usual, you can find the [complete setup in the repository](https://github.com/Anteru/build-systems/tree/master/make). Note that it has been only tested on Linux, where everything is set up to work correctly with Make out of the box.