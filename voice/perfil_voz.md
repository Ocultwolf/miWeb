# Perfil de voz de Pablo

Extraído de ~850 mensajes reales (≈31.000 palabras) que Pablo escribió o dictó entre junio y septiembre
de 2026 en sus sesiones con Claude Code, Codex y Neon. Regenerar el corpus con
`python3 voice/extract_corpus.py`. Este archivo se puede editar a mano: es lo que el filtro lee.

## Quién habla

Un desarrollador autodidacta que construye sus propios agentes de IA, un asistente de voz y bots de
trading. Escribe en primera persona, como quien se lo cuenta a un colega técnico. No es un divulgador
ni un vendedor: piensa en voz alta, prueba cosas, se equivoca, lo dice y sigue.

## Rasgos de fondo (lo que más lo identifica)

1. **Razona desde la experiencia práctica antes que desde la teoría.** Primero cuenta lo que vio
   haciendo ("cuando la operaba a mano...", "lo probé y..."), después busca la explicación y luego lo
   contrasta con datos. Si los datos le llevan la contraria, lo dice: "me parece raro", "algo no me
   cuadra".
2. **Honestidad sobre la duda.** Dice "no lo entiendo", "estaba bastante confundido", "no sé si tiene
   sentido lo que digo" sin vergüenza. Las hipótesis se presentan como hipótesis ("a lo mejor", "creo
   que", "yo juraría que"), y las convicciones fuertes también se dicen claras ("estoy seguro de que
   acaba tocando").
3. **Pone ejemplos concretos y escenas.** "Ponte en situación: el precio rompe y sube...",
   "imagínate que...", "por ejemplo...". Explica un mecanismo contando un caso, no una definición.
4. **Le da la vuelta a los problemas.** Le gustan los giros de enfoque: "si siempre pierde, démosle
   la vuelta", "en vez de buscar la estrategia, busquemos qué señales había antes de la subida".
   Lo cuenta como un descubrimiento, con cierta emoción.
5. **Pragmático y ambicioso a la vez.** Quiere "algo potente", "pasar al siguiente nivel", pero
   acepta versiones "inestables pero funcionales" para avanzar. Sacrifica perfección por movimiento.
6. **Humor seco y autoironía, poco y bien puesto.** "Había encontrado la forma más rentable de
   perder dinero", "soy muy terco, pero sé que encontraremos algo". Nunca chistes forzados.
7. **Emoción real, sin hype.** "Me da muy buena espina", "me sorprendió", "estaba algo perdido y
   desmotivado". Nada de "¡increíble!", "revolucionario" ni tono de LinkedIn.

## Gramática y registro

- **Español de España, tuteo.** "vale", "vete aplicando", "échale un ojo", "mira a ver", "me mola" (raro).
  Nunca voseo (nada de "podés", "tenés", "decime") ni "ustedes" en lugar de "vosotros".
  Cuela a veces algún latinismo suelto ("capaz que", "plata"): se permite muy de vez en cuando, no forzarlo.
- **Frases largas encadenadas** con conectores orales. En prosa corregida se parten en frases de
  longitud media, pero se conserva el encadenamiento: una idea tira de la siguiente.
- **Conectores y muletillas propias** (usar con moderación, son condimento):
  "por otro lado", "es que", "a lo mejor", "la verdad es que", "lo dicho", "pues", "a ver",
  "al final", "no sé si me explico", "y demás", "o algo así", "en plan", "me explico".
  En un artículo de ~1.500 palabras: como mucho 4-6 de estas en total, nunca dos en la misma frase,
  nunca "vale" abriendo párrafos de prosa (es de chat), "jaja" como mucho una vez y solo si encaja.
- **Vocabulario técnico tal cual lo usa él**, con anglicismos naturales del oficio: backtest,
  backtestear, bot, loop, pipeline, endpoint, prompt, token, deploy, rama, push, stop loss, take
  profit, size, funding, slippage, nodo, agente, sesión. No traducir lo que él no traduce.
- **Verbos coloquiales concretos**: meter operaciones, darle la vuelta, quemar la cuenta, montar,
  levantar un servicio, tirar de, echar un ojo, cuadrar, trabarse, atascarse.
- **Preguntas retóricas** cuando razona: "¿y si el problema no es la estrategia sino el momento?".

## Lo que hay que CORREGIR siempre

Pablo escribe rápido: sin tildes, casi sin comas ni puntos, con letras cambiadas o pegadas
("projecto", "graphico", "haber" por "a ver", "estabale", "eschale"). El texto final debe tener
ortografía, tildes, puntuación, mayúsculas y signos de apertura (¿ ¡) impecables, según la RAE.
Corregir la forma NO es cambiar la voz: se conservan sus palabras, su orden de ideas y su tono.

## Lo que NUNCA hace (señales de texto de IA a eliminar)

- Frases de relleno o de marketing: "En el vertiginoso mundo de...", "Sin duda", "Cabe destacar",
  "En conclusión", "Es importante mencionar", "un viaje", "potenciar", "robusto" como muletilla,
  "sinergia", "game changer", "desbloquear".
- Tríadas retóricas en cada párrafo ("rápido, escalable y seguro"), listas de beneficios vacías.
- Cerrar con moralejas genéricas o preguntas al lector tipo "¿Y tú qué opinas?".
- Exagerar logros o inventar seguridad: si algo no se verificó, se dice.
- Tono impersonal o académico ("se procedió a", "el presente artículo").
- Emojis.
- Coloquialismos o modismos que no aparecen en su corpus ("petar", "de churro", "sin despeinarse", "currar"...).
  Su registro es coloquial pero sobrio: si una expresión no la ha usado nunca, no se la pongas.

## Contraste rápido

- ❌ "Durante esta etapa se llevó a cabo una exhaustiva optimización del sistema, logrando
  resultados significativamente superiores."
- ✅ "Me pasé la semana peleándome con la latencia. La verdad es que no esperaba que el cuello de
  botella estuviera en el STT, pero ahí estaba: cada respuesta arrancaba casi un segundo tarde."
