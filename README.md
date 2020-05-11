# Streaming-com-RabbitMQ-
Aqui vamos montar nosso sistema de mensageria para streaming com RabbitMQ

#### instalando ambiente docker do rabbitMQ
```console

foo@bar:~ $ sudo docker run -d --hostname my-rabbit --name some-rabbit -p 8081:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management      

```

#### Crie ambiente python e instale as bibliotecas
```console

foo@bar:~ $ virtualenv env --python=python3.6

foo@bar:~ $ source env/bin/activate
(env) foo@bar:~ $ pip install -r requirementes.txt

```
---
#### Em seguida abra o terminal separadamente RODE O PRODUCER
```console
(env) foo@bar:~ $ python producer/producer_app.py

```


#### Em seguida abra o terminal separadamente RODE O CONSUMER
```console
(env) foo@bar:~ $ python consumer/consumer_app.py

```

#### DEMO 

![](https://media.giphy.com/media/kegaGtunKMln5lI93w/giphy.gif)


LINK - https://www.youtube.com/watch?v=DzO9vV2RBmI
