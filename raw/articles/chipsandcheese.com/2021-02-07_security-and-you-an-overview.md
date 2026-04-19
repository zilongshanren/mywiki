---
title: Security and You, an Overview
url: https://chipsandcheese.com/p/security-and-you-an-overview
author: Chips; Cheese
published: '2021-02-07'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Security and You, an Overview

#### Intel, AMD, and Nvidia have all had brushes with poor security in the past (widely published or otherwise) but that isn’t the focus of this content piece.

Instead, we will be exploring what the three companies have—or in one case haven’t—done to secure their products from the threats present in the world and on the net. All of the information sourced here comes from authoritative sources at all three companies, whether through their official statements or their whitepapers; we will not be using assumptions or third party tests except in cases where no other option exists.

## AMD: Secure Your Everything

AMD is a unique company when it comes to security, being the only one that creates CPUs and GPUs for both the datacenter and the desktop market. In this piece we’ll be focusing on datacenter, enterprise and professional security measures as these are both more numerous and more important in the grand scheme of things (you won’t be running anything that important on your home computer anyway).

First their GPUs. There isn’t much written by AMD on this topic overall, though they do have a security co-processor within their GPUs but details are scant. We do know that the driver can talk to it, otherwise the security patch that came with Radeon driver version 20.1.1 (fixing a flaw that allowed a few different attacks, including [Arbitrary Code Execution](https://en.wikipedia.org/wiki/Arbitrary_code_execution)) wouldn’t work. We also know that AMD can detect altered BIOSes and will prevent a flash of a non-signed bios, but other than that there are few details. What they have written about, however, is fascinating.

Virtualization is a very common thing in datacenters, both for security reasons and for getting as much out of a single CPU or GPU as possible. Fundamentally this is means having multiple users using the same bit of hardware at the same time. Most software solutions for this are flawed, however; they can’t keep the user data from intermingling and it can lead to inconsistent performance if one user takes up all of the (V)RAM or cache. AMD’s solution for this, called **MxGPU**, uses a PCI-Express specification called **SR-IOV** (Single-Root Input/Output Virtualization) to separate users, locking each user to different memory and scheduling regions. While this is not all-powerful, due to dynamic scheduling time being unsupported with most configurations, it does allow a set usage period for each user and a set resource allocation. More importantly, it keeps users from being able to affect each other (unless they exploit a hardware or software flaw at any rate). With each user getting their own register, it becomes nearly impossible to actually break out of their defined region and suck up resource time or, more importantly, data from others. This is, however, the only thing we could find that sets AMD GPUs apart from NVIDIA’s.

On the CPU front, AMD has written far more. First, the simple stuff; AMD has a BIOS checking function on their EPYC line of processors as well as their GPUs, though the CPU version is far more intrusive and advanced. AMD Secure Boot (not to be confused with Windows Secure Boot) not only checks for a modified BIOS ROM, it can also lock an EPYC package to only working with a single motherboard and bios version (and vice versa). While this is a powerful tool, it is typically not worth doing unless you’re handling very sensitive data as it damages both resale value and upgradability.

Next we have Secure Encrypted Virtualization and Secure Memory Encryption, or SEV and SME (only SEV is present on standard desktop platforms). What these do is more or less written on the tin; it secures virtual machines, or VMs, by encrypting each one with it’s own security key and secures RAM with the same method. Each CPU has 509 unique keys to use for SEV and a randomly generated 128bit wide AES key for SME. This means that it is highly unlikely, though not impossible, for two different users to get the same key; making decoding difficult for any wannabe hacker. This has three functions, the first is obvious: it keeps people from accessing anyone else’s data. The second is slightly less obvious but simple enough to figure out: it keeps people from injecting code into another VM’s environment. And the third is a very strange vulnerability that is never used seriously but is fun to think about: freezing the RAM with LN2 so that you can put it in another machine and, in theory, take the data within. Still, the last is only technically a vulnerability and, as it requires direct access, a lot of time, and a machine right nearby to take, the data it isn’t worth worrying about.

## Intel: Security at the Root

Like AMD, Intel’s complete suite of features isn’t available on all processors. Still, some features are; though which are available on what processors is a confusing mess that we will avoid. You can find which features are available on your hardware through the intel ark website ([https://ark.intel.com/content/www/us/en/ark.html](https://ark.intel.com/content/www/us/en/ark.html)).

Intel Boot Guard and Intel BIOS Guard: These two technologies together do something very, very simple, they prevent unsigned code from running at boot and prevent unsigned BIOSes from being installed. That’s it.

Intel Trusted Execution Technology, or TXT (because of course it needs an X), takes this a step further. Instead of attempting to prevent the installation of malicious code, it tries to prevent it from running once it has been installed (or at least informs the user about it). On top of this, it restricts the firmware from accessing non-critical systems until the OS or other security feature can ensure nothing malicious is being done on the hardware or firmware level. This only prevents attacks from those with direct access to the system (and it sometimes fails at even that), but it does help and has no performance cost.

Intel Runtime BIOS Resilience (or IRBR) locks the page table in the SMM/BIOS to prevent malicious code that had managed to get into the BIOS from getting a look inside the OS, potentially allowing an infected system to run and function normally, without any of the issues such a malware may pose otherwise. Still, it isn’t good to rely on this and such malware should be dealt with regardless.

Intel VT-x extensions are to the OS when TXT and IRBR are to the bios, it allows the software that uses it to virtualize the hardware and OS stack to prevent unauthorized code from interacting with either. Note that this can only be used if your software stack is written to do so, it will otherwise not function.

Intel, though later to the game than AMD was with Zen, has recently announced a new technology for their upcoming Ice Lake SP server processors (release date not known at this time) called Total Memory Encryption (TME) that supposedly does what it says on the tin, encrypting the system RAM and doing everything that AMD’s SME does. It uses AES-XTS and generates its keys using the(known compromised) RDRAND instruction.

Converged Security and Management Engine, or CSME, is a bug riddled, security hole filled, mess of a hardware feature that, instead of making your system more secure when you use it, instead has over 400 vulnerabilities associated with it; with many cloud facing. Why Intel decided to create an internet accessible management unit that the CPU can not control or affect is beyond this author’s comprehension. You are better off disabling this feature and instead using the after market solutions available on the market for node and internet based controls and boot equipment. This single feature invalidates every other security device and extension the CPU has, as the CPU is entirely unable to scan the CSME’s boot ROM or firmware and, even if it could, is unable to modify it.

## Nvidia: Security through Obfuscation

Not much is known about how nvidia secures their hardware, so this section of the article will be mostly speculation based on third and first party testing.

First, Nvidia introduced a BIOS security feature, which used a combination of a hash check and BIOS signing to prevent modified or malicious BIOS ROMs from being flashed onto a GPU; this primarily affected overclockers tuning the bios to allow more voltage or higher power limits but it can be used to enhance the security of a server using these GPUs.

Second, Nvidia does offer some level of hardware virtualization support; though this doesn’t use the SR-IOV extension, so it is less secure than some software solutions(if much faster).

On the other hand, there doesn’t seem to be anything on Nvidia’s end that prevents arbitrary code execution, independent testing has shown that you can even run an entire OS on the hardware, though it isn’t very fast. Nor do they have any memory encryption, potentially allowing other users to access the same data that someone else is using.

They do have, however, the Falcon line of co-processors embedded within their GPUs. Introduced in Maxwell 1(the most famous GPU being the GTX 750ti), it has slowly evolved over time. While it doesn’t prevent unsigned firmware, something that would break third party drivers, it does prevent the manipulation of a few separate settings within the GPU, primarily temperature sensors or thermal shutdown limits. They also prevent the other micro-controllers in the chip from interfacing with physical memory(instead using [virtual memory](https://www.techwalla.com/articles/difference-virtual-memory-physical-memory_)).

## No true ‘one approach fits all’

We leave it up to the reader to draw their own conclusions. Overall, each of the three companies has their own very different approach to security, some better than others. Our intention with this article is however to educate rather than criticize or speculate, so for now we will end the topic here. Certainly as the world becomes more digitized and more connected, security is set to play an even bigger role in company roadmaps and our daily lives.