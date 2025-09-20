FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1





    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Document internal port; the runtime will publish it
EXPOSE 8000

# Use $PORT if provided by host, else 8000
CMD ["bash", "-lc", "exec gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app --access-logfile - --error-logfile -"]