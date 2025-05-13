FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
