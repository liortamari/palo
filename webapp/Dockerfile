FROM python:3.8

ADD requirements.txt /
ADD runserver.sh /
ADD palo /palo

RUN pip install -r requirements.txt

CMD ["/runserver.sh"]