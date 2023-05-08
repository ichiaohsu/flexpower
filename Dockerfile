FROM python:3.11 

WORKDIR /code

COPY ./app /code/app
# COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY alembic.ini /code/alembic.ini

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]