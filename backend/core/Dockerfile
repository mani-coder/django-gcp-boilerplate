FROM --platform=linux/amd64 python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /usr/src/app

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    libffi-dev \
    libpq-dev

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Copy requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy the rest of the application code
COPY . .

RUN chmod +x /usr/src/app/entrypoint-prod.sh

ENTRYPOINT ["/usr/src/app/entrypoint-prod.sh"]

CMD uvicorn app.asgi:application --host 0.0.0.0 --port $PORT --workers 2 --log-level info
