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
    libelle_equipement VARCHAR(255),
    prix_equipement DECIMAL(63, 2),
    description_equipement VARCHAR(1023),
    image_equipement VARCHAR(255),
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

INSERT INTO COULEUR (libelle_couleur) VALUES(
    ("Rouge")
);

INSERT INTO TAILLE (libelle_taille) VALUES(
    ("XS")
);

INSERT INTO MORPHOLOGIE(libelle_morphologie) VALUES(
    ("Unisexe")
);

INSERT INTO CATEGORIE_SPORT(libelle_categorie_sport) VALUES(
    ("Sport de combat")
);

INSERT INTO MARQUE(libelle_marque) VALUES("Metal");


INSERT INTO SPORT(libelle_sport) VALUES(
    ("Boxe")
);

INSERT INTO EQUIPEMENT(id_equipement, libelle_equipement, prix_equipement, description_equipement, image_equipement, taille_equipement, marque_equipement, sport_equipement, couleur_equipement, morphologie_equipement) VALUES (
    1, 
    "Gant de boxe", 
    30.3, 
    "Gant pour la boxe", 
    "gant.jpg", 
    1,   -- This is the value for taille_equipement
    1,   -- This is the value for marque_equipement
    1,   -- This is the value for sport_equipement
    1,   -- This is the value for couleur_equipement
    1    -- This is the value for morphologie_equipement
);