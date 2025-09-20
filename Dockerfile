FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT 8000
EXPOSE 8000
# Use gunicorn for production; default to 4 workers and bind to 0.0.0.0:$PORT
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
