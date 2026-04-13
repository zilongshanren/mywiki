---
title: La seguridad es todavía mejor con Firefox 74 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2020/03/la-seguridad-es-todavia-mas-con-firefox-74/
author: Chris Mills
published: '2020-03-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

El día de hoy se lanza Firefox número 74. Las funciones más relevantes que te presentamos esta vez son mejoras en la seguridad: Política de funciones, el encabezado `Cross-Origin-Resource-Policy`

y la eliminación del soporte para TLS 1.0/1.1. También tenemos algunas nuevas funciones de propiedades de texto CSS, el operador de encadenamiento opcional JS y otras características de métricas de texto de canvas 2D, junto con el habitual conjunto de mejoras de las herramientas para desarrolladores y corrección de errores.

Como de costumbre, sigue leyendo para conocer los aspectos más destacados, o consulta la lista completa de añadidos en los siguientes artículos:

[Firefox 74 para desarrolladores](https://developer.mozilla.org/docs/Mozilla/Firefox/Releases/74)[Compatibilidad del sitio con Firefox 74](https://www.fxsitecompat.com/versions/74/)[Notas de publicación para el usuario final de Firefox 74](https://www.mozilla.org/firefox/74.0/releasenotes/)

## Mejoras en la seguridad

Veamos las mejoras en seguridad que tenemos en la versión 74.

### Política de funciones

Finalmente hemos habilitado la [Política de funciones](https://developer.mozilla.org/docs/Web/HTTP/Feature_Policy/Using_Feature_Policy) de forma predeterminada. Ahora puedes usar los atributos `<iframe>`

`allow`

y el encabezado HTTP [ Feature-Policy](https://developer.mozilla.org/docs/Web/HTTP/Headers/Feature-Policy) para definir las características de permisos de tus documentos de nivel superior e iFrames. A continuación tienes algunos ejemplos de su sintaxis:

`<iframe src="https://example.com" allow="fullscreen"></iframe>`


`Feature-Policy: microphone 'none'; geolocation 'none'`


### CORP

También hemos habilitado el soporte para el encabezado [ Cross-Origin-Resource-Policy(CORP)](https://developer.mozilla.org/docs/Web/HTTP/Cross-Origin_Resource_Policy_(CORP)), lo que permite a los sitios y aplicaciones web asignar protección contra ciertas solicitudes de origen cruzado (como las procedentes de elementos

`<img>`

y `<script>`

). Esto puede ser útil para mitigar ataques especulativos de canal lateral (como Spectre y Meltdown) así como los ataques de inclusión de ejecución de comandos entre sitios (Cross-Site Scripting).Los valores disponibles son `same-origin`

y `same-site`

. `same-origin`

solo permite solicitudes que compartan el mismo esquema, host y puerto para leer el recurso pertinente. Esto brinda un nivel adicional de protección más allá de la política del mismo origen de forma determinada de la web. `same-site`

solo permite solicitudes que comparten el mismo sitio.

Para usar CORP hay que establecer uno de estos valores en el encabezado, por ejemplo:

`Cross-Origin-Resource-Policy: same-site`


### Eliminación de TLS 1.0/1.1

Finalmente, pero igual de importante, Firefox 74 elimina el soporte de TLS 1.0/1.1, para ayudar a elevar el nivel general de seguridad de la plataforma web. Esto es vital para que el ecosistema TLS avance, así como eliminar una serie de puntos vulnerables que existían como resultado de que TLS 1.0/1.1 no fuera tan robusto como hubiéramos deseado. Por todo ello, es necesario que desaparezcan.

El cambio se anunció por primera vez en octubre de 2018 como una iniciativa conjunta de Mozilla, Microsoft y Apple. Ahora, en marzo del 2020, todos estamos cumpliendo nuestras promesas (a excepción de Apple, que realizará el cambio un poco más tarde).

El resultado es que tendrás que asegurarte de que, en adelante, tu servidor web sea compatible con TLS 1.2 o 1.3. Lee [Actualización de la eliminación de TLS 1.0 y 1.1](https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/) para saber cómo probar y actualizar tu configuración TLS/SSL. A partir de ahora, Firefox mostrará una página de error [Secure Connection Failed](https://support.mozilla.org/en-US/kb/secure-connection-failed-firefox-did-not-connect) al conectarse con servidores que usen versiones anteriores de TLS. **¡Actualízate ahora**, si todavía no lo has hecho!

**Nota**: durante algunas actualizaciones (y algo más de tiempo en el caso de Firefox ESR), la página de error *Falló la conexión segura* incluirá un botón de anulación que te permitirá habilitar TLS 1.0 y 1.1 en los casos en que un servidor aún no esté actualizado, pero no cuentes con esto durante mucho tiempo.

Para saber más sobre la eliminación de TLS 1.0/1.1 y lo que hay detrás, lee [It’s the Boot for TLS 1.0 and TLS 1.1](https://hacks.mozilla.org/2020/02/its-the-boot-for-tls-1-0-and-tls-1-1/).

## Otras adiciones a la plataforma web

Tenemos muchos más añadidos de plataforma web para ti en Firefox 74.

### Nuevas características de texto CSS

Para comenzar, la propiedad [ text-underline-position](https://developer.mozilla.org/docs/Web/CSS/text-underline-position) está habilitada de forma predeterminada. Esto es útil para posicionar subrayados establecidos en tu texto en determinados contextos a fin de realizar efectos tipográficos específicos.

Por ejemplo, si el [writing mode](https://developer.mozilla.org/docs/Learn/CSS/Building_blocks/Handling_different_text_directions) de tu texto es horizontal, puedes usar `text-underline-position: under;`

para colocar el subrayado debajo de todos los descendientes; esto es útil para asegurar la legibilidad en las fórmulas químicas y matemáticas, que hacen uso frecuente de los subíndices.

```
.horizontal {
text-underline-position: under;
}
```


En textos con modo de escritura [ writing-mode](https://developer.mozilla.org/docs/Web/CSS/writing-mode) vertical, podemos usar valores de

`left`

o `right`

para que el subrayado aparezca a izquierda o derecha del texto, según se requiera.```
.vertical {
writing-mode: vertical-rl;
text-underline-position: left;
}
```


Además, las propiedades [ text-underline-offset](https://developer.mozilla.org/docs/Web/CSS/text-underline-offset) y

[ahora aceptan valores porcentuales, por ejemplo:](https://developer.mozilla.org/docs/Web/CSS/text-decoration-thickness)

`text-decoration-thickness`

`text-decoration-thickness: 10%;`


Para estas propiedades, este es un porcentaje de `1em`

del tamaño actual de la fuente.

### Encadenamiento opcional en JavaScript

Ahora disponemos de un operador de [encadenamiento opcional en JavaScript](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Optional_chaining) (`?.`

). Cuando intentes acceder a un objeto dentro de otro en cadena, esto te permite comprobar implícitamente la existencia del primer objeto, evitando errores y la necesidad de escribir explícitamente código de validación.

`let nestedProp = obj.first?.second;`


### Nuevas métricas de texto de canvas en 2D

La API [ TextMetrics](https://developer.mozilla.org/docs/Web/API/TextMetrics) (que se obtiene usando el método

[) se ha ampliado para incluir cuatro nuevas propiedades que miden el cuadro delimitador real (actualBondingBox):](https://developer.mozilla.org/docs/Web/API/CanvasRenderingContext2D/measureText)

`CanvasRenderingContext2D.measureText()`

[,](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxLeft)

`actualBoundingBoxLeft`

[,](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxRight)

`actualBoundingBoxRight`

[y](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxAscent)

`actualBoundingBoxAscent`

[.](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxDescent)

`actualBoundingBoxDescent`

Por ejemplo:

```
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const text = ctx.measureText('Hello world');
text.width; // 56.08333206176758
text.actualBoundingBoxAscent; // 8
text.actualBoundingBoxDescent; // 0
text.actualBoundingBoxLeft; // 0
text.actualBoundingBoxRight; // 55.733333333333334
```


## Adiciones de las herramientas para desarrolladores

A continuación se detallan los añadidos de las herramientas para desarrolladores.

### Renderizado de dispositivos similares en modo de diseño

A pesar de que [Firefox for Android](https://blog.mozilla.org/futurereleases/2020/01/17/a-brand-new-browsing-experience-arrives-in-firefox-for-android-nightly/) se vuelve a lanzar con [GeckoView](https://mozilla.github.io/geckoview/) para tener [mayor velocidad y privacidad](https://blog.mozilla.org/firefox/es/las-7-mejores-caracteristicas-del-nuevo-navegador-firefox-para-android/), las herramientas para desarrolladores se deben mantener a la vanguardia. Las pruebas en dispositivos móviles deben tener la menor fricción posible, tanto al usar el [Modo de diseño responsivo](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode) (RDM) en tu equipo de escritorio como en el dispositivo con la [Depuración remota](https://developer.mozilla.org/docs/Tools/about:debugging).

Para que los desarrolladores puedan confiar en el resultado sin tener un dispositivo a mano, es fundamental que el modo de diseño responsivo funcione de la forma más correcta posible. En los últimos lanzamientos, hemos implementado mejoras importantes que aseguran que [meta viewport](https://developer.mozilla.org/docs/Mozilla/Mobile/Viewport_meta_tag) se aplique correctamente con *Touch Simulation*. Esto está relacionado con los preajustes mejorados de los dispositivos, que habilitan automáticamente la simulación táctil para dispositivos móviles.

![animated gif showing how responsive design mode now represents view meta settings better](../../assets/00f1ddda7748920e.gif)


Curiosidad: El equipo logró que esta simulación fuera tan precisa que ya ha permitido identificar y corregir errores de renderizado para Firefox en Android.

**Consejo para desarrolladores:** Abre el modo de diseño responsivo sin usar las herramientas para desarrolladores a través del menú de herramientas, o también Ctrl + Mayús + M (en Windows) o Cmd + Opt + M en macOS.

Nos gustaría conocer tus experiencias tras realizar un recorrido por tu sitio en el RDM o en tu teléfono Android con [Firefox Nightly for Developers](https://play.google.com/store/apps/details?id=org.mozilla.fennec_aurora).

### Herramientas útiles de CSS

Los nuevos avisos en contexto de [Inspector de la página](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector) con respecto a las reglas CSS inactivas han recibido muchos comentarios positivos. Te ayudan a resolver los intrincados problemas de CSS a la vez que te enseñan las complejas interdependencias de las reglas de las hojas de estilo en cascada.

Desde su lanzamiento, no hemos dejado de ajustar y añadir reglas, a menudo basadas en los comentarios de los usuarios. En la versión 74 podemos destacar una nueva configuración de detección que te advierte cuando las propiedades dependen de elementos posicionados, principalmente [ z-index](https://developer.mozilla.org/docs/Web/CSS/z-index),

[,](https://developer.mozilla.org/docs/Web/CSS/top)

`top`

[,](https://developer.mozilla.org/docs/Web/CSS/left)

`left`

[, y](https://developer.mozilla.org/docs/Web/CSS/bottom)

`bottom`

[.](https://developer.mozilla.org/docs/Web/CSS/right)

`right`

![Firefox Page Inspector now showing inactive position-related properties such as z-index and top](../../assets/5744426e48f2a528.png)

Tus comentarios y opiniones serán útiles para refinar y expandir las reglas. Saluda al equipo en [el chat DevTools](https://chat.mozilla.org/#/room/#devtools:mozilla.org) en [la instancia Matrix de Mozilla](https://wiki.mozilla.org/Matrix) o sigue nuestro trabajo a través de [@FirefoxDevTools](https://twitter.com/FirefoxDevTools).

### Depuración para trabajadores anidados

El equipo del [depurador de JavaScript](https://developer.mozilla.org/docs/Tools/Debugger) de Firefox se ha centrado en la optimización de los [Web Workers](https://developer.mozilla.org/docs/Web/API/Web_Workers_API/Using_web_workers) en las últimas versiones para una mayor facilidad de inspección y depuración. Cuanto más desarrolladores y marcos de trabajo utilicen los trabajadores para alejar el procesamiento del hilo principal, más fácil será para los navegadores priorizar el código en ejecución, que se dispara como resultado de las acciones de los usuarios.

Ahora se muestran en el Depurador los trabajadores web anidados, que permiten a los trabajadores generar y controlar sus propias instancias de trabajo:

![El depurador de JavaScript de Firefox ahora muestra los trabajadores anidados](../../assets/3b6dccb9bd207706.png)


### Integración mejorada de las React DevTools

El [complemento de herramientas para desarrolladores de React](https://addons.mozilla.org/firefox/addon/react-devtools/) es uno de muchos [complementos para desarrolladores](https://addons.mozilla.org/firefox/collections/4757633/webdeveloper/) que se integran estrechamente con las herramientas para desarrolladores de Firefox. Gracias a las [API de WebExtensions](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions), los desarrolladores pueden generar y publicar complementos para todos los navegadores de la misma base de código.

En [colaboración](https://github.com/facebook/react/issues/17681) con los encargados de mantener los complementos de React, trabajamos para rehabilitar y mejorar los menús contextuales de los complementos, incluido *Ir a definición*. Esta acción permite que los desarrolladores salten de los componentes de React directamente a sus archivos de origen en el Depurador. Ya se habilitó la misma función para saltar a los elementos en el Inspector. Queremos desarrollar esto aún más, para que [los flujos del framework](https://addons.mozilla.org/firefox/collections/4757633/webdeveloper/) estén perfectamente alineados con el resto de las herramientas.

### Acceso temprano a las funciones para desarrolladores en Developer Edition

[Developer Edition](https://www.mozilla.org/es-ES/firefox/developer/) es el canal de prelanzamiento de Firefox que permite el acceso anticipado a las herramientas y funciones de la plataforma. Su configuración también permite mayor funcionalidad de forma predeterminada para los desarrolladores. Queremos llevar pronto las nuevas funciones a la Developer Edition para recopilar tus comentarios, incluidos los siguientes puntos destacados.

#### Evaluación inmediata para las expresiones de consola

Parece magia explorar los objetos y funciones de JavaScript y el DOM con la evaluación inmediata. Siempre y cuando las expresiones tecleadas en la [Consola Web](https://developer.mozilla.org/docs/Tools/Web_Console) no presenten efectos secundarios, sus resultados se previsualizan mientras escribes, lo que te permite identificar y corregir los errores más rápido que antes.

#### Trazas de pila asíncronas para el depurador y la consola

La programación moderna en JavaScript depende en gran medida del apilamiento de [ async/await](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function), además de otras


[operaciones asíncronas](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous)como

[eventos](https://developer.mozilla.org/docs/Learn/JavaScript/Building_blocks/Events),

[promesas](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous/Promises)y

[tiempos de espera](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous/Timeouts_and_intervals). Gracias a una mejor integración con el motor de JavaScript, ahora se captura la ejecución asíncrona para ofrecer una imagen más completa.

Las pilas de llamadas asíncronas en el depurador te permiten recorrer los eventos, los tiempos de espera y las llamadas de funciones basadas en promesas que se ejecutan a lo largo del tiempo. En la consola, las pilas asíncronas facilitan la localización de la causa raíz de los errores.

![pila de llamadas asíncronas vista en el depurador de JavaScript de Firefox](../../assets/c5e2b14cc98d1326.png)


#### Un vistazo a la depuración de trabajadores de servicio

Hace tiempo que existe en Nightly y estamos más que entusiasmados por ponerlo en tus manos pronto. Espérala en Firefox 76, que se convertirá en la [Developer Edition](https://www.mozilla.org/es-ES/firefox/developer/) en 4 semanas.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.