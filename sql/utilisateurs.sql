create user 'nexusRead'@'localhost' identified by 'pkts';
grant select,execute on nexuschat.* to 'nexusRead'@'localhost';
flush privileges;


create user 'nexusCreate'@'localhost' identified by "pkts";
grant select,create,execute,update on nexuschat.* to 'nexusCreate'@'localhost';
flush privileges;