FROM python:3.11.4

WORKDIR /FastApi
COPY requirements.txt fastapi/requirements.txt


RUN pip install --no-cache-dir --upgrade -r fastapi/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
