FROM python

COPY requirements.txt requirements.txt
RUN apt update && apt -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv
RUN pip install -U pip && pip install -r requirements.txt

COPY core /app/core
COPY wsgi.py /app
COPY main.py /app
COPY run.sh /app

WORKDIR /app

EXPOSE 8889

ENTRYPOINT ["bash", "/app/run.sh"]
# ENTRYPOINT ["bash"]
