### Flask orders (test)

---
###### Flask, SQLAlchemy, PostgreSQL, Docker Compose

*Приложение отображает таблицу заказов и пользователей.
База данных реализована в виде Docker контейнера запускаемого через **docker-compose**.*

*Т.к. не удалось найти DB seeder работающий не из файла, реализована страница генерирующая тестовые данные для заполнения БД с использованием библиотеки **Faker**. По умолчанию генерируются 100 пользователей и 5000 заявок связанных с ними. Есть возможность удаления всех данных. При повторной генерации данных сохраняется инкрементация **id** если не удалён контейнер с базой данных.*

* установить docker & docker-compose
[_docker-compose documentation_](https://docs.docker.com/compose/)
* создать виртуальное окружение выполнив команду `pip -m venv .venv` ([*pip*](https://pypi.org/project/pip/) должен быть установлен в Вашу систему)
* активировать окружение `source .venv/bin/activate`
* из директории содержащей файл docker-compose.yaml выполнить команду `docker-compose up`. При необходимости изменить переменные: _user, password, port_ в *docker-compose.yaml*
* через оболочку Flask `flask shell` импортировать экземпляр БД и запустить процес создания таблиц: `from app.extensions import db`
`db.create_all()`
* запустить приложение `flask --app app run [--debug | --no-debug]`. Приложение запустится на 5000 порту, убедитесь, что он не занят.
* перейти на [страницу генерации данных](http://127.0.0.1:5000/sending_data/), выбрать *Yes*
* на [странице заказов](http://127.0.0.1:5000/payments/orders) будет отображены сгенерированные данные.
* по клику на **id** заказа или **id** пользователя отображается информация о них на новой странице

- [x] Создайте базу данных
- [x] Используйте DB seeder
- [x] Используйте Twitter Bootstrap для создания базовых стилей Вашей страницы.
- [x] Создайте еще одну страницу и выведите на ней список реквизитов
- [ ] Добавьте возможность поиска реквизитов по любому полю
- [ ] Добавьте возможность сортировать
- [ ] Используя стандартные функции Flask, осуществите аутентификацию
- [ ] Реализуйте с помощью FlaskAPI/Django REST framework API методы

---