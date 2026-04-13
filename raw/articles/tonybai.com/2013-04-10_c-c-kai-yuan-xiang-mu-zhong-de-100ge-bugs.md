---
title: C,C++开源项目中的100个Bugs
url: https://tonybai.com/2013/04/10/100-bugs-in-c-cpp-opensource-projects/
published: '2013-04-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C,C++开源项目中的100个Bugs

俄罗斯[OOO Program Verification Systems](http://www.viva64.com/)公司用自己的静态源码分析产品PVS-Studio对一些知名的C/C++开源项目，诸如[Apache Http Server](http://httpd.apache.org)、[Chromium](http://www.chromium.org)、[Clang](http://clang.llvm.org)、[CMake](http://www.cmake.org)、[MySQL](http://www.mysql.com)等的源码进行了分析，找出了[100个典型的Bugs](http://www.viva64.com/en/a/0079/)。个人觉得这份列表对C/C++ 程序员有一定参考意义。与其说事后用静态工具分析，倒不如在编码时就提高自知自觉，避免这份列表上的错误发生在你的代码中，因此这里将部分摘录一些Bugs（Bug编号这里不连续，为的是对应原文的编号）并做简要说明。原文将这份Bug列表分为了几类，这里也将沿用这个思路。

**一、数组和字符串处理错误**

数组和字符串处理错误是C/C++程序中最多的一类缺陷类型。这也可以看作是我们为拥有高效地底层内存操作能力而付出的代价。

**[**`#1`**]**[ Wolfenstein 3D](http://en.wikipedia.org/wiki/Wolfenstein_3D)项目 -"只有部分对象被clear了"

void CG_RegisterItemVisuals( int itemNum ) {

…

itemInfo_t *itemInfo;

…

memset( itemInfo, 0, sizeof( &itemInfo ) );

…

}

这里的Bug出现在memset那一行。代码的真实意图是clear iteminfo这块内存，但调用memset时，第三个参数传入的却是sizeof(&iteminfo)，要知道 sizeof(&itemInfo) != sizeof(itemInfo_t)，前者只是一个指针的大小罢了。正确的写法是：

memset(itemInfo, 0, sizeof(itemInfo_t)); 或memset(itemInfo, 0, sizeof(*itemInfo));

**[#2] **Wolfenstein 3D项目 -"只有部分Matrix被clear了"

ID_INLINE mat3_t::mat3_t( float src[ 3 ][ 3 ] ) {

memcpy( mat, src, sizeof( src ) );

}

这里的Bug出现在memcpy一行。程序的原意是将clear src[3][3]这个[二维数组](http://tonybai.com/2013/03/28/pointer-and-multi-dimension-array-in-c/)。但这里有个坑：那就是作为函数形式参数的数组名已经退化为指针了，对其sizeof只能得到一个指针的长度，因此这里的 memcpy只是copy了一个指针的长度，没有copy全。这里的代码是C++代码，原文中给出了正确的改正方法 – 传reference：

ID_INLINE mat3_t::mat3_t( float (&src)[3][3] )

{

memcpy( mat, src, sizeof( src ) );

}

**[#4] **[ReactOS](http://www.reactos.org)项目 – "错误地计算一个字符串的长度"

static const PCHAR Nv11Board = "NV11 (GeForce2) Board";

static const PCHAR Nv11Chip = "Chip Rev B2";

static const PCHAR Nv11Vendor = "NVidia Corporation";

BOOLEAN

IsVesaBiosOk(…)

{

…

if (!(strncmp(Vendor, Nv11Vendor, sizeof(Nv11Vendor))) &&

!(strncmp(Product, Nv11Board, sizeof(Nv11Board))) &&

!(strncmp(Revision, Nv11Chip, sizeof(Nv11Chip))) &&

(OemRevision == 0×311))

…

}

Bug处在IsVesaBiosOK中那一串strncmp调用中，代码将一个指针的size传入strncmp作为第三个参数，导致 strncmp实际只是比较了字符串的前4 or 8个字节，而不是字符串的全部内容。

**[#6] **CPU Identifying Tool项目 – 数组越界

#define FINDBUFFLEN 64 // Max buffer find/replace size

…

int WINAPI Sticky (…)

{

…

static char findWhat[FINDBUFFLEN] = {'\0'};

…

findWhat[FINDBUFFLEN] = '\0';

…

}

bug出在"findWhat[FINDBUFFLEN] = ‘\0′;”这一行。数组的最大长度为FINDBUFFLEN，但下标的最大值应该是FINDBUFFLEN-1，而不是FINDBUFFLEN。因此这 行代码显然应该改为findWhat[FINDBUFFLEN-1] = '\0';

**[#7]** Wolfenstein 3D项目 – 数组越界

typedef struct bot_state_s

{

…

char teamleader[32]; //netname of the team leader

…

} bot_state_t;

void BotTeamAI( bot_state_t *bs ) {

…

bs->teamleader[sizeof( bs->teamleader )] = '\0';

…

}

"sizeof( bs->teamleader )]"这行的结果值已经超出了数组的最大边界，正确的代码是：

bs->teamleader[

sizeof(bs->teamleader) / sizeof(bs->teamleader[0]) – 1

] = '\0';

**[#8] **[Miranda IM](http://www.miranda-im.org)项目 – 只Copy了部分字符串

struct _textrangew

{

CHARRANGE chrg;

LPWSTR lpstrText;

} TEXTRANGEW;

const wchar_t* Utils::extractURLFromRichEdit(…)

{

…

::CopyMemory(tr.lpstrText, L"mailto:", 7);

…

}

这里的bug在于L"mailto:"是宽字符串，宽字符串中的每个字符占2或4个字节（依Compiler使用的[字符集](http://tonybai.com/2007/11/03/also-talk-about-char-encoding/)编码而定），因此这里只 copy 7个字节显然是不够的，应该是7 * sizeof(wchar_t)。

**[#9]** CMake项目 – 循环內的数组越界

static const struct {

DWORD winerr;

int doserr;

} doserrors[] =

{

…

};

static void

la_dosmaperr(unsigned long e)

{

…

for (i = 0; i < sizeof(doserrors); i++)

{

if (doserrors[i].winerr == e)

{

errno = doserrors[i].doserr;

return;

}

}

…

}

作者原本意图la_dosmaperr中for循环的次数等于数组的元素个数，但sizeof(doserrors)返回的却是数组占用的字节个数，这远远大于数组元素个数，因此造成数组越界。正确的写法：

for (i = 0; i < sizeof(doserrors) / sizeof(*doserrors); i++)

**[#10]** CPU Identifying Tool项目 – 打印到自身的字符串

char * OSDetection ()

{

…

sprintf(szOperatingSystem,

"%sversion %d.%d %s (Build %d)",

szOperatingSystem,

osvi.dwMajorVersion,

osvi.dwMinorVersion,

osvi.szCSDVersion,

osvi.dwBuildNumber & 0xFFFF);

…

sprintf (szOperatingSystem, "%s%s(Build %d)",

szOperatingSystem, osvi.szCSDVersion,

osvi.dwBuildNumber & 0xFFFF);

…

}

通过sprintf，szOperatingSystem字符串将自己打印到自己里面，这是十分危险的，将导致无法预知的错误结果，可能会导致栈溢出等严重问题。

**[#12]** [Notepad++](http://notepad-plus-plus.org)项目 – 数组局部clear

#define CONT_MAP_MAX 50

int _iContMap[CONT_MAP_MAX];

…

DockingManager::DockingManager()

{

…

memset(_iContMap, -1, CONT_MAP_MAX);

…

}

代码的原本试图将数组_iContMap清零，但memset的第三个参数CONT_MAP_MAX并不能代表数组的真正大小，而只是数组的元素个数而已，显然其忘记乘以sizeof(int)了。

**二、未定义行为**

在C/C++的语言规范中，我们常常能看到“xx is undefined”。规范中并没有明确表明这类错误是什么样子的，只是说取决于Compiler的实现，也许Compiler会给出正确的结果，但这么使用却是不可移植的。

**[#1]** Chromium项目 – 智能指针的误用

void AccessibleContainsAccessible(…)

{

…

auto_ptr<VARIANT> child_array(new VARIANT[child_count]);

…

}

这里的问题在于使用new[]分配的内存，在智能指针释放时却用了delete，这将会导致未定义行为。看看autoptr的destructor就知道了：

~auto_ptr() {

delete _Myptr;

}

我们可以找一些更合适的类来fix这个问题，比如boost::scopedarray。

**[#2]** IPP Sample项目 – 经典未定义行为

template<typename T, Ipp32s size> void HadamardFwdFast(…)

{

Ipp32s *pTemp;

…

for(j=0;j<4;j++) {

a[0] = pTemp[0*4] + pTemp[1*4];

a[1] = pTemp[0*4] – pTemp[1*4];

a[2] = pTemp[2*4] + pTemp[3*4];

a[3] = pTemp[2*4] – pTemp[3*4];

pTemp = pTemp++;

…

}

…

}

很多人一眼就看到了"pTemp = pTemp++"这行，对于这个代码编译器会产生两种结果截然不同的翻译：

pTemp = pTemp + 1;

pTemp = pTemp;

或

TMP = pTemp;

pTemp = pTemp + 1;

pTemp = TMP;

到底是哪种呢？依赖于编译器的实现，甚至是优化级别的设定。

**三、与运算优先级相关的错误**

**[#1]** MySQL工程 – !和&的运算优先级

int ha_innobase::create(…)

{

…

if (srv_file_per_table

&& !mysqld_embedded

&& (!create_info->options & HA_LEX_CREATE_TMP_TABLE)) {

…

}

这段代码原意是想测试create_info->options变量中几个bit位的值是否set了，即!(create_info->options & HA_LEX_CREATE_TMP_TABLE)，但由于!的运算优先级高于&，实际逻辑变成了(!create_info->options) & HA_LEX_CREATE_TMP_TABLE了。如果想要这段代码如期工作，就不要吝啬小括号了。

**[#2]** [Emule](http://www.emule-project.net)工程 – *和++的运算优先级

STDMETHODIMP

CCustomAutoComplete::Next(…, ULONG *pceltFetched)

{

…

if (pceltFetched != NULL)

*pceltFetched++;

…

}

显然作者原意是想对pceltFetched所指向的long型变量进行++操作，但由于*和++的运算优先级没有搞对，导致实际上执行了*(pceltFetched++)的操作，而不是(*pceltFetched)++操作。

**[#3]** Chromium项目 – &和!=的运算优先级

#define FILE_ATTRIBUTE_DIRECTORY 0×00000010

bool GetPlatformFileInfo(PlatformFile file, PlatformFileInfo* info) {

…

info->is_directory =

file_info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY != 0;

…

}

这个程序员的意图是通过测试file_info.dwFileAttributes的几个bit位的值来判定是否是目录，逻辑上应该是(file_info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0，但由于!=优先级高于&，原代码中无括号，结果逻辑变成了file_info.dwFileAttributes & (FILE_ATTRIBUTE_DIRECTORY != 0)，导致is_directory将永远求值为true。

**[#4]** BCmenu项目 – if和else弄混

void BCMenu::InsertSpaces(void)

{

if(IsLunaMenuStyle())

if(!xp_space_accelerators) return;

else

if(!original_space_accelerators) return;

…

}

这又是C语言的一个“大坑”，无奈这个BCMenu项目的程序员掉坑里了。虽然从代码缩进上来看，else似乎是与最外层的if配对使用，但实际这段代码的效果是：

if(IsLunaMenuStyle())

{

if(!xp_space_accelerators) {

return;

} else {

if(!original_space_accelerators) return;

}

}

这显然不是程序员原意，看来括号必要时还是不能省略的。修改后的代码如下：

if(IsLunaMenuStyle()) {

if(!xp_space_accelerators) return;

} else {

if(!original_space_accelerators) return;

}

**四、格式化输出错误**

**[#1]** ReactOS项目 – 错误地输出WCHAR字符

static void REGPROC_unescape_string(WCHAR* str)

{

…

default:

fprintf(stderr,

"Warning! Unrecognized escape sequence: \\%c'\n",

str[str_idx]);

…

}

%c是用来格式化输出非宽字符的，这里用来输出WCHAR显然会得到错误的结果，fix solution是将%c换位%C。

**[#2]** Intel AMT SDK项目 – 缺少%s

void addAttribute(…)

{

…

int index = _snprintf(temp, 1023,

"%02x%02x:%02x%02x:%02x%02x:%02x%02x:"

"%02x%02x:02x%02x:%02x%02x:%02x%02x",

value[0],value[1],value[2],value[3],value[4],

value[5],value[6],value[7],value[8],

value[9],value[10],value[11],value[12],

value[13],value[14],value[15]);

…

}


不解释了，自己慢慢数和对照吧。

**[#3]** Intel AMT SDK项目 – 未使用的参数

bool GetUserValues(…)

{

…

printf("Error: illegal value. Aborting.\n", tmp);

return false;

}

显然tmp是多余的。

**五、书写错误**

**[#1]** Miranda IM项目 – 在if中赋值

void CIcqProto::handleUserOffline(BYTE *buf, WORD wLen)

{

…

else if (wTLVType = 0×29 && wTLVLen == sizeof(DWORD))

…

}

“wTLVType = 0×29”显然是笔误，应该是“wTLVType == 0×29”才对。

**[#3]** Clang项目 – 对象名书写错误

static Value *SimplifyICmpInst(…) {

…

case Instruction::Shl: {

bool NUW =

LBO->hasNoUnsignedWrap() && LBO->hasNoUnsignedWrap();

bool NSW =

LBO->hasNoSignedWrap() && RBO->hasNoSignedWrap();

…

}

从最后一行先后使用了LBO和RBO来看，前面只用了LBO的那行很可能是有问题的，正确的应该是：

bool NUW =

LBO->hasNoUnsignedWrap() && RBO->hasNoUnsignedWrap();

**[#6]** G3D Content Pak项目 – 一对括号放错了地方

bool Matrix4::operator==(const Matrix4& other) const {

if (memcmp(this, &other, sizeof(Matrix4) == 0)) {

return true;

}

…

}

由于括号放错了地方，导致memcmp最后的参数变成了sizeof(Matrix4) == 0，这行代码的正确写法应该是：

if (memcmp(this, &other, sizeof(Matrix4)) == 0) {

**[#8]** Apache Http Server项目 – 多余的sizeof

PSECURITY_ATTRIBUTES GetNullACL(void)

{

PSECURITY_ATTRIBUTES sa;

sa = (PSECURITY_ATTRIBUTES)

LocalAlloc(LPTR, sizeof(SECURITY_ATTRIBUTES));

sa->nLength = sizeof(sizeof(SECURITY_ATTRIBUTES));

…

}

最后一行显然是笔误，sizeof(sizeof(SECURITY_ATTRIBUTES))应该写为sizeof(SECURITY_ATTRIBUTES)才对。

**[#10]** Notepad++项目 – 在本来应该用&的地方使用了&&

TCHAR GetASCII(WPARAM wParam, LPARAM lParam)

{

…

result=ToAscii(wParam,

(lParam >> 16) && 0xff, keys,&dwReturnedValue,0);

…

}

(lParam >> 16) && 0xff没有什么意义，求值结果总是true。这里的代码应该是(lParam >> 16) & 0xff。

**[#12]** Fennec Media Project项目 – 额外的分号

int settings_default(void)

{

…

for(i=0; i<16; i++);

for(j=0; j<32; j++)

{

settings.conversion.equalizer_bands.boost[i][j] = 0.0;

settings.conversion.equalizer_bands.preamp[i] = 0.0;

}

}

这又是一个实际逻辑与代码缩进不符的例子。作者的原意是这样的：

for(i=0; i<16; i++)

{

for(j=0; j<32; j++)

{

settings.conversion.equalizer_bands.boost[i][j] = 0.0;

settings.conversion.equalizer_bands.preamp[i] = 0.0;

}

}

但实际执行代码逻辑却是：

for(i=0; i<16; i++)

{

;

}

for(j=0; j<32; j++)

{

settings.conversion.equalizer_bands.boost[i][j] = 0.0;

settings.conversion.equalizer_bands.preamp[i] = 0.0;

}

这一切都是那个;导致的。

**六、对基本函数和类的误用**

**[#2]** TortoiseSVN项目 – remove函数的误用

STDMETHODIMP CShellExt::Initialize(….)

{

…

ignoredprops = UTF8ToWide(st.c_str());

// remove all escape chars ('\\')

std::remove(ignoredprops.begin(), ignoredprops.end(), '\\');

break;

…

}

作者意图删除所有'\\'，但他用错了函数，remove函数只是交换元素的位置，将要删除的元素交换到尾部trash，并且返回指向trash首地址的iterator。正确的做法应该是"v.erase(remove(v.begin(), v.end(), 2), v.end())"。

**[#5]** Pixie项目 – 在循环中使用alloca函数

inline void triangulatePolygon(…) {

…

for (i=1;i<nloops;i++) {

…

do {

…

do {

…

CTriVertex *snVertex =

(CTriVertex *)alloca(2*sizeof(CTriVertex));

…

} while(dVertex != loops[0]);

…

} while(sVertex != loops[i]);

…

}

…

}

alloca函数在栈上分配内存，因此在循环中使用alloca可能会很快导致栈溢出。

**七、无意义的代码**

**[#1]** IPP Samples项目 – 不完整的条件

void lNormalizeVector_32f_P3IM(Ipp32f *vec[3],

Ipp32s* mask, Ipp32s len)

{

Ipp32s i;

Ipp32f norm;

for(i=0; i<len; i++) {

if(mask<0) continue;

norm = 1.0f/sqrt(vec[0][i]*vec[0][i]+

vec[1][i]*vec[1][i]+vec[2][i]*vec[2][i]);

vec[0][i] *= norm; vec[1][i] *= norm; vec[2][i] *= norm;

}

}

mask是Ipp32s类型指针，这样if (mask< 0)这句代码显然没啥意义，正确的代码应该是：

if (mask[i] < 0) continue;

**[#2]** QT项目 – 重复的检查

Q3TextCustomItem* Q3TextDocument::parseTable(…)

{

…

while (end < length

&& !hasPrefix(doc, length, end, QLatin1String("</td"))

&& !hasPrefix(doc, length, end, QLatin1String("<td"))

&& !hasPrefix(doc, length, end, QLatin1String("</th"))

&& !hasPrefix(doc, length, end, QLatin1String("<th"))

&& !hasPrefix(doc, length, end, QLatin1String("<td"))

&& !hasPrefix(doc, length, end, QLatin1String("</tr"))

&& !hasPrefix(doc, length, end, QLatin1String("<tr"))

&& !hasPrefix(doc, length, end, QLatin1String("</table"))) {

…

}

这里对"<td"做了两次check。

**八、总是True或False的条件**

**[#1]** Shareaza项目 – char类型的值范围

void CRemote::Output(LPCTSTR pszName)

{

…

CHAR* pBytes = new CHAR[ nBytes ];

hFile.Read( pBytes, nBytes );

…

if ( nBytes > 3 && pBytes[0] == 0xEF &&

pBytes[1] == 0xBB && pBytes[2] == 0xBF )

{

pBytes += 3;

nBytes -= 3;

bBOM = true;

}

…

}

表达式"pBytes[0] == 0xEF"总是False。char类型的值范围是-128~127 < 0xEF，因此这个表达式总是False，导致整个if condition总是为False，与预期逻辑不符。

**[#3]** VirtualDub项目 – 无符号类型总是>=0

typedef unsigned short wint_t;

…

void lexungetc(wint_t c) {

if (c < 0)

return;

g_backstack.push_back(c);

}

c是unsigned short类型，永远不会小于0,也就是说if (c < 0)永远为False。

**[#8]** MySQL项目 – 条件错误

enum enum_mysql_timestamp_type

str_to_datetime(…)

{

…

else if (str[0] != ‘a’ || str[0] != 'A')

continue; /* Not AM/PM */

…

}

if (str[0] != ‘a’ || str[0] != 'A')这个条件永远为真。也许这块本意是想用&&。

**九、代码漏洞**

导致漏洞的代码错误实际上也都是笔误、不正确的条件以及不正确的数组操作等。但这里还是想将一些特定错误划归为一类，因为入侵者可以利用这些错误来攻击你的代码，获取其利益。

**[#1]** Ultimate TCP/IP项目 – 空字符串的错误检查

char *CUT_CramMd5::GetClientResponse(LPCSTR ServerChallenge)

{

…

if (m_szPassword != NULL)

{

…

if (m_szPassword != '\0')

{

…

}

第二个if condition check意图检查m_szPassword是否为空字符串，但却错误的将指针与'\0'进行比较，正确的代码应该是这样的：

if (*m_szPassword != '\0')

**[#2]** Chromium项目 – NULL指针的处理

bool ChromeFrameNPAPI::Invoke(…)

{

ChromeFrameNPAPI* plugin_instance =

ChromeFrameInstanceFromNPObject(header);

if (!plugin_instance &&

(plugin_instance->automation_client_.get()))

return false;

…

}

一旦plugin_instance为NULL，!plugin_instance为True，代码对&&后面的子条件求值，引用plugin_instance将导致程序崩溃。正确的做法应该是：

if (plugin_instance &&

(plugin_instance->automation_client_.get()))

return false;

**[#5]** Apache httpd Server项目 – 不完整的缓冲区clear

#define MEMSET_BZERO(p,l) memset((p), 0, (l))

void apr__SHA256_Final(…, SHA256_CTX* context) {

…

MEMSET_BZERO(context, sizeof(context));

…

}

这个错误前面提到过，sizeof(context)只是指针的大小，将之改为sizeof(*context)就OK了。

**[#7]** PNG Library项目 – 意外的指针clear

png_size_t

png_check_keyword(png_structp png_ptr, png_charp key,

png_charpp new_key)

{

…

if (key_len > 79)

{

png_warning(png_ptr, "keyword length must be 1 – 79 characters");

new_key[79] = '\0';

key_len = 79;

}

…

}

new_key的类型为png_charpp，顾名思义，这是一个char**类型，但代码中new_key[79] = ‘\0′这句显然是要给某个char赋值，但new_key[n]得到的应该是一个地址，给一个地址赋值为’\0′显然是有误的。正确的写法应该是(*new_key)[79] = '\0'。

**[#10]** Miranda IM项目 – 保护没生效

void Append( PCXSTR pszSrc, int nLength )

{

…

UINT nOldLength = GetLength();

if (nOldLength < 0)

{

// protects from underflow

nOldLength = 0;

}

…

}

nOldLength椒UINT类型，其值永远不会小于0,因此if (nOldLength < 0)这行成了摆设。

**[#12]** Ultimate TCP/IP项目 – 不正确的循环结束条件

void CUT_StrMethods::RemoveSpaces(LPSTR szString) {

…

size_t loop, len = strlen(szString);

// Remove the trailing spaces

for(loop = (len-1); loop >= 0; loop–) {

if(szString[loop] != ' ')

break;

}

…

}

循环中的结束条件loop >= 0将永远为True，因为loop变量的类型是size_t是unsigned类型，永远不会小于0。

**十、拷贝粘贴**

和笔误不同，程序员们决不因该低估拷贝粘贴问题，这类问题发生了太多。程序员们花费了大量时间在这些问题的debug上。

**[#1]** Fennec Media Project项目 – 处理数组元素时出错

void* tag_write_setframe(char *tmem,

const char *tid, const string dstr)

{

…

if(lset)

{

fhead[11] = '\0';

fhead[12] = '\0';

fhead[13] = '\0';

fhead[13] = '\0';

}

…

}


咋看一下，fhead[13]做了两次赋值，似乎没啥问题。但仔细想一下，最后那行程序员的原意极可能是想写fhead[14] = '\0'。问题就在这里了。

[#2] MySQL项目 – 处理数组元素时出错

static int rr_cmp(uchar *a,uchar *b)

{

if (a[0] != b[0])

return (int) a[0] – (int) b[0];

if (a[1] != b[1])

return (int) a[1] – (int) b[1];

if (a[2] != b[2])

return (int) a[2] – (int) b[2];

if (a[3] != b[3])

return (int) a[3] – (int) b[3];

if (a[4] != b[4])

return (int) a[4] – (int) b[4];

if (a[5] != b[5])

return (int) a[1] – (int) b[5];

if (a[6] != b[6])

return (int) a[6] – (int) b[6];

return (int) a[7] – (int) b[7];

}


编写这类代码时，我猜绝大多数人会选择Copy-Paste，然后再逐行修改，问题就发生在修改过程中，上面的代码中当处理a[5] != b[5]时就忘记修改一个下标了：return (int) a[1] – (int) b[5];显然这里的正确代码应该是return (int) a[5] – (int) b[5]。

**[#3]** TortoiseSVN项目 文件名不正确

BOOL GetImageHlpVersion(DWORD &dwMS, DWORD &dwLS)

{

return(GetInMemoryFileVersion(("DBGHELP.DLL"),

dwMS,

dwLS)) ;

}

BOOL GetDbgHelpVersion(DWORD &dwMS, DWORD &dwLS)

{

return(GetInMemoryFileVersion(("DBGHELP.DLL"),

dwMS,

dwLS)) ;

}

GetImageHlpVersion和GetDbgHelpVersion都使用了"DBGHELP.DLL"文件，显然GetImageHlpVersion写错文件名了。应该用"IMAGEHLP.DLL"就对了。

**[#4]** Clang项目 – 等同的函数体

MapTy PerPtrTopDown;

MapTy PerPtrBottomUp;

void clearBottomUpPointers() {

PerPtrTopDown.clear();

}

void clearTopDownPointers() {

PerPtrTopDown.clear();

}

我们看到虽然两个函数名不同，但是函数体的内容是相同的，显然又是copy-paste惹的祸。做如下修改即可：

void clearBottomUpPointers() {

PerPtrBottomUp.clear();

}


**十一、Null指针的校验迟了**

这里的“迟了”的含义是先使用指针，然后再校验指针是否为NULL。

**[#1]** Quake-III-Arena项目 – 校验迟了

void Item_Paint(itemDef_t *item) {

vec4_t red;

menuDef_t *parent = (menuDef_t*)item->parent;

red[0] = red[3] = 1;

red[1] = red[2] = 0;

if (item == NULL) {

return;

}

…

}


在校验item是否为NULL前已经使用过item了，一旦item真的为NULL，那程序必然崩溃。

**十二、其他杂项**

**[#1]** Image Processing 项目 – 八进制数

inline

void elxLuminocity(const PixelRGBus& iPixel,

LuminanceCell< PixelRGBus >& oCell)

{

oCell._luminance = uint16(0.2220f*iPixel._red +

0.7067f*iPixel._blue + 0.0713f*iPixel._green);

oCell._pixel = iPixel;

}

inline

void elxLuminocity(const PixelRGBi& iPixel,

LuminanceCell< PixelRGBi >& oCell)

{

oCell._luminance = 2220*iPixel._red +

7067*iPixel._blue + 0713*iPixel._green;

oCell._pixel = iPixel;

}

第二个函数，程序员原意是使用713这个十进制整数，但0713 != 713，在C中，0713是八进制的表示法，Compiler会认为这是个八进制数。

**[#2]** IPP Sample工程 – 一个变量用于两个loop中

JERRCODE CJPEGDecoder::DecodeScanBaselineNI(void)

{

…

for(c = 0; c < m_scan_ncomps; c++)

{

block = m_block_buffer + (DCTSIZE2*m_nblock*(j+(i*m_numxMCU)));

// skip any relevant components

for(c = 0; c < m_ccomp[m_curr_comp_no].m_comp_no; c++)

{

block += (DCTSIZE2*m_ccomp[c][/c][/c].m_nblocks);

}

…

}

变量c用在了两个loop中，这会导致只有部分数据被处理，或外部循环中止。

**[#3]** Notepad++项目 – 怪异的条件表达式

int Notepad_plus::getHtmlXmlEncoding(….) const

{

…

if (langT != L_XML && langT != L_HTML && langT == L_PHP)

return -1;

…

}

代码中的那行if条件等价于 if (langT == L_PHP)，显然似乎不是作者原意，猜测正确的代码应该是这样的：

int Notepad_plus::getHtmlXmlEncoding(….) const

{

…

if (langT != L_XML && langT != L_HTML && langT != L_PHP)

return -1;

…

}

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

写 C/C++ 的都该注意了

很好,收藏了

好文，get。附原文地址：http://www.viva64.com/en/a/0079/

不错，也是在实际开发过程中的常见bug

好文！

过来支持一下 值得收藏分享

好东西 谢谢分享

很久没有过来了，今天过来看一看！