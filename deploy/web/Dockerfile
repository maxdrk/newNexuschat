FROM ubuntu/apache2

RUN rm -f /var/www/html/index.html
RUN rm -f /etc/apache2/sites-available/000-default.conf

COPY deploy/web/nexuschat.conf /etc/apache2/sites-available/nexuschat.conf
COPY . /var/www/html/

RUN  a2ensite nexuschat.conf