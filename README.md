[![foodgram workflow](https://github.com/SRSamoylenko/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/SRSamoylenko/foodgram-project-react/actions/workflows/main.yml)
# Приложение "Продуктовый помощник"
Пользователи могут регистрироваться, создавать свои рецепты, подписываться на публикации других пользователей, добавлять рецепты в избранное, формировать корзину покупок и скачивать ее.

Приложение доступно по адресу: http://foodgram.sytes.net/

API приложения - http://foodgram.sytes.net/api

Документация API - http://foodgram.sytes.net/api/docs/redoc.html

Для доступа к админ-панели:
- email: `admin@admin.com`
- пароль: `admin`

## Стек технологий
Backend: python3, Django Rest Framework, django-filter, Djoser, Docker, postgres, Pillow
Frontend: JavaScript, React
CI/CD: docker-compose + GitHub Actions


## Для запуска у себя на сервере:
1. Сделайте форк и склонируйте репозиторий
2. Скопируйте на сервер файлы `docker-compose.yml` и `nginx.conf` и папки `frontend` и `docs`.
3. В GitHub установите секреты репозитория по аналогии с файлом `.env.example`
4. В файле `nginx.conf` установите `server_name`
4. Перейдите в папку `foodgram` внутри `backend`
5. Сделайте push в репозиторий
   
### Опционально:
1. Откройте консоль web-приложения, для этого на сервере введите команду:
   ```
   docker exec -it <название контейнера> bash
   ```
2. Для доступа к админ панели приложения создайте суперпользователя:
    ```
    python manage.py createsuperuser
    ```
   и следуйте командам.
   
   Админ панель доступна по адресу: `<имя хоста>/admin`
   
2. Можете загрузить в бд предзаготовленный список ингредиентов:
    ```
    python manage.py loaddata ../../data/ingredients.json
    ```
