#topics = ['HRский', 'Python', 'ООП', 'Базы данных', 'Фреймворки', 'HTTP / API', 'Best Practices', 'Асинхронность', 'ORM', 'Алгоритмы, структуры', 'Tools', 'FastAPI', 'Django', 'SQL', 'Веб-разработка', 'Модули / Пакеты', 'REST & SOAP', 'Тестирование', 'Языки', 'SDLC', 'Flask', 'GIL', 'Микс']


prompt_all =("__init__, super, classmethod, staticmethod, del, polymorphism, Цикл for, Булево значение, Итерируемый объект, Лямбда-функция, Цикл While, len, type, range, input, open, sum, min, max, sorted, map, filter, enumerate, all, isinstance, Exception, JSON, HTTP, Django, SQL, SQLite, PostgreSQL, MySQL, Jupyter Notebook, Pandas, NumPy, SciPy, Matplotlib, PyTorch, BeautifulSoup, Requests, pytest, logging, connect, execute, self, append, remove, def, decorator, FastAPI, REST, SOAP, Git, Github, SDLC, GIL,Flask, mixin, type, dict, XML, CSS, PyCharm, SELECT, INSERT, UPDATE, DELETE, JOIN, WHERE, GROUP BY, ORDER BY, import, Thread, help, dir, filter, int, float, tuple, Class, set, file, Frontend, Backend, Full Stack,PyCharm, JOIN, pip, Linux, Ubuntu, key, primary, foreign")

prompt_0 = (
    " FastAPI, Pyramid, JSON, HTTP, "
    "Django, Flask, SQLAlchemy, SQLite, PostgreSQL, MySQL, Jupyter Notebook, "
    "Pandas, NumPy, SciPy, Matplotlib, PyTorch, BeautifulSoup, Requests, "
    "pytest, Unittest, logging, telebot, aiogram, Linux, Kali, Ubuntu, Git, GitHub"
    "Anaconda, PyCharm, Spyder, Visual Studio Code, Sublime Text, Atom, Eclipse with PyDev, Thonny, "
    "IDLE, Vim, Emacs, Jupyter Lab, PyScripter, "
    "Frontend,  Backend, Full Stack, teamleader"

)

prompt_1 = (
    "Python, PEP8, telebot, time, aiogram, env, venv, pip, PyPI, asyncio, len, type, range, input, open, sum, min, max, sorted, map, filter, enumerate, all, isinstance, Exception,git, Github, Linux, лямбда-функции, async/await, оператор with,classmethod, staticmethod, del, polymorphism, Цикл for, bool, Лямбда-функция, Цикл While, len, type, range, input, open, import, pytest, unittest, "
    "логирование, JSON, запросы, NumPy, Pandas, Matplotlib, SciPy, Flask, Django, "
    "len, type, range, input, open, sum, min, max, sorted, enumerate, int, float, tuple, Class, set, file, set, len, NoneType, super,MRO (Method Resolution Order), декоратор property, slots, сравнение через is и ==, "
    ", args, kwargs, Python, dunder методы, wraps"
)

prompt_2 = (
    "SOLID, def, mixin, singleton, super, abstract classes, Python, class method, self, static method, new, init, classes, "
    "__getitem__, __setitem__, __delitem__, __add__, __mul__, __sub__, __truediv__, destructor, MQ, lru cache, "
    "Visitor, Template method, Strategy, State, RPC, gRPC, Observer, abstract method, constructor, Memento, "
    "__len__, __abs__, Mediator, __bool__, __eq__, __ne__, __lt__, __le__, __gt__, __ge__, __call__, __enter__, __exit__, "
    "staticmethod, dataclass, Try Except, Interpreter, Command, Chain of responsibility, Proxy, Flyweight, Facade, Composite, "
    "Bridge, Adapter, Structural patterns, Prototype, Factory method, Builder, abstract factory"
     "ООП, полиморфизм,миксин, инкапсуляция,деструктор класса, паттерн, наследования, абстрактный, конструктор, Class, класс"
)

prompt_3 = (
    "базы данных, индексы, ACID, нереляционные, шардирование, Postgres, MySQL, SQL,  "
    "JOIN, RIGHT JOIN, LEFT JOIN, INNER JOIN, OUTER JOIN, cross join, self join, natural join, "
    "блокировки, EXPLAIN, EXPLAIN ANALYZE, репликация, CAP теорема, alembic, leftjoin, "
    "EXPLAIN запрос, профилирование, MongoDB, NoSQL, SQL Lite, Express SQL, "
    "PK, первичный ключ, FK, внешний ключ, VACUUM, redis, PostgreSQL, команды управления транзакциями, UNION, INTERSECT, EXCEPT, WHERE, HAVING, GROUP BY, "
    "шардирование, денормализация, SQL инъекция, SELECT, INSERT, UPDATE, DELETE, TRUNCATE, MERGE, CALL, CREATE, ALTER, DROP, GRANT, REVOKE"
)

prompt_4 = (
    "Middleware, архитектура middleware, обработка запросов, обработка вида (view handling), валидация данных, "
    "WSGI (Web Server Gateway Interface), веб-фреймворки, Flask, Django, FastAPI, ASGI (Asynchronous Server Gateway Interface), "
    "ASGI серверы, микрофреймворки, реализация проекта, обработка ответов, жизненный цикл запроса, "
    "сравнение фреймворков, оптимизация производительности, синхронные против асинхронных фреймворков"
)

prompt_5 = (
    "REST, принципы REST, HTTP методы, GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, "
    "HTTP статус коды, 200 OK, 404 Not Found, 500 Internal Server Error, 302 Found, "
    "сериализатор, сериализация, типы HTTP запросов, различия HTTP запросов, "
    "HTTP, HTTPS, шифрование, работа с сетью, транспортный уровень, безопасность передачи данных"
)

prompt_6 = (
    "PEP8, программные паттерны, DRY (Don't Repeat Yourself),  "
    "правильный код, KISS (Keep It Simple, Stupid), хеширование, адаптивный сайт, версионное управление, "
    "agile, scrum, импорты, requirements, mypy, аннотация, Monkey Patch, длина строки в PEP8, "
    "git flow, Docker, dock str, YAGNI (You Aren't Gonna Need It), SDLC (Software Development Life Cycle), "
    "изоморфное приложение, микросервисная, монолитная, архитектура, SRP (Single Responsibility Principle), хеширование против шифрования, Backend, избавление от дублирования, баланс между KISS и DRY, SOLID (Single Responsibility, Open/Closed, "
    "Liskov Substitution, Interface Segregation, Dependency Inversion)"
)

prompt_7 = (
    "асинхронность, time.sleep, import, time, threading, мультипроцессинг, "
    "корутина в Python, асинхронные, проект Celery, использование Celery, async, однопоточность, "
    "параллелизм, функция wait(), функция gather(), функция create_task(), "
    "функция sleep(), функция run(), асинхронность, await, asyncio, event loop, корутины, Future, Task, "
    "асинхронные операции, non-blocking I/O, callback, promise, async/await pattern, "
    "concurrency (конкурентность), parallelism (параллелизм), threading, multiprocessing, "
    "green threads, GIL (Global Interpreter Lock), asyncio.create_task(), asyncio.gather(), asyncio.wait(), asyncio.run(), "
    "аsynchronous server, asynchronous client, non-blocking server, websockets, HTTP/2, HTTP/3, asynchronous API, async I/O frameworks"
)

prompt_8 = (
    "ORM (Object-Relational Mapping), миграция, преимущества ORM, создание запросов вручную, "
    "автоматизация баз данных, синхронизация моделей и структур БД, упрощение работы с данными, "
    "нормализация данных, отношения между таблицами, lazy loading, eager loading, "
    "транзакции в ORM, каскадное удаление, полиморфизм в ORM, инверсия управления, "
    "SQLAlchemy, Django ORM, Active Record, Data Mapper, связи One-to-One, One-to-Many, Many-to-Many, "
    "сессии ORM, кэширование запросов, оптимизация запросов в ORM, миграционные скрипты"
)

prompt_9 = (
    "BigO notation, словарь, список, сложность алгоритма, хеш-функция, рекурсия, "
    "сложность операций в коллекциях, бинарное дерево, жадные алгоритмы, алгоритм Дейкстры, "
    "хвостовая рекурсия, оптимизация хвостовой рекурсии, линейная сложность, логарифмическая сложность, "
    "вычислительная сложность, O(n), O(n²), пузырьковая сортировка, индексация, массивы, "
    "хеш-таблица, хеш-мап, динамический массив, бинарный,рекурсия, итерирование, функциональное программирование, "
    "алгоритм подсчета, очередь, стек"
)

prompt_10 = (
    "виртуальное окружение, ветка в GIT, git stash, git flow, git, docker registry, docker image, "
    "docker daemon, docker container, cherry pick, PID процесса, Docker Compose, Docker, CSV, Apache Airflow, "
    "venv,Docker, poetry, различие между docker и виртуальной машиной, "
    "системы мониторинга, система прав в Linux, работа с AWS, Kubernetes, Terraform, Jenkins, Prometheus, "
    "Grafana, Ansible, Puppet, Chef, Nagios, Elasticsearch, Logstash, Kibana, Vagrant, GitLab CI/CD, "
    "GitHub Actions, Travis CI, Selenium, Postman, JIRA, Trello, Slack, Visual Studio Code, IntelliJ IDEA, "
    "PyCharm, Sublime Text, Atom, Eclipse, Jupyter Notebook, Bitbucket, SVN, Mercurial"
)

prompt_11 = (
    "FastAPI, асинхронность, Starlette для веб-сервера, Pydantic для валидации данных, "
    "автоматическая документация с Swagger UI и ReDoc, поддержка асинхронных запросов, "
    "встроенная валидация, зависимости и внедрение зависимостей, поддержка OAuth2 с JWT токенами, "
    "высокая производительность, совместимость с OpenAPI, middleware, CORS (Cross-Origin Resource Sharing), "
    "background tasks, WebSockets, GraphQL, автоматическая сериализация и десериализация, "
    "поддержка синхронных и асинхронных маршрутов, тестирование с pytest, поддержка PyCharm и других IDE"
)

prompt_12 = (
    "many to many, querySet, основные сущности Django, Model View Template (MVT), ленивые querySet, обработка HTTP запросов в Django, sqlparse, asgiref, запрос/ответ в Django, миграции, "
    "IntegerChoices, ApiView, ViewSet, кастомная авторизация, работа с websocket в Django, сериализатор, models, создание объекта в Django ORM, "
    "manage.py, Django REST framework, настройка ссылок, мидлвари, связь m2m, Django, URLconf, Django Admin, Django Channels, Django Forms, Django Sessions, Django Security, "
    "Django Middleware, Django Signals, Django Validators, Django Filters, Django Managers, Django Query Optimizations, Django Transactions, Django Field Lookups, Django Aggregations, "
    "Django Middleware, template tags and filters, class-based views, function-based views, "
    "Django Testing, Django Debugging, Django Deployment, Django Settings, Django Internationalization"
)


prompt_13 = (
    "реляционные базы данных, NoSQL базы данных, схема данных, SQL, ACID (Atomicity, Consistency, Isolation, Durability), "
    "масштабируемость, гибкость схемы, производительность, CAP теорема (Consistency, Availability, Partition tolerance), "
    "типы NoSQL баз (ключ-значение, документо-ориентированные, колоночные, графовые),транзакции, индексы, нормализация данных, денормализация, JOIN операции, репликация, шардирование, запросы SQL vs NoSQL, горизонтальное масштабирование, вертикальное масштабирование, "
    "SELECT, INSERT, UPDATE, DELETE, MERGE, TRUNCATE, VIEW, CURSORS, PRIMARY KEY, FOREIGN KEY, UNIQUE, INDEX, CONSTRAINTS, "
    "GROUP BY, ORDER BY, COMMIT, EXPLAIN"
)


prompt_14 = (
    "CGI (Common Gateway Interface), плюсы и минусы CGI, защита кукис, куки от воровства, куки от подделки, "
    "аутентификация, авторизация, разница между аутентификацией и авторизацией, XSS (Cross-Site Scripting), "
    "защита от XSS, CSRF (Cross-Site Request Forgery), web security, secure HTTP headers, Content Security Policy, "
    "HTTP Only cookies, SameSite cookies, token-based authentication, OAuth, OpenID, JSON Web Tokens (JWT), "
    "web frameworks, HTML escaping, input validation, output sanitization, HTTPS, SSL/TLS, secure coding practices"
)

prompt_15 = (
    "имя модуля, модульное программирование, поиск модулей, импорт модулей, Python module path, "
    "sys.path, PYTHONPATH, import statement, package, sub-package, __init__.py, namespace packages, "
    "relative imports, absolute imports, module resolution, dependency management, pip, virtual environments, "
    "site-packages, dist-packages, module caching, reload, importlib, sys.modules, built-in modules, "
    "third-party modules, Python Standard Library, module namespace, importing packages, package structure"
)

prompt_16 = (
    "production мониторинг, REST, SOAP, веб-сервисы, Docker Registry, "
    "Prometheus, Grafana, New Relic, Datadog, ELK stack, логирование, алерты, RESTful API, REST принципы, HTTP методы, CRUD операции, статeless, ресурсы, JSON, XML, "
    "SOAP веб-сервисы, WSDL, SOAP envelope, RPC (Remote Procedure Call), SOAP vs REST, "
    "Docker Registry, контейнеризация, управление образами Docker, репозиторий Docker, публичный registry, приватный registry, "
    "автоматическое развертывание, CI/CD, безопасность Docker, версионирование образов, APM (Application Performance Management), трассировка запросов, fault tolerance, мониторинг сети, управление логами"
)

prompt_17 = (
    "monkey patch, модули для тестирования, unit test, mock, необходимость тестов, виды тестов, "
    "покрытие тестами, проблемы покрытия тестами, пирамида тестирования, mocking, оптимизация тестируемой функции, "
    "интеграционное тестирование, функциональное тестирование, автоматическое тестирование, ручное тестирование, "
    "pytest, unittest, mock module, integration tests, functional tests, performance tests, regression tests, "
    "acceptance tests, load testing, stress testing, end-to-end testing, test-driven development (TDD), "
    "behavior-driven development (BDD), continuous integration, continuous deployment, code coverage, test fixtures, "
    "test isolation, test doubles, stubs, spies, test harness, test suites, test runners"
)

prompt_18 = (
    "C#, Python, интерпретируемый язык, компилируемый язык, типизация, динамическая, статическая, C++,  низкоуровневые, высокоуровневые, "
    "машинный код, Python, JavaScript, компилятор, интерпретатор, runtime, garbage collection, статическая проверка типов, duck typing, интерпретируемый байт-код, JIT-компиляция, "
    "стек вызовов, лямбда-выражения, объектно-ориентированное, программирование, функциональное, "
    "список (list), массив (array), словарь (dictionary), ассоциативный массив, динамическое выделение памяти, сборка мусора"
)

prompt_19 = (
    "Code Debt, технический долг, управление техническим долгом, рефакторинг, качество кода, долговременные последствия, "
    "важность тестирования, автоматическое тестирование, ручное тестирование,  "
    "Scrum, Kanban, спринты, доска Kanban, SDLC, этапы SDLC, инкрементная модель, итеративная модель, водопадная модель, agile, DevOps, "
    "метрики производительности, управление версиями, инструментальные средства SDLC, CI/CD (Continuous Integration/Continuous Deployment), "
    "user stories, задачи, JIRA, Trello, бэклог, демо, ретроспектива, ежедневные стендапы"
)


prompt_20 = (
    "Flask, микрофреймворк, легковесный фреймворк, гибкость, модульность, WSGI (Web Server Gateway Interface), Jinja2, Werkzeug, маршрутизация, "
    "поддержка RESTful API, расширения Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, "
    "авторизация и аутентификация, Flask-Login, Flask-Security, тестирование, Flask-Testing, "
    "Blueprint, миграции базы данных, ORM, интеграция с фронтендом, поддержка WebSockets, middleware, session management, гибкость развертывания, контейнеризация, "
    "разработка API, минимализм кода, сообщество Flask, документация Flask,"
)

prompt_21 = (
    "asyncio, параллелизм, конкурентность, задачи для параллелизации,  треды, нативные, GIL (Global Interpreter Lock), "
    "кодстайл, PEP8, flake8, pylint, black, isort, рефлексия, introspection, "
    "асинхронное, event loop, корутины, Future, Task, callback, concurrent.futures, "
    "мультипроцессинг, threading,  глобальная блокировка интерпретатора, "
    "интерпретатор CPython, интерпретируемый язык, компилируемый язык, инструменты для линтинга, рефакторинг, метапрограммирование, "
    "встроенные функции introspection, hasattr, getattr, setattr, dir, type, id, __dict__, __class__, модуль inspect"
)

prompt_22 = (
    "Git Rebase, commit, hash, merge, branch, squash, pull request, rebase, pick, fixup, HEAD, push, force push, "
    "pre-commit check, hook, Set-Cookie, module, package, import, static typing, dynamic typing, strong typing, weak typing, "
    "array, stack, heap, queue, linked list, graph, tree, hash table, Map, git init, git push, git commit, virtual environment, "
    "Flask, WSGI, Jinja2, Werkzeug, routing, RESTful API, Flask-RESTful, Flask-SQLAlchemy, Flask-WTF, authorization, authentication, "
    "Blueprint, WebSockets, middleware, session management, ORM, API development, refactoring, debugging, testing, pytest, unittest, "
    "Flask-Migrate, SQL, SELECT, FROM, many-to-many, components, f-strings, break, continue, docstring, comments, Docker, JSON, XML, CRUD, "
    "HTTP, SSL/TLS, asyncio, coroutine, Future, integration testing, functional testing, refactoring"
)

