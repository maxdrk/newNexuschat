-- ddl Nexuschat (version corrigée)
create database if not exists Nexuschat;
USE Nexuschat;

-- Un mail appartient à un seul utilisateur (1,1)
create table if not exists mail (
    idMail int primary key auto_increment,
    mail varchar(254) not null unique,
    mailVerify boolean not null default false
);

-- Un utilisateur a un seul mail (1,1)
create table if not exists users (
    idUser int primary key auto_increment,
    idMail int not null unique,
    password varchar(255) not null,
    foreign key (idMail) references mail(idMail)
);

-- Un utilisateur a un seul pseudo (1,1)
create table if not exists pseudo (
    idUser int primary key,
    username varchar(25) not null unique,
    foreign key (idUser) references users(idUser) on delete cascade
);

-- Une conversation entre deux utilisateurs
-- (la paire est unique ; l'ordre idUser1 < idUser2 est à respecter côté application)
create table if not exists conversations (
    convId int primary key auto_increment,
    idUser1 int not null,
    idUser2 int not null,
    createdAt timestamp not null default current_timestamp,
    unique (idUser1, idUser2),
    foreign key (idUser1) references users(idUser) on delete cascade,
    foreign key (idUser2) references users(idUser) on delete cascade
);

-- Un message appartient à une conversation et a un seul expéditeur
-- Le destinataire se déduit de la conversation
create table if not exists message (
    messageId int primary key auto_increment,
    convId int not null,
    fromUser int not null,
    contenu text not null,
    createdAt timestamp not null default current_timestamp,
    foreign key (convId) references conversations(convId) on delete cascade,
    foreign key (fromUser) references users(idUser) on delete cascade,
    index idx_message_conv (convId, createdAt)
);

-- Relation de contact (même convention : idUser1 < idUser2 côté application)
create table if not exists contacts (
    idUser1 int not null,
    idUser2 int not null,
    RelationDate timestamp not null default current_timestamp,
    primary key (idUser1, idUser2),
    foreign key (idUser1) references users(idUser) on delete cascade,
    foreign key (idUser2) references users(idUser) on delete cascade
);

-- Demandes de contact (directionnelles : fromUser -> toUser)
create table if not exists demandes (
    idDemande int primary key auto_increment,
    fromUser int not null,
    toUser int not null,
    statusD enum('pending', 'accepted', 'refused') not null default 'pending',
    createdAt timestamp not null default current_timestamp,
    unique (fromUser, toUser),
    foreign key (fromUser) references users(idUser) on delete cascade,
    foreign key (toUser) references users(idUser) on delete cascade
);
