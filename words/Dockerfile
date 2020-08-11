FROM python:3.8

ADD requirements.txt /
ADD words_clean.txt /
ADD main.py /

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]