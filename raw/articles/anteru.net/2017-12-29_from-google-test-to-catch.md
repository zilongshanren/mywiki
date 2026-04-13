---
title: From Google Test to Catch
url: https://anteru.net/blog/2017/from-google-test-to-catch
published: '2017-12-29'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you ever met me, you’ll probably know that I’m a big believer in automated testing. Even for small projects, I tend to implement some testing early on, and for large projects I consider testing an absolute necessity. I could ramble on for quite a while as to why tests are important and you should be doing them, but that’s not the topic for today. Instead, I’m going to cover why I moved all of my unit tests from Google Test – the previous test framework I used – to Catch, and shed some light on how I did this as well. Before we start with the present, let’s take a look back at how I arrived at Google Test and why I wanted to change something in the first place.

## A brief history

Many many moons ago [this blog post](http://gamesfromwithin.com/exploring-the-c-unit-testing-framework-jungle) got me interested into unit testing. Given I had no experience whatsoever, and as `UnitTest++`

looked as good as any other framework, I wrote my initial tests using that. This was sometime around 2008. In 2010, I was getting a bit frustrated with `UnitTest++`

as development wasn’t exactly going strong there, I was hoping for more test macros for things like string comparison, and so on. [Long story short](https://anteru.net/blog/2010/c-unit-testing-frameworks-revisited), I ended up porting all my tests to [Google Test](https://github.com/google/googletest).

Back in the day, Google Test was developed on Google Code, and releases did happen regularly but not too often. Which was rather good as bundling Google Test into a single file required running a separate tool (and it still does.) I ended up using Google Test for all of my tests – roughly 3000 of them total, with a bunch of fixtures. While developing, I run the unit tests on every build, so I also wrote a custom reporter so my console output would look like this:

```
SUCCESS (11 tests, 0 ms)
SUCCESS (1 tests, 0 ms)
SUCCESS (23 tests 1 ms)
```


You might wonder why the time is logged there as well: Given the tests were run on every single compilation, they better ran fast, so I always had my eye on the test times, and if something started to go slow, I could move it into a separate test suite.

Over the years, this served me well, but there were a few gripes with Google Test. First of all, it was clear this project was developed by and for Google, so the direction they were going – death tests, etc. – was not exactly making my life simpler. At the same time, a new framework appeared on my radar: [Catch](https://github.com/catchorg/Catch2).

## Enter Catch

Why Catch, you may ask? For me, mostly for two reasons:

- Simple setup – it’s always just a single header, no manual combining needed.
- No fixtures!
- More expressive matchers.

The first reason should be obvious, but let me elaborate on the second one. The way Catch solves the “fixture problem” is by having sections in your code which contain the test code, and everything before that is executed once *per section*. Here’s a small appetizer:

```
TEST_CASE("DateTime", "[core]")
{
const DateTime dt (1969, 7, 20, 20, 17, 40, 42, DateTimeReference::Utc);
SECTION("GetYear")
{
CHECK (dt.GetYear () == 1969);
}
SECTION("GetMonth")
{
CHECK (dt.GetMonth () == 7);
}
// And so on
}
```


This, together with nicer matchers – no more `ASSERT_EQ`

macros, instead, you can use a normal comparison, was enough to convince me of Catch. Now I needed a couple of things, though:

- Port a couple of thousand tests, with tens of thousands of test macros from Google Test to Catch.
- Implement a custom reporter for Catch.

### Porting

As I’m a rather lazy person, and because the tests are super-uniform in format, I decided to semi-automate the conversion from Google Test to Catch. It’s probably possible to make a perfect automated tool, at least for the assertions, by building it on Clang and rewriting things, but I figured if I get 80% or so done automatically that should be still fine. On top of that, I’m porting tests, so I can easily validate if the conversion worked (as the tests still should pass.) The [script](https://anteru.net/files/2017/MigrateFromGoogleTestToCatch.py) is not super interesting, it does a lot of regular expression matching on the macros and then hopes for the best. While it’s probably going to explode when used in anger, it still converted the vast majority of the tests in my code. In total, it took me less than a day of typing to finish porting all my tests over.

**Update 2021-04-04**: Reader Henry has created a [much expanded version of the conversion script](https://gist.github.com/henryiii/7dc93c6bd8404b346daa2647e72fbd55).

Before you ask why I’m not porting to some other framework like [doctest](https://github.com/onqtam/doctest) which is supposed to be faster: In my testing, Catch is fast enough to the point that the test overhead doesn’t matter. I can easily execute 20000 assertions in less than 10 milliseconds, so “faster” is not really an argument at this point.

What is interesting though is that there was a significant reduction in lines of code by moving over to Catch, most of which came from the fact that fixtures were gone, and some more code now used the `SECTION`

macros and I could merge common code. Previously, I would often end up duplicating some small setup because it was still less typing than writing a fixture. Witch Catch, this is so simple that I ended up cleaning my tests voluntarily. To give you some idea, this is the commit for the core library: `114 files changed, 6717 insertions(+), 6885 deletions(-)`

(or -3%). For my geometry library, which has more setup code, the relative reduction was quite a bit higher: `36 files changed, 2342 insertions(+), 2478 deletions(-)`

– 5%. A couple of percent here and there might not seem too significant, but they directly translate into improved readability due to less boilerplate.

There are a few corner cases where Catch just behaves differently from Google Test. Notably, a `EXPECT_FLOAT_EQ`

with 0 needs to be translated into `CHECK (a == Approx (0).margin (some_eps))`

as Catch by default uses a relative epsilon, which becomes 0 when comparing to 0. The other one affects `STREQ`

– in Catch, you need to use a [matcher](https://github.com/catchorg/Catch2/blob/master/docs/matchers.md) for this, which turns the whole test into `CHECK_THAT (str, Catch::Equals ("Expected str"));`

. The script wil try to translate that properly but be aware that those are the cases which are most likely to fail.

### Terse reporter

The last missing bit is the terse reporter. This got changed again for Catch2, which is the current stable release. The reporter is part of a `catch-main.cpp`

which I compile into a static library, which then gets linked into the test executable. The terse reporter is straightforward:

```
namespace Catch {
class TerseReporter : public StreamingReporterBase<TerseReporter>
{
public:
TerseReporter (ReporterConfig const& _config)
: StreamingReporterBase (_config)
{
}
static std::string getDescription ()
{
return "Terse output";
}
virtual void assertionStarting (AssertionInfo const&) {}
virtual bool assertionEnded (AssertionStats const& stats) {
if (!stats.assertionResult.succeeded ()) {
const auto location = stats.assertionResult.getSourceInfo ();
std::cout << location.file << "(" << location.line << ") error\n"
<< "\t";
switch (stats.assertionResult.getResultType ()) {
case ResultWas::DidntThrowException:
std::cout << "Expected exception was not thrown";
break;
case ResultWas::ExpressionFailed:
std::cout << "Expression is not true: " << stats.assertionResult.getExpandedExpression ();
break;
case ResultWas::Exception:
std::cout << "Unexpected exception";
break;
default:
std::cout << "Test failed";
break;
}
std::cout << std::endl;
}
return true;
}
void sectionStarting (const SectionInfo& info) override
{
++sectionNesting_;
StreamingReporterBase::sectionStarting (info);
}
void sectionEnded (const SectionStats& stats) override
{
if (--sectionNesting_ == 0) {
totalDuration_ += stats.durationInSeconds;
}
StreamingReporterBase::sectionEnded (stats);
}
void testRunEnded (const TestRunStats& stats) override
{
if (stats.totals.assertions.allPassed ()) {
std::cout << "SUCCESS (" << stats.totals.testCases.total () << " tests, "
<< stats.totals.assertions.total () << " assertions, "
<< static_cast<int> (totalDuration_ * 1000) << " ms)";
} else {
std::cout << "FAILURE (" << stats.totals.assertions.failed << " out of "
<< stats.totals.assertions.total () << " failed, "
<< static_cast<int> (totalDuration_ * 1000) << " ms)";
}
std::cout << std::endl;
StreamingReporterBase::testRunEnded (stats);
}
private:
int sectionNesting_ = 0;
double totalDuration_ = 0;
};
CATCH_REGISTER_REPORTER ("terse", TerseReporter)
}
```


To select it, run the tests with `-r terse`

, which will pick up the reporter. This will produce output like this:

```
SUCCESS (11 tests, 18 assertions, 0 ms)
SUCCESS (1 tests, 2 assertions, 0 ms)
SUCCESS (23 tests, 283 assertions, 1 ms)
```


As an added bonus, it also shows the number of test macros executed. This is mostly helpful to identify tests running through some long loops.

## Conclusion

Was the porting worth it? Having spent some time with the new Catch tests, and after writing some more tests in it, I’m still convinced it was worth it. Catch is really simple to integrate, the tests are terse and readable, and neither compile time nor runtime performance ended up being an issue for me. 10/10 would use again!