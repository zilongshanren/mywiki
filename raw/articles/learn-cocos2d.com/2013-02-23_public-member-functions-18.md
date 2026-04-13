---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_files_downloader/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

| (id) | -
|

Returns destination path which aFilename should be downloaded to. Doesn't check does aFilename exist in _filenames array.

| + (id) downloaderWithFiles: | (NSArray *) | files |
|
| withSourcePath: | (NSString *) | aSourcePath |
|

Creates [FilesDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_files_downloader/) with given source path & filenames.

| files | Array of NSStrings of filenames. Each string is subPath that will be added to aSourcePath to determine full URL for single file. I.e. "foo/bar/file.txt" |
| aSourcePath | - path to download from (shared part for all files) I.e. "
|

| - (id) initWithFiles: | (NSArray *) | files |
|
| withSourcePath: | (NSString *) | aSourcePath |
|

Inits [FilesDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_files_downloader/) with given source path & filenames.

| files | Array of NSStrings of filenames. Each string is subPath that will be added to aSourcePath to determine full URL for single file. I.e. "foo/bar/file.txt" |
| aSourcePath | - path to download from (shared part for all files) I.e. "
|

Delegate for download status callbacks.