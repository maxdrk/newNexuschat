create user 'nexusRead'@'localhost' identified by '';
grant select,execute on nexuschat.* to 'nexusRead'@'localhost';
flush privileges;


create user 'nexusCreate'@'localhost' identified by "";
grant select,create,execute,update on nexuschat.* to 'nexusCreate'@'localhost';
flush privileges;