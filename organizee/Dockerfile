FROM python:3.12

# Определяем переменные среды
ENV DJANGO_SETTINGS_MODULE=organizee.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри проекта
WORKDIR /usr/src/app

# Копируем все файлы проекта в Docker-контейнер
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Прослушиваем порт 8000
EXPOSE 8000