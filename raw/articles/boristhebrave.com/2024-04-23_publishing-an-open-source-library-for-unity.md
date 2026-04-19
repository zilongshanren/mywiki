---
title: Publishing An Open-Source Library for Unity
url: https://www.boristhebrave.com/2024/04/23/publishing-an-open-source-library-for-unity/
author: Boris
published: '2024-04-23'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

So you’ve got some open source C# code, and you want to publish it for other users in Unity? I’ve explored a few options, here are the pros and cons.

Table of Contents

GitHub lets you serve arbitrary files that are not part of the repository as part of it’s Releases feature. You can publish a cross platform .dll, or the full source code, or both. I use this for [DeBroglie](https://github.com/BorisTheBrave/DeBroglie/releases).

Install instructions for users are “Download this and drop it in your Assets folder”.

This is extremely easy to set up, and works basically fine 1. You don’t get dependency management or much by way of versioning, but do your users really use those things?

Also, if you are deploying a compiled dll you cannot take advantage of conditional compilation, and need a separate dll for the editor. You can have Unity components in a dll, but they are not interchangable with the same components defined in a source file due to how .meta files work, making them tricky to debug or work with.

I recommend this approach for fairly simple source distributions, or dlls that do not depend on Unity.

NuGet is the normal C# package manager. It’s more or less impossible to get this operating with Unity. I only publish here for “dual-use” libraries that can be compiled free of unity dependencies. Not recommended.

While convenient for users, publishing to the asset store is extremely tedious. Not recommended for free assets. It’s the only option for paid assets that integrates into the Editor, of course.

“[Asset Packages](https://docs.unity3d.com/Manual/upm-package-types.html)” are the old style of package, used internally by the Asset Store. They’re more or less just a file with the extension .unitypackage which contains a collection of files inside. They can be imported/exported in the assets menu with these items, and unpack into the Assets/ folder.

![](../../assets/6729c4ae4a0f4b32.png)

They’re pretty simple, but there aren’t good tools to work with them automatically. So they really have little advantage over a zip file. Not recommended.

The new style of packages is Unity Package Manager packages 2. This format is a bit flexible. It’s basically a directory with a

[package.json manifest](https://docs.unity3d.com/Manual/upm-manifestPkg.html), and optionally a

[recommended directory layout](https://docs.unity3d.com/Manual/cus-layout.html)for other details.

The manifest contains the sort of metadata you’d expect a package to have. In particular, UPM is the only format that supports dependencies between packages 3, which is a must if you have a lot of projects that share code.

All files in the UPM package are dumped into a subfolder of the Packages/ folder. Annoyingly, Unity treats everything in the packages folder as an asset, meaning that other distributed files such as documentation need to be in folders marked with a ~ to get Unity to ignore them. It’s a bit ugly.

UPM packages can be directly loaded from the package manager.

![](../../assets/4ea410796d09de62.png)

As you can see, they can be loaded from disk (usually used when developing a package), from tarball (a form of zipping, not dissimilar to .unitypackage distribution), and from a git URL.

The latter is how many developers like to deploy things. As long as you have the files pushed to github (or other public git host), you don’t need do any release process at all. You can just point users at the github url.

I think this works for ultra lightweight publishing, but it has some issues if you want to do a good job:

- It is conflating source files with release files. For a lot of things, that’s ok, but if you have any source preprocessing, or doc generation, it leads to trouble.
- It becomes awkward if the upm package is not at the root of the git repo, as this is only
[supported](https://docs.unity3d.com/Manual/upm-git.html#subfolder)from later versions of unity.

I recommend if you are looking for hassle free, and the above are not dealbreakers.

Another option for loading UPM files is via a “scoped registry”. This works a bit like alternative Asset Stores. They look like this.

![](../../assets/e25df79286cdbd55.png)

![](../../assets/b72d976b519b1674.png)

You can set up your own registry, but in practise, it’s easiest to publish to OpenUPM which already exists, and comes with a nice website and CLI tool as added conveniences for users using a registry. It gives [step by step instructions ](https://openupm.com/packages/com.boristhebrave.sylves/#modal-manualinstallation)for how to install a package, which is good as it’s not obvious.

OpenUPM has some [additional requirements for publishing](https://openupm.com/docs/adding-upm-package.html#handling-monorepo) to their registry. But they’re things like having [semver](https://semver.org/) and a license, which you’ll probably be doing anyway.

OpenUPM expects you to use tags to indicate actual released versions, which I quite like as it means not every push to github is immediately released. But it is one more step of process.

Recommended.

Finally, we’re reaching the solution I’ve used for [Sylves](https://github.com/BorisTheBrave/sylves). I like OpenUPM, but I refuse to make my source repo confirm to Unity’s layout. This turns out to be straighforward.

I have all my source files in git, on the [main branch](https://github.com/BorisTheBrave/sylves/tree/main/). When I want to release, I compile the documentation, preprocess source files, put together the package.json file, and so forth, and arrange everything in the UPM format in a separate directory. I then push that directory as a separate git commit, in a different branch, [upm](https://github.com/BorisTheBrave/sylves/tree/upm). That way I have complete control over what is published. I’ve a [short python script](https://github.com/BorisTheBrave/sylves/blob/main/upm_release.py) to do the whole thing.

(NB: the upm branch is an [orphan](https://stackoverflow.com/questions/34100048/create-empty-branch-on-github) so it does not share history with the main branch. They are separate, but live in the same repo).

Your choice probably depends on the size of project.

- Dead simple, no dependencies
**→**share the files, e.g. in GitHub releases.

- Project is complex, but you don’t want to waste time with release processes
**→**Use[the recommended layout](https://docs.unity3d.com/Manual/cus-layout.html), push to github, and share the github url.

- Gold standard
**→**Push to OpenUPM so it can be used as a scoped registry or a github url. Potentially separating source and release layouts.

Not many developers actually use UPM as it’s still new and the package manager is not as intuitive as dropping a file in the Assets folder. So consider offering both:

![](../../assets/2e75c7928b97cc5b.png)

After publishing a few projects, I’ve realized there are some extra bits you should be aware of while working with unity packages.

If you are using a method where the resulting files goes in the users Assets/ folder, then users may not like Unity’s default behaviour of putting things in the root. They will want to move it to a subdirectory. Be careful to make your project relocatable. The main gotcha here is paths to resource files. Use a subdirectory called Resources/ as these are all considered root paths by Unity regardless of where they are located.

[Assembly Definition files](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html) give Unity instructions on how to build your package into a separate assembly from the rest of the users game. This can offer a small boost to compilation, and is organizationally neater. A few of my users asked me to set these up.

You’ll need a separate asmdef for Editor source code, and they have some configurable features that are useful. But largely they are create once and forget.

If you are deploying dlls rather than source code, then you need to worry about platforms. A single .NET dll will already run perfectly on Mac/Windows/Linux. But make sure you build the dll targetting “.NET Standard 2.0” as this maximizes the Unity build options that can use your .dll.

I’ve also made my library Sylves truly cross platform – it compiles separate versions for Unity, Godot and .NET. But how I managed that is a question for another article.

With Asset Packages (including via the Asset Store), when updating a package, Unity naively just dumps the new files, overwriting old ones. It has no mechanism for cleaning up old files. For source code, that’s crippling, as the old and new will define the same class.

I’ve usually left empty source files in place to avoid this problem. I delete them during major version changes.

I think UPM solves this problem, as the Packages/ directory is immutable and thus safe for Unity to delete. Would be useful if someone could confirm?

- Although see the caveat on deleting/renaming at the bottom of the article
[↩︎](https://www.boristhebrave.com#5366bfdb-3431-4ed4-9239-6c569251aaa7-link) - Fresh from the
[Department of Redundancy Department](http://www.alexandraerin.com/2015/05/fiction-the-redundant-man-who-was-redundant/)[↩︎](https://www.boristhebrave.com#1e04e326-2a9a-41dd-a5ab-2df8accdc561-link) - You cannot do dependencies from a git-referenced package to another git referenced package for some reason. You need to use scoped registries for that.
[↩︎](https://www.boristhebrave.com#ab683f3a-78cd-4113-b83a-7d3beb73217b-link)