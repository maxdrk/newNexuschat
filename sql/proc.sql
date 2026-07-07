DELIMITER $$

create procedure createUser(
    in vusername varchar(20),
    in vemail varchar(254),
    in vpassword varchar(30)
)
begin
    declare vidMail int;
    declare vidUser int;

    insert into mail (mail, mailVerify)
    values (vemail, FALSE);

    set vidMail = LAST_INSERT_ID();

    insert into users (idMail, password)
    values (vidMail, vpassword);

    set vidUser = LAST_INSERT_ID();

    insert into pseudo (idUser, username)
    values (vidUser, vusername);
end$$

delimiter ;


delimiter$$
create procedure getUser(in vIdUser int) 
begin 
select P.username, m.mail from pseudo P
join users U on p.idUser = U.idUser
join mail M on U.idMail = M.idMail
where U.idUser = vidUser
end$$
delimiter;

DELIMITER $$

CREATE PROCEDURE loginUser(IN vemail VARCHAR(254), IN vpassword VARCHAR(30))
BEGIN
    SELECT U.idUser, P.username, M.mail
    FROM users U
    JOIN mail M ON U.idMail = M.idMail
    JOIN pseudo P ON U.idUser = P.idUser
    WHERE M.mail = vemail
    AND U.password = vpassword;
END$$

DELIMITER ;

DELIMITER $$

create procedure deleteUser(in vIdUser int)
begin
    declare vIdMail int;
    select idMail into vIdMail
    from users
    where idUser = vIdUser;
    delete from message
    where fromUser = vIdUser or toUser = vIdUser;
    delete from conversations
    where fromUser = vIdUser or toUser = vIdUser;
    delete from pseudo
    where idUser = vIdUser;
    delete from users
    where idUser = vIdUser;
    delete from mail
    where idMail = vIdMail;
end$$

DELIMITER ;
delimiter $$
create procedure createDemande(in idDemandeur int,in idDemande int)
begin 
insert into demandes(fromUser,toUser) values(idDemandeur,idDemande)
end$$
delimiter;

delimite $$

create procedure selectUser(in pseudo varchar(25))
select U.idUser as id , P.username as pseudo from users U
join pseudo P on U.idUser = P.idUser
where P.username = pseudo
end
delimiter $$

DELIMITER $$
CREATE PROCEDURE getContacts(IN inIdUser INT)
BEGIN 
    SELECT 
        CASE WHEN C.idUser1 = inIdUser THEN P2.username
             ELSE P1.username
        END AS contact
    FROM contacts C
    JOIN pseudo P1 ON C.idUser1 = P1.idUser
    JOIN pseudo P2 ON C.idUser2 = P2.idUser
    WHERE C.idUser1 = inIdUser OR C.idUser2 = inIdUser;
END$$
DELIMITER ;

delimiter $$

CREATE PROCEDURE `createDemande`(in idDemandeur int,in idDemande int,in vstatus char(10))
begin 
insert into demandes(fromUser,toUser,statusD) values(idDemandeur,idDemande,vstatus);
end $$
delimiter ;

delimiter $$
create procedure addContenu (in inContenu varchar(254), in inFromUser int,in inToUser int )
begin
INSERT INTO message (contenu, fromUser, toUser) VALUES (inContenu,inFromUser,inToUser);
end $$
delimiter ;