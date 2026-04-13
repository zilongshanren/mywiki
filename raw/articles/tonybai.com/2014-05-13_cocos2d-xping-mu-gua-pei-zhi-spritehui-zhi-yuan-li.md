---
title: Cocos2d-x屏幕适配之Sprite绘制原理
url: https://tonybai.com/2014/05/13/sprite-draw-principles-of-cocos2dx-screen-adaptation/
published: '2014-05-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x屏幕适配之Sprite绘制原理

手机(智能终端)游戏绝大多数为全屏(Full Screen)显示，这样开发人员在制作游戏时势必要考虑不同手机(智能终端）屏幕大小、宽高比的不同给游戏画面带来的影响，并且要将这种影响降低到最 小，努力使用不同终端的游戏玩家拥有几乎相同的游戏画面体验。为此各种游戏引擎在屏幕适配方面都给出了自己的方案，[Cocos2d-x](http://www.cocos2d-x.org)也不例外。 在Cocos2d-x官网Wiki上特地撰写了一篇讲解Cocos2d-x多屏幕适配原理的文章“[Detailed explanation of Cocos2d-x Multi-resolution adaptation](http://www.cocos2d-x.org/wiki /Detailed_explanation_of_Cocos2d-x_Multi-resolution_adaptation)”。

这里我们以Cocos2d-x引擎（基于2.2.2版本）自带的Sample项目HelloCpp(cocos2d-x-2.2.2/samples/Cpp/HelloCpp）为例，直观的看看这个方案带来的好 处。首先，我们对HelloCpp项目做些许改造：

– 注释掉AppDelegate.cpp中applicationDidFinishLaunching下的pEGLView->setDesignResolutionSize(designResolutionSize.width, designResolutionSize.height, kResolutionNoBorder);

– 仅使用Resource/iphone下的资源，即仅searchPath.push_back(smallResource.directory)； 这里我们有一张480×320分辨率大小PNG文件。

– 通过改变proj.linux/main.cpp中的eglView->setFrameSize(960, 640);来改变屏幕参数。（用linux工程模拟甚为方便，编译和运行占用资源小，极为迅捷，效果与Android平台是等 效的）

我们对比一下以下三种条件下的游戏Demo显示结果：

1) 屏幕大小480×320，未做任何屏幕适配工作，不调用pEGLView->setDesignResolutionSize。

2) 屏幕大小960×640，未做任何屏幕适配工作，不调用pEGLView->setDesignResolutionSize。

3) 屏幕大小同为960×640，按照上面Cocos2d-x屏幕适配指南Wiki中的做法，调用pEGLView->setDesignResolutionSize(480, 320);

如我们所料，我们得到三个截然不同的结果。

第一种情况，我们所得到的游戏屏幕截图如下：

![](../../assets/abaf187019e0bc08.jpg)


第二种情况，我们所得到的游戏屏幕截图如下：

![](../../assets/a8f2a554a09d9da6.jpg)


第三种情况，我们所得到的游戏屏幕截图如下：

![](../../assets/90d188b6a9292c61.jpg)


第一种情况是最理想的情况，屏幕大小与背景图片大小相同，如我们所愿，屏幕与背景图片吻合的天衣无缝。

第二种情况显然是模拟我们初次遇到问题的场景。屏幕Size扩大为原先的二倍，在资源没有变化的情况下，我们发现480×320大小的背景图片没 有铺满屏幕，仅仅是居中显示，并在四周露出较多”黑边“，这显然不是我们想要的。

第三种情况，也就是我们按照官方屏幕适配方案调整后得到的结果，在资源依旧不变的情况下，我们得到了相对令人满意的结果：背景图片恰如其分的铺满 整个屏幕，比例正确。这样我们用一套资源就可以同时适配两个屏幕了：480×320、960×640。这两种终端的玩家至少不会对我们的游戏心生 抱怨之情^_^。

当然在遇到第二种情况的时候，你也大可再准备一套新资源，比如一张960×640的背景图片。在480×320手机上，使用480×320的图 片；在960×640的手机上，使用960×640的背景图片。但这种方法的弊端至少有三：

– 包大了：游戏的安装包Size急剧变大。

– 活儿多了：因适配屏幕种类太多而制作大量的图片。

– 新屏幕出来咋办：如果某个厂家突然于某天出品一款手机，其分辨率与以往市面上的所有手机均不同，那你的游戏因没有对应的资源，肯定无法很好适配该手机，导 致较差用户体验。

为此，适配屏幕唯一的出路似乎只有按照官方推荐的方案进行了，当然适当结合有限种类的资源也许可以更好的提升游戏体验。

如果仅仅从游戏制作角度来看，我们找到了可以适配屏幕的方法就可以了，没有必要刨根问底。甚至当有人问起来：为何 setDesignResolutionSize后，背景图片就可以充满屏幕了呢？我们可以回答：“引擎对精灵进行了缩放，就是这样”。但对于上 面的背景精灵来说，真的是我们理解的普通意义上的“精灵缩放(Scale)吗？本着“知其然，也要知其所以然”的精神，这里对引擎如何对 Sprite进行绘制进行了一番研究，我还真发现了一些与我之前理解差异较大的“深奥”原理，这里与大家一起分享一下。

**一、绘制参数初始化**

我们还是从代码开始，了解一下引擎绘制参数的初始化工作是如何做的、在哪里做的，为后续的分析做些铺垫。这里以Cocos2d-x 2.2.2 Android平台为例。关于Cocos2d-x 2.2.2 Android平台的引擎粗线条启动流程分析，可以参考《[Hello，Cocos2d-x](http://tonybai.com/2014/03/11/hello-cocos2dx/)》这篇文章。看完这篇文章，你就会知道我们这次应该从Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit开 始。

// samples/Cpp/HelloCpp/proj.android/jni/hellocpp/main.cpp

void Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit(

JNIEnv* env, jobject thiz, jint w, jint h)

{

if (!CCDirector::**sharedDirector**()->getOpenGLView())

{

CCEGLView *view = CCEGLView::sharedOpenGLView();

**view->setFrameSize(w, h);**

AppDelegate *pAppDelegate = new AppDelegate();

CCApplication::sharedApplication()->run();

}

… …

}

这里是引擎部分初始化的起点:CCDirector和CCEGLView先后完成创建与初始化。接下来我们分别看一下这两个过程，我们主要关 注与绘制参数设置相关的内容：

bool CCDirector::init(void)

{

**setDefaultValues**();

… …

m_obWinSizeInPoints = CCSizeZero;

m_pobOpenGLView = NULL;

m_fContentScaleFactor = 1.0f;

… …

return true;

}

void CCDirector::setDefaultValues(void)

{

CCConfiguration *conf =

CCConfiguration::sharedConfiguration();

… …

// GL projection

const char *projection =

conf->getCString("cocos2d.x.gl.projection",

"**3d**");

if( strcmp(projection, "3d") == 0 )

m_eProjection = **kCCDirectorProjection3D**;

… …

}

由于conf中没有配置“cocos2d.x.gl.projection”，因此projection使用了 getCString传入的默认值："3d"，m_eProjection则被赋值为kCCDirectorProjection3D。

CCEGLView的创建更为简单：

CCEGLView::CCEGLView()

{

initExtensions();

}

但背后真正发挥关键作用的是其父类CCEGLViewProtocol。

CCEGLViewProtocol::CCEGLViewProtocol()

: m_pDelegate(NULL)

, m_fScaleX(1.0f)

, m_fScaleY(1.0f)

, m_eResolutionPolicy(kResolutionUnKnown)

{

}

这里我们看到了三个重要的字段：m_fScaleX、m_fScaleY以及m_eResolutionPolicy，这三个字段对于后续屏 幕适配起到至关重要的作用。

nativeInit中的view->SetFrameSize(w, h)用于设置的屏幕物理分辨率，如果你的手机是960×640分辨率的，那FrameSize就是960×640。

void CCEGLViewProtocol::setFrameSize(float width,

float height)

{

m_obDesignResolutionSize

= m_obScreenSize

= CCSizeMake(width, height);

}

初始情况下，CCEGLViewProtocol将“设计分辨率”m_obDesignResolutionSize也设置为与 FrameSize or m_obScreenSize同等大小。

我们回到游戏逻辑层代码AppDelegate.cpp，我们知道游戏逻辑的入口在这里，最初的参数初始化是在为Director设置 GLView实例时进行的：

bool AppDelegate::applicationDidFinishLaunching() {

// initialize director

CCDirector* pDirector = CCDirector::sharedDirector();

CCEGLView* pEGLView = CCEGLView::sharedOpenGLView();

pDirector->**setOpenGLView**(pEGLView);

CCSize frameSize = pEGLView->getFrameSize();

… …

}

void CCDirector::setOpenGLView(CCEGLView *pobOpenGLView)

{

m_pobOpenGLView = pobOpenGLView;

// set size

m_obWinSizeInPoints =

** m_pobOpenGLView->getDesignResolutionSize()**;

… …

if (m_pobOpenGLView)

{

**setGLDefaultValues();**

}

CHECK_GL_ERROR_DEBUG();

… …

}

}

由于尚未调用setDesignResolutionSize，因此m_obWinSizeInPoints的值与FrameSize大小相 同。

setGLDefaultValues最为关键，这是我们第一次遇到该函数，该方法用于初始化一些OpenGL的参数，建立好后续 OpenGL操作时所需要的各种数据结构。

void CCDirector::setGLDefaultValues(void)

{

… …

setAlphaBlending(true);

setDepthTest(false);

**setProjection(**m_eProjection);

// set other opengl default values

glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

}

glClearColor(0.0f, 0.0f, 0.0f, 1.0f);设置初始颜色为黑色，alpha为1.0f，即完全不透明。setProjection是实际上绘制参数设置的核心。

void CCDirector::setProjection(ccDirectorProjection kProjection)

{

CCSize size = m_obWinSizeInPoints;

**setViewport**();


switch (kProjection)

{

case kCCDirectorProjection3D:

{

float zeye = this->**getZEye**();

kmMat4 matrixPerspective, matrixLookup;

**kmGLMatrixMode(KM_GL_PROJECTION);**

kmGLLoadIdentity();

… …

// issue #1334

**kmMat4PerspectiveProjection**( &matrixPerspective,

60,

(GLfloat)size.width/size.height,

0.1f, zeye*2);

kmGLMultMatrix(&matrixPerspective);

**kmGLMatrixMode(KM_GL_MODELVIEW);**

kmGLLoadIdentity();

kmVec3 eye, center, up;

kmVec3Fill( &eye, size.width/2,

size.height/2, zeye );

kmVec3Fill( ¢er, size.width/2,

size.height/2, 0.0f );

kmVec3Fill( &up, 0.0f, 1.0f, 0.0f);

**kmMat4LookAt**(&matrixLookup, &eye,

¢er, &up);

kmGLMultMatrix(&matrixLookup);

}

break;

… …

}

m_eProjection = kProjection;

ccSetProjectionMatrixDirty();

}

由于前面m_eProjection已经被赋值为kCCDirectorProjection3D，因此我们只分析 kCCDirectorProjection3D这个case分支。该函数大致进行设置的顺序是：设置视口变换（ViewPort)、设置投影变换矩阵和 设置模型视图变换矩阵。我们分别来看：

*** 设置视口(ViewPort)**

void CCDirector::setViewport()

{

if (m_pobOpenGLView)

{

m_pobOpenGLView->**setViewPortInPoints**(0, 0,

m_obWinSizeInPoints.width,

m_obWinSizeInPoints.height);

}

}

void CCEGLViewProtocol::setViewPortInPoints(float x ,

float y , float w , float h)

{

**glViewport**((GLint)(x * m_fScaleX

+ m_obViewPortRect.origin.x),

(GLint)(y * m_fScaleY

+ m_obViewPortRect.origin.y),

(GLsizei)(w * m_fScaleX),

(GLsizei)(h * m_fScaleY));

}

这是我们遇到的第一个OpenGL概念：设置视口变换，关于视口变换究竟起到什么作用，后续会细说。

*** 设置“投影变换”矩阵参数**

kmMat4PerspectiveProjection( &**matrixPerspective**, 60,

(GLfloat)size.width/size.height, 0.1f, zeye*2);

kmGLMultMatrix(&matrixPerspective);

*** 设置“模型视图变换”矩阵参数**

kmVec3 eye, center, up;

kmVec3Fill( &eye, size.width/2,

size.height/2, zeye );

kmVec3Fill( ¢er, size.width/2,

size.height/2, 0.0f );

kmVec3Fill( &up, 0.0f, 1.0f, 0.0f);

kmMat4LookAt(&**matrixLookup**, &eye,

¢er, &up);

至此，引擎的绘制参数初始化设置就OK了，在你调用setDesignResolutionSize之前，这些参数不会被改变。

**二、kazmath**

Cocos2d-x引擎最底层采用OpenGL ES 2.0进行图形绘制，这样要想搞清楚前面的问题缘由，对OpenGL那一套技术体系至少要有一些直观认识才行。在这之前，我们还要先了解一些 Cocos2d-x深度使用的kazmath库。根据《[Cocos2d-x高级开发教程](http://book.douban.com/subject/24704115/)》书 中说: “因为在Cocos2d-x 2.0采用的OpenGL ES 2.0中，而那些OpenGL ES 1.0函数已经不可使用了。但OpenGL ES 2.0已经放弃了固定的渲染流水线，取而代之的是自定义的各种着色器，在这种情况下变换操作通常需要由开发者来维护。所幸引擎也引入了一套第三方库 Kazmath，它使得我们几乎可以按照原来OpenGL ES 1.0所采用的方式进行开发”。

至此，我们大致知道了Kazmath库是用来辅助我们按照OpenGL ES 1.0的方式管理变换矩阵以及做变换操作的，接下来我们一起来看看kazmath库的结构吧：

//cocos2d-x-2.2.2/cocos2dx/kazmath/src/GL/matrix.c

km_mat4_stack modelview_matrix_stack;

km_mat4_stack projection_matrix_stack;

km_mat4_stack texture_matrix_stack;

km_mat4_stack* current_stack = NULL;

static unsigned char initialized = 0;

以上是Cocos2d-x整个引擎生命周期内会用到的与opengl变换矩阵相关的一些全局变量。

kazmath声明了三个变换矩阵的栈，modelview_matrix_stack（模型视图矩阵栈）、 projection_matrix_stack（投影矩阵栈）以及texture_matrix_stack（纹理矩阵栈）。不过Cocos2d-x引 擎只用到了前两个变化矩阵栈。current_stack指向当前所使用的那个变换矩阵栈。

这些栈的初始化在lazyInitialize中：

void lazyInitialize()

{

if (!initialized) {

kmMat4 identity; //Temporary identity matrix

//Initialize all 3 stacks

//modelview_matrix_stack =

(km_mat4_stack*) malloc(sizeof(km_mat4_stack));

km_mat4_stack_initialize(&modelview_matrix_stack);

//projection_matrix_stack =

(km_mat4_stack*) malloc(sizeof(km_mat4_stack));

km_mat4_stack_initialize(&projection_matrix_stack);

//texture_matrix_stack =

(km_mat4_stack*) malloc(sizeof(km_mat4_stack));

km_mat4_stack_initialize(&texture_matrix_stack);

current_stack = &**modelview_matrix_stack**;

initialized = 1;

**kmMat4Identity(&identity);**

//Make sure that each stack has the identity matrix

km_mat4_stack_push(&modelview_matrix_stack, &identity);

km_mat4_stack_push(&projection_matrix_stack, &identity);

km_mat4_stack_push(&texture_matrix_stack, &identity);

}

}

kmMat4Identify用于初始化“单位矩阵(Indentify Matrix)”，所谓"单位矩阵"，指的是对脚线上元素都为1的矩阵。从kmMat4Identify的实现，我们也可以看出这一点：

kmMat4* const kmMat4Identity(kmMat4* pOut)

{

memset(pOut->mat, 0, sizeof(float) * 16);

**pOut->mat[0] = pOut->mat[5]
= pOut->mat[10]
= pOut->mat[15] = 1.0f;**

return pOut;

}

最后，lazyInitialize函数将单位矩阵分别圧入（km_mat4_stack_push）不同的matrix stack。

再回顾一下CCDirector::setProjection，该函数通过kazmath先后设置了 projection_matrix_stack和modelview_matrix_stack的top元素。

kmGLMatrixMode(**KM_GL_PROJECTION**);

kmGLLoadIdentity();

**kmMat4PerspectiveProjection**( &matrixPerspective, 60,

(GLfloat)size.width/size.height, 0.1f, zeye*2);

kmGLMultMatrix(&matrixPerspective);


kmGLMatrixMode(**KM_GL_MODELVIEW**);

kmGLLoadIdentity();

kmVec3 eye, center, up;

kmVec3Fill( &eye, size.width/2,

size.height/2, zeye );

kmVec3Fill( ¢er, size.width/2,

size.height/2, 0.0f );

kmVec3Fill( &up, 0.0f, 1.0f, 0.0f);

**kmMat4LookAt**(&matrixLookup, &eye,

¢er, &up);

kmGLMultMatrix(&matrixLookup);

**三、精灵绘制**

由《[Hello，Cocos2d-x](http://tonybai.com/2014/03/11/hello-cocos2dx/)》一文我们知道，一旦引擎初始化完毕，就开始了每帧图像的绘制工作，Render Thread在一个“死循环”中反复调用CCDirector的drawScene方法 （CCDisplayLinkDirector::mainLoop中调用了drawScene）：

void CCDirector::drawScene(void)

{

… …

glClear(GL_COLOR_BUFFER_BIT

| GL_DEPTH_BUFFER_BIT);

… …

**kmGLPushMatrix**();

// draw the scene

if (m_pRunningScene)

{

m_pRunningScene->**visit**();

}

… …

**kmGLPopMatrix**();

… …

}

Cocos2d-x采用“渲染树”的方式进行绘制，即先从场景(Scene)的顶层根节点开始，深度优先的递归绘制Child Node。而整个绘制的顶层节点是CCScene。绘制从m_pRunningScene->visit()真正开始。visit是Scene、 Layer、Sprite的共同父类CCNode实现的方法：

void CCNode::visit()

{

if (!m_bVisible)

{

return;

}

**kmGLPushMatrix**();

… …

this->**transform**();

… …


if(m_pChildren &&

m_pChildren->count() > 0)

{

sortAllChildren();

// **draw children zOrder** < 0

… ..

// self draw

this->**draw**();

// **draw other children nodes**

… …

} else {

this->draw();

}

… …

**kmGLPopMatrix**();

}


Visit大致做了这么几件事：

– 向当前OpenGL变换矩阵栈Push元素

– 用当前OpenGL变换矩阵栈栈顶元素的变换参数做节点变换

– 递归绘制zOrder < 0 的子节点

– 绘制自己

– 递归绘制其他子节点

– 从当前OpenGL变换矩阵栈Pop元素

如果你想知道为什么父节点缩放(Scale)、旋转(Rotate)、扭曲(Skew)后，子节点也会跟着父节点同样缩放(Scale)、旋 转(Rotate)、扭曲？其原理就在这里的transform方法中：

void CCNode::transform()

{

kmMat4 transfrom4x4;

// Convert 3×3 into 4×4 matrix

CCAffineTransform tmpAffine

= this->nodeToParentTransform();

CGAffineToGL(&tmpAffine,

transfrom4x4.mat);

// Update Z vertex manually

transfrom4x4.mat[14] = m_fVertexZ;

kmGLMultMatrix( &transfrom4x4 );

… …

}

在进入tranform以前，Cocos2d-x做了啥？对了，kmGLPushMatrix()：

void kmGLPushMatrix(void)

{

kmMat4 top;

lazyInitialize();

//**Duplicate the top of the stack (i.e the current matrix)**

kmMat4Assign(&top, current_stack->top);

km_mat4_stack_push(current_stack, &top);

}

在引擎初始化后，我们的current_stack是模型视图矩阵栈modelview_matrix_stack。所有设置的初始参数都保 存在该栈的栈顶元素中。在每次Node绘制前，Node都会创建自己的变换矩阵，但这个矩阵不是凭空创造的，从kmGLPushMatrix 可以看出，在当前Node将新创建的矩阵元素圧栈前，它复制了原栈顶元素，也就**携带有父节点所有的初始变换信息**，也就是说在 km_mat4_stack_push后，栈顶放置的元素其实是原栈顶元素的复制品，而后续所有操作都是基于这个复制品的。这样一来，如果父 节点做了缩放或旋转或扭曲，那这些信息都会作为初始信息作为子节点变换的基础，后续子节点自身的变换参数也都是在这个基础上做出的，最终的矩 阵是transform方法中的kmGLMultMatrix后得出的。真正的矩阵变换计算都在nodeToParentTransform 中，不过要想看懂这个函数，需要对OpenGL有更深入的了解才行，这里略过^_^。

真正绘制Node的方法是CCNode::draw的override方法。CCNode::draw是一个空函数，各个子类 override该方法进行各自的绘制。以CCSprite::draw为例：

void CCSprite::draw(void)

{

CC_NODE_DRAW_SETUP();

ccGLBlendFunc( m_sBlendFunc.src, m_sBlendFunc.dst );

ccGLBindTexture2D( m_pobTexture->getName() );

ccGLEnableVertexAttribs( kCCVertexAttribFlag_PosColorTex );

#define kQuadSize sizeof(m_sQuad.bl)

long offset = (long)&m_sQuad;

// vertex

int diff = offsetof( ccV3F_C4B_T2F, vertices);

glVertexAttribPointer(kCCVertexAttrib_Position, 3,

GL_FLOAT, GL_FALSE, kQuadSize, (void*) (offset + diff));

// texCoods

diff = offsetof( ccV3F_C4B_T2F, texCoords);

glVertexAttribPointer(kCCVertexAttrib_TexCoords, 2,

GL_FLOAT, GL_FALSE, kQuadSize, (void*)(offset + diff));

// color

diff = offsetof( ccV3F_C4B_T2F, colors);

glVertexAttribPointer(kCCVertexAttrib_Color, 4,

GL_UNSIGNED_BYTE, GL_TRUE,

kQuadSize, (void*)(offset + diff));

glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

… …

}

这里的draw是一个典型的OpenGL绘制工序。CC_NODE_DRAW_SETUP()将之前的经过若干准备而得到的最终各类变换矩阵 整合并传给OpenGL：

/** @def CC_NODE_DRAW_SETUP

Helpful macro that setups the GL server state,

the correct GL program and sets the Model View

Projection matrix

@since v2.0

*/

#define CC_NODE_DRAW_SETUP() \

do { \

ccGLEnable(m_eGLServerState); \

CCAssert(getShaderProgram(), "No shader program set for this node"); \

{ \

getShaderProgram()->use(); \

getShaderProgram()->**setUniformsForBuiltins**(); \

} \

} while(0)

void CCGLProgram::setUniformsForBuiltins()

{

kmMat4 matrixP;

kmMat4 matrixMV;

kmMat4 matrixMVP;

kmGLGetMatrix(KM_GL_PROJECTION, &matrixP);

kmGLGetMatrix(KM_GL_MODELVIEW, &matrixMV);

kmMat4Multiply(&matrixMVP, &matrixP, &matrixMV);

setUniformLocationWithMatrix4fv(m_uUniforms[kCCUniformPMatrix],

matrixP.mat, 1);

setUniformLocationWithMatrix4fv(m_uUniforms[kCCUniformMVMatrix],

matrixMV.mat, 1);

setUniformLocationWithMatrix4fv(m_uUniforms[kCCUniformMVPMatrix],

matrixMVP.mat, 1);

… …

}

经过计算顶点、绑定纹理等步骤后，最终由glDrawArrays完成Node绘制。

**四、m_fScaleX和m_fScaleY都是1.0，背景精灵为何被放大？**

根据上面的分析，我们了解到“子节点将跟随父节点的缩放而缩放”。据此，我们来分析一下前面提到的屏幕适配例子中的第三种情况，即屏幕大小为 960×640，按照Cocos2d-x屏幕适配指南Wiki中的做法，调用 pEGLView->setDesignResolutionSize(480, 320)。在该情况中，我们得到的结果是480×320大小的背景图片充满了大小为960×640的屏幕窗口，这给我们的直观印象就是背景图片被放大了一 倍。下面我们就尝试用上面的分析来解释一下这个现象。

在这个例子中，渲染树结构如下：

CCScene

– CCLayer

– CCSprite – 背景图精灵

按照之前的理论，背景图精灵自身或父类应该有缩放的设置，比如m_fScaleX = 2.0之类的设置，于是我在代码中输出了Scene、Layer以及Sprite的m_fScaleX和m_fScaleY值。但出乎预料的是，这些 Node子类的两个轴向缩放值都保持了默认值，即1.0f。在代码里翻了半天，也的确没有找到改写Scene、Layer或Sprite Scale的地方。又一想：代码中调用了setDesignResolutionSize，这样CCEGLView的m_fScaleX = m_fScaleY = 2.0f，难道是CCEGLView的m_fScale传递给了CCScene等Node子类，但事实总是残酷的，代表这一联系的代码也始终未被我所找 到，看来继续纠结m_fScale的值设置是无法搞清楚真正原因，应该换换思路了。这里背景图的放大不应该是Node scale值设置的问题，也就是说关键环节不应该在绘制流程，而是在之前的OpenGL变换矩阵参数设置，看来不再深入学习点OpenGL知识，这个问题 就很难搞定了，于是开始翻看《[OpenGL编程指南](http://book.douban.com/subject/4311129/)7th》（号称OpenGL红宝书）和《[OpenGL超级宝典](http://book.douban.com/subject/10774590/)》（号称OpenGL蓝宝 书）。虽然我的阅读是粗粒度的，但还是收获到了一些答案。

**五、OpenGL基础**

OpenGL是帮助我们将三维世界的物体转换到二维屏幕上的一组接口。在新技术尚未出现之前，我们的屏幕永远是二维的，即便是现在的3D电影 也是双眼视角二维图像叠加的结果。我们知道“将大象装进冰箱总共分三 步”，将一个三维模型转换到二维屏幕上，OpenGL也规定了相对流水线般的步骤。

![](../../assets/1e6fa9b8e70673d7.jpg)


OpenGL三维图形的显示流程

三维图形显示流程中，涉及到OpenGL的一个重要操作，那就是“变换(Transformation)”，主要的变换包括模型视图变换 （model-view transformation）、投影变换(projection transformation)以及视口变换(ViewPort transformation)。我们经常用相机模拟来对比OpenGL解决这一问题的过程以及相关概念。

![](../../assets/7511eb74624d87cb.jpg)


回顾一下我们自己用相机拍照的步骤吧。

第零步，选景。景就是所谓的三维模型或三维物体，或简称**模型**(Model)，就是我们要显示到屏幕上的物体；

第一步，确定相机位置。让相机以一定的距离、高度、角度对准模型。在这里，相机的位置变换，对应OpenGL的“视图变换或叫视点变换 (View Transformation)”。在这一步里（对应上面图中的第二步），我们还可以调整三维物体的相对位置、角度与相机的距离，这就是模型变换 （Modeling Transformation），两种变换达成的效果是相同的，因此总称模型视图变换(Model-View Transformation)。

第二步，选镜头，并调焦。确定图像投影在胶片上的范围以及景深等。这一步叫投影变换（Projection Transformation）。

第三步，冲洗照片。拍摄好的图像放在底片上，但我们需要选择冲洗后最终是放在6寸相纸还是20寸相纸上，显然在不同大小相纸上，图像的显示效 果不同（比如大小）。这个过程叫视口变换（Viewport Transformation）。

`三维空间的物体都是用三维坐标描述的，谈到坐标就离不开坐标系，OpenGL中的坐标系就有多种，我们最常用的就是世界坐标系。`

`世界坐标系是以屏幕中心为原点(0, 0, 0)，你面对屏幕，你的右边是x正轴，上面是y正轴，屏幕指向你的为z正轴。``无论如何变换，世界坐标系都不动。`我们在Cocos2d-x中设置 初始参数时，参数的单位多为世界坐标系中的单位。

视点变换时会涉及到视点坐标系，但这个变换由opengl接口来负责，我们不用过多关心。

绘图坐标系（局部坐标系），当前绘图坐标系是绘制物体时的坐标系。程序刚初始化时，世界坐标系和当前绘图坐标系是重合的，当用 glTranslatef()等变换函数做移动和旋转时，都是改变的当前绘图坐标系，改变的位置都是当前绘图坐标系相对自己的x,y,z轴所做的 改变，改变以后，再绘图时，都是在当前绘图坐标系进行绘图，所有的函数参数也都是相对当前绘图坐标系来讲的。

屏幕坐标系，即终端屏幕上的坐标系，与世界坐标系有不同，它以屏幕左上角的点为原点，向右是x正轴，向下是y正轴，屏幕指向你的为z正轴。

注意视口(Viewport)的设置是以实际屏幕坐标定义了窗口中的区域，长度宽度都是以**实际像素**为单位。当然引擎在精灵绘图时用 的是绘图坐标系，我们理解原点在左下角即可。

**六、Cocos2d-x各种变换矩阵的初始参数设置**

前面说过，Cocos2d-x在CCDirector::setProjection中完成了对变换矩阵的初始参数设置，我们逐一来看看这些设置对模型映射后的二维图像有何影响，这也是理解篇头几个问题的关键环节。

*** 投影变换**


前面提到过，投影变换相当于调节相机镜头。OpenGL中提供了两种投影方式，一种是正射投影，另一种是透视投影。Cocos2d-x使用的是透视投影 （Perspective Projection)。透视投影是实际人们观察事物的真实反馈，即离视点近的物体大，离视点远的物体小，远到极点即为消失，成为灭点。Cocos2d- x使用的是kmMat4PerspectiveProjection，对应OpenGL中的gluPerspective，该方法创建一个对称透视视景体 (View Volumn)，见下图：

![](../../assets/0a93c617993c0c5f.jpg)


gluPerspective的函数原型如下：void gluPerspective(GLdouble fovy,GLdouble aspect,GLdouble zNear, GLdouble zFar);

参数fovy定义视野在X-Z平面的角度，范围是[0.0, 180.0]，也就是上图中的“视角”；

参数aspect是投影平面宽度与高度的比率；

参数zNear和Far分别是近远裁剪面沿Z负轴到视点的距离，它们总为正值。


Cocos2d-x中是这么设置投影变换矩阵的：

float zeye = this->getZEye();

kmMat4PerspectiveProjection( &matrixPerspective, 60, (GLfloat)size.width/size.height, 0.1f, zeye*2);

float CCDirector::getZEye(void)

{

return (m_obWinSizeInPoints.height / 1.1566f);

}

从参数上来看，

视角 = 60度

宽高比 = 设计分辨率的宽高比，

近平面 = 距离视点0.1f，几乎与视点重合

远平面 = 距离视点zeye * 2距离。

视点位置 = 设计分辨率.height / 1.1566f

投影是用来对模型进行截取的，只有在投影变换所建立的平头截体（Frustum，投影的近、远两个截面以及其他四个面构成的立体体）内的模型部分才会被最终映射和显示。我们用下面的图来直观了解一下各个参数在三维空间的概念吧。

![](../../assets/56eb24e00a1e352a.jpg)


显然引擎如此设置投影矩阵的参数是有考虑的：

首先就是投影平头截体的宽高比 = 设计分辨率的宽高比，这样设置使得一切符合设计分辨率宽高比的模型都可以被理想截取。

其次，视角60度，zEye的在Z轴正方向距离世界原点的距离 = (m_obWinSizeInPoints.height / 1.1566f),这里的1.1566f是怎么来的呢？我们沿着X轴负方向向zy平面投影，得到下图：

![](../../assets/cf0dd6ab6bc421aa.jpg)


看这个图，让我想起了初中几何，通过60度的视角，我们可以推断由eye、XZ截断上平面与Y轴的交点、XZ截断下平面与Y轴的交点组成一个等边三角形， 现在我们已知在Zy平面投影中视点与原点的距离为m_obWinSizeInPoints.height / 1.1566f, 我们还知道夹角是60度，我们求一下投影在(z=0，XY平面)的截面高度h。

cos30 = (m_obWinSizeInPoints.height / 1.1566f)/ h

h = (m_obWinSizeInPoints.height / 1.1566f)/cos30 = m_obWinSizeInPoints.height;

我们计算出来的结果是 h = m_obWinSizeInPoints.height = 设计分辨率中的高度分量。这意味这什么呢？Cocos2d-x是2D游戏渲染引擎，针对该引擎的模型的z坐标都是0，因此模型实际上就在xy平面内，也就 是说eye与原点的距离恰好就是eye与模型的距离，而模型可显示区域的最大高度也就是h，即m_obWinSizeInPoints.height。这 个结论会在后续问题分析时发挥作用。

注意虽然这里知道eye在Z轴正方向距离世界原点的距离，但eye的(x, y)坐标在投影设置后依旧无法确认，我们需要在设置模型视图变换时得到eye的(x, y)坐标。

*** 视图变换**

kmGLMatrixMode(KM_GL_MODELVIEW);

kmGLLoadIdentity();

kmVec3 eye, center, up;

kmVec3Fill( &eye, size.width/2, size.height/2, zeye );

kmVec3Fill( ¢er, size.width/2, size.height/2, 0.0f );

kmVec3Fill( &up, 0.0f, 1.0f, 0.0f);

kmMat4LookAt(&matrixLookup, &eye, ¢er, &up);

kmGLMultMatrix(&matrixLookup);

OpenGL原生的视图变换参数设置方法是gluLookAt，在kazmath中对应的方法为kmMat4LookAt。gluLookAt的函数原型是：

void gluLookAt(GLdouble eyex, GLdouble exey, GLdouble eyez,

GLdouble centrex, GLdouble centrey, GLdouble centrez,

GLdouble upx, GLdouble upy, GLdouble upz);

eye的坐标(eyex, eyey, eyez), Cocos2d-x中是这么设置的kmVec3Fill( &eye, size.width/2, size.height/2, zeye )。可以看出eye在xy平面的投影恰好是以屏幕分辨率构成的矩形的中心。

centre坐标，表示的是视线方向，该方向矢量是由eye坐标、centre坐标共同构成的，由eye指向center。Cocos2d-x的设置 kmVec3Fill( ¢er, size.width/2, size.height/2, 0.0f )。x, y坐标与eye的相同，因此视线平行于Z轴。

最后的up参数可以理解为头顶方向，这里设置为Y轴方向。

![](../../assets/652612c3c51672df.jpg)


可以看出，eye就在投影区的中心，由于投影区的高度为size.height(投影变换时分析得到的)，这样根据投影矩阵设置的宽高比，得出该投影区的宽度也恰为size.width。

**七、再分析**

有了以上关于Cocos2d-x引擎的了解，我们再回过头来用OpenGL的变换原理对篇头的三种情况做分析。

1) 屏幕大小480×320，未做任何屏幕适配工作，不调用pEGLView->setDesignResolutionSize。结果：背景图充满窗口。

在这种情况下，各个OpenGL变换矩阵参数值如下：

eye视点坐标(240, 160, 320/1.1566f);

投影变换矩阵在xy平面的截面区域恰好是480×320；

背景图锚点位置(240, 160, 0)；

在这种情况下，截面区域恰与背景图重合，显示在屏幕上后，背景图恰充满窗口，见下图：

![](../../assets/1c8bbcdf5643d0de.jpg)



2) 屏幕大小960×640，未做任何屏幕适配工作，不调用pEGLView->setDesignResolutionSize。结果：背景图未充满窗口，四周有较大黑边。


在这种情况下，各个OpenGL变换矩阵参数值如下：

eye视点坐标(480, 320, 480/1.1566f);

投影变换矩阵在xy平面的截面区域是960×640；

而背景图锚点位置(480, 320, 0)；

因此背景图(480×320)未能完整充满截面区域(960×640)，背景图周围将有较大黑边，见下图：


![](../../assets/520df2d1c6ec895b.jpg)


3) 屏幕大小同为960×640，按照上面Cocos2d-x屏幕适配指南Wiki中的做法，调用pEGLView->setDesignResolutionSize(480, 320)。结果：背景图放大为原来2倍，充满屏幕窗口。

在这种情况下，各个OpenGL变换矩阵参数值如下：

eye视点坐标(240, 160, 320/1.1566f);

投影变换矩阵在xy平面的截面区域是480×320；

而背景图锚点位置(240, 160, 0)；

在这种情况下，截面区域恰与背景图重合。但这里需要注意的是现在屏幕是960×640，而截面区域仅仅是480×320，为何映射后，背景图充满屏幕了呢？这里就不能不提到视口的作用了。

前面说过视口相当于相片，现在我们拍摄出的图片是480×320的，但我们选择的底片Viewport却是960×640的，怎么办，在视口转换 时，OpenGL自动将480×320的图片映射到960×640的底片上，相当于对图像进行的放大。而960×640的视口恰好与屏幕窗口大小一致且坐 标重叠，于是我们就在屏幕上看到了一个铺满屏幕的背景图，见下图：

![](../../assets/ffae2e9f01cab82d.jpg)


4) 我们再来说两个有关视口的例子

以第三种情况为基础，我们修改一下引擎代码，看看视口的作用。


我们手工将CCDirector::setViewport()中的：

m_pobOpenGLView->setViewPortInPoints(0, 0, m_obWinSizeInPoints.width, m_obWinSizeInPoints.height);

改为：

m_pobOpenGLView->setViewPortInPoints(0, 0, m_obWinSizeInPoints.width/2, m_obWinSizeInPoints.height/2);

这样修改后，Viewport从point(0,0), rect (960×640)变成了point(0,0), rect (480×320)。也就是说用照相机拍出的景物大小是480×320，底片也是480×320，但屏幕是960×640，我们可以将屏幕理解为相框，把 一张480×320的照片，放到960×640大小的相框里，相片只能占据相框的四分之一。这个例子的最终屏幕显示结果见下图：

![](../../assets/d67f58f84a32c232.jpg)


前面的例子中背景图片size均小于屏幕大小，我们再来举一个资源图片大于屏幕大小的例子，看看经过一系列变换会得到什么样的结果。


首先将CCDirector::setViewport()中的代码恢复原先状态。然后我们准备一张1024×768(>屏幕的960×640)的 背景图片"HelloWorld-1024×768.jpg"，修改HelloWorldScene.cpp，将：

CCSprite* pSprite = CCSprite::create("HelloWorld.png");

修改为：

CCSprite* pSprite = CCSprite::create("**HelloWorld-1024×768.png**");

注释掉AppDelegate.cpp中的pEGLView->setDesignResolutionSize调用，这样更直观。

这样修改后，各参数如下：

eye视点坐标(480, 320, 640/1.1566f);

投影变换矩阵在xy平面的截面区域是960×640；

而背景图锚点位置(480, 320, 0)；

Viewport point(0,0), rect (960×640)


由于背景资源图片太大(1024×768)，大于我们的投影截面区域960×640，因此模型真正能显示的部分仅仅是投影截面区域中的那960×640范围内的图片。于是显示结果如下：

![](../../assets/6be67162ed0d1710.jpg)


矩阵变换过程如下：

![](../../assets/aaa4eeffad3e0d36.jpg)


投影截面区域与视口区域重叠，这里就不再赘述了。

**八、CCDirector::m_fContentScaleFactor**

决定图像在屏幕上的最终显示结果的因素还有一个，那就是CCDirector::m_fContentScaleFactor。在最初的HelloCpp例子中，我们能看到这样的代码：

if (frameSize.height > mediumResource.size.height)

{

searchPath.push_back(largeResource.directory);

pDirector->setContentScaleFactor(

MIN(largeResource.size.height/designResolutionSize.height,

largeResource.size.width/designResolutionSize.width));

}

… …

可以看出这个contentScaleFactor存储的是资源分辨率与设计分辨率的比值。我们还是用例子来看看该元素对显示的影响。我们在第一种情况的基础上验证。

第一种情况：屏幕480×320，未调用setDesignResolutionSize，资源大小480×320。结果：图片充满屏幕。

现在我们增加并使用一个新资源：HelloWorld-960×640.png，这个图片大小960×640，是屏幕大小的二倍，根据上面的分析，我们很容易猜测到最终结果是：只有图片中央区域(480×320)可以显示出来，其余部分被投影矩阵截掉。

现在我们使用setContentScaleFactor，在AppDelegate.cpp中做如下调用：

pDirector->setContentScaleFactor(MIN(960/480, 640/320));

这样我们得到的m_fContentScaleFactor = 2。而我们编译运行后得到的结果是：图片铺满整个屏幕。为什么会这样呢？

我们在代码中搜索contentScaleFactor，我们找到一些宏和调用：


#define CC_CONTENT_SCALE_FACTOR() CCDirector::sharedDirector()->getContentScaleFactor()

CCSize CCTexture2D::getContentSize()

{

CCSize ret;

ret.width = **m_tContentSize.width / CC_CONTENT_SCALE_FACTOR();**

ret.height = **m_tContentSize.height / CC_CONTENT_SCALE_FACTOR();**

return ret;

}

#define CC_RECT_PIXELS_TO_POINTS(__rect_in_pixels__) \

CCRectMake( (__rect_in_pixels__).origin.x / CC_CONTENT_SCALE_FACTOR(), (__rect_in_pixels__).origin.y / CC_CONTENT_SCALE_FACTOR(), \

(__rect_in_pixels__).size.width / CC_CONTENT_SCALE_FACTOR(), (__rect_in_pixels__).size.height / CC_CONTENT_SCALE_FACTOR() )

… …

bool CCSprite::initWithTexture(CCTexture2D *pTexture)

{

CCAssert(pTexture != NULL, "Invalid texture for sprite");

CCRect rect = CCRectZero;

rect.size = pTexture->getContentSize();

return initWithTexture(pTexture, rect);

}

这些代码都在告诉我们，如果m_fContentScaleFactor = 2，那代码会对Sprite的纹理进行缩放，让上面得到的数据是经过contentScaleFactor变换的，我们可以认为我们所用的实际资源大小是 原资源的1/m_fContentScaleFactor即可。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

赞~

very well

Awesome~

学习了，感谢。

感谢

l

very good～

赞,剖析的很清楚

大神不是在东软么，怎么有兴趣研究游戏行业的东东？

博主。虽然你讲的很详细了。可是有几个地方我还是不太了解。希望授业解惑啊。1.在投影模型中，坐标是怎么样的。假如我在代码中设置一个点的坐标是（10,10,10），它在这个投影模型中是在什么位置。2.视景体的模型被投影。是被投影到哪个面上呢。还望解答~

层主，我也遇到了同样的问题，您解决了么 求帮忙 联系QQ 348351174 谢谢

已经好久不从事这方面的开发了，估计也没办法帮得上你了。自己研究一下吧。或向其他游戏开发大神请教

能告诉我这些图是这么画出来的吗

在powerpoint中将相关子图放入，加上线条，合成的图片。

那个1.1566貌似是计算1/cos30得来的，但是1/cos30的近似值是1.1547啊。

感谢分享

膜拜。。。