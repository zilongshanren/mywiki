---
title: Total Commander – a Plugin Supporting a Custom Archive Format
url: https://asawicki.info/articles/total_commander_plugin_en.php
published: '2026-01-01'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

*This article was originally published in Polish language in issue 5/2025 (120) of Programista magazine.*

**In this article, we will design our own file format that allows multiple files to be packed and compressed into a single archive, similar to formats like ZIP or 7Z. Using the C++ language and the Visual Studio environment on Windows, we will then write a plugin for the Total Commander file manager that enables creating and manipulating such an archive, including freely adding and removing files inside it.**

Most Windows users probably manage their files using the default system tool, Windows Explorer. However, there are also separate applications dedicated to this purpose. Among them, it is worth getting to know [ Total Commander](https://www.ghisler.com). This tool features a characteristic interface divided into two columns. In each of them – on the left and on the right – we are always inside a selected folder from our disk. It is also possible to create multiple tabs on each side. This allows convenient browsing and comparing of files, as well as performing operations such as copying and moving from one side to the other. An example screenshot is shown in Figure 1.

![Figure 1. Screenshot from the Total Commander program](../../assets/39dba660417a9bdb.png)

*Figure 1. Screenshot from the Total Commander program*

Total Commander is available under a shareware license. It provides full functionality for free. When launching, it only displays an additional window reminding the user about the required registration. After 30 days of use, it should be registered. Although it continues to work even without registration, it is worth staying compliant with the license and supporting the author with the required fee of 42 euros. Especially since the author – Swiss programmer Christian Ghisler – has been tirelessly developing this product since 1993.

In addition to simple operations on files and folders, Total Commander offers many other useful features, including file preview and comparison, folder synchronization, advanced search, batch renaming of multiple files, checksum calculation, and a built-in FTP client. It also supports many archive formats, including ZIP, RAR, and ARJ. The Windows system file explorer has supported ZIP archives for some time as well, but the program discussed here supports a wider range of formats. It also supports plugins that allow adding support for additional file formats. This is exactly what this article will focus on.

Why pack multiple files into a single archive in the first place? There can be many reasons. A single file is easier and more convenient to download from the Internet, share with someone online, copy, or move. The operation of copying or even deleting thousands of small files would also be slower than performing the same operation on a single file. When a set of files forms a coherent whole, packaging them together also reduces the risk that only some of them will be copied or that certain files will be accidentally deleted, which could lead to an inconsistent state of the program that uses them and consequently cause various errors.

Additionally, when packaging files into an archive, we often have the option of compression. However, we need to distinguish between two different concepts here:

The word “compression” can be understood in several ways. Compression can be either lossy or lossless. Lossy compression is used for multimedia content, where some loss of quality is acceptable. It is used by file formats such as images (e.g., JPEG), music (e.g., MP3), or video (e.g., MP4 and codecs such as H.264). However, this type of compression is not what we will focus on here, because our goal is to be able to package arbitrary files, and any other types of files (such as text documents, executable files, or any other binary files) must not have even a single bit changed after being packed and unpacked. Therefore, in this article we will use only lossless compression.

Lossless compression, in turn, can be discussed in the context of using a specific algorithm. One such algorithm is Deflate, supported by the [zlib](https://zlib.net) library, or LZMA, which also has its own SDK. Libraries of this type support compressing and decompressing streams of data in memory. Based on them, specific file formats are then designed, which additionally allow multiple files to be packed into a single archive and define the required headers and other elements of the format. For example, the ZIP format uses the Deflate algorithm by default, while 7Z uses the LZMA algorithm.

Therefore, data compression and packaging multiple files into a single archive format often go hand in hand, but they are not the same thing, so it is worth being aware of this distinction. A good example comes from Unix/Linux: the TAR format supports packaging multiple files but does not support compression, while GZIP supports compression but operates on only a single file at a time. Only their combination makes it possible to package and compress multiple files at once. That is why, in the Linux world, files with combined extensions such as .tar.gz or .tgz are commonly encountered.

In the next section, we will design our own archive format similar to ZIP. At first, we will focus only on packaging multiple files and performing operations on them, and only at the end will we add support for compression using the zlib library.

One might still ask: why design a **custom archive file format** at all instead of using an existing one, such as ZIP? This approach is popular, for example, among developers of games and game engines. Thousands of small files containing models, textures, or sound effects are often packaged into large archives not only for convenience and better game loading performance (thanks to compression), but also to hide these resources from the curious eye of the player, who might try to extract or modify them. In the long run, however, this is not effective and represents the flawed approach of security by obscurity, because it will not stop advanced programmers familiar with reverse engineering.

We will now design our own simple archive file format. First, let us define its basic parameters. Its name will be “Sample Archive”, and the recommended file extension will be .smpa. It will be a binary file in which multi-byte numbers are stored in little-endian order, which is the natural format for PCs with x86 processors. The structure of the file is shown in Figure 2.

![Figure 2. Structure of our archive file](../../assets/613ac4595d307b4f.png)

*Figure 2. Structure of our archive file*

The file begins with an 8-byte header consisting of the characters: `"SMPA100A"`

. It is good practice for a file format to be identifiable right at the beginning. By checking such a header, we avoid attempting to read a file in a different format as our archive, which could otherwise lead to various errors at a later stage. The first 4 characters `"SMPA"`

identify our file format, while the next 4 – `"100A"`

– represent the version number. In the future, we may extend our format with new features. An updated program could then identify and support both the old version of the format and a new one, for example with the version number `"200A"`

, which in turn would be unknown to an older version of the program. In this article, however, we will stick exclusively to the first version.

After the header, entries describing subsequent files and directories continue until the end of the file. Each such `Entry`

can have a variable length, but it always begins with a 28-byte entry header – `EntryHeader`

. This header contains several fields:

`magic`

(32 bits) – a magic number identifying the beginning of an entry, with the constant value 0x1743C8F1 (note that in little-endian order the individual bytes will be written as: F1 C8 43 17). By checking it, we verify that we have reached the correct header of the next entry rather than somewhere in the middle of the data.`flags`

(8 bits) – bit flags: 0x1 means the entry is deleted (the file or directory no longer exists, so it should be ignored and skipped), 0x2 means the data is compressed (support for compression will be added only in a later section).`attributes`

(8 bits) – additional bit flags encoding file or directory attributes, in a format compatible with the Total Commander API. Of particular interest is the value 0x10, which indicates that the entry is a directory rather than a file. The remaining values are standard attributes that can be assigned to files in Windows.`time`

(32 bits) – the file modification date and time, in the format used by Total Commander.`pack_size`

(64 bity) – (64 bits) – the length of the file data in bytes as stored in the archive, possibly already compressed.`unp_size`

(64 bity) – (64 bits) – the original file length in bytes, before compression. If compression is not used, these two sizes are equal.`path_len`

(16 bitów) – (16 bits) – the length of the string containing the path to the file/directory, given as the number of Unicode characters.After each such header comes the path to the file or directory, stored as a sequence of 16-bit Unicode characters (`wchar_t`

). This string is not null-terminated because its length is already known from the header read earlier. For example, the test archive contains one directory, inside it a single .jpg file with a photo, and additionally a text file. Altogether, the archive therefore contains 3 entries:

path = "Photos", attributes = 0x10 (DIRECTORY) path = "Photos\IMG_4627.jpg", attributes = 0x20 path = "TextFile.txt", attributes = 0x20

Finally, after the path come the actual data. In the case of directories, there is of course no data, so in that case `pack_size = unp_size = 0`

.

**Why this file format?**

Why was our file format designed this way, with consecutive entries describing subsequent directories and files? Wouldn’t scanning all entries sequentially, and jumping across different parts of the archive to skip file data, be less efficient? Wouldn’t it be better to design the format so that it contains a single, central index of all files and directories with their names and attributes (ideally organized hierarchically), while the data itself would only be accessed when needed using specific offsets within the archive?

Indeed, all of this is true. However, this format serves as an educational example, so it should remain as simple as possible. At the same time, the Total Commander WCX plugin API operates exactly in this model, requiring entries to be processed sequentially. This is not optimal and probably stems from historical reasons – from the structure of formats such as ZIP and TAR. Therefore, we designed our format in this way so that the Total Commander plugin supporting it would be as easy as possible to implement.

The code described in this article can be found on GitHub in the repository: [ sawickiap/TotalCommanderPluginTutorial](https://github.com/sawickiap/TotalCommanderPluginTutorial). We will refer to it throughout the rest of the article. To implement our plugin, we will use the C++20 language and the Visual Studio 2022 environment. It will be a project created directly in Visual Studio, without using additional tools such as CMake.

Total Commander supports four types of plugins:

The documentation for the WCX plugin API can be found on the [ghisler.com](https://www.ghisler.com) website, in the Addons → Plugins section, by downloading and extracting the “WCX Plugin Guide” and opening the file *pkplugin.chm*. The CHM format is supported by applications such as SumatraPDF.

Our project must compile into a dynamically loaded library **DLL**, but with the extension changed to **.wcx64** – which can be configured in the project options → Advanced → Target File Extension.

Total Commander, as an application developed for many decades, maintains backward compatibility with older versions of the plugin API. We will implement only the latest version – as 64-bit code, supporting 64-bit file sizes (so that files larger than the 32-bit limit of 4 GB can be handled) and Unicode paths (so that local diacritical characters and any other symbols in file and directory names are supported). Therefore, our Visual Studio project will be compiled exclusively in the 64-bit configuration, and Total Commander API functions that accept strings will use the “W” suffix indicating “wide” strings, i.e., of type **wchar_t** – similarly to the WinAPI.

A correctly implemented Total Commander plugin must not only be a DLL library, but it must also **export** specific functions. Some of them are required, while others are optional. Exported functions are marked with the following directives:

`extern "C"`

– disables C++ name mangling so that the function name appears exactly as written.`__declspec(dllexport)`

– exports the function outside the library (an alternative would be to use a separate .def file listing such functions).`__stdcall`

– declares the standard calling convention (the order in which parameters are placed on the stack).In the file *entry_points_legacy.cpp* we can see those exported functions that are considered obsolete. We leave them unimplemented. Internally, they execute `assert(0)`

and return an error code. We assume that modern versions of Total Commander running on modern 64-bit versions of Windows will never call them. The functions actually invoked by Total Commander that we want to implement are located in the file *entry_points.cpp*. Their declarations are shown in Listing 1. We will discuss them later in the article.

*Listing 1. Total Commander API functions for WCX plugins*

int __stdcall GetPackerCaps(); int __stdcall GetBackgroundFlags(); HANDLE __stdcall OpenArchiveW(tOpenArchiveDataW* archiveData); int __stdcall CloseArchive(HANDLE hArcData); int __stdcall ReadHeaderExW(HANDLE hArcData, tHeaderDataExW *headerData); int __stdcall ProcessFileW(HANDLE hArcData, int operation, wchar_t *destPath, wchar_t *destName); void __stdcall SetChangeVolProcW(HANDLE hArcData, tChangeVolProcW pChangeVolProc1); void __stdcall SetProcessDataProcW(HANDLE hArcData, tProcessDataProcW pProcessDataProc); // PK_CAPS_BY_CONTENT BOOL __stdcall CanYouHandleThisFileW(wchar_t* FileName); // PK_CAPS_NEW, PK_CAPS_MODIFY int __stdcall PackFilesW(wchar_t *packedFile, wchar_t *subPath, wchar_t *srcPath, wchar_t *addList, int flags); // PK_CAPS_DELETE int __stdcall DeleteFilesW(wchar_t *packedFile, wchar_t *deleteList);

First, however, we need to discuss a few general topics. After compiling our plugin into a .wcx64 file, **we can install it** in Total Commander in the Configuration → Options → Plugins window → the Packer plugins (.WCX) section → by pressing the Configure button, entering the file extension smpa, and selecting the path to our compiled .wcx64 file. An example is shown in Figure 3.

![Figure 3. Configuring a WCX plugin in Total Commander](../../assets/fe31140e322489d9.png)

*Figure 3. Configuring a WCX plugin in Total Commander*

It is worth knowing that even though we are not building an executable EXE file, we can still use Visual Studio to **debug** our code. We only need to configure the project so that it launches the Total Commander EXE file. To do this, in the project options under the Debugging tab, set the Command field to the path of the program, such as *c:\Program Files\totalcmd\TOTALCMD64.EXE*. Then, after building the project, simply run Debug → Start Debugging (keyboard shortcut F5), and Total Commander will launch. As soon as we enter an .smpa archive inside it, our library will be loaded, and at that point breakpoints and all other debugger features will start working.

Before starting the implementation, it is worth establishing and documenting a certain convention that we will follow. Since we are using modern C++, errors will be reported as **exceptions**. The Total Commander API defines a number of numeric error codes (file *third_party\wcxhead.h*, constants such as `E_END_ARCHIVE`

, `E_NO_MEMORY`

, etc.). In case of an error, we will therefore throw these numeric values as exceptions. However, since our API is written in C, an exception cannot leave our library. Therefore, the top-level functions (those exported from the DLL) catch exceptions and convert them into returning an error code as the function’s result.

When using exceptions, to avoid memory leaks it is advisable not to allocate memory directly with the `malloc`

function or the `new`

operator, but instead to use the RAII technique and **smart pointers**. This is exactly what we will do – to store pointers to resources we will use `std::unique_ptr`

. Even other types of resources besides ordinary dynamically allocated memory will be stored in these pointers, and their proper release will be handled by custom deleters. In the code we can find structures such as `FcloseDeleter`

(calling `fclose`

), `CloseHandleDeleter`

(calling `CloseHandle`

), and other similar ones.

To store Unicode **strings** (such as file paths), we will use the standard type `std::wstring`

. Wherever we need to pass a constant reference to an existing string, instead of the type `std::wstring_view`

we will use the `wstr_view`

class from the external [str_view library](https://github.com/sawickiap/str_view). It provides an improved version of such a “string view”, offering conversion to a null-terminated string (the `c_str`

method returning the type `const wchar_t*`

) and remembering whether the original string was null-terminated, so that it does not allocate a new one unnecessarily.

Total Commander can use our plugin to open an archive in one of several modes. Object-oriented programming is well suited to implementing this logic. In the files *archive.hpp* and *archive.cpp*, the base class `ArchiveBase`

defines the fields and methods common to different modes, while derived classes will implement the specific operating modes.

The first exported function:

is responsible for returning flags that indicate which features our plugin supports. As a basic set, it is worth returning:**GetPackerCaps**

`PK_CAPS_MULTIPLE`

– indicates that our archive supports packing multiple files at once. This may seem obvious, but remember that not every format satisfies this requirement (such as the previously mentioned GZ).`PK_CAPS_SEARCHTEXT`

– allows Total Commander to use our plugin to search inside the archive as if it were a regular directory, including scanning the contents of files inside for full-text search. Interestingly, we do not need to implement anything special for this feature to work, so there is no harm in including this flag.The second exported function is

. It returns flags indicating that our plugin is thread-safe during packing (**GetBackgroundFlags**`BACKGROUND_PACK`

) as well as unpacking (`BACKGROUND_UNPACK`

), which allows the user to perform operations on our archives in the background. We can safely return these flags because our code will naturally be thread-safe, since we will use classes and objects rather than storing the current state in global variables.

The first and basic operating mode consists of opening the archive for reading and iterating through all the files and directories it contains. Its implementation is provided in the first derived class: `ReadingArchive`

.

In the exported function

, our task is to open the file specified in the parameter **OpenArchiveW**`archiveData->ArcName`

and return some kind of “handle” to the opened archive. To do this, in the implementation of this function we create an object of the class `ReadingArchive`

, and return a pointer to this object to Total Commander as the handle, cast to the type `HANDLE`

. The same handle will later be passed back to us as the first parameter to the other functions discussed in this section.

We open the archive file in binary mode for reading only, so we call the function `_wfopen_s`

with the parameter `"rb"`

. Similarly, the exported function

is responsible for closing the archive, so in its implementation we cast the received handle back to a pointer to our class object and then delete our object. This will automatically invoke the **CloseArchive**`fclose`

function on the `archive_file_`

field, which is stored as a smart pointer.

Between the functions that open and close the archive, the application alternately calls the functions `ReadHeaderExW`

and `ProcessFileW`

.

is responsible for reading the parameters of the next entry (file or directory) and returning them through a pointer to a structure passed as a parameter. For example, the parameter **ReadHeaderExW**`headerData->FileName`

should receive the name together with the local path to the given element, while `headerData->FileAttr`

should receive its attributes, corresponding to the `attributes`

field shown in Figure 2. The function should return 0 if reading the next entry was successful, or `E_END_ARCHIVE`

if it was not possible because the end of the archive has been reached. Other return values are of course also allowed to indicate an error.

After each header is read, Total Commander calls the function

, where our task is to process the most recently read file or directory. The parameter **ProcessFileW**`operation`

specifies what we should do with it and may take the value:

`PK_SKIP`

– skip this entry. We should move on to the next one. To do this, we call the function `_fseeki64`

, which advances the position in the archive file by the number of bytes occupied by the current file’s data.`PK_TEST`

– test this entry, for example by computing and verifying a checksum of the file’s data. Our format does not support checksums, so we simply skip the entry in the same way as in the previous case.`PK_EXTRACT`

– extract the directory or file.In the case of our test archive, the sequence of functions that Total Commander calls from our library, together with the data they return, expressed in pseudocode, may look as follows:

OpenArchiveW(ArcName="C:\Tmp\SampleArchive.smpa") → returned handle ReadHeaderExW(handle) → FileName="Photos", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → FileName="Photos\IMG_4627.jpg", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → FileName="TextFile.txt", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → returned E_END_ARCHIVE CloseArchive(handle)

Extraction is implemented by the function `ReadingArchive::ExtractFile`

. It performs several operations:

`CombinePath`

. For example, if the user wants to extract the previously mentioned .jpg file and the destination directory is `CreateDirectoryW`

.`ReadingArchive::UnpackFileContent`

.`SetFileAttributes`

.`SetFileTime`

.Since archives can be very large and packing or unpacking them may take a long time, it is useful to show the user a progress bar. Total Commander provides such functionality. However, as plugin developers we must implement the updating of this progress bar. For this purpose, we implement the exported function

. Through it, the application passes to our code a pointer to a callback function of type **SetProcessDataProcW**`tProcessDataProc`

, which we can then call at various moments to update the user interface with the progress bar during our operations.

This function can be called in two modes:

`ArchiveBase::UpdateBytesProcessedProgress`

.`ArchiveBase::UpdateDirectProgress`

.How often should the function that updates the progress bar be called? On one hand, it is useful to inform the user about progress relatively frequently so that they do not get the impression that the program has frozen. It is worth doing this not only between files but also while unpacking a single large file. On the other hand, if calling this function causes the application window to be redrawn, invoking it too often may become a performance bottleneck, limiting performance more than the data processing itself – especially when operating on modern, fast SSD drives.

To balance these two opposing concerns, both of the functions mentioned above implement additional logic that queries the system for the current time in milliseconds (the system function `GetTickCount64`

) and calls the Total Commander function that updates the progress bar only when at least a specified number of milliseconds have passed since the previous update (the constant `kProgressUpdateIntervalMilliseconds = 40`

).

Additionally, the window with the progress bar allows the user to press the *Cancel* button. In that case, the callback function returns the value 0. In our program we handle this by interrupting the ongoing operation. Furthermore, a file whose extraction was interrupted or ended with an error is deleted using the system function `DeleteFileW`

, so that an empty or incomplete file is not left on the disk.

At this point, we could essentially finish implementing our plugin if its purpose were only to browse the contents of .smpa archives and extract directories and files. From here on, we begin discussing additional features.

The first and simplest of these is detecting the file format based on its contents. Without this feature, Total Commander uses only the file extension to identify the format. When our plugin supports recognizing its format by content, the user will be able to “enter” such an archive by pressing Enter, even if the file has a completely different extension. If that extension is associated with opening the file in some application, this can still be done using the alternative keyboard shortcut Ctrl+PgDn.

To add this feature to our plugin, we need to do two things:

`PK_CAPS_BY_CONTENT`

from the exported function `GetPackerCaps`

.**CanYouHandleThisFileW**

.It is worth noting that after adding new flags returned by `GetPackerCaps`

, the plugin must be removed and added again in the Total Commander configuration, because the program stores the flags of installed plugins.

The function `CanYouHandleThisFileW`

is simply a new operating mode of our code. In this case, Total Commander does not call `OpenArchiveW`

or any of the other functions previously discussed in the “Reading an archive” section, but only this single function. In this mode, our task is to open the specified archive for reading and then check only its header (the first 8 bytes) to verify whether it matches the specification of our file format. For this purpose, we will use a second derived class: `HeaderCheckingArchive`

. At the end, the function `CanYouHandleThisFileW`

should return a value of type `BOOL`

– true if the specified file was successfully recognized as an archive in our format, and false if it was not or if any other problem occurred.

The ability to browse the contents of an archive as if it were a regular directory, as well as extract (copy) files from it, is very convenient. However, only the ability to create new archives and modify existing ones provides the full functionality that Total Commander offers.

To create a new archive, you need to:

To add files to an existing archive, simply enter that archive on one side as if it were a directory, and on the other side select the desired files or directories and issue the standard command to copy them to the opposite side (the F5 key).

To enable our plugin to support both of these features, we need to do two things:

`PK_CAPS_NEW`

and `PK_CAPS_MODIFY`

from the exported function `GetPackerCaps`

.**PackFilesW**

.This function is simply another element of full support for the new archive format implemented in our code. We therefore create a new derived class: `PackingArchive`

. In the `OpenForPack`

method it opens the archive file for writing. First it calls the function `_wfopen_s`

with the parameter `"r+b"`

, attempting to open an existing file for reading and writing. If that fails, it creates a new file using the parameter `"wb"`

.

The parameters passed to `PackFilesW`

are quite complex, so they require a detailed explanation.

`PackedFile`

is the absolute path to the archive that the user wants to create or extend with new files.`SubPath`

contains the relative path inside our archive where the files being added should be placed. It may also be `NULL`

– in that case the files should be added at the top level of the archive, not inside any subdirectory.`SrcPath`

is the base absolute path where the source files and directories to be added are located.`AddList`

contains the full list of relative paths to individual files and directories that should be added. Each entry in this list is terminated with a zero, and after the last entry there are two zero bytes. In other words, the list is terminated with an empty string. Therefore we must carefully use pointers to read all the strings from this list one by one. In our code this is handled by the function `ParseStringList`

.To better understand this, let us consider an example. The situation being described is shown in Figure 4. The directory in which we are currently located in Total Commander is marked with a red arrow, on the left and right side respectively. The user wants to add more photos to the *Photos* subdirectory in our sample archive. To do this:

![Figure 4. Example of adding files to an archive](../../assets/6275af10dd6299fc.png)

*Figure 4. Example of adding files to an archive*

To perform this entire operation, our plugin receives a single call to the function `PackFilesW`

with the following parameters:

`PackedFile="c:\Tmp\SampleArchive.smpa"`

– the path to the destination archive`SubPath="Photos"`

– the destination directory inside the archive`SrcPath="c:\MyNewPhotos\"`

– the base source directory (note the additional backslash at the end)`AddList`

– a list of strings with paths to the source files and directories:
`"London at night.jpg"`

`"Family\"`

(here as well, an entry representing a directory ends with a backslash)`"Family\Mother.jpg"`

`"Family\Son.jpg"`

The new contents of the archive after completing the entire operation are illustrated in Figure 5.

![Figure 5. Archive after adding new files](../../assets/d9e7e1a2185c0c06.png)

*Figure 5. Archive after adding new files*

Performing such an operation would be quite simple if it always involved only adding new files and directories to the archive. After all, our file format was designed so that entries follow one after another, so it would be enough to open the file in append mode (parameter `"ab"`

) and add new entries at the end.

However, it may happen that the newly added files have the same names as files that already exist in the archive. In that case the situation becomes more complicated. We do not want to have two files with the same name in the archive (even if they differ only in letter casing – following the Windows convention, we compare names case-insensitively, using the function `_wcsicmp`

).

If we opened an existing archive rather than creating a new one, we must therefore scan all existing entries and remove those that correspond to the files being overwritten. Most of the logic in the method `PackingArchive::PackFilesW`

serves exactly this purpose, in particular the call to the method `PackingArchive::DeleteIf`

. In our file format, entries are removed simply by marking them as deleted – by adding the value `Deleted = 0x1`

to the field `EntryHeader::flags`

.

We still have not discussed the last parameter of the function `PackFilesW`

– `flags`

. It may contain additional bit flags indicating special operating modes:

`PK_PACK_MOVE_FILES`

– indicates that the source files and directories being packed should be moved rather than copied, so after writing them to the archive the originals should be deleted. Directories are removed using the system function `RemoveDirectoryW`

, and files using `DeleteFileW`

.`PK_PACK_SAVE_PATHS`

is a mode in which the user may request packing only a flat list of files, without the subdirectory structure, by unchecking the “Also pack path names (only recursed)” option in the Pack files dialog. This does not seem like a particularly useful feature, but for completeness it has been implemented in the sample plugin.As the final optional part of the Total Commander API that we will implement, we are left with the ability to delete files and directories inside the archive. From the user’s perspective, using this feature is simple: just enter the archive as if it were a directory, select the desired items, and issue the delete command (F8 or Del key).

For our plugin to start supporting this function, we need to do two things:

`PK_CAPS_DELETE`

from the exported function `GetPackerCaps`

.**DeleteFilesW**

.The parameters passed to the function `DeleteFilesW`

are to some extent similar to those of `PackFilesW`

. The first parameter is again the full path to the archive file on which we should operate. The second one is the entire list of paths to directories and files inside the archive that should be removed.

If the user enters the archive described in the previous section, already appended with the new .jpg files (Figure 5), navigates to the *Photos* subdirectory, selects all 3 items located there, and issues the delete command, then the function `DeleteFilesW`

will be called once, and the parameter `deleteList`

will contain the following strings:

"Photos\Family\*.*" "Photos\IMG_4627.jpg" "Photos\London at night.jpg"

Note that – unlike before – this time Total Commander does not provide the path to each file and directory separately. Instead, it specifies the entire directory to be removed, expecting us to recursively delete all files and subdirectories within it.

The path to the directory ends with the string `"\*.*"`

, but it does not seem that we need to treat this element as a real file mask for deletion, because the user has no way to choose any other mask, for example to delete only files with a specific extension. It is simply the way Total Commander signals that the entire directory together with its contents should be deleted, rather than a single file. In our code we simply remove this mask from the end of the string.

The implementation of the method `DeletingArchive::DeleteFilesW`

therefore builds a vector of strings containing the paths to files and directories that should be removed (converted to uppercase and sorted for easier searching), and finally calls the previously mentioned method `DeleteIf`

, which iterates through all entries in the archive and marks those that satisfy the given predicate as deleted by adding the appropriate flag.

**How should files be deleted from an archive?**

As you have probably guessed by now, deleting files from an archive by marking them with the Deleted flag so that they are skipped during processing is not the best approach. Not only does our archive remain the same size after deleting selected – or even all – of its elements, but the data of the deleted files is still present inside, which could potentially lead to unwanted leakage of sensitive information. This deletion method was implemented in the sample code because of its simplicity.

How could this be done better? Unfortunately, among the functions that operate on files there is none that can cut out a portion of bytes from the middle of a file. The only things we can do are append new bytes to the end of a file (increasing its size) or overwrite existing bytes (when we move the file cursor somewhere into the middle of the file). There is also a function that sets the file length by shortening it and discarding the data at its end (`_chsize_s`

from the Visual Studio standard library or `SetEndOfFile`

from the WinAPI). Using these functions, we can imagine various approaches to deleting elements from inside an archive:

As the final part of our plugin code, we will add support for compression. Our file format is already prepared for this. Therefore, we do not need to define a new version of it. The `EntryHeader`

structure can have the Compressed flag (value 0x2) and contains separate fields for the size of the compressed data in the archive `pack_size`

and the uncompressed size `unp_size`

. We only need to start using these capabilities now.

For compression we will use the [zlib](https://zlib.net) library. This is a well-known open source library that implements the Deflate algorithm. It is written entirely in C, including its interface, which may seem somewhat inconvenient for programmers accustomed to object-oriented programming. Therefore, it is worth explaining the correct way to use it.

The code that performs compression can be found in the method `PackingArchive::PackFileContent`

. When compression is disabled, it creates a single buffer in memory (with size `kBufSize`

equal to 64 KB), into which it reads data piece by piece from the already opened input file and writes it to the output archive file. When compression is enabled, however, it calls the zlib library.

To compress data in memory, you need to:

`z_stream`

, which serves as the main “context” structure for the compression algorithm, and initialize it with zeros.`deflateInit`

, which initializes this structure and thus effectively creates the main object of the compression algorithm.`src_buf`

, pointer assigned to the `next_in`

field of the structure) and another for the compressed output data (variable `dst_buf`

, pointer assigned to the `next_out`

field of the structure).`deflateEnd`

, which in our code is handled by a smart pointer equipped with a custom deleter.By “performing data compression” we mean the code that repeatedly calls the function `deflate`

in a loop. This function compresses a portion of the data. In doing so, it advances the `next_in`

pointer and decreases the `avail_in`

counter in the structure by the number of bytes consumed from the input, and also advances the `next_out`

pointer while decreasing the `avail_out`

counter by the number of bytes written to the output. Therefore, our loop must additionally perform two tasks:

`deflate`

function, we check whether the input buffer is empty. If it is, we read another 64 KB of data into that buffer (unless we have already reached the end of the input file).Decompression works in a similar way. Its implementation can be found in the method `ReadingArchive::UnpackFileContent`

. We simply use different functions from the zlib library – `inflateInit, inflate, inflateEnd`

. In this case, the input buffer provides compressed data, while the destination buffer contains the decompressed data.

Note that at no point do we keep the entire contents of a file in memory, whether compressed or uncompressed. Instead, we operate on a “stream” of data, read and written piece by piece. Thanks to this approach, our program can process files of any size regardless of how much RAM the computer has.

At the beginning of this article we looked at the Total Commander window that allows us to add our plugin (a .wcx64 file) to handle a selected archive file extension. However, it turns out that the application offers a more convenient way to install such plugins. Here is what we need to do:

Then, when the user enters such a ZIP archive, they will see the message: *“This archive contains the following Total Commander plugin/addon: Sample Archive from Tutorial. Do you want to install it?”* After confirming, the plugin will be copied to the Total Commander installation directory and installed there.

*Listing 2. The “pluginst.inf” file for the plugin installer*

[plugininstall] description=Sample Archive from Tutorial type=wcx file=SampleArchive.wcx64 defaultdir=SampleArchive defaultextension=smpa

In this article we explored Total Commander as a convenient file management application for Windows. We learned how to write a Packer Plugin (WCX) in C++ that allows it to support new archive formats. With such a plugin, multiple files and directories can be packed and compressed into a single file. In the process, we also designed our own simple format for this purpose. The article is accompanied by sample code available in the GitHub repository: [ sawickiap/TotalCommanderPluginTutorial](https://github.com/sawickiap/TotalCommanderPluginTutorial).

This knowledge can be useful for creating your own optimized archive format tailored to specific needs, or for writing a plugin that adds support in Total Commander for an existing format. And that format does not necessarily have to be an equivalent of ZIP or 7Z! We can also imagine the ability to “enter” EXE or DLL files (which Total Commander already supports) or any other binary formats, and offer browsing of the various types of data (resources) contained within them as “virtual” files and subdirectories.

Finally, it is worth noting how many features Total Commander itself provides and handles without any effort on our side, making manipulation of archive files almost as convenient as navigating regular directories on disk. For example, the code from the “Reading an archive” section automatically enables not only browsing and extracting files, but also searching them (by name or full-text content) and previewing them with the F3 key (in this case the file is extracted to a temporary directory). Similarly, when packing or unpacking files, the application itself asks the user whether an existing file should be replaced.

This concludes the description of our sample WCX plugin implementation for Total Commander, but it does not mean we have exhausted all the possibilities of such plugins. There are several functions that we did not implement. While adding a 32-bit version of the DLL does not seem necessary nowadays, it may still be useful to add support for features such as:

`PK_TEST`

).`PK_CAPS_OPTIONS`

, exported function `ConfigurePacker`

).`PackSetDefaultParams`

).`PK_CAPS_ENCRYPT`

).`SetChangeVolProc`

, callback `tChangeVolProc`

).