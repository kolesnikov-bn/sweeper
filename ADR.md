# ADR N: Краткое название решения

## Проблема и контекст

Опишите контекст, какие силы были задействованы, включая социальные, технологические, финансовые обстоятельства.
Пишите нейтральным языком, описывайте факты. Целесообразность (aka Rationale) должна быть очевидна из вашего описания.

## Решение

Опишите ваш ответ на обстоятельства, пишите полными предложениями в активном залоге, например, "Мы сделали ...".

## Недостатки
Почему это не делать? Что мы ухудшим?

## Статус
[Предложено | Принято | Устарело | Заменено]


---
# ADR 1: Использование получения mimetype через системы, а не через встроенную библиотеку mimetypes

## Проблема и контекст

- получение MIME через встроенную библиотеку mimetypes является плохим решением, так как оно может определять только
- по средствам расширения файла, что является проблемой при работе с файлами

## Решение
можно использользовать получение или через систему, или другие модули, например python-magic.
На текущий момент выбираю через систему, так как magic требует установки дополнительных библиотек в системе


## Недостатки


## Статус
[Принято]
