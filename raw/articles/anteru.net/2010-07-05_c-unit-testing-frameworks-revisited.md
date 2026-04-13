---
title: C++ unit testing frameworks revisited
url: https://anteru.net/blog/2010/c-unit-testing-frameworks-revisited
published: '2010-07-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

For a long time, I’ve been using UnitTest++ for all of my C++ unit testing needs. UnitTest++ is a very nice and small unit testing library, which covers all basic needs and is very easy to integrate with a project. The problem is that the development has been on halt since 2008; I’ve been doing some minor adjustments locally, but in the long run, I would like to use an up-to-date library and get new features from time to time.

So I went out to search for a modern unit-testing framework in C++. Primary requirements were:

**Mature**: It should be used on larger projects and have a stable API. I don’t want to have to update all my unit tests anytime soon again.**Portable**: Linux and Windows is a must, Mac OS X is a nice-to-have, console platforms is bonus. It should be at least reasonably easy to port if necessary.**Fast integration**: It should require minimal work to integrate. Tests should require at most one macro (something like`TEST(Foo)`

.) It should not require to link against a shared DLL and the framework itself should be very easy to integrate. Ideally, I would like to compile it as part of the project (using CMake.)

After some searching, I found two major contenders:

[Google Test](http://code.google.com/p/googletest/): The framework used by Google (internally), LLVM and Chromium[Boost.Test](http://www.boost.org/libs/test/): The Boost testing framework, used by Boost

## Boost.Test

Boost.Test is a huge library bundled with Boost. It has to be built using the Boost tools, but as I’m a heavy Boost user anyway, this is no problem. On the fast integration side, it has `BOOST_AUTO_*`

which make it very easy to get started. The test macros are easy to use, and provide check and require test levels (i.e. if a require fails, the test execution stops, while it continues over checks. This is very useful, you can break a test for instance if the result has zero size, and then check all contents of the results with checks.) It also brings collection equality tests, which are handy.

As you would expect from a good test framework, it has also support for fixtures and output customisation. From the portability side, it runs everywhere Boost runs, which covers all platforms mentioned above. Being used to test Boost, it also qualifies as mature, even though I’m not aware of any bigger project outside Boost that uses it.

## Google Test

Google Test is the framework used internally by Google and now available for free. Building is trivial, as there is a single-source amalgamation file. Integrating is easy as well, for each test, you have to use a single macro. Test suites are defined along with each test, which means you’re forced to group them – which is not as bad as it sounds, as you usually want to group all tests for a submodule/class together anyway. The test functionality is very similar to Boost; on the one hand, GoogleTest provides death tests which Boost hasn’t, but it is missing a few tests that Boost provides (collection equality.) Adding additional tests is straightforward though.

The output customisation is very simple through an event-based interface. Portability is slightly worse than Boost; some features are supported on a one platform only (some only run on Linux.) On the other hand, it has nice platform-dependent tests (for instance, you can check HRESULTs on Windows.) It’s used on LLVM, which is a quite large library, as well as on Chromium, so it also qualifies as mature.

## Conclusion

It’s a really tight race between Google Test and Boost.Test with no clear winner. For small one-off projects, I typically use Boost.Test now, as it’s really dead simple to integrate and puts the least burden on the client (i.e. I assume all users of my stuff have Boost installed.) For utmost portability, you should also stick with Boost.Test, as it focuses on standard-conformant C++ and should run almost everywhere.

On the other hand, the simple customisation of Google Test and the nice [Google Mock](http://code.google.com/p/googlemock/) library makes it an excellent candidate for larger libraries. In my case, I’ve integrated it into the build of my in-house stuff, so it gets built along with the rest of the projects. In this case, I also spent some time to customise the output etc. By providing platform-dependent tests, it also excels for applications which are supposed to run on Linux/Windows/Mac OS X.

It’s actually good to see that there are two equally good C++ testing frameworks out there which are on par with the tools you get for Java/C# and other languages. A much more comfortable situation [than several years ago](http://gamesfromwithin.com/exploring-the-c-unit-testing-framework-jungle), where you basically were forced to [write your own testing framework](http://gamesfromwithin.com/unittest-v10-released) if you were serious about unit testing.