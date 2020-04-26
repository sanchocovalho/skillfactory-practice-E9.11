# Задание E9.11

   Сервис для планирования событий

   ТехЗадание:
1) Сервис должен поддерживать работу нескольких пользователей. Пользователи должны создавать событие, которое доступно остальным пользователям.
2) У каждого события есть следующие параметры: автор, время начала, время конца, тема и описание.
3) Каждый пользователь может просматривать все события, которые созданы любыми пользователями.
4) Каждый пользователь может редактировать, удалять и создавать события, где пользователем является он
5) Должна быть реализована страница, на которой есть общий вид всех событий.
6) Данное задание мы будем деплоить на heroku. Чтобы это сделать, нужно установить Heroku CLI, с ее помощью можно будет синхронизировать heroku с git-репозиторием и настроить деплой.

Критерии оценки задания:
   - ссылка на github с кодом приложения на Python с использованием Flask в качестве фреймворка и PostgreSQL в качестве базы данных и ссылка на heroku с задеплоенным приложением;
   - в репозитории есть README.md, в котором написано, как стартовать и как протестировать задеплоенное на heroku приложение;
   - приложение позволяет нескольким пользователям залогиниться;
   - для залогиненного пользователя доступна форма, на которой видны все существующие события;
   - для залогиненного пользователя доступна форма, которая позволяет добавить событие. У события должны быть следующие параметры: автор, время начала, время конца, тема и описание;
   - для залогиненного пользователя доступна форма, которая позволяет редактировать и удалять свои события.

Для того, чтобы запустить сервис необходимо:
1) Распакуйте проект в папку и через терминал зайдите в директорию проекта
2) Создате виртуальное окружение:
   - python -m venv flask
3) Активируйте виртуальное окружение:
   - flask\Scripts\activate.bat
4) Установите все необходимые пакеты:
   - pip install -r requirements.txt
5) Запустите локальный сервер:
   - python manage.py runserver
6) Также можно воспользоваться следующими командами:
   - python manage.py db migrate --> создать миграции
   - python manage.py db upgrade --> применить миграции
   - python manage.py createsuperuser --> создать суперпользователя (администратора)

Для того, чтобы сделать деплой на heroku необходимо:
1) Через терминал зайдите в директорию проекта:
2) Выполнить следующий команды:
   - git init
   - git add .
   - git commit -m "initial commit
   - heroku login
   - heroku create
   - heroku rename -a oldname newname (переименовываем приложение, если необходимо)
   - heroku addons:create heroku-postgresql --as DATABASE
   - heroku config:set SECRET_KEY=Ваш_секретный_код
   - git push heroku master
   - heroku run python manage.py db migrate
   - heroku run python manage.py db upgrade
   - heroku run python manage.py createsuperuser
3) Запускаем приложение:
   - heroku open

Данный проект находится на https://eventplanservice-skillfactory.herokuapp.com/

