USE Nexuschat;

DELIMITER $$

-- Création d'un utilisateur (mail + users + pseudo) en une seule transaction
-- vpassword doit contenir un HASH (bcrypt, argon2...) calculé côté application
DROP PROCEDURE IF EXISTS createUser$$
CREATE PROCEDURE createUser(
    IN vusername VARCHAR(25),
    IN vemail VARCHAR(254),
    IN vpassword VARCHAR(255)
)
BEGIN
    DECLARE vidMail INT;
    DECLARE vidUser INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO mail (mail, mailVerify)
    VALUES (vemail, FALSE);
    SET vidMail = LAST_INSERT_ID();

    INSERT INTO users (idMail, password)
    VALUES (vidMail, vpassword);
    SET vidUser = LAST_INSERT_ID();

    INSERT INTO pseudo (idUser, username)
    VALUES (vidUser, vusername);

    COMMIT;
END$$

DROP PROCEDURE IF EXISTS getUser$$
CREATE PROCEDURE getUser(IN vIdUser INT)
BEGIN
    SELECT P.username, M.mail
    FROM pseudo P
    JOIN users U ON P.idUser = U.idUser
    JOIN mail M ON U.idMail = M.idMail
    WHERE U.idUser = vIdUser;
END$$

-- Renvoie le hash : la comparaison du mot de passe se fait côté application
DELIMITER //

CREATE PROCEDURE loginUser(
    IN vemail VARCHAR(254),
    IN vpassword VARCHAR(254)
)
BEGIN
    SELECT U.idUser, P.username, M.mail, U.password AS passwordHash
    FROM users U
    JOIN mail M ON U.idMail = M.idMail
    JOIN pseudo P ON U.idUser = P.idUser
    WHERE M.mail = vemail
      AND U.password = vpassword;
END //

DELIMITER ;

-- Les on delete cascade suppriment pseudo, conversations, messages,
-- contacts et demandes ; il ne reste que le mail à supprimer
DROP PROCEDURE IF EXISTS deleteUser$$
CREATE PROCEDURE deleteUser(IN vIdUser INT)
BEGIN
    DECLARE vIdMail INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT idMail INTO vIdMail
    FROM users
    WHERE idUser = vIdUser;

    DELETE FROM users WHERE idUser = vIdUser;
    DELETE FROM mail WHERE idMail = vIdMail;

    COMMIT;
END$$

DROP PROCEDURE IF EXISTS selectUser$$
CREATE PROCEDURE selectUser(IN vUsername VARCHAR(25))
BEGIN
    SELECT U.idUser AS id, P.username AS pseudo
    FROM users U
    JOIN pseudo P ON U.idUser = P.idUser
    WHERE P.username = vUsername;
END$$

DROP PROCEDURE IF EXISTS getContacts$$
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

-- Le statut vaut 'pending' par défaut (défini dans la table)
DROP PROCEDURE IF EXISTS createDemande$$
CREATE PROCEDURE createDemande(IN vFromUser INT, IN vToUser INT)
BEGIN
    IF vFromUser = vToUser THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Impossible de se faire une demande à soi-même';
    END IF;

    INSERT INTO demandes (fromUser, toUser)
    VALUES (vFromUser, vToUser);
END$$

-- Le message est rattaché à une conversation ; le destinataire se déduit d'elle
DROP PROCEDURE IF EXISTS addContenu$$
CREATE PROCEDURE addContenu(
    IN inConvId INT,
    IN inFromUser INT,
    IN inContenu TEXT
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM conversations
        WHERE convId = inConvId
          AND inFromUser IN (idUser1, idUser2)
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Utilisateur absent de cette conversation';
    END IF;

    INSERT INTO message (convId, fromUser, contenu)
    VALUES (inConvId, inFromUser, inContenu);
END$$

DELIMITER ;
DELIMITER //

CREATE PROCEDURE getDemandes(IN inToUser INT)
BEGIN
    SELECT *
    FROM demandes
    WHERE toUser = inToUser;
END //

DELIMITER ;
