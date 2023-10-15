FROM       python:3.10-slim
LABEL      maintainer="Sana451 label"

WORKDIR    /web_app
COPY       requirements.txt /web_app/
RUN        pip install --upgrade pip
RUN        pip install -r requirements.txt

COPY       *.py /web_app/
COPY       /repository /web_app/repository
COPY       /service /web_app/service
RUN        chmod a+x *.py


CMD        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]