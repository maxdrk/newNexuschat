FROM ubuntu/apache2

RUN rm -f /var/www/html/index.html \
    && a2dissite 000-default.conf

COPY . /var/www/html/
COPY deploy/web/nexuschat.conf /etc/apache2/sites-available/nexuschat.conf

RUN find /var/www/html -type f \( \
      -name 'api.js' -o \
      -name 'avatars.js' -o \
      -name 'chat.js' -o \
      -name 'main.js' -o \
      -name 'profile.js' -o \
      -name 'utilisateurs.js' \
    \) -exec sed -i 's|http://127\.0\.0\.1|http://api-nexuschat|g' {} + \
    && a2ensite nexuschat.conf
