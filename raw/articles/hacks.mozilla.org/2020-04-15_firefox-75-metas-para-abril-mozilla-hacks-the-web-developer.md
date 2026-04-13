---
title: 'Firefox 75: Metas para abril – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/04/firefox-75/
author: Chris Mills
published: '2020-04-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Incluso en los actuales tiempos de aislamiento, nuestros equipos de ingeniería han sabido adaptarse, enfocarse y trabajar duro para ofrecer otra nueva y emocionante versión de Firefox al mundo. En lo que respecta a las herramientas para desarrollador, a partir de ahora encontramos un sistema de evaluación instantánea en la consola, puntos de interrupción de eventos para WebSockets y muchas otras cosas más.

En el lado de la plataforma web, las nuevas adiciones incluyen la carga diferida (*lazy loading*) de HTML para imágenes, las funciones `min()`

, `max()`

y `clamp()`

de CSS, los campos public static class y otras novedades al soporte de la API Web Animations.

Como siempre, sigue leyendo para conocer los aspectos más destacados o consulta la lista completa de adiciones en los siguientes artículos:

[Firefox 75 para desarrolladores](https://developer.mozilla.org/docs/Mozilla/Firefox/Releases/75)[Compatibilidad de sitios web para Firefox 75](https://www.fxsitecompat.com/versions/75/)[Notas de la versión de usuario final de Firefox 75](https://www.mozilla.org/firefox/75.0/releasenotes/)

## Adiciones a las herramientas para desarrolladores

Comencemos por revisar las adiciones más interesantes de las herramientas para desarrolladores de la versión 75.

### Evaluación instantánea de las expresiones de consola

Evaluar expresiones en la [consola](https://developer.mozilla.org/docs/Tools/Web_Console) es una forma rápida de analizar el estado de su aplicación, consultar el DOM o, simplemente, probar las API de JavaScript.

Ahora es más fácil prototipar código más largo con el [modo multilínea de la consola de Firefox](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode), que se vuelve cada vez más cómodo de usar, más similar a un entorno de desarrollo como tal.

El nuevo sistema de *evaluación instantánea* [muestra una vista previa](https://quokkajs.com/) de los resultados de la expresión actual a medida que se escribe, de forma similar a editores como [Quokka.js](https://quokkajs.com/). En caso de que las expresiones introducidas en la consola no produzcan efectos secundarios, sus resultados se previsualizarán mientras se escriben.

Se ha trabajado mucho para conseguir que la vista previa sea lo más fluida posible. Los elementos de los nodos del DOM aparecen resaltados en los resultados. La herramienta de autocompletar código recomienda métodos y propiedades en base al tipo del resultado. Además, se puede obtener una vista previa de los errores para poder corregir las expresiones más rápido.

### Mejor inspección y medición

#### La medición del área ahora es redimensionable

Mediante la ![Una captura de pantalla que muestra la herramienta de medición de érea en las herramientas para desarrolladores, que permite dibujar rápidamente rectángulos sobre la página para medir la altura, la anchura y la longitud diagonal de áreas específicas.](../../assets/91554d43b1a27144.png)


[herramienta de medición de área](https://developer.mozilla.org/docs/Tools/Measure_a_portion_of_the_page)opcional en las herramientas para desarrolladores, puede dibujar rápidamente rectángulos sobre su página para medir la altura, la anchura y la longitud diagonal de áreas específicas. Puede habilitar la herramienta en la configuración, bajo "Botones disponibles en la caja de herramientas". Gracias a

[Sebastian Zartner [:sebo]](https://github.com/SebastianZ), estos rectángulos ahora tienen controles para redimensionar que permiten ajustarlos con precisión.

#### Usar XPath para encontrar elementos DOM

Las herramientas de automatización suelen hacer uso de las [consultas XPath](https://developer.mozilla.org/docs/Web/XPath) para indicarle al software qué elementos buscar para interactuar. Gracias, de nuevo, a sebo, ahora puede usar XPath en la [búsqueda de HTML del Inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_HTML#XPath_search) para los elementos del DOM. Esto hace que sea más fácil probar expresiones y afinar las consultas con precisión en entornos reales.

### Puntos de interrupción de eventos para WebSockets

Las características de [inspección de WebSockets](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/) han mejorado en todas las versiones recientes de las herramientas de desarrollo. Esta vez tenemos buenos aportes a la depuración, gracias a una contribución del talentoso [Chujun Lu](https://bugzilla.mozilla.org/user_profile?user_id=632471).

Ahora tenemos la opción de pausar o registrar los manejadores de eventos de WebSocket cuando estos se ejecuten. Utilice los [puntos de interrupción para event listeners](https://developer.mozilla.org/docs/Tools/Debugger/Set_event_listener_breakpoints), recientemente agregados en el depurador. Cuando selecciona la opción de registro, se guardarán los datos del evento y el manejador que se ha ejecutado sin detener la ejecución. Entre otras novedades del inspector de WebSocket, el filtro de mensajes ahora admite expresiones regulares gracias a nuestro ampliamente conocido colaborador [Outvi V](https://bugzilla.mozilla.org/user_profile?user_id=603026).

### Adiciones de red

Se ha realizado una gran cantidad de trabajo en mejorar la calidad y el rendimiento del panel de red para Firefox 75. Esta versión incorpora importantes avances en cuanto a la rapidez con la que se procesan las solicitudes simultáneas de ejecución rápida sin afectar a la CPU.

En el lado de la interfaz, el colaborador [Florens Verschelde](https://fvsch.com/) dirigió la propuesta y el diseño de los nuevos bordes entre columnas, pensados para facilitar la legibilidad. Ahora podemos observar cómo el diseño es más consistente con el aspecto general de las herramientas de desarrollo. Los botones de filtro también son más legibles, con un mejor contraste entre estados, gracias al colaborador [Vitalii](https://bugzilla.mozilla.org/user_profile?user_id=657068).

El panel de bloqueo de peticiones sirve para probar la resistencia de un sitio cuando fallan las solicitudes coincidentes. Ahora permite patrones comodín con "*". Gracias a [Duncan Dean](https://bugzilla.mozilla.org/user_profile?user_id=472694) por tal contribución.

### Funciones de acceso temprano en las herramientas de desarrollo

[Developer Edition](https://www.mozilla.org/firefox/developer/) es el canal de prelanzamiento de Firefox, que proporciona acceso temprano a las nuevas herramientas y funciones de la plataforma. Su configuración también facilita más características para los desarrolladores de forma predeterminada. Nos complace poder llevar nuevas funciones rápidamente a Developer Edition para poder conocer sus comentarios, como los de los siguientes aspectos destacados.

#### Rastros de pila asíncrona para el depurador y la consola

El código de JavaScript moderno depende en gran medida del uso de [ async/await](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function), además de otras

[operaciones asíncronas](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous)como eventos, promesas y temporizadores. Gracias a una mejor integración con el motor de JavaScript, ahora se captura la ejecución asincrónica para proporcionar una imagen más completa.

Las pilas de llamadas asíncronas en el depurador le permiten ver eventos, temporizadores y llamadas a funciones basadas en promesas que se ejecutan en diferentes momentos de tiempo. En la consola, las pilas asíncronas facilitan la búsqueda de las causas raíz de los errores.

## Actualizaciones de la plataforma web

Observemos lo que nos proporciona Firefox 75 en términos de actualizaciones de la plataforma web.

### Carga diferida de HTML para imágenes

La [carga diferida](https://developer.mozilla.org/docs/Web/Performance/Lazy_loading) (*lazy load*) es una estrategia común para mejorar el rendimiento al identificar recursos como no bloqueantes (no críticos) y cargarlos solo cuando sea necesario, en lugar de cargarlos todos de inmediato. Las imágenes son uno de los elementos más comúnmente responsables de la lentitud en la carga de las aplicaciones web.

Para facilitar la carga diferida de imágenes, hemos introducido soporte para el atributo load en el elemento HTML [ <img>](https://developer.mozilla.org/docs/Web/HTML/Element/img). Establecer el valor en

*lazy*le indicará al navegador que posponga la carga de imágenes que están fuera de la pantalla hasta que el desplazamiento del usuario se aproxime a ellas. El otro único valor posible es

*eager*, que es el predeterminado, como era de esperar.

`<img src="image.jpg" loading="lazy" alt="..." />`


Puede determinar si una imagen determinada ha terminado de cargar examinando el valor de su propiedad booleana `complete`

. Nota: El evento `load`

se ejecuta cuando se ha terminado de cargar todo el contenido con el atributo eager. En ese punto, es posible (o incluso probable) que haya imágenes que deban cargarse en diferido dentro de pantalla y que aún no lo hayan hecho.

Nota: Chrome también ha implementado un soporte experimental para la carga diferida de contenidos [ <iframe>](https://developer.mozilla.org/docs/Web/HTML/Element/iframe), pero esto aún no es estándar. Por nuestro lado, estamos esperando hasta que se haya estandarizado.

### CSS `min()`

, `max()`

y `clamp()`


¡Algunas nuevas y emocionantes adiciones de CSS este mes! Hemos agregado soporte para tres funciones CSS muy útiles que, a pesar de estar estrechamente relacionadas entre sí, tienen diferentes propósitos:

— acepta uno o más posibles valores o cálculos entre los que elegir, y garantiza que el valor utilizado en todas las situaciones sea el más pequeño de entre las posibilidades. En la práctica, esto proporciona un rango de valores para diseños responsivos, junto con un valor máximo permitido.`min()`

— acepta uno o más posibles valores o cálculos entre los que elegir, y garantiza que el valor utilizado en todas las situaciones sea el más grande de entre las posibilidades. En la práctica, esto proporciona un rango de valores para diseños responsivos, junto con un valor mínimo permitido.`max()`

— acepta tres valores o cálculos: un mínimo, un preferido y un máximo. Se utilizará el mínimo o el máximo si el valor calculado cae por debajo del mínimo o por encima del máximo, respectivamente. Si el valor calculado cae entre ambos, se usará el valor preferido. Esto permite que el valor de la propiedad se adapte a los cambios en el elemento o la página a la que está asignado, al mismo tiempo que permanece entre los valores mínimo y máximo.`clamp()`


Estas funciones son muy útiles para un diseño responsivo, y permiten ahorrar tiempo y código haciendo cosas que anteriormente se podían hacer usando una combinación de [ min-width](https://developer.mozilla.org/docs/Web/CSS/min-width),

[y](https://developer.mozilla.org/docs/Web/CSS/width)

`width`

[, múltiples](https://developer.mozilla.org/docs/Web/CSS/max-width)

`max-width`

[media queries](https://developer.mozilla.org/docs/Web/CSS/Media_Queries)o, incluso,

[JavaScript](https://developer.mozilla.org/docs/Web/javascript).

#### CSS `min()`

, `max()`

y `clamp()`

en acción

Estudiemos el siguiente ejemplo:

`html { font-family: sans-serif; } body { margin: 0 auto; width: min(1000px, calc(70% + 100px)); } h1 { letter-spacing: 2px; font-size: clamp(1.8rem, 2.5vw, 2.8rem) } p { line-height: 1.5; font-size: max(1.2rem, 1.2vw); }`


Aquí, tenemos el ancho del body establecido en `min(1000px, calc(70% + 100px))`

, lo que significa que, en viewports más amplios, el contenido del body tendrá una anchura de `1000px`

. En viewports más estrechos, el contenido del body será un `70%`

del ancho del viewport más `100px`

(hasta que el resultado de este cálculo sea `1000px`

o más).

El tamaño de fuente del encabezado de nivel superior se establece en `clamp(1.8rem, 2.5vw, 2.8rem)`

. Por lo tanto, tendrá un mínimo de `1.8rem`

y un máximo de `2.8rem`

. Entre esos valores, se activará el valor ideal de `2.5vw`

, por lo que veremos crecer el texto del encabezado, y reducirse en los anchos de viewport donde `2.5vw`

se calcule como mayor que `1.8rem`

, pero menor que `2.8rem`

.

El tamaño de fuente del párrafo se establece en `max(1.2rem, 1.2vw)`

, lo que significa que tendrá un mínimo de `1.2rem`

. Pero comenzará a crecer en el momento en que el valor calculado de `1.2vw`

sea mayor que el valor calculado de `1.2rem`

.

Se puede ver esto en acción en nuestro [sencillo ejemplo de min(), max(), clamp()](https://mdn.github.io/css-examples/min-max-clamp/).



### Funciones del lenguaje JavaScript

Ha habido algunas adiciones interesantes de JavaScript en la versión 75.

En primer lugar, ahora tenemos [campos public static class](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Class_fields#Public_static_fields). Son útiles cuando queremos que un campo exista solo una vez por clase, pero no en cada instancia de clase que se cree. Esto es particularmente relevante para la caché, la configuración fija o cualquier otro tipo de información que no haga falta replicar en todas las instancias. La sintaxis básica tiene este aspecto:

`class ClassWithStaticField { static staticField = 'static field' } console.log(ClassWithStaticField.staticField) // expected output: "static field"`


A continuación, tenemos otra mejora a la funcionalidad de internacionalización (i18n) con la adición de [ Intl.Locale](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Locale), un constructor estándar incorporado que representa un identificador de configuración regional Unicode. Por ejemplo, podría crear un objeto de configuración regional para el coreano así:

`const korean = new Intl.Locale('ko', { script: 'Kore', region: 'KR', hourCycle: 'h24', calendar: 'gregory' });`


Y, luego, retorna las propiedades del objeto como cabría esperar:

`console.log(korean.hourCycle, japanese.hourCycle); // expected output: "h24" "h12"`


### Adiciones para formularios

Tenemos un par de adiciones útiles específicas para la de API de formulario en Firefox 75:

- La interfaz
ahora tiene un nuevo método,`HTMLFormElement`

. A diferencia del antiguo (y aún disponible) método`requestSubmit()`

,`submit()`

`requestSubmit()`

actúa como si se hubiera hecho clic en un botón de enviar (submit) concreto, en lugar de, simplemente, enviar los datos del formulario al destinatario. Por lo tanto, se ejecuta el eventoy se verifica la validez del formulario antes de enviar los datos.`submit`

- El evento
ahora está representado por un objeto de tipo`submit`

en lugar de un simple`SubmitEvent`

.`Event`

`SubmitEvent`

incluye una nueva propiedadque devuelve el`submitter`

invocado para activar el envío del formulario. Con este evento, podemos disponer de un único manejador para eventos submit que puede discernir cuál de los múltiples botones o enlaces de submit se ha utilizado para enviar el formulario.`Element`


### Mejoras en la API de Animaciones Web (Web Animations)

En la versión 75, hemos añadido una serie de nuevas características de la API Web Animations, haciendo que esta especificación sea aún más interesante y útil.

#### Fotogramas clave con inicio o final implícitos

A partir de ahora, se puede establecer un estado inicial o final solo para una animación (es decir, un único fotograma clave o keyframe). A continuación, el navegador inferirá el otro extremo de la animación, si puede. Por ejemplo, veamos [esta sencilla animación](https://mdn.github.io/dom-examples/web-animations-api/implicit-keyframes.html): el objeto del fotograma clave se ve así:

`let rotate360 = [ { transform: 'rotate(360deg)' } ];`


Solo hemos especificado el estado final de la animación, y el inicial está implícito.

#### Eliminar automáticamente animaciones de relleno

Es posible activar una gran cantidad de animaciones en el mismo elemento. Si son indefinidas (es decir, llenan hacia adelante), se podría generar una lista de animaciones enorme que produciría un desbordamiento de memoria. Por esta razón, hemos implementado la parte de la especificación de Web Animations que elimina automáticamente las animaciones de relleno hacia adelante, a menos que el desarrollador indique explícitamente que quiere conservarlas.

Esto se puede ver acción en nuestra [sencilla demostración de sustitución de animaciones indefinidas](https://mdn.github.io/dom-examples/web-animations-api/replace-indefinite-animations.html). Las características de JavaScript implicadas son las siguientes:

`animation.commitStyles()`

— ejecute este método para confirmar el estado final del estilo de una animación en el elemento que se está animando, incluso después de que se haya eliminado dicha animación. Provocará que el estado final del estilo se escriba en el elemento que se está animando, en la forma de propiedades de un atributo de estilo.`animation.onremove`

— permite ejecutar un controlador de eventos que se activa cuando se elimina la animación (es decir, se ubica en un estado de reemplazo activo).`animation.persist()`

— cuando se desea explícitamente que se conserven las animaciones hay que invocar`persist()`

.`animation.replaceState`

— devuelve el estado de reemplazo de la animación. Este será`active`

si la animación ha sido eliminada, o`persisted`

si se ha invocado`persist()`

.

#### Líneas de Tiempo (*Timelines*)

El getter [ Animation.timeline](https://developer.mozilla.org/docs/Web/API/Animation/timeline) o las funciones

[,](https://developer.mozilla.org/docs/Web/API/Document/timeline)

`Document.timeline`

[y](https://developer.mozilla.org/docs/Web/API/DocumentTimeline)

`DocumentTimeline`

[ahora están habilitados de manera predeterminada, lo que significa que ya se puede acceder a la información de la línea de tiempo de su animación. Esta característica es valiosísima para devolver valores de tiempo con propósitos de sincronización.](https://developer.mozilla.org/docs/Web/API/AnimationTimeline)

`AnimationTimeline`

Por defecto, la línea de tiempo de la animación y la del documento son las mismas.

#### Obtener animaciones activas

Por último, pero no menos importante, los métodos [ Document.getAnimations()](https://developer.mozilla.org/docs/Web/API/Document/getAnimations) y

[ahora estén habilitados por defecto. Respectivamente, permiten devolver una matriz de todas las animaciones activas en un documento completo o en un elemento específico.](https://developer.mozilla.org/docs/Web/API/Element/getAnimations)

`Element.getAnimations()`

### Anotaciones ARIA

En Firefox 75 (en Linux y Windows), veré la adición de soporte para un conjunto de nuevas características de accesibilidad conocidas colectivamente como anotaciones ARIA, que se publicarén en la próxima versión 1.3 de la especificación WAI-ARIA. Estas características hacen posible crear anotaciones accesibles dentro de los documentos web. Los casos de uso típicos incluyen sugerencias de edición (es decir, una adición y/o eliminación en un documento editable) y comentarios (por ejemplo, un comentario editorial relacionado con una parte de un documento en revisión).

Todavía no hay soporte disponible para las anotaciones ARIA en lectores de pantalla, pero pronto podremos utilizar estos nuevos roles y demás atributos. Para ver ejemplos y más información de compatibilidad, lea las [anotaciones de ARIA](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Annotations) en MDN.

## Extensiones del navegador

Se han añadido dos nuevos [ browserSettings](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings) a la

[API de WebExtensions](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions):

[para ampliar el texto en una pégina y](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings/zoomFullPage)

`zoomFullPage`

[, que determina si el zoom se aplica solo a la pestaña activa o a todas las pestañas del mismo sitio.](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/browserSettings/zoomSiteSpecific)

`zoomSiteSpecific`

## Resumen

Eso ha sido todo. Hemos incluido nuevas características interesantes en Firefox 75. ¡No dudes en echarles un vistazo y diviértete probando! Como siempre, siéntase libre de dar us opiniones y formular sus preguntas en los comentarios.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.