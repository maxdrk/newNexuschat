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