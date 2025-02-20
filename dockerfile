# Використовуємо базовий образ, наприклад, з Ubuntu або Debian
FROM ubuntu:20.04
# Оновлюємо репозиторії і встановлюємо необхідні залежності
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fontconfig \
    xfonts-75dpi \
    xfonts-base \
    wkhtmltopdf \*

# Встановлюємо робочий каталог (опціонально)
WORKDIR /app

# Команда за умовчанням, яка запускається при запуску контейнера
CMD ["wkhtmltopdf", "--help"]

# (Опціонально) Якщо хочете дозволити додавати свої файли чи шаблони, можна створити volume
VOLUME ["/app"]