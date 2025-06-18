# Magister Quiz

Magister Quiz es un módulo para Odoo que extiende la funcionalidad del módulo de encuestas "survey" para ofrecer características similares a Kahoot!, incluyendo puntuación basada en tiempo, preguntas condicionales, rankings por sesión y más.

## Características principales

### 1. **Puntuación basada en tiempo**
- Las preguntas pueden configurarse con un límite de tiempo.
- La puntuación se calcula en función del tiempo de respuestas.
- Fórmula ajustada para evitar puntuaciones negativas y premiar respuestas rápidas.

### 2. **Preguntas condicionales**
- Las respuestas pueden redirigir a preguntas específicas, saltándose otras preguntas intermedias.

### 3. **Tipos de preguntas**
- Se agrega el tipo de pregunta "True or False" con lógica personalizada.
- Las respuestas correctas se generan automáticamente al crear una pregunta de este tipo.

### 4. **Ranking por sesión**
- Se calcula la puntuación total de cada usuario al finalizar la encuesta.
- Se genera un ranking por sesión que muestra las mejores puntuaciones.

### 5. **Temporizador visual**
- Temporizador en tiempo real para cada pregunta.
- Se muestra en la interfaz del usuario y se actualiza dinámicamente.
- Si finaliza el tiempo, se dejará la pregunta sin conststar y se pasa a la siguiente.

### 6. **Explicaciones después de cada pregunta**
- Se pueden agregar explicaciones breves que se muestran después de responder cada pregunta.
- Ayuda a los usuarios a entender las respuestas correctas.

### 7. **Estilo personalizado**
- Diseño visual inspirado en Kahoot! con colores vibrantes.
- Fuentes personalizadas para dar una experiencia más única.

## Instalación

1. Primero debemos clonar este repositorio en tu instancia de Odoo, una vez situados en nuestra carpeta (ej. /home/usuario/odoo/mis_modulos):
    - git clone https://github.com/alvarofuentes1/kahoot_odoo
2. Ahora nos colocamos en nuestra carpeta con en codigo fuente de odoo y ejecutamos el siguiente comando:
    - ./odoo-bin -u mi_modulo -d nombre_base_datos --addons-path=/home/usuario/odoo/mis_modulos
    - Es importante añadir la ruta exacta en la sección de --addons-path
3. Una vez hecho esto, nuestro modulo debería estar disponible en la sección de apps de Odoo.