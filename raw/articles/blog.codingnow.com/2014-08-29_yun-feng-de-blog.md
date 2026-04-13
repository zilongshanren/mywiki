---
title: 云风的 BLOG
url: https://blog.codingnow.com/2014/08/
published: '2014-08-29'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

Unity3D 的 asset bundle 的格式并没有公开。但为了做更好的差异更新，我们还是希望了解其打包格式。这样可以制作专门的差异比较合并工具，会比直接做二进制差异比较效果好的多。因为可以把 asset bundle 内的数据拆分为独立单元，只对变更的单元做差异比较即可。

网上能查到的资料并不是官方给出的，最为流行的是一个叫做 [disunity](https://github.com/ata4/disunity) 的开源工具。它是用 java 编写的，只有源代码，而没有给出格式说明（而后者比代码重要的多）。通过阅读 disunity 的代码，我整理出如下记录：


asset bundle 分为压缩模式和非压缩模式。压缩模式仅仅是用开源的 [lzma 库](http://www.7-zip.org/sdk.html) 对整个非压缩包做了一次整体压缩。压缩数据的头有 13 个字节，前 5 个字节是 lzma 解压缩的 API 需要穿入的 props ，接下来的 4 字节是解压缩后的数据库长度。最后 4 字节不用理会它。

把压缩数据解开后，就和非压缩模式没有差别，下面只讨论非压缩格式：

assert bundle 的文件头是从这样一个数据结构序列化出来的。

struct AssetBundleFileHead {
struct LevelInfo {
unsigned int PackSize;
unsigned int UncompressedSize;
};
string FileID;
unsigned int Version;
string MainVersion;
string BuildVersion;
size_t MinimumStreamedBytes;
size_t HeaderSize;
size_t NumberOfLevelsToDownloadBeforeStreaming;
size_t LevelCount;
LevelInfo LevelList[];
size_t CompleteFileSize;
size_t FileInfoHeaderSize;
bool Compressed;
};

string 是直接以 \0 结尾的字符串，顺序序列化；size_t 是大端的 4 字节数字；bool 是单个字节；vector 就是顺着排列的结构。

根据 Unity 版本的不同，assert bundle 的格式也不完全相同。Version 指明了 bundle 的格式版本，从 Unity 3.5 开始到 4.x 版都使用 Version = 3 ，下面只讨论这个版本。HeaderSize 应该恰好等于以上这个文件头的数据长度。

一个 assert bundle 是由多个 asset 文件打包而成，接下来顺序打包了这些 asset 。序列化成这样的结构：

struct AssetFileHeader {
struct AssetFileInfo {
string name;
size_t offset;
size_t length;
};
size_t FileCount;
AssetFileInfo File[];
};

## 这样我们就可以分解出被打包在一起的多个 Asset 了（大多数情况下只有一个）。offset 表示的是除去 HeaderSize 后的偏移量。我们可以用 HeaderSize 加上那个部分的 offset 得到这个部分相对于整个 bundle 的文件偏移。

对于每个 asset ，又有它自己的数据头。数据头除了基本的数据头结构 AssetHeader 外，还有额外的三个部分。disunity 把它们称为 TypeTree ObjectPath 和 AssetRef 。注意：这里 Format 随不同 Unity3D 的版本有所不同，我们只关心目前的版本的格式，这里 Format 为 9 （其它版本的格式，在大小端等问题上有所不同）。

struct AssetHeader {
size_t TypeTreeSize;
size_t FileSize;
unsigned int Format;
size_t dataOffset;
size_t Unknown;

Unity 对 Asset 数据做了简单粗暴的序列化操作。整个序列化过程是针对每种对象的数据结构进行的。TypeTree 是对数据结构本身的描述，通过这个描述，就可以反序列化出每个对象。

AssetHeader 后面紧跟着的就是 TypeTree 。但是，这个 TypeTree 对于 asset bundle 来说是可选的，因为数据结构的信息可以事先放置在引擎中（引擎多半只支持固有的数据类型）。在发布到移动设备上时，TypeTree 是不打包到 asset bundle 中的。

每个 asset 对象，都有一个 class id ，可以在 TypeTree 中查到如何反序列化。class id 的和具体类型的对应关系，在 [Unity3d 的官方文档](http://docs.unity3d.com/Manual/ClassIDReference.html) 可以查到。但若我们只是想将差异比较在对象一级进行（而不是具体比较对象中具体的属性），那么就不需要解开具体对象的细节信息，这部分也不用关心。所以这里也不展开（有兴趣可以读一下 disunity 的代码，格式并不复杂）。

在 AssetHeader 中的 TypeTreeSize 指的就是 TypeTree 部分的大小。接下来是每个 AssetObject 的描述数据。

struct ObjectHeader {
struct ObjectInfo {
int pathID;
int offset;
int length;
byte classID[8];
};
int ObjectCount;
ObjectInfo Object[];
};

这里，所有的 int 都是以小端编码的 4 字节整数（不同于外部文件格式采用的大端编码）。在 Unity3D 中，每个对象都有唯一的字符串 path ，但是在 asset bundle 里并没有直接保存字符串，而是一个 hash 过的整数，也可以看成是对这个对象的索引号。真正的对象放在数据头的后面，偏移量为 offset 的地方。

这里的 offset 是相对当前 asset 块的。如果想取得正确的相对整个文件的位置，应该是文件的 HeaderSize + asset 的 offset + asset 的 dataOffset + 这里的 object offset 。


接在 ObjectHeader 后的是 AssetRef 表，记录了 Asset 的引用关系。用于指明这个 bundle 内 asset 对外部 asset 的引用情况。AssetRefTable 结构如下：

struct AssetTable {
struct AssetRef {
byte GUID[8];
int type;
string filePath;
string assetPath;
};
int Count;
byte Unknown;
vector Refs;