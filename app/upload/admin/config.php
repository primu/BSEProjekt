<?php
// HTTP
define('HTTP_SERVER', 'http://localhost:8090/admin/');
define('HTTP_CATALOG', 'http://localhost:8090/');
// HTTPS
define('HTTPS_SERVER', 'https://localhost/admin/');
define('HTTPS_CATALOG', 'https://localhost/');
// DIR
define('DIR_APPLICATION', '/vagrant/app/upload/admin/');
define('DIR_SYSTEM', '/vagrant/app/upload/system/');
define('DIR_DATABASE', '/vagrant/app/upload/system/database/');
define('DIR_LANGUAGE', '/vagrant/app/upload/admin/language/');
define('DIR_TEMPLATE', '/vagrant/app/upload/admin/view/template/');
define('DIR_CONFIG', '/vagrant/app/upload/system/config/');
define('DIR_IMAGE', '/vagrant/app/upload/image/');
define('DIR_CACHE', '/vagrant/app/upload/system/storage/cache/');
define('DIR_DOWNLOAD', '/vagrant/app/upload/system/storage/download/');
define('DIR_UPLOAD', '/vagrant/app/upload/system/storage/upload/');
define('DIR_LOGS', '/vagrant/app/upload/system/storage/logs/');
define('DIR_MODIFICATION', '/vagrant/app/upload/system/storage/modification/');
define('DIR_CATALOG', '/vagrant/app/upload/catalog/');

// DB
define('DB_DRIVER', 'mysqli');
define('DB_HOSTNAME', 'localhost');
define('DB_USERNAME', 'opencart');
define('DB_PASSWORD', 'vagrant');
define('DB_DATABASE', 'opencart');
define('DB_PREFIX', 'oc_');
define('DB_PORT', '3306');
?>