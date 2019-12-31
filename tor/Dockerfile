FROM alpine:edge

RUN apk add --no-cache --update \
        tor=0.4.1.7-r0 \
        python3=3.8.0-r0 \
        && pip3 install --upgrade pip==19.3.1 \
        && pip3 install nyx==2.1.0

COPY torrc /etc/tor/torrc

EXPOSE 9050 9051

VOLUME ["/var/lib/tor"]

USER tor

CMD ["/usr/bin/tor"]
