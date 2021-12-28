# Sweeper
Сортировщик скаченных файлов. Предназначен как расширение для Mac Workflow

## Описание
Скрипт предназначен в первую очередь для Mac Workflow, как `action folder`.


## Запуск и настройка

## Build
```shell
pyinstaller sweeper/main.py --onefile --windowed
```

### Pre-commit hooks
Проверка кода на соответствие определенным стандартам.
Для этого используем утилиту [pre-commit](https://pre-commit.com),
которая проверяет код перед созданием каждого коммита.

```shell
pre-commit install
pre-commit autoupdate
```

Так же можно запустить проверку всех файлов, вне зависимости от изменений в текущем коммите командой:

```shell
pre-commit run -a
```

Она позволит запустить все доступные чекеры для хуков

Так есть возможность запускать только отдельные доступные хуки:
- Black hooks:
    ```shell
    pre-commit run black -a
    ```
- Isort hooks:
    ```shell
    pre-commit run isort -a
    ```

### Tests
#### TOX
[tox](https://tox.readthedocs.io/en/latest/)

Автоматизация и тестирование процесса выпуска продукта в изолированном окружении.

##### Запуск тестов через tox
```shell
poetry run tox
```

Данная команда выполнит следующие действия:
- создание и установка всех зависимостей в vintualenv
- тестирование в virtualenv
- test coverage


#### Линтеры
Проверка кода различными линтерами
```shell
poetry run tox -e linter
```

Полный список доступных линтеров можно посмотреть в `tox.ini.testenv:linter.deps`
