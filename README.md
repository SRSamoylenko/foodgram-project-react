# API онлайн-каталога YaMDb
Приложение "Продуктовый помощник". Пользователи могут регистрироваться, создавать свои рецепты, подписываться на публикации других пользователей, добавлять рецепты в избранное, формировать корзину покупок и скачивать ее.

## Стек технологий
Backend: python3, Django Rest Framework, django-filter, Djoser, Docker, postgres, Pillow
Frontend: JavaScript, React

ВНИМАНИЕ! На данный момент frontend и backend приложения функционируют отдельно.

## Для запуска frontend приложения:
1. Проверьте установлен ли Docker.
2. Клонируйте репозиторий.
3. В папке `infra` выполните команду:
    ```
    docker-compose up -d --build
    ```
4. Проект запустится по адресу `http://localhost`, посмотреть спецификацию API сможете по адресу: `http://localhost/api/docs/`

## Для запуска backend приложения:
1. Перейдите в папку `backend`
2. Создайте и запустите виртуальное окружение:
   ```
   python3 -m venv venv
   . venv/bin/activate
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Coздайте файл `.env` по примеру `.env.example`
4. Перейдите в папку `foodgram` внутри `backend`
5. Запустите проект:
   ```
   python manage.py runserver
   ```
6. Приложение доступно по адресу: `http://127.0.0.1/`.
   
### Опционально:
1. Для доступа к админ панели API создайте суперпользователя:
    ```
    python manage.py createsuperuser
    ```
2. Можете загрузить в бд предзаготовленный список ингредиентов:
    ```
    python manage.py loaddata ../../data/ingredients.json
    ```
