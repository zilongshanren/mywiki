---
title: Letting users block injected third-party DLLs in Firefox – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2023/03/letting-users-block-injected-third-party-dlls-in-firefox/
author: Greg Stoll
published: '2023-03-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In Firefox 110, users now have the ability to [control which third-party DLLs are allowed to load into Firefox processes](https://support.mozilla.org/en-US/kb/identify-problems-third-party-modules-firefox-windows#w_block-modules-that-cause-firefox-to-crash).

Let’s talk about what this means and when it might be useful.

## What is third-party DLL injection?

On Windows, third-party products have a variety of ways to inject their code into other running processes. This is done for a number of reasons; the most common is for antivirus software, but other uses include hardware drivers, screen readers, banking (in some countries) and, unfortunately, malware.

Having a DLL from a third-party product injected into a Firefox process is surprisingly common – according to our telemetry, over 70% of users on Windows have at least one such DLL! (to be clear, this means any DLL not digitally signed by Mozilla or part of the OS).

Most users are unaware when DLLs are injected into Firefox, as most of the time there’s no obvious indication this is happening, other than checking the [about:third-party page](https://support.mozilla.org/en-US/kb/identify-problems-third-party-modules-firefox-windows).

Unfortunately, having DLLs injected into Firefox can lead to performance, security, or stability problems. This is for a number of reasons:

- DLLs will often hook into internal Firefox functions, which are subject to change from release to release. We make no special effort to maintain the behavior of internal functions (of which there are thousands), so the publisher of the third-party product has to be diligent about testing with new versions of Firefox to avoid stability problems.
- Firefox, being a web browser, loads and runs code from untrusted and potentially hostile websites. Knowing this, we go to a lot of effort to keep Firefox secure; see, for example, the
[Site Isolation Security Architecture](https://hacks.mozilla.org/2021/05/introducing-firefox-new-site-isolation-security-architecture/)and[Improved Process Isolation](https://hacks.mozilla.org/2022/05/improved-process-isolation-in-firefox-100/). Third-party products may not have the same focus on security. - We run an
[extensive number of tests on Firefox](https://hacks.mozilla.org/2020/07/testing-firefox-more-efficiently-with-machine-learning/), and third-party products may not test to that extent since they’re probably not designed to work specifically with Firefox.

Indeed, our data shows that just over 2% of **all** Firefox crash reports on Windows are in third-party code. This is despite the fact that Firefox already blocks a number of specific third-party DLLs that are known to cause a crash (see below for details).

This also undercounts crashes that are caused indirectly by third-party DLLs, since our metrics only look for third-party DLLs directly in the call stack. Additionally, third-party DLLs are a bit more likely to cause crashes at startup, which are much more serious for users.

Firefox has a [third-party injection policy](https://www.mozilla.org/en-US/security/third-party-software-injection/), and whenever possible we recommend third parties instead use [extensions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions) to integrate into Firefox, as this is officially supported and much more stable.

## Why not block all DLL injection by default?

For maximum stability and performance, Firefox could try to block all third-party DLLs from being injected into its processes. However, this would break some useful products like screen readers that users want to be able to use with Firefox. This would also be technically challenging and it would probably be impossible to block every third-party DLL, especially third-party products that run with higher privilege than Firefox.

Since 2010, Mozilla has had the ability to block specific third-party DLLs for all Windows users of Firefox. We do this only as a last resort, after trying to communicate with the vendor to get the underlying issue fixed, and we tailor it as tightly as we can to make Firefox users stop crashing. (We have the ability to only block specific versions of the DLL and only in specific Firefox processes where it’s causing problems). This is a helpful tool, but we only consider using it if a particular third-party DLL is causing lots of crashes such that it shows up on our list of top crashes in Firefox.

Even if we know a third-party DLL can cause a crash in Firefox, there are times when the functionality that the DLL provides is essential to the user, and the user would not want us to block the DLL on their behalf. If the user’s bank or government requires some software to access their accounts or file their taxes, we wouldn’t be doing them any favors by blocking it, even if blocking it would make Firefox more stable.

## Giving users the power to block injected DLLs

With Firefox 110, users can block third-party DLLs from being loaded into Firefox. This can be done on the [about:third-party page](https://support.mozilla.org/en-US/kb/identify-problems-third-party-modules-firefox-windows), which already lists all loaded third-party modules. The about:third-party page also shows which third-party DLLs have been involved in previous Firefox crashes; along with the name of the publisher of the DLL, hopefully this will let users make an informed decision about whether or not to block a DLL. Here’s an example of a DLL that recently crashed Firefox; clicking the button with a dash on it will block it:

![Screenshot of the about:third-party page showing a module named "CrashingInjectibleDll.dll" with a yellow triangle indicating it has recently caused a crash, and a button with a dash on it that can be used to block it from loading into Firefox.](../../assets/29c199f305d88926.png)


Here’s what it looks like after blocking the DLL and restarting Firefox:

![Screenshot of the about:third-party page showing a module named "CrashingInjectibleDll.dll" with a yellow triangle indicating it has recently caused a crash, and a red button with an X on it indicating that it is blocked from loading into Firefox.](../../assets/9211c4c4e7c54ac5.png)


If blocking a DLL causes a problem, launching Firefox in [Troubleshoot Mode](https://support.mozilla.org/en-US/kb/diagnose-firefox-issues-using-troubleshoot-mode) will disable all third-party DLL blocking for that run of Firefox, and DLLs can be blocked or unblocked on the about:third-party page as usual.

## How it works

Blocking DLLs from loading into a process is tricky business. In order to detect all DLLs loading into a Firefox process, the blocklist has to be set up very early during startup. For this purpose, we have the [launcher process](https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html#launcher-process), which creates the main browser process in a suspended state. Then it sets up any sandboxing policies, loads the blocklist file from disk, and copies the entries into the browser process before starting that process.

The copying is done in an interesting way: the launcher process creates an OS-backed file mapping object with [ CreateFileMapping()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-createfilemappingw), and, after populating that with blocklist entries, duplicates the handle and uses

[to write that handle value into the browser process. Ironically,](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory)

`WriteProcessMemory()`

`WriteProcessMemory()`

is often used as a way for third-party DLLs to inject themselves into other processes; here we’re using it to set a variable at a known location, since the launcher process and the browser process are run from the same .exe file!Because everything happens so early during startup, well before the Firefox profile is loaded, the list of blocked DLLs is stored per Windows user instead of per Firefox profile. Specifically, the file is in `%AppData%\Mozilla\Firefox`

, and the filename has the format `blocklist-{install hash}`

, where the install hash is a [hash](https://github.com/google/cityhash) of the location on disk of Firefox. This is an easy way of keeping the blocklist separate for different Firefox installations.

### Detecting and blocking DLLs from loading

To detect when a DLL is trying to load, Firefox uses a technique known as function interception or hooking. This modifies an existing function in memory so another function can be called before the existing function begins to execute. This can be useful for many reasons; it allows changing the function’s behavior even if the function wasn’t designed to allow changes. [Microsoft Detours](https://github.com/microsoft/Detours) is a tool commonly used to intercept functions.

In Firefox’s case, the function we’re interested in is [ NtMapViewOfSection()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-zwmapviewofsection), which gets called whenever a DLL loads. The goal is to get notified when this happens so we can check the blocklist and forbid a DLL from loading if it’s on the blocklist.

To do this, Firefox uses a [homegrown function interceptor](https://searchfox.org/mozilla-central/source/toolkit/xre/dllservices/mozglue/nsWindowsDllInterceptor.h) to intercept calls to `NtMapViewOfSection()`

and return that the mapping failed if the DLL is on the blocklist. To do this, the interceptor tries two different techniques:

- On the 32-bit x86 platform,
[some functions exported from a DLL](https://devblogs.microsoft.com/oldnewthing/20110921-00/?p=9583)will begin with a two-byte instruction that does nothing (`mov edi, edi`

) and have five one-byte unused instructions before that. (either`nop`

or`int 3`

) For example:nop nop nop nop nop DLLFunction: mov edi, edi (actual function code starts here)

If the interceptor

[detects that this is the case](https://searchfox.org/mozilla-central/source/toolkit/xre/dllservices/mozglue/interceptor/PatcherNopSpace.h#147), it can replace the five bytes of unused instructions with a`jmp`

to the address of the function to call instead. (since we’re on a 32-bit platform, we just need one byte to indicate a jump and four bytes for the address) So, this would look likejmp <address of Firefox patched function> DLLFunction: jmp $-5 # encodes in two bytes: EB F9 (actual function code starts here)

When the patched function wants to call the unpatched version of

`DLLFunction()`

, it simply jumps 2 bytes past the address of`DLLFunction()`

to start the actual function code. - Otherwise, things get a bit more complicated. Let’s consider the x64 case. The instructions to jump to our patched function require 13 bytes: 10 bytes for loading the address into a register, and 3 bytes to jump to that register’s location. So the interceptor needs to move at least the first 13 bytes worth of instructions, plus enough to finish the last instruction if needed, to a trampoline function. (it’s known as a trampoline because typically code jumps there, which causes a few instructions to run, and then jumps out to the rest of the target function). Let’s look at a real example. Here’s a simple function that we’re going to intercept, first the C source (
[Godbolt compiler explorer link](https://godbolt.org/#g:!((g:!((g:!((h:codeEditor,i:(filename:'1',fontScale:14,fontUsePx:'0',j:2,lang:c%2B%2B,selection:(endColumn:2,endLineNumber:8,positionColumn:1,positionLineNumber:3,selectionStartColumn:2,selectionStartLineNumber:8,startColumn:1,startLineNumber:3),source:'%23include+%3Cstdio.h%3E%0A%0Aint+fn(int+aX,+int+aY)+%7B%0A++++if+(aX+%2B+1+%3E%3D+aY)+%7B%0A++++++++return+aX+*+3%3B%0A++++%7D%0A++++return+aY+%2B+5+-+aX%3B%0A%7D%0A'),l:'5',n:'0',o:'C%2B%2B+source+%232',t:'0')),header:(),k:48.35219031041486,l:'4',m:100,n:'0',o:'',s:0,t:'0'),(g:!((h:compiler,i:(compiler:clang1500,deviceViewOpen:'1',filters:(b:'0',binary:'1',binaryObject:'0',commentOnly:'0',demangle:'0',directives:'0',execute:'1',intel:'0',libraryCode:'0',trim:'1'),flagsViewOpen:'1',fontScale:14,fontUsePx:'0',j:2,lang:c%2B%2B,libs:!(),options:'-O3',selection:(endColumn:16,endLineNumber:3,positionColumn:16,positionLineNumber:3,selectionStartColumn:16,selectionStartLineNumber:3,startColumn:16,startLineNumber:3),source:2),l:'5',n:'0',o:'+x86-64+clang+15.0.0+(Editor+%232)',t:'0')),header:(),k:51.64780968958515,l:'4',m:100,n:'0',o:'',s:0,t:'0')),l:'2',n:'0',o:'',t:'0')),version:4)):int fn(int aX, int aY) { if (aX + 1 >= aY) { return aX * 3; } return aY + 5 - aX; }

and the assembly, with corresponding raw instructions. Note that this was compiled with -O3, so it’s a little dense:

fn(int,int): lea eax,[rdi+0x1] # 8d 47 01 mov ecx,esi # 89 f1 sub ecx,edi # 29 f9 add ecx,0x5 # 83 c1 05 cmp eax,esi # 39 f0 lea eax,[rdi+rdi*2] # 8d 04 7f cmovl eax,ecx # 0f 4c c1 ret # c3

Now, counting 13 bytes from the beginning of

`fn()`

puts us in the middle of the`lea eax,[rdi+rdi*2]`

instruction, so we’ll have to copy everything down to that point to the trampoline.The end result looks like this:

fn(int,int) (address 0x100000000): # overwritten code mov r11, 0x600000000 # 49 bb 00 00 00 00 06 00 00 00 jmp r11 # 41 ff e3 # leftover bytes from the last instruction # so the addresses of everything stays the same # We could also fill these with nop’s or int 3’s, # since they won’t be executed .byte 04 .byte 7f # rest of fn() starts here cmovl eax,ecx # 0f 4c c1 ret # c3 Trampoline (address 0x300000000): # First 13 bytes worth of instructions from fn() lea eax,[rdi+0x1] # 8d 47 01 mov ecx,esi # 89 f1 sub ecx,edi # 29 f9 add ecx,0x5 # 83 c1 05 cmp eax,esi # 39 f0 lea eax,[rdi+rdi*2] # 8d 04 7f # Now jump past first 13 bytes of fn() jmp [RIP+0x0] # ff 25 00 00 00 00 # implemented as jmp [RIP+0x0], then storing # address to jump to directly after this # instruction .qword 0x10000000f Firefox patched function (address 0x600000000): <whatever the patched function wants to do>

If the Firefox patched function wants to call the unpatched

`fn()`

, the patcher has stored the address of the trampoline (0x300000000 in this example). In C++ code we encapsulate this in theclass, and the patched function can just call the trampoline with the same syntax as a normal function call.`FuncHook`

This whole setup is significantly more complicated than the first case; you can see that the

[patcher for the first case](https://searchfox.org/mozilla-central/source/toolkit/xre/dllservices/mozglue/interceptor/PatcherNopSpace.h)is only around 200 lines long while the[patcher that handles this case](https://searchfox.org/mozilla-central/source/toolkit/xre/dllservices/mozglue/interceptor/PatcherDetour.h)is more than 1700 lines long! Some additional notes and complications:- Not all instructions that get moved to the trampoline can necessarily stay exactly the same. One example is jumping to a relative address that didn’t get moved to the trampoline – since the instruction has moved in memory, the patcher needs to replace this with an absolute jump. The patcher doesn’t handle every kind of x64 instruction (otherwise it would have to be much longer!), but we have
[automated tests](https://searchfox.org/mozilla-central/source/toolkit/xre/dllservices/tests/TestDllInterceptor.cpp)to make sure we can successfully intercept the Windows functions that we know Firefox needs. - We specifically use r11 to load the address of the patched function into because according to the
[x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170), r11 is a volatile register that is not required to be preserved by the callee. - Since we use
`jmp`

to get from`fn()`

to the patched function instead of`ret`

, and similarly to get from the trampoline back into the main code of`fn()`

, this keeps the code stack-neutral. So calling other functions and returning from`fn()`

all work correctly with respect to the position of the stack. - If there are any jumps from later in
`fn()`

into the first 13 bytes, these will now be jumping into the middle of the jump to the patched function and bad things will almost certainly happen. Luckily this is very rare; most functions are doing function prologue operations in their beginning, so this isn’t a problem for the functions that Firefox intercepts. - Similarly, in some cases
`fn()`

has some data stored in the first 13 bytes that are used by later instructions, and moving this data to the trampoline will result in the later instructions getting the wrong data. We have[run into this](https://bugzilla.mozilla.org/show_bug.cgi?id=1489391), and can work around it by using a shorter`mov`

instruction if we can allocate space for a trampoline that’s within the first 2 GB of address space. This results in a 10 byte patch instead of a 13 byte patch, which in many cases is good enough to avoid problems. - Some other complications to quickly mention (not an exhaustive list!):
- Firefox also has a way to do this interception across processes. Fun!
- Trampolines are tricky for the
[Control Flow Guard](https://learn.microsoft.com/en-us/windows/win32/secbp/control-flow-guard)security measure: since they are legitimate indirect call targets that do not exist at compile time, it requires special care to allow Firefox patched functions to call into them. - Trampolines also involve some more fixing up for exception handling, as we must provide
[unwind info](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170)for them.


- Not all instructions that get moved to the trampoline can necessarily stay exactly the same. One example is jumping to a relative address that didn’t get moved to the trampoline – since the instruction has moved in memory, the patcher needs to replace this with an absolute jump. The patcher doesn’t handle every kind of x64 instruction (otherwise it would have to be much longer!), but we have

If the DLL is on the blocklist, our patched version of `NtMapViewOfSection()`

will return that the mapping fails, which causes the whole DLL load to fail. This will not work to block every kind of injection, but it does block most of them.

One added complication is that some DLLs will inject themselves by modifying firefox.exe’s [Import Address Table](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#import-address-table), which is a list of external functions that firefox.exe calls into. If one of these functions fails to load, Windows will terminate the Firefox process. So if Firefox detects this sort of injection and wants to block the DLL, we will instead redirect the DLL’s `DllMain()`

to a function that does nothing.

## Final words

Principle 4 of the [Mozilla Manifesto](https://www.mozilla.org/en-US/about/manifesto/) states that “Individuals’ security and privacy on the internet are fundamental and must not be treated as optional”, and we hope that this will give Firefox users the power to access the internet with more confidence. Instead of having to choose between uninstalling a useful third-party product and having stability problems with Firefox, now users have a third option of leaving the third-party product installed and blocking it from injecting into Firefox!

As this is a new feature, if you have problems with blocking third-party DLLs, please file [a bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=DLL%20Services). If you have issues with a third-party product causing problems in Firefox, please don’t forget to file an issue with the vendor of that product – since you’re the user of that product, any report the vendor gets means more coming from you than it does coming from us!

## More information

[Technical documentation about DLL blocklisting](https://firefox-source-docs.mozilla.org/widget/windows/blocklist.html)[An Empirical Study of DLL Injection Bugs in the Firefox Ecosystem](https://marco-c.github.io/publications/dll_injection-emse2019.pdf)(.pdf)

Special thanks to David Parks and Yannis Juglaret for reading and providing feedback on many drafts of this post and Toshihito Kikuchi for the initial prototype of the dynamic blocklist.

## One comment

HalesMarch 31st, 2023 at 20:39