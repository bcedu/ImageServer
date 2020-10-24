# ImageServer
Servidor de imatges amb flask amb la possibilitat de obtenir imatges aleatories segons tags

## Crides disponibles

- `/image/<string:id>`: obtenir imatge per ID
- `/random_image`: obtenir imatge aleatoria
- `/random_image/<string:tag>`: obtenir imatge aleatoria que contingui el tag especificat
