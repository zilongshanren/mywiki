---
title: Cocos2d-x集成Amazon内购和GameCircle服务
url: https://tonybai.com/2014/08/04/amazon-inapp-purchasing-and-gamecirle-in-cocos2dx/
published: '2014-08-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x集成Amazon内购和GameCircle服务

由于种种原因，这篇文章已经拖延了N多时间了。今天花了些时间把如何在[Cocos2d-x](http://cocos2d-x.org/)(我用的版本是2.2.2)游戏中集成[Amazon](https://developer.amazon.com/public)的[内购](https://developer.amazon.com/public/apis/earn/in-app-purchasing)和[GameCircle](https://developer.amazon.com/public/apis/engage/gamecircle)服务(仅适用于Android版本)整理一下，发出来，作备忘。

之前在做“[手指足球世界杯2014](http://iwobi.net)”时，想给这款小游戏加上内购(In-App Purchasing)和积分榜(ScoreBoard)功能。说到Android手机游戏的内购，人们第一时间想到的就是[Google Play](http://play.google.com)，不过悲催的是，Google Play在国内各种无法访问，行货机也不预装，其相关Service的测试十分困难，翻看了一些集成Google Game Service的文章，其过程坎坷之程度让人望而却步。于是我将目光转而投向了Amazon Game Service。亚马逊的游戏服务起步要晚些，成熟性肯定不如Google，但在国内来说也不失为另一个不错的选择，Google虽好，但访问不了有啥 法。但似乎国内同行使用Amazon游戏服务的并不多，度娘上相关中文资料甚少。但从Amazon发布的数据来看，其市场正在逐步扩大，并紧紧跟随 Google Play的脚步。

之前用kindle paperwhite时在amazon.com上注册了一个国际帐号，这次正好用这个。不过你要使用Amazon的Game Service，普通Amazon帐号是不行的。你要升级为Amazon的Developer。申请Developer帐号的过程还是蛮繁琐的，要提交一 堆资料，具体细节我大致忘的差不多了，这里就不说了。按照Amazon网站的提示一步一步做就是了。

有了帐号后，你可以下载Amazon的Game SDK了，这个包有近50M大小，本地解压后可以看到其提供的Android SDK种类：

AmazonSDK/Android$ ls

Ads AmazonInsights DeviceMessaging GameCircle InAppPurchasing LoginWithAmazon Maps MobileAssociates README.txt

Ads我之前用的是Google Admob，这里就不再用Amazon的了，我需要的是这里的InAppPurchasing和GameCircle。我们接下来一个一个来说。

*** Amazon InAppPurchasing**

Amazon支持三种内购类型：Consumables、Entitlements和Subscriptions：

Consumables就像游戏中的红心、金币等，用户可以多次购买，每次可以买多个，并根据游戏规则，每次消耗若干个以达到某种游戏目的；在哪台设备上购买，就只能在哪台设备上使用。

Entitlements是某种授权协议，一个用户只需购买一次，即可长期使用某种特权功能，并与设备无关，可在多个设备下授权使用。比如鳄鱼洗澡游戏中购买高级关卡等。

Subscriptions有订阅的意思，需要某种Entitlements或某种访问权，在一定时间段内绑定有效，到期后自动renew，比如某种杂志的阅读权等。

我只想给游戏增加一些红心功能，一颗红心，可以让游戏者有一次续命的机会，因此我需要实现Consumables型内购。Amazon SDK中提供了Consumeables类内购的Android范例AmazonSDK/Android/InAppPurchasing/samples/SampleIAPConsumablesApp。我们可以参考这个例子来实现我的"红心内购"。

*1、添加依赖的jar包*

在你的游戏proj中添加内购功能所依赖的Amazon SDK jar包，包括AmazonInsights-android-sdk-2.1.26.jar、in-app-purchasing-1.0.3.jar 和login-with-amazon-sdk.jar。

*2、添加源文件*

参照例子，将AppPurchasingObserver.java、AppPurchasingObserverListener.java和MySKU.java拷贝到你的与XXActivity.java同级目录下。

*3、初始化Amazon IAP*


在你的XXActivity类中添加如下方法：

public PurchaseDataStorage purchaseDataStorage;

private void setupIAPOnCreate() {

purchaseDataStorage = new PurchaseDataStorage(this);

AppPurchasingObserver purchasingObserver

= new AppPurchasingObserver(this, purchaseDataStorage);

purchasingObserver.setListener(this);

Log.i(TAG, "onCreate: registering AppPurchasingObserver");

PurchasingManager.registerObserver(purchasingObserver);

}

protected void onCreate(Bundle savedInstanceState){

… …

setupIAPOnCreate();

}

protected void onResume() {

super.onResume();


Log.i(TAG, "onResume: call initiateGetUserIdRequest");

PurchasingManager.initiateGetUserIdRequest();

Log.i(TAG, "onResume: call initiateItemDataRequest for skus: "

+ MySKU.getAll());

PurchasingManager.initiateItemDataRequest(MySKU.getAll());

}

* 4、添加购买方法*

在Cocos2d-x的某个Scene或Layer中实现的购买方法事件的callback，后者通过Jni调用Java静态方法：

void BuyHeartScene::buyHearts(int number) {

#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)

JniMethodInfo t;

if (JniHelper::getStaticMethodInfo(t, "net/iwobi/game/flickworldcup/FlickWorldCupActivity",

"onBuyHeartClick", "(I)V")) {

t.env->CallStaticVoidMethod(t.classID, t.methodID, number);

if (t.env->ExceptionOccurred()) {

t.env->ExceptionDescribe();

t.env->ExceptionClear();

return;

}

t.env->DeleteLocalRef(t.classID);

}

#endif

}

该Java方法的实现如下(我这里有五种商品ONEHEART到FIVEHEART)：

public static void onBuyHeartClick(int type) {

String requestId;


switch (type) {

case 1:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.ONEHEART.getSku());

break;

case 2:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.TWOHEART.getSku());

break;

case 3:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.THREEHEART.getSku());

break;

case 4:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.FOURHEART.getSku());

break;

case 5:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.FIVEHEART.getSku());

break;

default:

requestId = PurchasingManager.initiatePurchaseRequest(MySKU.ONEHEART.getSku());

break;

}

PurchaseData purchaseData = ((FlickWorldCupActivity)context).purchaseDataStorage

.newPurchaseData(requestId);

Log.i(TAG, "onBuyHeartClick: requestId (" + requestId

+ ") requestState (" + purchaseData.getRequestState() + ")");

}

*5、修改各种回调方法*

将SampleIAPConsumablesApp/src/com/amazon/sample/iap/consumable /MainActivity.java中的onPurchase为前缀名的方法以及onGetUserIdResponseSuccessful挪到你的 Activity源文件中。这些方法绝大部分是不需要修改的，除非你不喜欢例子中日志输出的格式，或是想用toast之类的提示方式改造各种 callback的结果显示方式。

这里我主要修改了一个方法：onPurchaseResponseSuccess。该方法在购买成功后被调用，我们在这个事件发生时更新Scene或Layer的显示(updateHeartInScene)。

@Override

public void onPurchaseResponseSuccess(String userId, String sku,

String purchaseToken) {

Log.i(TAG, "onPurchaseResponseSuccess: for userId (" + userId

+ ") sku (" + sku + ")");

SKUData skuData = purchaseDataStorage.getSKUData(sku);

if (skuData == null)

return;

if (MySKU.ONEHEART.getSku().equals(skuData.getSKU())) {

updateHeartInScene(1);

}

if (MySKU.TWOHEART.getSku().equals(skuData.getSKU())) {

updateHeartInScene(2);

}

if (MySKU.THREEHEART.getSku().equals(skuData.getSKU())) {

updateHeartInScene(3);

}

if (MySKU.FOURHEART.getSku().equals(skuData.getSKU())) {

updateHeartInScene(4);

}

if (MySKU.FIVEHEART.getSku().equals(skuData.getSKU())) {

updateHeartInScene(5);

}

}

*6、AndroidManifest.xml和其他Java文件*

AppPurchasingObserver.java和AppPurchasingObserverListener.java你可以原封不动的使用。MySKU.java可以根据你的内购项目做改造：

public enum MySKU {

ONEHEART("net.iwobi.game.flickworldcup.iap.consumable.oneheart", 1),

TWOHEART("net.iwobi.game.flickworldcup.iap.consumable.twoheart", 1),

THREEHEART("net.iwobi.game.flickworldcup.iap.consumable.threeheart", 1),

FOURHEART("net.iwobi.game.flickworldcup.iap.consumable.fourheart", 1),

FIVEHEART("net.iwobi.game.flickworldcup.iap.consumable.fiveheart", 1);


private String sku;

private int quantity;

private MySKU(String sku, int quantity) {

this.sku = sku;

this.quantity = quantity;

}

public static MySKU valueForSKU(String sku) {

if (ONEHEART.getSku().equals(sku)) {

return ONEHEART;

}


if (TWOHEART.getSku().equals(sku)) {

return TWOHEART;

}

if (THREEHEART.getSku().equals(sku)) {

return THREEHEART;

}

if (FOURHEART.getSku().equals(sku)) {

return FOURHEART;

}

if (FIVEHEART.getSku().equals(sku)) {

return FIVEHEART;

}


return null;

}

public String getSku() {

return sku;

}

public int getQuantity() {

return quantity;

}

private static Set<String> SKUS = new HashSet<String>();

static {

SKUS.add(ONEHEART.getSku());

SKUS.add(TWOHEART.getSku());

SKUS.add(THREEHEART.getSku());

SKUS.add(FOURHEART.getSku());

SKUS.add(FIVEHEART.getSku());

}

public static Set<String> getAll() {

return SKUS;

}

}

AndroidManifest.xml中在application标签下添加如下配置：

<receiver android:name="com.amazon.inapp.purchasing.ResponseReceiver" >

<intent-filter>

<action

android:name="com.amazon.inapp.purchasing.NOTIFY"

android:permission="com.amazon.inapp.purchasing.Permission.NOTIFY" />

</intent-filter>

</receiver>

有了以上代码，我们的内购就可以运行起来了。** **

* 内购测试

使用Amazon In-app Purchasing API一个最大好处就是测试简单。Amazon提供一个本地测试程序Amazon App Tester（安装到Android模拟器中），可以模拟内购Server，SDK自动判断当前场景，如果是测试，你的集成了内购SDK的游戏将连接本地 测试程序完成内购流程。通过在本地测试程序中设置模拟不同的内购流程，我们可以轻松完成测试。

你需要给Amazon App Tester提供一个名为amazon.sdktester.json的文件，这样Amazon App Tester可以知道你的游戏有哪些内购项目，并模拟出这些内购项目。这个json文件可以自行编辑，也可以在Amazon deveoper网站上生成下载。

我直接将内购项目添加到我的Amazon帐号的游戏应用下面，一共五个，添加成功后，下载json文件。将该文件放在模拟器的/mnt/sdcard下，绝对路径为/mnt/sdcard/amazon.sdktester.json。

之后，启动App Tester，再启动你的游戏，点击内购项目，看看是否能购买成功。

*** 内购上线**

按照Amazon官方说法，SDK会自动区分测试场景和正式场景，因此通过App Tester测试的游戏在发布后，理论上内购是没有问题的。不过我上线后还是遇到了问题，即点击购买某个项目后，游戏没有任何反应，等了若干分钟都是这 样。我将这个问题反馈给Amazon Support，得到的答复居然是游戏代码没有问题，他们测试了若干中机型，都可以打开内购页面，并进行内购。只是有时内购页面打开有些延迟，但都能打 开。看到这里，我猜是否又是大陆网络的问题呢！不管它了，至少通过Amazon Support的回复可以证明我的代码是ok的。只能希望美国人民多多购买我的内购项目了^_^。

*** Amazon游戏圈**

想给游戏增加成就榜和成就提交功能，如果自己实现服务端，显然麻烦，工作量大不说，还得维护一个Server。但市面上提供这类服务的游戏平台不多。 Google Play的游戏Service提供这种服务，不过还是上面提到的原因，我与Google的这个服务无缘啊。Amazon Game SDK后期推出了GameCircle服务。

GameCircle目前提供achievements, leaderboards和Whispersync三种特性：

achievements就是奖励机制，帮助游戏提高玩家粘性。

leaderboards类似于积分榜，可以用于提交玩家积分以及显示玩家的全球排名。

Whispersync是一种数据游戏同步服务，同步玩家进度，保寸玩家个性化数据等。

这里我要用到的是leaderboards。

*1、建立GameCircle*

使用游戏圈前，你需要在Amazon官方的Amazon Apps & Services Developer Console下创建属于你的Game Circle，然后创建一个LeaderBoard，设置LeaderBoard属性。SDK中提供了GameCircle的Demo：AmazonSDK/Android/GameCircle。

*2、导入jar包，设置AndroidManifest.xml*

要想使用GameCircle，我们需要导入相应的SDK jar包：gamecirclesdk.jar。

在AndroidManifest.xml中，需要在application标签下添加以下配置：

<activity

android:name="com.amazon.ags.html5.overlay.GameCircleUserInterface"

android:hardwareAccelerated="false"

android:theme="@style/GCOverlay" >

</activity>

<activity

android:name="com.amazon.identity.auth.device.authorization.AuthorizationActivity"

android:allowTaskReparenting="true"

android:launchMode="singleTask"

android:theme="@android:style/Theme.NoDisplay" >

<intent-filter>

<action android:name="android.intent.action.VIEW" />

<category android:name="android.intent.category.DEFAULT" />

<category android:name="android.intent.category.BROWSABLE" />

<data

android:host="net.iwobi.game.flickworldcup"

android:scheme="amzn" />

</intent-filter>

</activity>

<activity

android:name="com.amazon.ags.html5.overlay.GameCircleAlertUserInterface"

android:hardwareAccelerated="false"

android:theme="@style/GCAlert" >

</activity>

<receiver

android:name="com.amazon.identity.auth.device.authorization.PackageIntentReceiver"

android:enabled="true" >

<intent-filter>

<action android:name="android.intent.action.PACKAGE_INSTALL" />

<action android:name="android.intent.action.PACKAGE_ADDED" />

<data android:scheme="package" />

</intent-filter>

</receiver>


这些配置中需要的res，可以从AmazonSDK/Android/GameCircle/GameCircleSDK/res/中找到并copy到你的project中。

*3、初始化GameCircle*

GameCircleSDK这个Demo中没有提供太多源码，src目录下是空的。因此我们只能参考Amazon Developer站点上页面上的说明一步步的添加和调整我们的代码了。

在你的XXActivity类中，我们添加如下方法：

//reference to the agsClient

public AmazonGamesClient agsClient;


AmazonGamesCallback callback = new AmazonGamesCallback() {

@Override

public void onServiceNotReady(AmazonGamesStatus status) {

Message msg = new Message();

switch (status) {

// The SDK failed to initialize correctly.

case CANNOT_INITIALIZE:

Log.i(TAG, "onServiceNotReady: CANNOT_INITIALIZE");

msg.obj = "Can not initialize Amazon Game Services";

break;

// The SDK is in the process of initializing.

case INITIALIZING:

Log.i(TAG, "onServiceNotReady: INITIALIZING");

msg.obj = "Initializing Amazon Game Services";

break;

// The device not registered with an account

case NOT_AUTHENTICATED:

Log.i(TAG, "onServiceNotReady: NOT_AUTHENTICATED");

msg.obj = "The Device does not registered with an account";

break;

// The game is not authorized to use this service.

case NOT_AUTHORIZED:

Log.i(TAG, "onServiceNotReady: NOT_AUTHORIZED");

msg.obj = "Not authorized to use Amazon Game Services";

break;

}


//unable to use service

msg.what = 21;

notifyHandler.sendMessage(msg);

}

@Override

public void onServiceReady(AmazonGamesClient amazonGamesClient) {

agsClient = amazonGamesClient;


//ready to use GameCircle

if (agsClient != null)

Log.i(TAG, "on AmazonGamesCallback: call onServiceReady, agsClient init ok");

else

Log.i(TAG, "on AmazonGamesCallback: call onServiceReady, agsClient init failed");

}

};


//list of features your game uses (in this example, achievements and leaderboards)

EnumSet<AmazonGamesFeature> myGameFeatures = EnumSet.of(

AmazonGamesFeature.Leaderboards);

protected void onResume() {

super.onResume();


… …

AmazonGamesClient.initialize(this, **callback, myGameFeatures**);

}

public void onPause() {

super.onPause();

if (agsClient != null) {

agsClient.release();

}

}


*4、提交成就积分*

当玩家结束游戏时，可以选择将此次的高分上传到leaderboards上。游戏中应对积分提交的代码也在XXActivity中。

public static void onSubmitScoreToLeaderBoard(int score) {

if (((FlickWorldCupActivity)context).agsClient == null) {

Message msg = new Message();

msg.what = 21;

msg.obj = "Unable to use Amazon Game Services";

notifyHandler.sendMessage(msg);

return;

}


LeaderboardsClient lbClient = ((FlickWorldCupActivity)context).agsClient.getLeaderboardsClient();

AGResponseHandle<SubmitScoreResponse> handle = lbClient.submitScore("**FlickWorldCupTopScore**", score);


// Optional callback to receive notification of success/failure.

handle.setCallback(new AGResponseCallback<SubmitScoreResponse>() {


@Override

public void onComplete(SubmitScoreResponse result) {

if (result.isError()) {

// Add optional error handling here. Not strictly required

// since retries and on-device request caching are automatic.

Message msg = new Message();

msg.what = 22;

msg.obj = "Submit Score to LeaderBoard Failed!";

notifyHandler.sendMessage(msg);

} else {

// Continue game flow.

Message msg = new Message();

msg.what = 23;

msg.obj = "Submit Score to LeaderBoard OK!";

notifyHandler.sendMessage(msg);

}

}

});

}

如果仅是查看积分排行，可以用下面这个方法：

public static void onShowLeaderBoardOverlay() {

if (((FlickWorldCupActivity)context).agsClient == null) {

Message msg = new Message();

msg.what = 21;

msg.obj = "Unable to use Amazon Game Services";

notifyHandler.sendMessage(msg);

return;

}


LeaderboardsClient lbClient = ((FlickWorldCupActivity)context).agsClient.getLeaderboardsClient();

AGResponseHandle<RequestResponse> handle = lbClient.showLeaderboardOverlay("FlickWorldCupTopScore");


handle.setCallback(new AGResponseCallback<RequestResponse>() {


@Override

public void onComplete(RequestResponse result) {

if (result.isError()) {

// Add optional error handling here. Not strictly required

// since retries and on-device request caching are automatic.

Log.i(TAG, "onShowLeaderBoardOverlay – onComplete: Show LeaderBoard Request Failed!");

}

}

});

}


*** 游戏圈上线**

游戏圈无法在本地进行测试，只能在真实的游戏圈中测试代码是否ok。不过Amazon的游戏圈提供了管理功能，在测试后发布前可将游戏圈 leaderboard的值reset。游戏圈leaderboard发布后，你就可以使用leaderboard了。游戏圈功能在国内访问是没有任何问 题的，查看积分榜，提交分数到积分榜都很顺畅。

*** 小结**

Amazon游戏SDK在国内的应用估计比较小众，大家可能更多的选择用Google Play提供的服务或是AppStore的，但Amazon毕竟为游戏开发者提供了一个选择（而且是完全免费的哦），另外Amazon的Support对 提交问题的反馈较为及时(无论是mail还是forum上的提问)，基本24小时内就会有答复。各种设施的发布也比较快，有时候3-4个小时即可生效。

目前Amazon Game SDK的资料多为英文，且集中在Amazon官方站点以及官方维护的[support论坛](http://forums.developer.amazon.com/forums/index.jspa)中。遇到问题，亚马逊的论坛是第一选择。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论