---
title: 'Review: PVS Studio'
url: https://anteru.net/blog/2011/review-pvs-studio
published: '2011-07-18'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Disclaimer: The friendly folks at [Viva64](http://www.viva64.com/) have kindly provided me a review version of [PVS Studio](http://www.viva64.com/en/pvs-studio/). I could test it completely on my own, on my machine, just as if I would have bought it.

As I have been curious for some while how PVS Studio stacks up against solutions I have already tried ([C++-Check](http://sourceforge.net/apps/mediawiki/cppcheck/index.php?title=Main_Page), [Visual Studio Code Analysis](http://msdn.microsoft.com/en-us/library/a5b9aa09.aspx), [Intel C++ Code Analysis](http://software.intel.com/en-us/articles/static-security-analysis/)), I gladly took the opportunity to test-drive it one two of my projects: *VPlan4*, a small Qt based task tracker and *niven*, my research engine. *VPlan4* consists of ~ 20 source files, compromising ~ 4 kLoC while *niven* consists of ~ 550kLoC, with 70 kLoC in the main library and the rest being external dependencies (400 kLoC), test code, infrastructure and scaffolding.

I tested PVS Studio on a quad-core Core i7 with 2.8 GHz and 12 GiB of memory; all data coming from a 7200 rpm HDD RAID-0. The interesting timings are for the larger project: For one library (~17 kLoC) is takes several minutes. The whole project requires ~ 45 minutes. PVS studio compiles each file and stores the preprocessed output, so using precompiled headers hurts in this case. On the upside you can easily restrict PVS studio to run on a single project or file only. For comparison, processing *VPlan4* takes only a few seconds.

## Setup

PVS Studio directly integrates itself into Visual Studio 2010. It also features an auto-update tool which is run at each startup, so there is no annoying resident update application. Painless procedure, just as it should be. After the installation, you can immediately run it on any C++ project (no need to modify the project files!)

## Results

After the checking is done, PVS Studio groups the warnings into 3 categories sorted by severity. For the *niven* libraries, this results in ~10k warnings, the majority in the lowest-impact category. PVS Studio usually provides distinct warnings for similar-but-not-exactly-the-same issues which enables precise disabling of warnings. That and the fact that you only need two clicks to disable a warning makes the warning list manageable.

Now, the most important part: In the *niven* code base, it did find three real bugs – which haven’t been found by C++-Check and the Visual Studio Code Analysis. Three bugs might not sound a lot, but many code analysis tools are not even able to find a single real bug, and the *niven* code base is pretty mature and has been tested with lots of static code analysis tools already, so three bugs are an excellent result here. On *VPlan4*, I got very few warnings and nothing serious, so I guess the code was written ok’ish :)

To give you an idea of what kind of bugs PVS Studio captures, here is one from *niven*:

```
TASKDIALOGCONFIG tc = { 0 };
tc.cbSize = sizeof (tc);
tc.pszWindowTitle = L"Title";
if (ok) {
tc.pszMainInstruction = L"Done";
tc.pszMainIcon = TD_INFORMATION_ICON;
} else {
tc.pszMainInstruction = L"Error";
tc.pszMainIcon = TD_ERROR_ICON;
// No longer valid after assignment, caught by PVS Studio!
wchar_t errorString [256] = {0};
wsprintf (errorString, L"Error code: %d", GetLastError ());
tc.pszExpandedInformation = errorString;
}
```


On the other hand, using PVS Studio does not mean you can throw away all other analysis tools you are using, as some bugs reported by other tools are not found. For instance, C++-Check finds this one but PVS Studio doesn’t:

```
char s [5];
strcpy (s, "Sixchr");
```


There’s also a bunch of things that get reported which shouldn’t, but the folks at Viva64 told me that future releases will get those fixed. Overall, as far as I can tell, the analysis quality is pretty good (make sure you take a look at the [list of issues which PVS Studio can find](http://www.viva64.com/en/d/)) and I couldn’t spot any junk warnings or incorrect warnings.

Short rant: Having used lots of static code analysis tools so far, I’m still puzzled why nobody bothers to check for portability issues. *niven* compiles with GCC and MSVC. I’d be very happy to have a tool which gives me a warning if I’m using some construct which is not understood by GCC. That would definitely save me a lot of porting pain.

## Overall

### Good

- Works directly on Visual Studio solutions
- Finds a lot of issues
- Good, precise warning messages
- Good support

### Bad

- Slow
- Too many spurious warnings*
- No porting/non-standard C++ warnings

In practice, I found that I’m checking my code base once every 2-3 months. As it’s pretty infrequent, I don’t worry too much if the tool produces a few spurious warnings but I do worry if something is missed. In that regard, PVS Studio fits the bill very well.

## Final remarks

If you are new to static analysis, I can recommend giving PVS Studio a shot (there is a [trial version](http://www.viva64.com/en/pvs-studio-download/).) Static code analysis for C++ is still at an early stage, but even now, a tool like PVS Studio can already help you discover lurking bugs. Especially if your code base is not already covered by unit tests, a static code analysis tool can quickly give you a hint which parts of your code base are ripe for review.

Oh, and before I forget: It also gets regular updates and the support is good – in fact, I reported a bug at the beginning of my review which was fixed in just a few days.

Thanks again to Viva64 for the review version, and keep up the good work!