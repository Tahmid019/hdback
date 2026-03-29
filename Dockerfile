FROM python:3.11-slim

# env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# workdir
WORKDIR /app

# deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app
COPY . .

# port
EXPOSE 8000

# run
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "hd_backend.asgi:application"]
