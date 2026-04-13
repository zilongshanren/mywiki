---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/
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

uses NSURLConnection to download file from URL, that is set by concatanating source URL (i.e [http://foo.com/files/](http://foo.com/files/) ) and file name (i.e. bar.png ), so URL for this file will be [http://foo.com/files/bar.png](http://www.learn-cocos2d.com#) , to APP_SANDBOX/Library/Caches on iOS or to ~/Library/Caches/APP_BUNDLE_ID on Mac (According to Mac OS X File System Guide ).

At the first [SingleFileDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/) creates tmp file and downloads contents into it, only after downloading successfully ends - it renames tmp file to destination filename.

[SingleFileDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/) is used internally in [FilesDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_files_downloader/) class, if you're downloading many files at time from one place - you don't need to use [SingleFileDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/) - use [FilesDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_files_downloader/) instead.

Returns total content size in bytes. This value can be changed each. Use this method in downloadSizeUpdated delegate method to determine new expected content size.

Returns shared destination path part for all files ~/Library/Caches/APP_BUNDLE_ID on Mac & APP_SANDBOX/Library/Caches on iOS.

| + (id) fileDownloaderWithSourcePath: | (NSString *) | sourcePath |
|
| targetFilename: | (NSString *) | aTargetFilename |
|
| delegate: | (id<
|

Creates [SingleFileDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/) with given source path, target filename & delegate.

| sourcePath | - path from which to download file, without filename. I.e. "
|

| - (id) initWithSourcePath: | (NSString *) | sourcePath |
|
| targetFilename: | (NSString *) | aTargetFilename |
|
| delegate: | (id<
|

Inits [SingleFileDownloader](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_single_file_downloader/) with given source path, target filename & delegate.

| sourcePath | - path from which to download file, without filename. I.e. "
|

Returns full target path for file, that will be downloaded I.e. "APP_SANDBOX/Library/Caches/fooBar.png" (iOS) or @"~/Library/Caches/APP_BUNDLE_ID" (Mac)