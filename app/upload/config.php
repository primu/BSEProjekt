<?php
// HTTP
define('HTTP_SERVER', 'http://localhost:8090/');
define('HTTP_ADMIN', 'http://localhost:8090/admin/');

// HTTPS
define('HTTPS_SERVER', 'https://localhost/');
// DIR
define('DIR_APPLICATION', '/vagrant/app/upload/catalog/');
define('DIR_SYSTEM', '/vagrant/app/upload/system/');
define('DIR_DATABASE', '/vagrant/app/upload/system/database/');
define('DIR_LANGUAGE', '/vagrant/app/upload/catalog/language/');
define('DIR_TEMPLATE', '/vagrant/app/upload/catalog/view/theme/');
define('DIR_CONFIG', '/vagrant/app/upload/system/config/');
define('DIR_IMAGE', '/vagrant/app/upload/image/');
define('DIR_CACHE', '/vagrant/app/upload/system/storage/cache/');
define('DIR_DOWNLOAD', '/vagrant/app/upload/system/storage/download/');
define('DIR_UPLOAD', '/vagrant/app/upload/system/storage/upload/');
define('DIR_MODIFICATION', '/vagrant/app/upload/system/storage/modification/');
define('DIR_LOGS', '/vagrant/app/upload/system/storage/logs/');

// DB
define('DB_DRIVER', 'mysqli');
define('DB_HOSTNAME', 'localhost');
define('DB_USERNAME', 'opencart');
define('DB_PASSWORD', 'vagrant');
define('DB_DATABASE', 'opencart');
define('DB_PREFIX', 'oc_');
define('DB_PORT', '3306');
?>