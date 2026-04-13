---
title: Triggering .NET Core Lambdas from Multiple Services
url: https://www.vertexfragment.com/ramblings/multiple-lambda-triggers/
author: Steven Sell
published: '2020-01-08'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

When creating an AWS Lambda you may choose to use a pre-existing runtime (such as .NET 2.1, Python 3.6) or roll your own custom runtime. One of the primary benefits of using a custom runtime is that you may use any language to develop your Lambda. At the time of writing, the only way to use .NET Core 3.0 as a Lambda is to use one of these custom runtimes.

The standard approach for a Lambda, at least a .NET-based one, is to handle a single message source such as an API Gateway or SQS. Amazon makes it very easy to create such a Lambda and provides plenty of examples which are triggered by a single specific service.

But what if you want your Lambda to be able to be triggered from multiple different sources without having to split your codebase? As this ramble will show this is entirely possible, though not well documented for a .NET developer. It took a deep dive into the [AWS .NET Lambda](https://github.com/aws/aws-lambda-dotnet) source to piece together, and hopefully this may ease someone else’s pain.

In order to put together how to trigger from multiple sources we first need to really understand how Lambdas work and what is hidden away by all of the Amazon bootstraps and helper classes. If this isn’t a concern for you, feel free to jump ahead to the next section.

To begin, Lambdas are super simple. Now it took a lot of documentation and code delving to come to that conclusion but it is one of those things that is deviously simple once you understand it.

The high-level Amazon documentation will lead you to believe that your Lambda is launched anew each time a request comes in. This makes it appear very straightforward - something hits my API Gateway or enters my SQS and then my Lambda launches! However this is not technically correct. It is true that Lambdas launch and scale dynamically according to load but they do not launch for each and every trigger.

Instead, the Lambda will launch and then poll for incoming invocation requests. It will process that request and then resume polling. The “warm up” time people like to mention is the actual startup of your Lambdas, whereas the typical near-instant response is an already launched Lambda polling and picking up your triggered event.

This is the magic hidden by the [Amazon bootstraps and it all boils down to](https://github.com/aws/aws-lambda-dotnet/blob/b64ab94e9c83b7840dc6052613bf5e5eb58cfd46/Libraries/src/Amazon.Lambda.RuntimeSupport/Bootstrap/LambdaBootstrap.cs#L110)

```
while not cancelled
{
check for event
process event
report processing status
}
```


The `check for event`

and `report status`

are achieved by making calls to the [AWS Lambda Runtime Interface](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html) which provides a basic HTTP API. This HTTP API is what allows for Lambdas in a custom runtime to be written with any language, as long as the language provides the most basic of HTTP capabilities.

And it is this same API that we will use to detect what the source of the incoming event is and process it accordingly.

So why are Lambdas limited to only a single trigger source? They aren’t, it is just the bootstraps provided by Amazon that are.

In order to handle multiple trigger sources we simply need to peek at the invocation message and then act accordingly. We perform this peek using the same HTTP API that the bootstraps use, and we will implement it in a custom `LambdaDetector`

class. [The full source](https://www.vertexfragment.com#full-source) can be found at the end of this article as we will only cover the key parts.

To detect what service triggered the Lambda we can peek and retrieve the invocation event. The structure and contents of this event can then be used to determine the trigger service.

```
public static class LambdaDetector
{
private static readonly string NextInvocationUrl = $"http://{Environment.GetEnvironmentVariable("AWS_LAMBDA_RUNTIME_API")}/2018-06-01/runtime/invocation/next";
// ...
private static LambdaInvocationEvent GetInvocationEvent(CancellationToken token = default)
{
using (var client = new HttpClient())
using (var request = new HttpRequestMessage())
{
request.Method = new HttpMethod("GET");
request.Headers.Accept.Add(MediaTypeWithQualityHeaderValue.Parse("application/json"));
request.RequestUri = new Uri(NextInvocationUrl, UriKind.RelativeOrAbsolute);
var responseTask = client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, token);
responseTask.Wait();
var response = responseTask.Result;
if ((response.StatusCode != System.Net.HttpStatusCode.OK) &&
(response.StatusCode != System.Net.HttpStatusCode.NoContent))
{
throw new Exception($"API request '{request.RequestUri}' returned error status code {response.StatusCode}");
}
return LambdaInvocationEvent.Build(response);
}
}
// ...
```


Very straightforward `GET`

request to the API whose URL is provided as [an environment variable](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime).

The response is used to build our `LambdaInvocationEvent`

which is defined in the [Lambda Runtime API - Next Invocation](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-next). For the purpose of trigger service detection we are only concerned about the `Payload`

member which is the JSON body that contains our service-specific event.

For example if our Lambda was triggered by an API Gateway then the `Payload`

is an [ APIGatewayProxyRequest](https://github.com/aws/aws-lambda-dotnet/blob/master/Libraries/src/Amazon.Lambda.APIGatewayEvents/APIGatewayProxyRequest.cs), whereas if it was triggered by an SQS then it is a

[, etc. Since Lambdas are typically designed as only having a single known source there is no other identifying information within the invocation event and/or payload to determine the trigger service.](https://github.com/aws/aws-lambda-dotnet/blob/master/Libraries/src/Amazon.Lambda.SQSEvents/SQSEvent.cs)

`SQSEvent`

So we must attempt to deserialize the payload into the different possible events:

```
private static (APIGatewayProxyRequest api, SQSEvent sqs) GetEventBody(LambdaInvocationEvent invocationEvent)
{
var api = JsonConvert.DeserializeObject<APIGatewayProxyRequest>(invocationEvent.Payload);
var sqs = JsonConvert.DeserializeObject<SQSEvent>(invocationEvent.Payload);
return ((api?.Resource == null ? null : api),
(sqs?.Records == null ? null : sqs));
}
```


Which is used to make the final determination:

```
public static LambdaSource DetectSource()
{
APIGatewayProxyRequest api = null;
SQSEvent sqs = null;
var invocationEventTask = GetInvocationEvent();
(api, sqs) = GetEventBody(invocationEventTask);
return (api != null) ? LambdaSource.ApiGateway : LambdaSource.Sqs;
}
```


And that’s it, we now know which service triggered our Lambda.

Once we know the source we can make our life easier by then simply routing to one of the standard Lambda bootstraps. Of course one could roll their own custom bootstrap but that is an entirely different effort.

For our API Gateway + SQS example we would see something similar to the following.

```
public static void Main(string[] args)
{
LambdaSource triggerSource = LambdaDetector.DetectSource();
switch (triggerSource)
{
case LambdaSource.ApiGateway:
TriggerFromApiGateway();
break;
case LambdaSource.Sqs:
TriggerFromSqs();
break;
default:
break;
}
}
public static void TriggerFromApiGateway()
{
var lambdaEntry = new ApiGatewayLambdaFunction();
var functionHandler = (Func<APIGatewayProxyRequest, ILambdaContext, Task<APIGatewayProxyResponse>>)(lambdaEntry.FunctionHandlerAsync);
using (var handlerWrapper = HandlerWrapper.GetHandlerWrapper(functionHandler, new JsonSerializer()))
using (var bootstrap = new LambdaBootstrap(handlerWrapper))
{
bootstrap.RunAsync().Wait();
}
}
public static void TriggerFromSqs()
{
var lambdaEntry = new SqsLambdaFunction();
Action<SQSEvent, ILambdaContext> func = lambdaEntry.FunctionHandler;
using (var handlerWrapper = HandlerWrapper.GetHandlerWrapper(func, new JsonSerializer()))
using (var bootstrap = new LambdaBootstrap(handlerWrapper))
{
bootstrap.RunAsync().Wait();
}
}
```


While the above approach works it is not without it’s concerns. Chiefly,

- Is the message preserved when “peeking”?
- Can the Lambda have multiple different trigger sources simultaneously?

When the `/runtime/invocation/next`

API is used it does not pop the message off or otherwise alter it. The message is preserved until your Lambda makes an accompanying call to the `/runtime/invocation/{request-id}/response`

API which reports whether processing the message was successful or not.

This is why when a standard SQS Lambda processing multiple messages fails, the underlying bootstrap “requeues” all of the messages. The messages are all packed into a single invocation event and they pass or fail together.

Unfortnately this approach does not allow for multiple simultaneous trigger sources for a single Lambda.

But wait, wasn’t that the whole point? Not exactly.

Using the `LambdaDetector`

described above allows for the reusing of a *single codebase* but you will still need a unique Lambda for each potential trigger source. Though if you are using CloudFormation templates then this should not be a limiting factor and this allows for a single template file that may be deployed using

```
dotnet lambda deploy-serverless
```


Which means technically on AWS you will have multiple Lambdas, but in practice you will only have a single .NET project and CloudFormation template.

But why is this necessary? This is because we perform our detection before we enter into one of the Amazon-provided bootstraps. It is within these bootstraps that we enter the `while`

loop described at the start of this ramble. This limitation could be worked around, but it would require rolling your own custom Lambda bootstrap which is beyond the scope of this.

So if we have multiple simultaneous triggers we see the following:

- Peek - see API Gateway invocation event
- Route to API Gateway bootstrap
- Process API Gateway invocation event
- Incoming SQS invocation event but we are still in the API Gateway bootstrap
- The SQS event is processed as an API Gateway event (and most likely fails)

The full C# source for the Lambda Detector can be found in the companion repository:

It should be noted that it provides only the C# source and project. Other components, such as a CloudFormation template, are left to the reader and their personal requirements.