---
title: Symstore for easier PDB handling
url: https://anteru.net/blog/2012/symstore-for-easier-pdb-handling
published: '2012-09-08'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you’re developing on Windows, you are probably familiar with .PDB files. Those files provide debug information for binaries, making them invaluable when debugging crash dumps and other issues. Unfortunately, raw PDBs have some problems:

- They are built for one binary only: Rebuilding your project from source control will yield a different binary and hence PDB file, so you really need to archive the matching PDBs for each released binary.
- They are usually really large: We’re talking hundreds of MiB for a release, and you need to keep around many of them.
- Matching a binary to the PDB requires you to set up the path to the PDB. This can become cumbersome if you have released 10 different versions.

Fortunately, there is a solution which solves all of this problems at the same time: Enter [symstore](http://msdn.microsoft.com/en-us/library/windows/desktop/ms681417(v=vs.85).aspx), a tool for creating of a symbol store.

Symstore is a Windows SDK tool which creates a symbol store. You can find it for instance in the [Windows 8 SDK](http://msdn.microsoft.com/en-us/windows/hardware/hh852363.aspx) under the `debuggers` directory. A symbol store is just a folder with a special layout and some additional information, which can store multiple PDB versions in such a way that Visual Studio can pick them up easily. You just point Visual Studio to the symbol store folder (which can be also on a network drive), and if the PDB for the binary you want to debug is present in the store, it just works. This works for multiple versions of the same binary as well.

All you need is to call the symstore binary and add the PDBs to the symbol store on each release. It doesn’t matter from which machine this is done, as all required information is stored in the symbol store. In my case, the deployment script takes care of this while preparing a release. And as a final bonus, file size is also no longer a problem as the symbol store comes with a [compression option](http://msdn.microsoft.com/en-us/library/windows/desktop/ms681378(v=vs.85).aspx) which typically reduces the PDB size by 80%. That’s great when the network storage location doesn’t support file compression.