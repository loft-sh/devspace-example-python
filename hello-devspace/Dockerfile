FROM python:3.10.7-slim-bullseye

WORKDIR /hello-devspace

COPY ./requirements.txt /hello-devspace/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /hello-devspace/app

ENTRYPOINT ["uvicorn", "app.main:app"]
CMD ["--host", "0.0.0.0", "--port", "80"]
