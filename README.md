# Веб-приложение на Python с использованием FastAPI
## Стек технологий
1. python == 3.9
2. fastapi == 0.111.0
3. uvicorn == 0.30.1
4. starlette == 0.37.2
5. uvicorn == 0.30.1
6. sqlalchemy == 2.0.31
7. pydantic == 2.8.2
8. FastAPI-SQLAlchemy  == 0.2.1
9. python-dotenv == 1.0.1
10. pytest == 8.2.2
11. psycopg2 == 2.9.9
12. alembic == 1.13.2
13. python-multipart == 0.0.12
14. httpx == 0.27.2
15. psycopg2-binary == 2.9.10
16. passlib == 1.7.4
17. pika == 1.3.2
18. python-jose == 3.3.0
19. bcrypt == 4.2.0
20. image == 1.5.33
21. replit == 4.1.0
## Функционал
1. GET/image: Получить список информации всех изображений
2. GET/image/{id}: Получить информацию о конкретном товаре по его id
3. POST/image: Добавить новое изображение
4. PUT/image/{id}: Обновить существующее изображение
5. DELETE/image/{id}: Удалить изображение
## Запуск
1. Склонировать репозиторий
2. Создать базу данных в PostgreSQL
```env
CREATE DATABASE {db_name};
```
3. Создать .env в папке src и записать следующие данные в нее
```env
DB_HOST = "host.docker.internal"
DB_PORT = "5432"
DB_NAME = {name}
DB_USER = {user}
DB_PASS = {pass}

ALGORITHM = {algotithm}
JWT_SECRET_KEY = {key}
JWT_REFRESH_SECRET_KEY = {key}

HOST = "host.docker.internal"
USERNAME = {user}
PASSWORD = {pass}
```
4. Создать и запустить Docker 
```env
docker-compose up --build
```
5. Перейти по URL к Swagger: http://localhost:8000/docs
6. Перейти по URL к RabbitMQ: http://localhost:15672.
7. Для запуска unit-тестов необходимо выполнить следующие
команды.
```env
 docker-compose exec pytest bash
 pytest
```