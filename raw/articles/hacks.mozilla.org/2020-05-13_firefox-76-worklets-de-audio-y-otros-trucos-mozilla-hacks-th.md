---
title: 'Firefox 76: Worklets de audio y otros trucos – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2020/05/firefox-76-worklets-de-audio-y-otros-trucos-2/
author: Chris Mills
published: '2020-05-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Hola amigos, espero que todos estén bien y se mantengan sanos y salvos.

Cada nueva versión de nuestro navegador favorito viene siempre con una buena pizca de expectación, ¡y ya estamos aquí con Firefox 76! El soporte de la plataforma web recibe algunas excelentes novedades en esta actualización, como los [worklets de audio](https://developer.mozilla.org/docs/Web/API/AudioWorklet) y ciertas [mejoras Intl](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl) del lado de JavaScript.

Además, hemos añadido varias funcionalidades estupendas en las herramientas de desarrollador a fin de conseguir que programar con ayuda de Firefox sea más fácil y rápido.

Como siempre, siga leyendo para conocer los aspectos más destacados o consulte la lista completa de adiciones en los siguientes artículos:

[Firefox 76 para desarrolladores](https://developer.mozilla.org/docs/Mozilla/Firefox/Releases/76)[Compatibilidad de sitios web para Firefox 76](https://www.fxsitecompat.com/en-CA/versions/76/)[Notas de la versión de usuario final de Firefox 76](https://www.mozilla.org/en-US/firefox/76.0/releasenotes/)

## Adiciones de herramientas para desarrolladores

En esta versión, encontramos interesantes actualizaciones en todos los paneles de las herramientas para desarrolladores.

Además, las próximas funcionalidades ya se pueden previsualizar en [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/).

### Más trucos de productividad de JavaScript

La depuración de JavaScript en Firefox es aún mejor.

#### Ignorar carpetas completas en el depurador

A menudo, los esfuerzos a la hora de depurar solo se centran en un determinado conjunto de archivos muy específico, donde probablemente se encuentre el culpable.

Al *blackboxing*, podemos decirle al [depurador](https://developer.mozilla.org/docs/Tools/Debugger) que ignore aquellos ficheros que no necesitamos depurar.

Ahora es más fácil hacer esto con carpetas enteras gracias al nuevo menú contextual de [Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974) en el panel de fuentes del depurador.

Se puede escoger entre limitar la función de ignorar a los archivos de dentro o de fuera de la carpeta seleccionada.

Ahora, además, se puede combinar esta característica con “Establecer raíz de directorio” para una experiencia de depuración tan precisa como un cirujano.

#### Salida contraída para grandes fragmentos de consola

El [modo de editor multilínea](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode) de la [consola](https://developer.mozilla.org/docs/Tools/Web_Console) es ideal para trabajar con fragmentos de código más largos.

Los primeros comentarios señalaban que los usuarios no querían que se repitiera el código en la salida de la consola, a fin de evitar la sobrecarga de información.

Gracias a la contribución de [thelehhman](https://github.com/thelehhman), los fragmentos de código de múltiples líneas se colapsan limpiamente y se pueden expandir a voluntad.

#### Copiar las URL completas en la pila de llamadas

Copiar las pilas en el depurador posibilita compartir instantáneas durante cada paso, permitiendo localizar mejor los errores y facilitar la tarea de los compañeros.

Para proporcionar a los colaboradores el contexto completo de un error, el menú “Copiar seguimiento de la pila” del [panel de la pila de llamadas](https://developer.mozilla.org/docs/Tools/Debugger/UI_Tour#Call_stack) ahora copia las URL completas, no solo los nombres de archivo.

#### Siempre aparece “Expandir todo” en la vista previa de JSON de Firefox

Las vistas previas integradas para archivos JSON facilitan la búsqueda de respuestas y la exploración de extremos de API.

Esta función también da buenos resultados con archivos grandes, para los que se pueden expandir los datos según sea necesario.

Gracias a una contribución de [zacnomore](https://github.com/zacnomore), la opción “Expandir todo” ahora está siempre visible.

### Más trucos de inspección de red

Firefox 76 proporciona un acceso aún más fácil a la información de la red a través del [Monitor de red](https://developer.mozilla.org/docs/Tools/Network_Monitor).

#### Soporte de Action Cables en la inspección de WebSockets

Las bibliotecas de WebSocket usan múltiples formatos diferentes para codificar sus mensajes.

Queremos asegurarnos de que sus cargas se formateen correctamente para que pueda leerlas.

En versiones anteriores, añadimos compatibilidad con la [inspección de mensajes de WebSocket](https://developer.mozilla.org/docs/Tools/Network_Monitor/Inspecting_web_sockets) para Socket.IO, SignalR y WAMP.

Gracias a la colaboración de [Uday Mewada](https://bugzilla.mozilla.org/show_bug.cgi?id=1590046), los mensajes de Action Cable ahora también se muestran correctamente formateados.

#### Ocultar marcos de control de WebSocket

Los servidores y los navegadores utilizan los marcos de control de WebSocket para gestionar conexiones en tiempo real, aunque no contengan ningún dato.

La contribución de [kishlaya.j](https://bugzilla.mozilla.org/show_bug.cgi?id=1566780) posibilita ocultar los marcos de control de forma predeterminada, permitiéndonos depurar con un poco menos de ruido.

Quien necesite verlos puede habilitarlos en el menú desplegable de enviados/recibidos.

#### Cambiar el tamaño de las columnas de la tabla de red para ajustarse al contenido

Cuando se trabaja con el panel de red, podemos enfrentarnos a una cantidad inmensa de información sobre solicitudes y respuestas conforme se examinan las actualizaciones en tiempo real para centrarse en puntos de datos concretos.

Personalizar las columnas visibles del panel de red permite adaptar la salida al problema en cuestión.

En el pasado, exigía arrastrar y redimensionar un montón de veces.

Ahora, gracias a [Farooq AR](https://twitter.com/Farooq_AR), se puede simplemente hacer doble clic en los controles de cambio de tamaño de la tabla para escalar el ancho de una columna a fin de que esta se ajuste a su contenido, como en las tablas de datos modernas.

#### Mejoras en detalles y copiado de respuestas de red

Nos han comentado que debería ser más fácil copiar partes de los datos de la red para su análisis posterior.

Por ello, se ha modernizado la sección “Respuesta” de los detalles de la red para facilitar la inspección y la copia, haciendo que estas operaciones sean más rápidas y fiables.

Seguiremos añadiendo más mejoras para facilitar el uso del análisis de red próximamente, [gracias a vuestro apoyo](https://twitter.com/FirefoxDevTools/status/1255209764541263872).

### Contribuciones de la comunidad

[Laurențiu Nicola](https://bugzilla.mozilla.org/show_bug.cgi?id=1549773)arregló el menú de solicitud de red[“Copiar como cURL”](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_list#Copy_as_cURL)y lo hizo más fiable al agregar`--globoff`

al comando generado.[Patricia Lee](https://bugzilla.mozilla.org/show_bug.cgi?id=1612276)añadió la opción “Revelar en el inspector” del menú contextual de la consola como otra forma de saltar de los elementos DOM registrados a su posición en el árbol.[sankalp.sans](https://bugzilla.mozilla.org/show_bug.cgi?id=1424863)mejoró el formato copiado en[el panel “Cambios” del inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes).Ahora, “Copiar reglas CSS” inserta líneas vacías entre ellas, para que puedan reutilizarse más fácilmente en los editores.

[Basavaraj](https://bugzilla.mozilla.org/show_bug.cgi?id=1574456)solucionó un problema que hacía que no se mostraran los[parámetros de consulta de red](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_details#Params)que contenían “+”.[Aarushivij](https://bugzilla.mozilla.org/show_bug.cgi?id=1339558)arregló el renderizado del[análisis de rendimiento de la red](https://developer.mozilla.org/docs/Tools/Network_Monitor/Performance_Analysis)para que responda mejor a tamaños más pequeños.

### Novedades de la Developer Edition: Panel de compatibilidad de CSS

[Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) es el canal de prelanzamiento de Firefox, que proporciona acceso temprano a las nuevas herramientas y funcionalidades de la plataforma.

Su configuración también facilita más características para los desarrolladores de forma predeterminada.

Nos complace poder llevar nuevas funcionalidades rápidamente a Developer Edition para poder conocer sus comentarios, como los de los siguientes aspectos destacados.

Ante todo, en el lanzamiento de la Developer Edition 77 estamos recabando opiniones acerca de nuestro nuevo panel de compatibilidad.

Este panel informará sobre cualquier propiedad CSS que pueda no ser compatible con otros navegadores, y será accesible desde el inspector.

Invitamos a todo el mundo a probarla y utilizar el enlace provisto “Comentarios” para indicar qué les parece y cómo podemos mejorarlo aún más.![El panel de compatibilidad indica dos problemas para el elemento actual](../../assets/907569e9d14a3af9.png)


## Actualizaciones de la plataforma web

Vamos a analizar qué nos trae Firefox 77 en términos de actualizaciones de la plataforma web.

### Worklets de audio

Los worklets de audio ofrecen una forma útil de ejecutar código de procesamiento de audio JavaScript personalizado.

¿En qué se diferencian los worklets de audio de su predecesor, [ ScriptProcessorNode](https://developer.mozilla.org/docs/Web/API/ScriptProcessorNode)? Los worklets se ejecutan en el subproceso principal de forma similar a otros web workers, resolviendo los problemas de rendimiento que podíamos sufrir anteriormente.

La idea básica es esta: se define un [ AudioWorkletProcessor](https://developer.mozilla.org/docs/Web/API/AudioWorkletProcessor) personalizado que se encargará del procesamiento.

Luego, se registra.

`// white-noise-processor.js class WhiteNoiseProcessor extends AudioWorkletProcessor { process (inputs, outputs, parameters) { const output = outputs[0] output.forEach(channel => { for (let i = 0; i < channel.length; i++) { channel[i] = Math.random() * 2 - 1 } }) return true } } registerProcessor('white-noise-processor', WhiteNoiseProcessor)`


En el script principal, cargamos el procesador, creamos una instancia de [ AudioWorkletNode](https://developer.mozilla.org/docs/Web/API/AudioWorkletNode) y le pasamos el nombre del procesador.

Finalmente, conectamos el nodo a un gráfico de audio.

`async function createAudioProcessor() { const audioContext = new AudioContext() await audioContext.audioWorklet.addModule('white-noise-processor.js') const whiteNoiseNode = new AudioWorkletNode(audioContext, 'white-noise-processor') whiteNoiseNode.connect(audioContext.destination) }`


Hay más información en nuestra guía de [procesamiento de audio de fondo usando AudioWorklet](https://developer.mozilla.org/docs/Web/API/Web_Audio_API/Using_AudioWorklet).

### Otras actualizaciones

Además de los worklets, hemos añadido algunas otras características para la plataforma web.

`<input>`

HTML

Los atributos de los elementos `<input>`

[ min](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-min) y

[de HTML ahora funcionan correctamente cuando el valor de](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-max)

`max`

`min`

es mayor que el valor de `max`

, para aquellos tipos de control cuyos valores son periódicos (los valores periódicos se repiten a intervalos regulares y se pasan desde el final hasta el inicio de nuevo).Esto resulta particularmente útil con las entradas `date`

y `time`

, donde es posible que se especifique un rango de tiempo de 11 P.M. a 2 A.M, por ejemplo.

#### Mejoras en `Intl`


Las opciones `numberingSystem`

y `calendar`

de los constructores [ Intl.NumberFormat](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat),

[y](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

`Intl.DateTimeFormat`

[ahora están habilitadas por defecto.](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat)

`Intl.RelativeTimeFormat`

Prueben estos ejemplos:

`const number = 123456.789; console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'latn' }).format(number)); console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'arab' }).format(number)); console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'thai' }).format(number)); var date = Date.now(); console.log(new Intl.DateTimeFormat('th', { calendar: 'buddhist' }).format(date)); console.log(new Intl.DateTimeFormat('th', { calendar: 'gregory' }).format(date)); console.log(new Intl.DateTimeFormat('th', { calendar: 'chinese' }).format(date));`


#### Observador de intersección

El constructor [ IntersectionObserver()](https://developer.mozilla.org/docs/Web/API/IntersectionObserver/IntersectionObserver) ahora acepta como raíz a objetos

[y](https://developer.mozilla.org/docs/Web/API/Document)

`Document`

[.](https://developer.mozilla.org/docs/Web/API/Element)

`Element`

En este contexto, la raíz es el área cuyo cuadro delimitador se considera la vista para fines de observación.

## Extensiones del navegador

[Firefox Profiler](https://profiler.firefox.com/) es una herramienta para ayudar a analizar y mejorar el rendimiento de su sitio web en Firefox.

Ahora mostrará marcadores cuando se suspendan solicitudes de red a causa de los [controladores bloqueantes](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/BlockingResponse) de [ webRequest](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/BlockingResponse).

Esto es especialmente útil para los desarrolladores de extensiones de bloqueadores de contenido, ya que les permite garantizar que Firefox rinda a la máxima velocidad.

Aquí hay una captura de pantalla de Firefox Profiler en acción: ![IU de la extensión Firefox Profiler](../../assets/9d5e920fb9762921.png)


## Resumen

Y eso es todo para la última edición de Firefox.

¡Esperamos que disfrute de las nuevas funcionalidades! Como siempre, siéntase libre de dar sus opiniones y formular sus preguntas en los comentarios.

FIN Extracto: Firefox 76 recibe algunas excelentes novedades para favorecer el soporte de plataforma web, como los worklets de audio e Intl, en lo que respecta a JavaScript.

Además, hemos incluido una serie de mejoras de primer nivel a las herramientas de desarrollador de Firefox para conseguir que la depuración y el desarrollo de JavaScript sean más fáciles y rápidos.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.