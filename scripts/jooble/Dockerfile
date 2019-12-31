FROM python:alpine
RUN pip3 install 'requests[socks]'==2.21.0 beautifulsoup4==4.8.1
WORKDIR /jooble
COPY . .
ENTRYPOINT ["/jooble/jooble.py"]
