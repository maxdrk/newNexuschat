CREATE USER IF NOT EXISTS 'nexusCreate'@'%' IDENTIFIED BY 'change-moi';
CREATE USER IF NOT EXISTS 'neuxsRead'@'%' IDENTIFIED BY 'change-moi-aussi';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON nexuschat.* TO 'nexusRead'@'%';

GRANT SELECT
    ON nexuschat.* TO 'nexusRead'@'%';

FLUSH PRIVILEGES;