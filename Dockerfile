FROM python:3.7-alpine3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Start the app
CMD ["python", "backend/main.py"]
