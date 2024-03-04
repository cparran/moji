# MOJI
MOJI es un ambicioso proyecto dedicado a facilitar la experiencia de lectura de mangas japoneses para hablantes de español. Basado en técnicas avanzadas de aprendizaje profundo (Deep Learning), MOJI aborda dos desafíos clave: el reconocimiento óptico de caracteres (OCR) para extraer texto de páginas de manga y la traducción precisa de ese texto al español. Con un enfoque principalmente supervisado, el proyecto utiliza modelos de entrenamiento, como Redes Neuronales Convolucionales (CNN) para OCR y Redes Neuronales Recurrentes (RNN) o modelos Transformer para la traducción.

# Componentes Claves

Entrada (X): MOJI comienza con imágenes de páginas de manga como entrada. Estas imágenes se someten a un proceso de segmentación para identificar y aislar bloques de texto (text bubbles y text-free), transformando efectivamente el problema en uno de procesamiento de texto.

Salida (Y): Para el OCR, la salida se conceptualiza como clases, donde cada clase representa un carácter o conjunto de caracteres reconocidos. En la etapa de traducción, la salida es el texto traducido al español, representado por secuencias de texto.

Aprendizaje Automático (ML): MOJI adopta un enfoque de aprendizaje profundo, utilizando CNN para el reconocimiento de texto en imágenes, dada su eficacia en tareas de visión por computadora. Para la traducción de texto, se consideran modelos como RNN o Transformer, aprovechando la atención y la capacidad de manejar secuencias de texto complejas.

# Desarrollo del Proyecto

Entrenamiento del Modelo: La fase inicial implica el entrenamiento de modelos, especialmente en OCR, donde se requiere una cantidad significativa de datos etiquetados para reconocer con precisión caracteres en imágenes.

Exploración y Visualización: Aunque la exploración y visualización no son el enfoque principal, se pueden realizar análisis iniciales para comprender mejor los datos de manga, optimizando así la eficiencia del proceso.

Implementación de Traducción: Una vez extraído el texto mediante OCR, MOJI emplea técnicas avanzadas de traducción utilizando modelos de aprendizaje profundo, permitiendo una experiencia de lectura fluida y comprensible para los usuarios de habla hispana.

MOJI, como proyecto pionero en la convergencia de tecnologías de OCR y traducción automática, tiene el potencial de transformar la accesibilidad y disfrute de los mangas japoneses para una audiencia más amplia.
