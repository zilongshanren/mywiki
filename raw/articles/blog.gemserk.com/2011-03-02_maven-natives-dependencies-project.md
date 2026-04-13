---
title: Maven Natives Dependencies Project
url: https://blog.gemserk.com/2011/03/02/maven-natives-dependencies-project/
published: '2011-03-02'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

[Mavennatives project](https://code.google.com/p/mavennatives/) is composed by a Maven plug-in and an Eclipse plug-in we developed in order to simplify working with natives dependencies.

The [Maven plug-in](https://code.google.com/p/mavennatives/#maven-nativedependencies-plugin) unpacks every dependency with a classifier beginning with “natives-“. By default its executed in the package phase, and unpacks in the `target/natives`

directory.

The [Eclipse plug-in](https://code.google.com/p/mavennatives/#Eclipse_Plugin) automatically executes the Maven plug-in and configures the `java.library.path`

for Eclipse projects with natives dependencies. This makes working with natives dependencies transparent and you can use the Run menu without having to set `java.library.path`

manually for each run configuration. Right now this Eclipse plug-in only works with an outdated version of m2eclipse but a new version is in the works.

To work with LWJGL natives, we made custom releases of LWJGL jars with classifiers “natives-win”, “natives-linux” and “natives-mac” with corresponding OS natives each one. As the Eclipse plug-in is not working with current m2eclipse version, we added the goal `nativedependencies:copy`

to Maven -> Life Cycle from Eclipse project properties, so each time you clean the project the maven plug-in executes and the natives are copied to `target/natives`

folder, after that, we configure by hand the `java.library.path`

to point to that folder.

| Mavennatives plug-in is [already on Maven central](http://mavencentral.sonatype.com/#search | ga | 1 | mavennatives) and
`natives-${os}` we defined for this plug-in. |

If you want to take a look at the project, visit googlecode at [mavennatives](https://code.google.com/p/mavennatives/).

~~UPDATE: maven natives eclipse plug-in is updated so it should be working for latest version of m2eclipse~~

UPDATE2: maven natives eclipse plug-in is not working with the latest version of m2eclipse hosted in eclipse.org.

UPDATE3: [LWJGL is already on maven central](http://lwjgl.org/forum/index.php?topic=3707.new;topicseen#new).