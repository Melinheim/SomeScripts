# Projects_Updater

## Описание.

Данный проект позволяет осуществлять автоматическое зеркалирование проектов из открытых источников на сервер GitLab.

Обновление производится по списку задач (job) `/ci_include/project_update_jobs.yml` по установленному в проекте расписанию (CI/CD -> Schedules).
Файл со списком задач на обновление генерируется при внесении изменений в конфигурационный файл `mirror_config.yaml`.\
Доступ к внесению изменений в репозитории для gitlab-runner осуществляется с использованием GitLab Deploy Keys.

**Обязательно.** Для возможности зеркалирования отдельно взятого проекта:
- на сервере GitLab создать проект, в который будет осуществляться зеркалирование;
- в созданном проекте добавить ветку по умолчанию.

Порядок действий:
- пользователь вносит изменение в конфигурацонный файл `mirror_config.yaml`;
- запускается конвейер для генерации списка задач по обновлению зеркал `/ci_include/project_update_jobs.yml` скриптом `script/job_creator.py`; gitlab-runner записывает сгенерированный список задач в проект Projects_Updater;
- по заданному расписанию (CI/CD -> Schedules) производится обновление зеркал на сервере GitLab (gitlab-runner вносит изменения в проекты на сервере GitLab).

Для включения новых проектов в процесс зеркалирования добавьте их в конфигурационный файл `mirror_config.yaml`.

## Конфигурационный файл `mirror_config.yaml`.

Формат конфигурационного файла `mirror_config.yaml`:

```yaml
<project_name1>:
  clone_origin: <clone_origin1>
  clone_branch: <clone_origin1>
  push_origin: <push_origin1>
  push_branch: <push_branch1>

<project_name2>:
  clone_origin: <clone_origin2>
  clone_branch: <clone_origin2>
  push_origin: <push_origin2>
  push_branch: <push_branch2>

...

<project_nameN>:
  clone_origin: <clone_originN>
  clone_branch: <clone_originN>
  push_origin: <push_originN>
  push_branch: <push_branchN>
```

`project_name` - название проекта, можно выбрать произвольно; нужно для наименования задач и каталога клонирования. 

`clone_origin` - адрес клонируемого репозитория.

`clone_branch` - название ветки клонируемого репозитория.

`push_origin` - SSH-адрес зеркала.

`push_branch` - название ветки зеркала, в которую пишется ветка клонируемого репозитория.
