---
title: How to resume a paused or broken file upload – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/04/resumeupload/
author: Simon Speich
published: '2011-04-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post written by Simon Speich. Simon is a web developer, believer in web standards and a lover of Mozilla since Mozilla 0.8 (!).*

*Today, Simon is experimenting with the File API and the new Slice() method introduced in Firefox 4. Here is how he implements a resume upload feature in a file uploader.*

Uploading a file is done with the [XHR Level2 object](https://developer.mozilla.org/En/Using_XMLHttpRequest). It provides different methods and events to handle the request (e.g., sending data and monitoring its progress) and to handle the response (e.g., checking if uploading was OK or an error occurred). For more information, read [How to develop a HTML5 Image Uploader](https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/).

Unfortunately, the XHR object does not provide a method to pause and resume an upload. But it is possible to implement that functionality by combining the new [File API’s slice()](https://developer.mozilla.org/en/DOM/Blob) method with the XHR’s abort() method. Let’s see how.

## Live demo

You can check out the [live fileUploader demo](https://www.speich.net/articles/html5-uploader.php) or [download the JavaScript and PHP code from github.com](https://github.com/speich/fileUploader).

## Pause and resume an upload

The idea is to provide the user with a button to pause an upload in progress and to resume it again later. Pausing the request is simple. Just abort the request with the abort() method. Make sure your user interface doesn’t report this as an error.

The harder part is resuming the upload, since the request was aborted and the connection closed. Instead of sending the whole file again, we use the blob’s mozSlice() method to first create a chunk containing the remaining part of the file. Then we create the new request, send the chunk, and append it to the part already saved on the server before the request was aborted.

### Creating a chunk

The chunk can be created as:

```
var chunk = file.mozSlice(start, end);
```

All we need to know is where to start slicing, that is, the number of bytes that was already uploaded. The easiest way would be to save the ProgressEvent’s `loaded`

property before we aborted the request. However, this number is not necessarily exactly the same as the number of bites written on the server. The most reliable approach is to send an additional request to fetch the size of the partially written file from the server before we upload again. Then this information can be used to slice the file and create the chunk.

### Summarizing the above chain of events

(assuming an upload is already in progress):

- user pauses upload
- state of UI is set to paused
- uploading is aborted
- server stops writing file to disk
- user resumes upload
- state of UI is set to resuming
- get size of partially written file from server
- slice file into remaining part (chunk)
- upload chunk
- state of UI is set to uploading
- server appends data

### JavaScript code

```
// Assuming that the request to fetch the already written bytes has just
// taken place and xhr.result contains the response from the server.
var start = xhr.result.numWrittenBytes;
var chunk = file.mozSlice(start, file.size);
var req = new XMLHttpRequest();
req.open('post', 'fnc.php?fnc=resume', true);
req.setRequestHeader("Cache-Control", "no-cache");
req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
req.setRequestHeader("X-File-Name", file.name);
req.setRequestHeader("X-File-Size", file.size);
req.send(chunk);
```

### PHP code

The only difference on the server side between handling a normal upload and a resumed upload is that in the latter case you need to append to your file instead of creating it.

```
$headers = getallheaders();
$protocol = $_SERVER[‘SERVER_PROTOCOL’];
$fnc = isset($_GET['fnc']) ? $_GET['fnc'] : null;
$file = new stdClass();
$file->name = basename($headers['X-File-Name']));
$file->size = $headers['X-File-Size']);
// php://input bypasses the php.ini settings, so we have to limit the file size ourselves:
$maxUpload = getBytes(ini_get('upload_max_filesize'));
$maxPost = getBytes(ini_get('post_max_size'));
$memoryLimit = getBytes(ini_get('memory_limit'));
$limit = min($maxUpload, $maxPost, $memoryLimit);
if ($headers['Content-Length'] > $limit) {
header($protocol.' 403 Forbidden');
exit('File size to big. Limit is '.$limit. ' bytes.');
}
$file->content = file_get_contents(’php://input’);
$flag = ($fnc == ‘resume’ ? FILE_APPEND : 0);
file_put_contents($file->name, $file->content, $flag);
function getBytes($val) {
$val = trim($val);
$last = strtolower($val[strlen($val) - 1]);
switch ($last) {
case 'g': $val *= 1024;
case 'm': $val *= 1024;
case 'k': $val *= 1024;
}
return $val;
}
```

**Caution!**

The PHP code example above does not do any security checks. A user can send and write any type of file to your disk or append to or even overwrite any of your files. So make sure you take the appropriate security measures when enabling uploading on your website.

## Resume upload after an error

The sequence of events for pause-and-resume can also be used to continue uploading after a network error. Instead of trying to upload the whole file again, get the already written file size from the server and slice the file into a new chunk first.

## Note about resuming a paused or broken file upload

Appending the chunk to the file might create a corrupted file, since you don’t have control over what the server writes after the request is aborted — if it writes anything at all.

## Resume upload after a browser crash

You can take the pause-and-resume functionality even a step further. It is possible (at least in theory) to even recover uploading after an unexpected closing or crashing of the browser. The problem is that after the browser was closed, the file object, which was read into memory, is lost. The user would have to re-pick or drag over the file again first, before being able to slice the file to resume the upload.

Instead, you could use the new [IndexedDB](https://developer.mozilla.org/en/IndexedDB) API and store the file before any uploading is done. Then after a browser crash, load the file from the database, slice into the remaining chunk and resume the upload.

## About
[
Simon Speich ](https://www.speich.net)

Simon Speich is a web developer, believer in web standards and a lover of Mozilla since Mozilla 0.8 He is also passionate about [photography](https://www.speich.net/photo/photodb/photo.php). You can find out more about him on his website [www.speich.net](https://www.speich.net/?lang=en).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 18 comments

Tim ReynoldsApril 8th, 2011 at 10:59voracityApril 9th, 2011 at 03:59voracityApril 9th, 2011 at 04:03Tony MechelynckApril 8th, 2011 at 11:47BazzarghApril 8th, 2011 at 13:39Jeremy WaltonApril 11th, 2011 at 22:32YanskyApril 12th, 2011 at 02:16SimonApril 12th, 2011 at 06:50Simon SpeichFebruary 9th, 2012 at 11:01Simon SpeichFebruary 26th, 2012 at 03:22DavitAugust 19th, 2011 at 03:54Simon SpeichAugust 19th, 2011 at 23:43Alejandro Invertir en bolsaSeptember 9th, 2011 at 16:21AlmasJanuary 5th, 2012 at 05:05Simon SpeichJanuary 6th, 2012 at 01:17Simon SpeichJanuary 7th, 2012 at 10:20AlmasJanuary 7th, 2012 at 10:46filkorJune 30th, 2012 at 14:29