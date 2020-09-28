FROM python:3.8-slim
LABEL MAINTAINER="Milchdealer/Teraku"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./src/main.py", "-i", "./res/ISINLIST"]
