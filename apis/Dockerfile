FROM python:3.11 

WORKDIR /code

COPY . /code/apis

RUN pip install --no-cache-dir --upgrade -r apis/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "apis.main:app", "--host", "0.0.0.0", "--port", "8000"]