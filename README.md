MongoDB references
==================

https://habrahabr.ru/company/latera/blog/280196/
http://eax.me/mongodb/
https://habrahabr.ru/post/240405/ (Hadoop)
https://habrahabr.ru/post/217393/ (Шардинг)
https://docs.mongodb.com/manual/reference/ulimit/#recommended-settings (Настройки)
http://docs.mongoengine.org/

OFF (UPD: работа с кастомным полем в тестовом задании)

Установка на Centos7
====================

echo "[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.2.asc
" >> /etc/yum.repos.d/mongodb-org-3.2.repo
yum install -y mongodb-org

nano /etc/mongod.conf
<<dbPath /var/data
chown -R mongod:mongod /var/data/

https://docs.mongodb.com/manual/tutorial/transparent-huge-pages/#configure-thp-tuned
and
nano /etc/default/grub
<<GRUB_CMDLINE_LINUX_DEFAULT="transparent_hugepage=never"
update-grub
https://docs.mongodb.com/manual/reference/ulimit/

Базовая настройка Mongo
=======================
https://docs.mongodb.com/manual/tutorial/enable-authentication/
https://docs.mongodb.com/manual/tutorial/manage-users-and-roles/
http://stackoverflow.com/questions/35341670/how-can-i-remove-user-from-my-mongodb-database

use admin
db.createUser(
  {
    user: "admin",
    pwd: "adminmongo",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
nano /etc/mongod.conf
<<security:
<<authorization: enabled

use laptopshop
db.createUser(
  {
    user: "pit",
    pwd: "userpass",
    roles: [ { role: "readWrite", db: "laptopshop" },
             { role: "read", db: "reporting" } ]
  }
)

Mongoengine
===========
pip install mongoengine

from pymongo import MongoClient

client = MongoClient('localhost:27017')   
client.admin.authenticate('admin', 'adminmongo')
client.testdb.add_user('newTestUser', 'Test123', roles=[{'role':'readWrite','db':'testdb'}])

https://habrahabr.ru/post/134590/
https://habrahabr.ru/sandbox/26218/
http://api.mongodb.com/python/current/api/pymongo/index.html
https://docs.mongodb.com/manual/tutorial/query-documents/

