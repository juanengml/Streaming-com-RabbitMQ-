FROM python:3.7-buster


ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirementes.txt /producer/requirementes.txt
COPY * /consumer/
WORKDIR /consumer
RUN  pip3 install -r requirementes.txt

CMD python3.7 ./consumer.py

