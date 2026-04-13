---
title: How to Properly Setup Git for Unreal Engine, Unity and Godot Projects
url: https://alfredbaudisch.com/gamedev/how-to-properly-setup-git-for-unreal-engine-unity-and-godot-projects/
author: Alfred Reinold Baudisch
published: '2022-08-12'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In order to have a Git repository for a game development project, the repository must be properly set with [Git LFS](https://git-lfs.github.com/), otherwise Git is going to make full copies of binary files. With Git LFS you can also version control huge files (in the size of GBs).

But it can be tricky to understand the correct workflow to setup Git LFS, also it's common to add LFS to a repository but incorrectly track binary files with the normal Git workflow instead of LFS (due to wrong setup order and incorrect `lfs track`

).

Before we move forward, understand that **when I talk about "binary files" I mean "assets" (meshes, textures, sounds, etc.), anything that is not source-code**. In the case of Unreal Engine, everything is an asset, including Blueprints (because BP files are binaries) – with the exception of C++ files, of course.

When using Git LFS, your commits will point to a lightweight reference object instead of pointing back to the binary file (you're actually pushing the original binary file to an LFS repo).


## Setup

If you still don't have a Git repository set in your project folder, initialize the repository and install LFS.

```
git init
git lfs install
```


Track the folders and subfolders that will contain binary assets. To track a parent folder and all of its children and subfolders recursively add two "**":

```
\# Unreal Engine:
git lfs track "Content/**"
# Godot (as long as you keep only binary files
# inside the folder "Assets" and its subfolders. Adjust accordingly):
git lfs track "Assets/**"
# Unity: check the special section below in the article, grab
# Unity's .gitattributes template instead of calling lfs track manually
```


If you are going to have source-code files in any of the sub-folders of your Assets/Content folder, then you have to manually call `git lfs track`

for each of the binary folders (ex: `Assets/Meshes/**`

) or binary file types (ex: `*.fbx`

).

In this case, instead of doing this, which can be error prone, I recommend keeping source-code files in another root folder, away from the assets root folder. Check [Tracking files with Git LFS](https://www.atlassian.com/git/tutorials/git-lfs#tracking-files) for more options.

Example:

```
Project/
-- Content/
---- Assets/ (track with LFS: git lfs track "Content/Assets/**")
---- Scripts/ (Non-LFS, normal Git)
```


Then **before adding any other file, you must add and commit the .gitattributes file** (this is where it's common to mess up):

```
git add .gitattributes
git commit -m "LFS attributes"
```


![](../../assets/cd9769f1a3fa2ee0.png)


![](../../assets/cd9769f1a3fa2ee0.png)

## Adding Binary Files and Tracking LFS Status

Add files normally, for example: `git add .`

or `git add Content/Specific/File.fbx`

.

Then you can track whether they are being treated as LFS or not with:

```
git lfs status
```


Files tracked as LFS will have their paths appended by `(LFS: <id>)`

.

You can also list LFS files with:

```
git lfs ls-files
```


If a binary file does not appear in these lists, they are going to be incorrectly treated in the main Git workflow, not taking advantage of LFS.

## Git GUI Clients and LFS

After LFS is set, you can normally use Git GUI Clients in your workflow, no need to further use the command line. I personally use [SmartGit](https://www.syntevo.com/smartgit/), which has [LFS support](https://docs.syntevo.com/SmartGit/Latest/Git-LFS.html).

## Special Unity Setup

Unity offers a special tool to merge scene and prefab files, "[Smart Merge](https://docs.unity3d.com/Manual/SmartMerge.html)".

Open your global `.gitconfig`

file or your project's `.git`

file and add (see [the docs](https://docs.unity3d.com/Manual/SmartMerge.html) to find out where `UnityYAMLMerge`

is located):

```
[merge]
tool = unityyamlmerge
[mergetool "unityyamlmerge"]
trustExitCode = false
cmd = '<path to UnityYAMLMerge>' merge -p "$BASE" "$REMOTE" "$LOCAL" "$MERGED"
```


Project Settings:

![](../../assets/350e829ed33a2ce0.png)


![](../../assets/b0fc24401e3c2cb1.png)


## Further Info

Because git LFS hashes the file to determine its identity, identical files in multiple repos will all point to the same place in memory, like a symbolic link/fancier shortcut.

It makes a huge difference, *especially* if you're indie and parched for disk space.

— 🐑🐑🐑🐑🐑🐑🐑 (@GorduneDelaine)

[August 13, 2022]