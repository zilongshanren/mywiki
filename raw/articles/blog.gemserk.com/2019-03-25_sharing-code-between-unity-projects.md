---
title: Sharing code between Unity projects
url: https://blog.gemserk.com/2019/03/25/sharing-code-between-unity-projects/
published: '2019-03-25'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Over the last months, I was researching, in my spare time, some ideas to reuse code between Unity projects. I was mainly interested in using generic code from Iron Marines in multiple projects we were prototyping at Ironhide.

The target solution in mind was to have something like [NPM](https://www.npmjs.com/) or [Maven](https://maven.apache.org/) where packages are stored in a remote repository, and you can depend on a version of them in any project by just adding a configuration.

Some time ago, Unity added the Unity Package Manager (UPM) which does exactly that, it automatically downloads a list of packages given a dependency configuration. I was really excited with this solution since it goes along the direction I wanted.

*Note: to know more about dependency management follow this link, even though it is about specific dependency manager, it gives the global idea of how they work.*

# Workflow

So, a good workflow would be something like this.

Imagine there are two projects, project A and project B and the first has some useful code we want to use in the second.

In order to do that, project A must be uploaded to the dependency system and tagged with a specific version to be identified, for example, version 0.0.1.

Then, to import that code in project B, we just add a dependency in the package dependency declaration.

```
{
"dependencies": {
"com.gemserk.projectA": "0.0.1"
}
}
```


Suppose we keep working on the project B while someone working on another stuff added a new functionality to project A, and we want it. Since the new feature was released in version 0.0.5 of project A, we need to update the package dependency declaration to depend on it, like this:

```
{
"dependencies": {
"com.gemserk.projectA": "0.0.5"
}
}
```


And that will download it and now project B can access the new feature. That is basically a common workflow.

Since we aren’t Unity, we can’t upload our code to their packages repository (yet?). However, there other are ways to declare dependencies stored elsewhere.

## Depend on a project in the local filesystem

UPM supports [depending on a project stored in the local filesystem](https://forum.unity.com/threads/local-packages.637630/) like this:

```
{
"dependencies": {
"com.gemserk.projectA": "file:../../ProjectA/"
}
}
```


For example, project A is stored in a sibling folder to project B.

```
/Workspace
/ProjectB
/Packages
manifest.json
/ProjectA
```


*Note: There is a great Gist by LotteMakesStuff about this topic and more (thanks Rubén for the link).*

This approach has the advantage of using local projects with any structure, stored anywhere (Git or not, more on that later). It even allows depending on a sub folder of project A, so project A could be a complete Unity project with lots of stuff (test scenes, testing assemblies, etc) but project B only depends on the shared code.

It needs all developers to use a similar folder structure for all the projects and download all of them together to work. Transitive dependencies is not supported by UPM following this approach, so if project A depends on project Zero, project B would never automatically find out.

It has some unexpected behaviors in code, at least in Visual Studio, when editing project A (add new code, refactor, etc) by opening project B solution through Unity. That’s is probably a side effect on how they create the VS solution or may be just a bug.

It doesn’t support versioning. Each time project A is modified, project B will automatically know about the change. This could be an issue if project A changed its API and we don’t want to (or can’t) update project B yet.

## Depend on a Git project

Another option is to use a [link to a Git project](https://forum.unity.com/threads/git-support-on-package-manager.573673/), like this:

```
"dependencies": {
"com.gemserk.projectA": "https://github.com/gemserk/projectA.git",
}
```


Dependencies can be stored directly in Git projects (in Github or any other Git server). It supports depending on a specific commit, branch or tag to simulate versioning, but changing versions should be done by hand since UPM doesn’t show the list of versions like it does with Unity packages.

Since it looks at the root folder, a different Git project is needed for each dependency. This is not necessary a bad thing, but it is not possible to have a Git project with multiple folders, one for each project, something that might be common in some cases, like we did with our [LibGDX projects](https://github.com/gemserk/commons-gdx).

A bigger problem related to this is that project A should have only the code to be used by other projects, otherwise UPM will import everything.

It also lacks support for transitive dependencies since UPM doesn’t process the dependencies declaration of the Git project.

*UPDATE: this is a great tutorial on using git as package provider.*

## Mixing both approaches with Git submodules

There is also a mix using filesystem reference and Git submodules to overcome the versioning disadvantage of the first approach.

For example, project A is downloaded as project B submodule structure pointing to specific branch/tag/commit.

```
/ProjectB_Root
/ProjectB
/Packages/manifest.json
/ProjectA (Git submodule, specific tag)
```


In this way, we have specific versions of project A in each project, and we can share code by uploading it to Git to that submodule and tagging versions. We still have the transitive dependency limitation, and other problems related to Git submodules (more on that later).

## Using a packages repository

The last way is to use a [local or remote package repository](https://forum.unity.com/threads/setup-for-scoped-registries-private-registries.573934/) like Nexus, Artifactory, [NPM](https://forum.unity.com/threads/other-registries-than-unitys-own-already-work-nice.533691/), Verdaccio, etc, and then configure it in the manifest.json:

```
{
"registry": "https://unitypackages.gemserk.com",
"dependencies": {
"com.gemserk.projectA": "0.0.1"
}
}
```


This approach is similar to using Unity’s packages but a remote repository in a private server is needed to share code among developers. It is also possible to upload the code to a public server like NPM. Obviously, a private server need maintenance but I believe it is the long term solution if you have private code you can’t share with the world.

At Gemserk we had our own repository using Nexus and at some point we even uploaded some of our dependencies to Maven central. We configured it when we started making games and probably touched once or twice per year, maintenance wasn’t a problem at all.

I tried to use version range with UPM to see if I can add a dependency to a package 1.0.x and that would automatically download latest 1.0 (for example, 1.0.26) but couldn’t make it work, [not sure if it is not supported yet or I am doing it wrong](https://forum.unity.com/threads/semantic-versioning-like-1-0-x-is-not-working.649774/). *UPDATE: it is not supported yet but it is going to be in the long term plan.*

With this approach, project A is integrated like any Unity’s package and the code is accessible in the VS solution but it can’t be easily modified through project B. Any changes in project A should be made apart, a new version must be uploaded to the repository and then update project B dependency declaration. In some cases this shouldn’t be an issue but, for some development cycles, it could.

*Note: When we used Maven, there was a concept of SNAPSHOT which is a work in progress version that it is overwritten each time it is uploaded to the dependency system and projects depending on it use latest version automatically. That was super useful for development and the reason I tested version ranges with UPM.*

*UPDATE: I tested creating a packages server using Verdaccio and see how UPM interacts with it, and how hard it was to upload a package to the server. It turns out that it is relatively simple, UPM shows the list of available versions and probably get transitive dependencies (didn’t test that yet). I followed this tutorial in case you want to test it too.*

After that initial research and considering some of the current limitations of the UPM, I started looking for other options as well.

## Using Git Submodules without UPM

In this approach, code is imported using a Git submodule in the project B itself.

```
/ProjectB
/Assets
/ProjectA (submodule)
```


Following this approach the code is more integrated, changes can be made and uploaded to that submodule directly from project B. In case there are different versions, project B can depend on specific branch/tag/commit of that submodule too.

Similar to the Git + UPM approach, the submodule should contain only the stuff needed to be reused, otherwise it will import it too since submodules point to the root folder of the Git project. However, since it is integrated in the other projects, it should be easier to edit in some way.

It is an interesting approach but has some [drawbacks as well](https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407), for example, having to update each Git submodule manually by each developer, or the root folder problem.

## Reusing code by hand

There is an ultimate form of reusing code: copy and paste the code from project to project. Even though it is ugly and doesn’t scale at all, it might work when having to do some quick tests. Worst case scenario, create a script to automatically copy from one project o another, maybe using rsync or something like that.

# Conclusion

Whatever the chosen way of sharing code, first it must be decoupled in a nice way and that’s what I’m planning to write about in the next blog post.

That was my research for now, there are a lot of links to keep digging in the UPM solution. I hope they keep improving it to support transitive dependencies for filesystem and git approaches and version ranges.