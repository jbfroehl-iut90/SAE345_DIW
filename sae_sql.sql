DROP TABLE IF EXISTS EQUIPEMENT, COULEUR, MORPHOLOGIE, TAILLE, MARQUE,  SPORT, CATEGORIE_SPORT;

CREATE TABLE CATEGORIE_SPORT(
    id_categorie_sport INT AUTO_INCREMENT,
    libelle_categorie_sport VARCHAR(255),
    PRIMARY KEY(id_categorie_sport)
);

CREATE TABLE SPORT(
    id_sport INT AUTO_INCREMENT,
    libelle_sport VARCHAR(255),
    categorie_sport INT,
    PRIMARY KEY(id_sport),
    CONSTRAINT fk_sport_categorie_sport FOREIGN KEY (categorie_sport) REFERENCES CATEGORIE_SPORT(id_categorie_sport)
);

CREATE TABLE COULEUR(
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(255),
    PRIMARY KEY(id_couleur)
);

CREATE TABLE MORPHOLOGIE(
    id_morphologie INT AUTO_INCREMENT,
    libelle_morphologie VARCHAR(255),
    PRIMARY KEY(id_morphologie)
);

CREATE TABLE MARQUE(
    id_marque INT AUTO_INCREMENT,
    libelle_marque VARCHAR(255),
    PRIMARY KEY(id_marque)
);

CREATE TABLE TAILLE(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY(id_taille)
);

CREATE TABLE EQUIPEMENT(
    id_equipement INT AUTO_INCREMENT,
    libelle_equipement VARCHAR(10000),
    prix_equipement INT,
    description_equipement VARCHAR(1000),
    image_equipement VARCHAR(1000),
    taille_equipement INT,
    marque_equipement INT,
    sport_equipement INT,
    couleur_equipement INT,
    morphologie_equipement INT,
    PRIMARY KEY(id_equipement),
    CONSTRAINT fk_equipement_taille FOREIGN KEY (taille_equipement) REFERENCES TAILLE(id_taille),
    CONSTRAINT fk_equipement_marque FOREIGN KEY (marque_equipement) REFERENCES MARQUE(id_marque),
    CONSTRAINT fk_equipement_sport FOREIGN KEY (sport_equipement) REFERENCES SPORT(id_sport),
    CONSTRAINT fk_equipement_couleur FOREIGN KEY (couleur_equipement) REFERENCES COULEUR(id_couleur),
    CONSTRAINT fk_equipement_morphologie FOREIGN KEY (morphologie_equipement) REFERENCES MORPHOLOGIE(id_morphologie)
);

LOAD DATA LOCAL INFILE 'COULEUR.csv' INTO TABLE COULEUR FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'TAILLE.csv' INTO TABLE TAILLE FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'MORPHOLOGIE.csv' INTO TABLE MORPHOLOGIE FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'CATEGORIE.csv' INTO TABLE CATEGORIE_SPORT FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'MARQUE.csv' INTO TABLE MARQUE FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'SPORT.csv' INTO TABLE SPORT FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE 'EQUIPEMENT.csv' INTO TABLE EQUIPEMENT FIELDS TERMINATED BY ',';

SELECT libelle_equipement FROM EQUIPEMENT;