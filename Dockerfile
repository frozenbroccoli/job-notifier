FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 80

COPY ./api /code/api

COPY ./chromedriver /code/chromedriver

COPY ./interactions /code/interactions

COPY ./linkedin /code/linkedin

COPY ./main.py /code/main.py

CMD ["uvicorn", "api.linkedin_search:app", "--host", "0.0.0.0", "--port", "80"]