---
title: Distributing Svelto through OpenUPM - Seba's Lab
url: https://www.sebaslab.com/distributing-svelto-through-openupm/
author: Sebastiano Mandalà
published: '2020-01-12'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

The [Unity Package Manager](https://docs.unity3d.com/Manual/upm-ui.html) is a good effort from Unity to distribute project dependencies similarly to what [NPM does](https://www.w3schools.com/whatis/whatis_npm.asp). UPM is still in its infancy and some problems are to be addressed, among them the conflicts arising from common .net dll is the problem that annoys me the most.

Currently, Unity doesn’t provide a centralised registry where to find 3rd party projects. As workaround UPM leverages on the fact that [it can import git projects as well](https://www.patreon.com/posts/25070968). This feature, while extremely useful, is limited as well. For example, a *package.json* cannot reference a hard dependency to another git repository, [unless external plugins are used](https://www.patreon.com/posts/25070968).

Since I need this option to link automatically *Svelto.Common* to *Svelto.ECS *and *Svelto.Tasks*, I decided to accept the invite to use [OpenUPM](https://openupm.com/docs/#how-it-works). I have zero experience with NPM and therefore I had to understand it from scratch. At first it’s not super intuitive, but it does the job.

### The problem with .net dll dependencies

Like UPM, OpenUPM cannot automatically download external .net dlls and resolve possible conflicts. I hope the helpful author will introduce this feature as there is a chance that soon Svelto.Common and Svelto.ECS will depend on *System.Runtime.CompilerServices.Unsafe.dll* and potentially on *System.Buffers* and *System.Memory* too.

Currently adding *System.Runtime.CompilerServices.Unsafe.dll* directly in the code folder can result in conflicts with the same dll used by other packages. For example *Unity.Collections* uses it and Unity will refuse to compile if the same dll is found in two different folders. Workarounds to this problem exist, but they are awkward.

### Updates are automatically available

One important benefit of using OpenUPM is that once the package is installed, it works like a normal Unity package. Updates do not need to be manually tracked, but they will be available as they are released.

### Svelto.ECS and Svelto.Tasks on OpenUPM

[Svelto.ECS and Svelto.Tasks can now be installed in Unity using OpenUPM](https://openupm.com/packages/topics/dots/). In order to do so, [please follow this simple tutorial](https://openupm.com/docs/). For the first time use, you will need to download a [command line tool (which needs node.js , follow the instructions on github)](https://github.com/openupm/openupm-cli), but it’s very simple. Once the package you choose is downloaded, the command line tool won’t need to be used anymore, unless you want to install another package from the OpenUPM registry.

### Install Svelto.ECS through OpenUPM for the first time

Once you have downloaded the CLI tool, open your project and follow these instructions:

# Enter your unity project folder $ cd YOUR_UNITY_PROJECT_FOLDER # Install package $ openupm add com.sebaslab.svelto.ecs

Once done, you will find Svelto as part of your packages

![](https://i1.wp.com/www.sebaslab.com/wp-content/uploads/2020/01/image.png?fit=600%2C239)

From now on Svelto.ECS and Svelto.Common will be automatically updated when new releases are deployed.

### Deploy new releases with OpenUPM

This paragraph is not important for the final user and I wrote it in case you are thinking to use OpenUPM too. There are a couple of annoying bits to the deployment process: first one is Unity related. All the packages need to ship with the relative meta files which is problematic for a platform agnostic library like Svelto is. I don’t want to force people using c#, but not Unity, to manage meta files that they won’t need. To solve this problem, the standard solution is to create a UPM dedicated git branch. From now on Svelto.ECS, Svelto.Common and Svelto.Tasks will have UPM branches dedicated to Unity.

The second issue is due to the OpenUPM deployment process itself. At the moment is still too easy to make mistakes if the release is deployed manually. I hope the author will introduce some tools for simple projects like Svelto which don’t use any kind of automatic deployment (neither I intend to spend time in researching how to add one).

The OpenUPM steps to deploy a new release are currently:

- bump the release version inside the package.json
- create a new git release that
*must match*the version in the package.json. Luckily a release can be created from any branch.

Hi SEBASTIANO, Thanks for writing a blog to share your experience with UPM and OpenUPM. Related improvements have been made since our long conversation OpenUPM build pipelines can detect the path of package.json automatically now. OpenUPM build pipelines will delete the failed build if the git tag is removed or re-tagged. For example, you created tag 1.0.1 but forget to update the version of package.json. This will cause the build pipelines failed with reason package conflict. Then you fixed the issue and re-tagged 1.0.1. The build pipeline will process it correctly. But the build pipelines will do nothing for already… Read more »