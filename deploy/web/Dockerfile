from ubuntu/apache2

WORKDIR /var/www

run rm -f index.html

COPY ../../ ./


run rm /etc/apache2/site-available/000-default.conf

COPY ./nexuschat.conf /etc/apache2/sites-available/

run a2ensite nexuschat

