FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN adduser u1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "sharefile:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
