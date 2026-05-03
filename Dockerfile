
FROM python:3.12-slim

WORKDIR /app

RUN pip install pytest

CMD ["tail", "-f", "/dev/null"]