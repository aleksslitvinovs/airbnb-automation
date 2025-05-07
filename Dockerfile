FROM mcr.microsoft.com/playwright/python:v1.52.0

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN pip install ./plugins

ENTRYPOINT ["pytest", "tests/"]