FROM python:3.9.10-buster
#почему не самый новый (может и 11)

# install ru locales
RUN apt-get update  \
    && apt-get install -y locales  \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip  install -r /requirements.txt
RUN apt-get -y clean

COPY . /stock_trades/
WORKDIR /stock_trades
EXPOSE 8001
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8001"]