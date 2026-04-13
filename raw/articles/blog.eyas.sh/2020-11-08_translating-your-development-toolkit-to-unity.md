---
title: Translating your Development Toolkit to Unity
url: https://blog.eyas.sh/2020/11/unity-for-engineers-pt8-tooling/
author: Eyas Sharaiha
published: '2020-11-08'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Whether you’re a backend, UI, web, or full-stack developer, much of the Software Development toolkit looks similar. Even when the exact tools are different, the toolkit translates intuitively between fields: version control systems, debugging and profiling tools, editors and language servers, and package managers work together similarly. What do these tools like when developing software and games with Unity? We’ll dive into this today.

*Welcome to another installment of
Unity for Software Engineers (now
updated and available as a book), a
series for those seeking an accelerated introduction to game development in
Unity. More is coming over the next few weeks, so
consider subscribing.*

Unity—as a proprietary, closed source 1 Engine—is a walled garden
of sorts For better or worse. You’re often given an entire ecosystem of tools
made

*by*Unity Technologies that fill the end-to-end needs of a game developer, from an editor, build system, profiling, and debugging system, to a package manager, UI styling language

, version control system, etc. Sometimes, using the tools you know and love is relatively easy, but at others, interoperability is less than ideal. One advantage of walled gardens is that they often offer an optimized experience. The disadvantage, of course, is that interoperability and choice are lacking. This article will show which parts of Unity can fulfill your needs and which tools outside Unity can interoperate well.

[2](https://blog.eyas.sh#user-content-fn-2)## Version Control

Unity Technologies now offers a single integrated solution: **Unity Version
Control** (formerly PlasticSCM).

Unity Version Control is derived from Plastic SCM (acquired by Unity in 2020)
and serves as the standard solution for handling large Unity projects with
binary assets. **Unity Collaborate**, the previous built-in tool, has been
deprecated and replaced.

Unity Version Control provides branching support and handles large binary files efficiently, making it more robust than the old Collaborate tool.

The two advantages of Collaborate and PlasticSCM are:

- They work well with large binary files, and
- They are intuitive for someone not familiar with other VCS.

You might not even care about the size of your repository *vis a vis* handling
large binary files. If you do, with traditional VCS, you can either choose SVN,
which has a better handle on non-text files, or something like
[Git LFS](https://git-lfs.github.com/). Similarly, if you’re working solo (or
with a small team of other folks comfortable with whatever your VCS of choice
is), then you can choose your favorite version control system.

### Using Git with Unity

![Photo of a Git Commit Tree](../../assets/bd3af8974b47dd7a.img)

Photo by Yancy Min [via Unsplashed](https://unsplash.com/photos/842ofHC6MaI).

Like
[~80%+ of developers](https://insights.stackoverflow.com/survey/2018#work-_-version-control),
I prefer Git in day-to-day version control. Unity, for its part, works well with
Git.
[Rick Reilly’s “How to Git with Unity”](https://thoughtbot.com/blog/how-to-git-with-unity)
remains the best resource for using Unity with Git. The summary there is:

- Make sure Scenes & Prefabs are serialized on-disk as YAML text files, rather than in a binary format,
[Ignore](https://github.com/github/gitignore/blob/master/Unity.gitignore)the right files,- Optionally, Use GitLFS.

Even with scenes persisted as text, note that large scenes might result in very nasty merge conflicts. A common recommendation I would echo here is to prefab objects early and often. Prefab objects are extracted out of a scene into a separate asset file. The scene merely contains a reference to the prefab, plus any local modifications. This makes it easier to makes sense of merge conflicts with a larger number of small files.

## Package Management

As I’ve discussed in
[my piece on the new Unity Input System package](https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system),
much of the Unity Engine’s more recent pieces are released as modularized
[packages](https://docs.unity3d.com/Manual/PackagesList.html). Unity packages
are installed from the *Unity Package Manager* UI in the editor (open it in
*Window > Package Manager*). The package updates a `manifest.json`

file that has
a `"dependencies"`

entry identical to a
[ package.json](https://docs.npmjs.com/files/package.json#dependencies). The
package manager resolves dependencies and writes to a

`package-lock.json`

.As far as I’m aware, you’re expected to entirely manage your project’s packages
from the Unity Editor UI (in the *Package Manager* window). The package manager
can browse and install various packages from various *registries*. By default,
the package manager only knows about the official Unity Technologies registry.

Projects like [OpenUPM](https://openupm.com/) introduce *both* an ergonomic CLI
for UPM *and* a package registry for Unity. I highly recommend getting OpenUPM.

If you’re familiar with .NET, the prevalent .NET package manager is
[NuGet](https://www.nuget.org/). You can’t directly download NuGet packages into
Unity. Instead, you’ll have to download those manually and put the DLLs in the
right place. [Some projects](https://github.com/GlitchEnzo/NuGetForUnity) exist
that attempt to make the NuGet picture more compelling, but this process is
parallel to Unity’s package system. You might want to resort to NuGetForUnity if
you’re considering relying on seminal packages, not in the .NET BCL, such as
[System.Collection.Immutable](https://docs.microsoft.com/en-us/dotnet/api/system.collections.immutable).

## Editors & Debugging

You can use your IDE / Editor of Choice to edit the C# code in your project. If
you would like intelligent completions and recommendations, your editor will
need to be aware of Unity-specific magic (e.g., uncalled private Unity message
functions *will* end being called). Unity provides integrations with two
editors:

These integrations are implemented as *Unity Packages*. To use a specific
Editor:

- Make sure it is already installed,
- Make the integration package is installed,
- From
*Edit > Preferences > External Tools > External Script Editor*, choose your editor of choice.

In addition, VS Code, which used to be supported directly by Unity, is
officially supported by Microsoft via the
** C# Dev Kit**
and

**.**

[Unity Extension](https://marketplace.visualstudio.com/items?itemName=VisualStudioToolsForUnity.vstuc)## Profiling

![Screenshot of the Unity Profiler](../../assets/f5a5c971c57c41f6.img)

The Unity Profiler provides frame-by-frame profiles of CPU, Rendering, Memory, and other performance characteristics of your game. You’ll likely spend time looking at both the timing of your functions in the CPU view, as well as any excess allocations in the game loop that cause excessive GC cycles. In addition to the Timeline view shown above, a Hierarchy view is also available from the drop-down.

Unity has a built-in profiler that analyzes the runtime and heap allocations on
a frame-by-frame basis in your game. Enable it from *Window > Analysis >
Profiler*. It gives you both indications of how CPU-bound your code might be, as
well as how GPU-bound various render logic is.

Unity’s documentation on
[getting started with the profiler](https://docs.unity3d.com/Manual/ProfilerWindow.html)
is probably your best bet.

## Continuous Integration

While Unity provides a
[Cloud Build](https://docs.unity3d.com/Manual/UnityCloudBuild.html) CI service
as part of [Unity Teams](https://unity3d.com/get-teams), you can also roll your
own, which I recommend trying; [unity-ci.com](https://unity-ci.com/) provides
instructions for setting up test and build runs on GitHub, GitLab, and Travis
CI.

## Conclusion

The software engineering toolkit equivalents are often provided *within* the
Unity Editor (or as Unity Technologies -owned solutions/services). Usually, that
provides a tailored end-to-end experience, but it often means that developing on
Unity is an isolated “island” 3 with its tooling and tech.

Do you disagree with some of these recommendations? Let me know! You can join
the discussion on [Twitter](https://twitter.com/EyasSH) or by
[reaching out](https://eyas.sh/).

## Update Notes (2025)

This post was updated in 2025 to reflect ecosystem changes:

**Unity Version Control**: “Unity Collaborate” is deprecated and has been replaced by Unity Version Control (based on Plastic SCM).**VS Code Support**: The old “Unity Debugger” extension is deprecated. The recommended workflow is now the**C# Dev Kit**and the official**Unity Extension**for VS Code.

## Footnotes

-
Unity’s C# code is

[publicly available](https://blogs.unity3d.com/2018/03/26/releasing-the-unity-c-source-code/)under a reference-only license, rather than an open-source license. The core C++ Engine source isn’t available at all.[↩](https://blog.eyas.sh#user-content-fnref-1) -
This isn’t relevant to anything we’re talking about today, but I think it illustrates the point. Unity’s new UI Toolkit has a very HTML-like markup language called UXML and a very CSS-like styling language called USS.

[↩](https://blog.eyas.sh#user-content-fnref-2) -
It

*should*be said that this isn’t much different than, say, UnrealEngine, where you also have an entire ecosystem you can be locked into.[↩](https://blog.eyas.sh#user-content-fnref-3)