FROM python:3.8

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD runserver.sh /
ADD words_clean.txt /
ADD palo /palo

CMD ["/runserver.sh"]