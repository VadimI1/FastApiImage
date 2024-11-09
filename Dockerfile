# Dockerfile

# pull the official docker image
FROM python:3.9

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", ".\src\rabbitMQ\receive.py"]
##CMD uvicorn src.main:app --reload
##["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"]
