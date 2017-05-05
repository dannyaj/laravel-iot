FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y apache2 curl 
RUN apt-get install -y php7.0 php7.0-zip php-common php-mbstring php-xml libapache2-mod-php7.0 php-curl

RUN sed -i 's|;extension=php_curl.dll|extension=php_curl.dll|g' /etc/php/7.0/apache2/php.ini

RUN curl -sS https://getcomposer.org/installer | php
RUN mv composer.phar /usr/local/bin/composer
RUN chmod +x /usr/local/bin/composer

RUN composer create-project laravel/laravel /var/www/laravel --prefer-dist
RUN composer require php-curl-class/php-curl-class

RUN chown -R www-data:www-data /var/www/laravel/storage

RUN /usr/sbin/a2enmod rewrite
ADD 000-laravel.conf /etc/apache2/sites-available/
RUN /usr/sbin/a2dissite '*' && /usr/sbin/a2ensite 000-laravel

# Optional for MongoDB
RUN apt-get install -y php7.0-dev php-pear pkg-config
RUN pecl install mongodb

RUN echo "extension=mongodb.so" >> /etc/php/7.0/apache2/php.ini
RUN echo "extension=mongodb.so" >> /etc/php/7.0/cli/php.ini

# Optional for access message queue
RUN apt-get install -y python python-pip
RUN pip install --upgrade pip
RUN pip install pika
COPY iot-integration /opt/iot-integration

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
