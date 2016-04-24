echo "Konfiguruje SSLa"
cp /vagrant/ssl/default-ssl.conf /etc/apache2/sites-available/
a2enmod "ssl"
a2ensite "default-ssl"
/etc/init.d/apache2 reload
