-- ddl Nexuschat
-- Normalisation suivant le schéma 
create database if not exists Nexuschat;
USE Nexuschat;

-- Un mail appartient à un seul utilisateur (1,1)
-- Un utilisateur a un seul mail (1,1)
create table if not exists mail(
    idMail int primary key AUTO_INCREMENT,
    mail varchar(254) unique,
    mailVerify boolean
);

-- Un utilisateur a un seul mail (1,1)
-- Un utilisateur a un seul pseudo (1,1)
create table if not exists users (
    idUser int primary key AUTO_INCREMENT, 
    idMail int UNIQUE,
    password varchar(255),
    foreign key (idMail) references mail(idMail)
); 

-- Un pseudo appartient à un seul utilisateur (1,1)
-- Un utilisateur a un seul pseudo (1,1)
create table if not exists pseudo(
    idUser int primary key,
    username varchar(25) unique,
    foreign key (idUser) references users(idUser)
);

-- Un message est envoyé par un seul utilisateur (1,1)
-- Un utilisateur peut envoyer plusieurs messages (1,N)
-- Un message est reçu par un seul utilisateur (1,1)
-- Un utilisateur peut recevoir plusieurs messages (1,N)
create table if not exists message(
    messageId int primary key AUTO_INCREMENT,
    contenu text,
    fromUser int,
    toUser int,
    createdAt timestamp default CURRENT_TIMESTAMP,
    foreign key (fromUser) references pseudo(idUser),
    foreign key  (toUser) references pseudo(idUser)
);