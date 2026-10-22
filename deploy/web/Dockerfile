FROM ubuntu/apache2

RUN rm -f /var/www/html/index.html

COPY deploy/web/nexuschat.conf /etc/apache2/sites-available/nexuschat.conf
COPY . /var/www/html/

RUN a2dissite 000-default.conf \
    && a2ensite nexuschat.conf