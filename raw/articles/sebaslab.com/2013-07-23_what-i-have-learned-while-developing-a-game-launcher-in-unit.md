---
title: What I have learned while developing a game launcher in Unity - Seba's Lab
url: https://www.sebaslab.com/what-i-have-learned-while-developing-a-game-launcher-in-unity/
author: Sebastiano Mandalà
published: '2013-07-23'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*This post can be considered partially outdated as my mind changed quite a bit since when I originally wrote it.
First of all, I would never suggest to write a game launcher in Unity now. Use instead .net or the latest version of mono with xamarin. Mono library embedded with Unity 4 is too outdated and its use results in several problems when using advanced HTTP functions. However, if you decide to use .net, please be aware that your installer must be able to download and install .net from the internet if it is not installed on the machine already. It is also possible to embed mono, more or less like Unity does, but it is quite tricky under Windows.
We also changed our mind about the admin rights. Many of our users use Windows without admin rights, so we wanted our launcher to never ask for any.
I also think Unity now fixed the check of the SSL certificates, but I am not 100% sure about it.
At last, I would search around for libraries that can generate diff patches of binary files, since hashing and downloading files one by one is neither convenient nor efficient.*

In case you didn’t know yet, it has been already a while since I co-founded a company called Freejam, in the UK, and started to work on a new game named Robocraft ([http://robocraftgame.com](http://robocraftgame.com)). For this indie product we are extensively adopting the [Lean startup](http://theleanstartup.com) approach even for the development cycles, so features come as they are actually requested by our early adopters.

Last feature our early adopters were eager to see was a proper game launcher. A game launcher is basically a must for every online game, since, as you all know, in this way is possible to patch and update the game without being forced to install it over and over.

I never implemented a launcher before, so I was completely ignorant about some tricky issues that could arise and their relative workarounds, which I now want to share with you to avoid wasting days trying to solve similar problems.

I started to develop the launcher in Unity just because it needed a graphical interface and I did not want to spend time learning/using new libraries for other development platforms (either c++ or pure c#). Size wise, considering that Unity applications embed the mono libraries and runtimes, the resulting compressed 6MB installer wasn’t too bad.

The graphic interface has been easily developed with [NGUI ](http://www.tasharen.com/?page_id=140)and the information shown are a mix of rss news taken directly from the game blog and images configurable by the artists through an external xml.

The update process instead has been a little bit more convoluted, with a couple of unforeseen tedious obstacles that made my life a bit miserable for few days.

The update process is split into several predefined tasks:

- check if the game is already running and ask to the user to close it before the update could be launched
- check if another launcher is running and ask to close the other one
- check if a new version of the patcher is available and in this case force to update the patcher
- check if a new game build is available
- download the list of files built together with the new game build. This list contains the name of the files, the size and a hash as checksum
- download an
*asymmetric encrypted digital signature*of the game - verify that the digital signature is valid using the public key embedded in the client
- verify that all the files on the server are ready to be downloaded
- verify which files on the hard disk must be updated, using file size and generated hash (comparing the value with the hash from the file list previously downloaded)
- if it is needed, files are downloaded, uncompressed and saved (they are stored as gzip on the server)
- delete obsolete files if there are any

On our side our [Jenkins ](http://jenkins-ci.org)building machine handles two separate jobs (actually more, but I keep it simple for the sake of this article), **one to build the patcher, generate a new patcher version and deploy it to the CDN and the other to build the game, generate a new game version, generate the files list with hashes, create the digital signature using the private key that only our building machine knows, compressing the files to upload and deploy everything to the CDN**.

The whole development process has been long, but thanks to the .net framework relatively easy. Nevertheless there are two specific features I have to go into detail with, since they are very important to know and not so intuitive:

first one is the reason why I implemented an asymmetric encrypted digital signature verification. A launcher without this kind of protection is vulnerable to *man in the middle attacks* that could be shown under the form of DNS spoofing. When a hacker successfully spoof a dns node, simply creates a deviation of the normal TCP/IP routing that the client cannot recognize. In this way the client does not know that it is downloading files from unknown sources and since the game includes executables as well, it could be relatively easy for a hacker to attack a specific pool of users and let them download malicious files.

This is one of the reasons why HTTPS has been invented, however HTTPS is effective against this attack only if the client can verify the certificate provided by the HTTPS server ([http://en.wikipedia.org/wiki/Public_key_certificate](http://en.wikipedia.org/wiki/Public_key_certificate)). With my surprise, I found out that while Unity supports HTTPS connections, **it does not verify the SSL certificates at all; **Therefore using HTTPS in Unity does not prevent [Man In Middle Attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack). Luckily the implementation of a digital signature was already planned, so while I was disappointed of the Unity behaviour, we were already ready to face the issue.

Implementing a Digital Signature in C# and .net is very simple and a lot of code is already available around. Just look for *RSACryptoServiceProvider* on Google to know more.

Once all this stuff was implemented I thought I was finally done with the launcher, but a dark and vicious evil bugger was awaiting me behind the corner: the [UAC ](http://en.wikipedia.org/wiki/User_Account_Control)implementation of Windows Vista+!

After I understood what the UAC implementation of windows actually does, I realized why most of the online games suggest to use the *c:\games* folder to install the game instead of the standard *c\:Program Files*. The Program Files folder is seen by modern windows operative system (excluding XP) as a protected folder and only administrators can write in it.

Our launcher is installed by Inno Setup, which asks to the user to run in administrative mode, so Inno Setup is able to write wherever the user wants the game to be installed in. However, once it is installed, the problems start.

At this point of the explanation, If the launcher is launched directly from Inno Setup, it inherits the administrative rights from the installer and then it is able to update the game folder under Program Files. However, once the launcher is started again by the user, it will not start as administrator, but as normal user changing the behaviour of the file writing.

This is when the things start to be idiotic. If a normal user application tries to write inside a folder under Program Files, the writing of the file does not fail as I initially expected. Instead Windows creates a Virtual Store folder under *C:\UsersusernameAppDataLocalVirtualStore* that virtualises the game folder. The result is that all the files that the launcher tries to write under program files are actually stored in a specific and predefined folder in the virtual store.

Hence, First lesson is: if your Unity application needs to write new files, never write them in to the folder where the application has been installed. Use the application data folder instead! However this cannot be applied to a launcher, since the launcher must be able to update the game wherever the user decided to install it in.

First solution came to my mind was then to embed a manifest in the application to ask to vista to run the launcher in administrative mode. This is easier than it sounds, at least once I understood that a command line tool, that can be found inside the windows SDK, can do it. Once followed the [instructions, ](http://msdn.microsoft.com/en-us/library/ms235591(v=vs.80).aspx)every time the launcher starts, windows UAC prompts a message box to the user, asking if to give the administrative rights to the application or not.

If the user authorizes the application, the launcher will be able to update the game, otherwise it will throw an error.

However and unluckily, this was not the final solution. The tricky situation here is that the launcher must be able to launch the game as well, but a process launched by another process will inherit its rights. This means that the game launched by the launcher would start as administrator, while if the user decides to start the game on its own, without using the launcher, it runs in normal mode (if the user is not administrator or the UAC is fully enabled).

Launching the game in administrative mode can be a bad idea for several reasons, but the most annoying one is that the user is not used to authorize a game everytime it is launched, so we decided to get rid of this issue.

After some research and after I tried all the possible solutions I could find on google and stackoverflow, I realized that the only working one is to use a bootstrapper to launch the launcher.

The bootstrapper must be a tiny application that runs in normal mode and must be able to launch the launcher as administrator user. This is pretty straightforward since .net allows to raise the application rights (but never allows to downgrade 🙁 ). Once the launcher does its dirty job, it will close itself and it will communicate to the bootstrapper that it is now time to launch the game. The bootstrapper is now able to launch the game as normal user, because the bootstrapper itself has not started with elevated rights.

This solution sounds convoluted, but it is actually quite commonly adopted. Of course I could not use unity to create the bootstrapper, since this must be just few hundred Kbytes.~~ For this reason I ~~ [downloaded xamarin and mono ](http://www.go-mono.com/mono-downloads/download.html)and I have to say I was quite impressed by it.~~I have been able to setup a project and run it in few minutes. The bootstrapper itself has been developed in few minutes as well.~~ For this reason we were forced to create a very simple c++ application in order to be .net framework agnostic (that otherwise must be installed on the machine)

Hope all of this can help you one day!


Hi Sebastiano, Found this post while searching for solutions to my kid’s woes, who were eager to try Robocraft but were unable to start a game. They got it from Steam and the program “froze” when starting a game, either online or in practice mode. After the usual driver updates that did not improve anything, I found that the game ran perfectly when started from an administrative account. For obvious reasons, but more so in case of kids, you should expect most of your players to not have admin privileges on their machines, so this is going to be quite… Read more »

Hello,

I totally changed my mind since I wrote this post that I really want to update with my new experience. Our current launcher doesn’t require administrative rights and the game cannot be installed under program files unless the user intentionally start it as administrator.

Many things have changed, so soon or later I ought to update this post.

The game however, doesn’t need administrative rights. It could need administrative rights if starts from Steam, I have to test it.

Hi Sebastiano,

Thank you for the post – it gave me a good starting point. Can I ask you some questions regarding your launcher?

1. How do you update the launcher itself? Is there another process that updates launcher?

2. How do you install a launcher? Do you use third-party tools?

3. How do you install game FROM the launcher?

4. After update how do you register new files for uninstall or how do you register them in registry?

I have never noticed these questions, but I want to answer now anyway. 1. You need another application to update the launcher. Probably the best solution is to start from this meta launcher. It will check if a new version is available and if it is will start the download immediately, otherwise it will launch the launcher. 2. Yeah, we use a third party free installer. You can find some googling. 3. The launcher simply download the files from internet and uncompress them to the given folder. 4. Modern installer should allow you to script the uninstalling process so that… Read more »

Thank you 🙂