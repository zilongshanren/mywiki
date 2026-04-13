---
title: How to uninstall the Intel OpenCL SDK 2013 after upgrading to Windows 8.1
url: https://anteru.net/blog/2013/how-to-uninstall-the-intel-opencl-sdk-2013-after-upgrading-to-windows-8-1
published: '2013-11-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you have the [Intel OpenCL SDK 2013](http://software.intel.com/en-us/vcsource/tools/opencl-sdk) installed before you upgrade your machine to Windows 8.1, you’ll notice that you cannot uninstall it after the update, as it will always fail with the following error message:

Intel® SDK for OpenCL

Applications 2013 designed to work on Microsoft Windows Vistax64, Windows7 x64, Windows8 x64, Windows Server* 2008 R2 x64 operating systems only. The installer detected that you’re trying to install the SDK on a different version. Aborting installation

Great. This prevents you from upgrading to the 2013 R2 release, which does support 8.1 – if you simply run the 2013 R2 installer, it will fail when trying to remove the old one as well. So how can we solve this? First of all, you have to find the MSI file. I’ve downloaded the `intel_sdk_for_ocl_applications_2013_x64_setup.exe`

and extracted it using [7zip](http://www.7-zip.org/), which gives me the `Intel® SDK for OpenCL Applications 2013#x64#intel_sdk_for_ocl_applications_2013_x64.msi`

file, which I’ve renamed to `sdk.msi`

to reduce typing. Now, uninstall with logging enabled using `msiexec.exe /x sdk.msi /L*V "log.log"`

.

If you open the log file, you’ll find:

```
Action 09:57:30: LaunchConditions. Evaluating launch conditions
Action start 09:57:30: LaunchConditions.
Intel® SDK for OpenCL* Applications 2013 designed to work on Microsoft Windows Vista* x64, Windows* 7 x64, Windows* 8 x64, Windows Server* 2008 R2 x64 operating systems only. The installer detected that you're trying to install the SDK on a different version. Aborting installation
```


So the problem is a launch condition. Let’s take a look at the installer database to find out which one it is. For this, you’ll need to install the [Windows SDK](http://msdn.microsoft.com/en-US/windows/desktop/aa904949) to get [Orca](http://msdn.microsoft.com/en-us/library/aa370557%28v=vs.85%29.aspx), a tool for inspecting and modifying MSI packages. Orca is a separate installer which is bundled in the Windows SDK.

Once you have Orca installed, you can right-click the MSI file, “Edit with Orca”, and then go to “`LaunchCondition`

” on the left side. Lo and behold, here it is. If this condition is true: `((VersionNT64 AND (((VersionNT64=600) AND (MsiNTProductType=1)) OR VersionNT64=601 OR VersionNT64=602)) OR (VersionNT AND (((VersionNT=600) AND (MsiNTProductType=1)) OR VersionNT=601 OR VersionNT=602)))`

, we’re getting the error we see. Ok, so we have to get rid of it. Just right click and remove the row and you’re done … not so fast. Unfortunately, this is not the MSI file that is actually used during uninstall, as the MSI file has been already cached by the system, so we need to find out which MSI file is really used. Open up the log again and look for a line like this:

```
MSI (s) (F4:F8) [23:37:48:764]: Package we're running from ==> C:\Windows\Installer\6bcd9687.msi
```


That’s the file we really need to modify. You’ll have to run Orca as an administrator for this, and then you can open the file above and remove the launch condition. Now, you can start the uninstall, and voilà, it works.