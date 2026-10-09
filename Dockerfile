FROM python:3.13-slim
WORKDIR /app
COPY app/ ./app/
COPY config/app.conf ./config/app.conf
RUN python -m compileall -q app
EXPOSE 8000
CMD ["python", "-u", "app/main.py"]
