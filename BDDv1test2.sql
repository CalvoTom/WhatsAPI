DROP TABLE IF EXISTS UTILISATEUR;

CREATE TABLE UTILISATEUR
    (id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT, pseudo_utilisateur VARCHAR(20) UNIQUE);

INSERT INTO UTILISATEUR
(id_utilisateur, pseudo_utilisateur)
VALUES
(1,'Tom.clv'),
(2,'Dorian.jsr');
