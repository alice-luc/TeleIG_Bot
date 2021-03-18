FROM python:3.8
WORKDIR /src
COPY req.txt /src
RUN pip3 install -r req.txt && pip3 install aiogram
COPY . /src
CMD ['python', 'app.py']
