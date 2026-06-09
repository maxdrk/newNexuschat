DELIMITER $$

CREATE PROCEDURE createUser(
    IN vusername VARCHAR(20),
    IN vemail VARCHAR(254),
    IN vpassword VARCHAR(30)
)
BEGIN
    DECLARE vidMail INT;
    DECLARE vidUser INT;

    INSERT INTO mail (mail, mailVerify)
    VALUES (vemail, FALSE);

    SET vidMail = LAST_INSERT_ID();

    INSERT INTO users (idMail, password)
    VALUES (vidMail, vpassword);

    SET vidUser = LAST_INSERT_ID();

    INSERT INTO pseudo (idUser, username)
    VALUES (vidUser, vusername);
END$$

DELIMITER ;


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