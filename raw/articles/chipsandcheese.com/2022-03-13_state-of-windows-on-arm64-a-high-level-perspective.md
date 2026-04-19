---
title: 'State of Windows on Arm64: a high-level perspective'
url: https://chipsandcheese.com/p/state-of-windows-on-arm64-a-high-level-perspective
author: Rndbutterfly
published: '2022-03-13'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# State of Windows on Arm64: a high-level perspective

For a port of Windows to another architecture to be usable, a high level of backwards compatibility is needed to delight customers. Customer frustration has to be maintained at a minimum. Otherwise, such an endeavor can get very expensive quickly, with rising return rates hampering profitability across the whole chain among other issues.

## Start early or start late?

One of the important things on an ecosystem as large as Windows is to give time for the ecosystem to port software to the forthcoming architecture. This can mean releasing the platform quickly.

Windows on ARM64 was released quite early in the wild, with Windows 10 version 1709 (late 2017) on the Snapdragon 835 processor. This processor is no longer supported on Windows 11, resulting in a relatively short support timeframe for early adopters. However, security updates are provided for the Windows 10 lifecycle for those devices.

Snapdragon 835’s hardware virtualization capabilities are also not usable, because Qualcomm’s software stack [already virtualizes the user’s operating system](https://www.qualcomm.com/news/onq/2019/08/21/secure-boot-and-image-authentication-improvements). That means no WSL2 or Hyper-V on that hardware. This also applies for the initial release firmware for Snapdragon 850 devices. Notably, Lenovo devices using that processor didn’t get the update needed to enable *Secure Launch* in order to give hypervisor privileges to Windows.

Snapdragon 850 devices did get Windows 11 support, but did *not* get x86_64-compatible GPU user-mode drivers. This means that on those platforms, 64-bit x86 applications run without GPU acceleration.

## Feature parity?

### The application compatibility perspective

Before Windows 11, Windows on ARM64 didn’t run 64-bit x86 applications. This was a major catch affecting compatibility across a wide range of software. It also didn’t support hardware accelerated OpenGL and OpenCL meaning some programs, like Minecraft, wouldn’t run.

Now on Qualcomm hardware, OpenGL and OpenCL support is provided through GLon12 and CLon12, providing OpenGL 3.3 and OpenCL 1.2 compatibility on top of the D3D12 API. However, this functionality was only added in Windows 11 and Vulkan still isn’t available.

Drivers have to be built for the 64-bit Arm architecture, including user-mode drivers.

### The framework-level perspective

Before the upcoming *Nickel* release with .NET 4.8.1, Windows 11 didn’t support .NET Framework natively on the 64-bit Arm architecture. This meant that applications and OS components relying on those, such as MMC or PowerShell, had to be x86 or x86_64 components. It also meant that first or third-party applications using .NET Framework couldn’t be ported to native without a sometimes costly migration to .NET 6.

### User-exposed features

Before Windows 11, Hyper-V virtual machines couldn’t be created on Windows on Arm64. And prior to the upcoming *Nickel* release, Windows Sandbox and Internet Information Services were not available on on arm64 Windows either.

Also something of note, container images for Windows on arm64 are also not available at this point in time.

## The different compatibility layers available

### 32-bit Arm

Allowing Universal Windows Platform applications to run, this backwards compatibility layer leverages the software collection built for Windows 10 Mobile devices, a platform that had since been driven to extinction.

It’s slowly going away, driven by 32-bit Arm compatibility going away on modern Arm hardware. Apple M1’s Firestorm and Icestorm, along with Cortex-X2 and the Cortex-A510 are some of the cores which do not support 32-bit Arm backwards compatibility.

### 32-bit x86

32-bit x86 compatibility has been present since the initial release of Windows on Arm64, providing a baseline level of backwards compatibility for the ecosystem as a whole.

CHPE (*Compact Hybrid Portable Executable*) binaries are present to reduce emulation overhead, by having the OS libraries be native instead of having to go through the XtaJIT (*x86 to ARM64 JIT*) dynamic binary translator. CHPE is a private ABI not exposed to the public – and has been changed in the past. As such, third-parties couldn’t ship their own CHPE code in a supported way.

*XtaJIT*‘s historical roots are the Virtual PC for PowerPC Mac code base, which had its origins from Connectix. Virtual PC for Mac got abandoned in the switch of the Mac platform to Intel processors, with that JIT compiler living on the Xbox 360 for compatibility with 1st-generation Xbox titles.

### 64-bit x86

The importance of 32-bit x86 decreased with time. 64-bit application compatibility is a requirement to reach mass market adoption.

Starting from Windows 11, backwards compatibility for x86_64 applications is provided through XtaJIT64 (*x86_64-to-ARM64 JIT*) . ARM64 *Emulation Compatible*, an ABI compatible with x86_64 code was developed. This allows to mix ARM64EC and x86_64 binary code in the same process. Unlike CHPE, this ABI is available for the public with development tools shipping as part of Visual Studio.

The 64-bit x86 compatibility layer on 64-bit Arm Windows very often provides better performance than when emulating 32-bit x86.

## Performance for emulated applications

### Memory ordering

Due to emulating a guest machine with a single exposed core, Virtual PC for PowerPC Macs didn’t have to deal with emulating the x86 memory model semantics, unlike Windows on ARM64.

Emulating the x86’s memory model semantics can be a quite sizeable part of the x86 to Arm64 emulation overhead, which will be explored more in a future article of this series. Rosetta 2 on arm64 macOS relies on a Total Store Ordering implementation provided in hardware instead, bypassing having to handle this issue from a software perspective. However, that approach cannot run on any 64-bit Arm core.

### x87 floating point extensions

Some 32-bit x86 applications also tend to have heavy reliance on x87 floating point extensions. This quite outdated floating point extension was superseded by SSE. To provide proper semantics, it often has to be implemented in a slow manner, as precision requirements can make leveraging the hardware floating point units not possible in this scenario.

Sometimes, those instructions are used on x86_64 apps too, resulting in unneeded performance cliffs under emulation. Using x87 isn’t fast on modern x86 hardware either, using the x87 *long double* type is as such *not* recommended when writing x86_64 applications. When using Visual C++ on Windows, *double* and *long double* refer to the same underlying type.

### Just-in-time compilers

Because of its just-in-time nature, .NET Framework when running in an emulated environment can have performance cliffs due the double-JIT problem. This also affects web browsers, which shouldn’t be used on an emulated environment because of performance issues.

## Hardware availability

Hardware availability is essential for a nascent platform. Currently, the options available for 64-bit Arm Windows are quite limited. The highest performance options available today aren’t an intended target by Microsoft – those being the Apple machines using the M1 processor family.

At the lower end, the Galaxy Book Go is available at a low price, but is a platform with a maximum of 4GB of RAM. The same issues apply to the Snapdragon Developer Kit, which has a significantly high price point ($219) and poor availability when compared to the Galaxy Book Go.

There’s also currently a lack of options on the server side, with GitHub Actions ARM64 support and Azure IaaS Arm virtual machines not being released yet.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).