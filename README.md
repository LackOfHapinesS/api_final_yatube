# API для Yatube

API для социальной сети с возможностью публикации постов, комментариев, создания групп и подписок.

---

## Запуск проекта

### 1. Клонирование репозитория

```sh
git clone https://github.com/LackOfHapinesS/api_final_yatube.git
cd api_final_yatube
```

### 2. Создание и активация виртуального окружения
```sh
python3 -m venv .venv
source .venv/bin/activate  # macOS & Linux
```

### 3. Установка зависимостей
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Применение миграций
```sh
python manage.py migrate
```

### 5. Запуск сервера
```sh
python manage.py runserver
```
