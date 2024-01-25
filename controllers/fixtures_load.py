#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql=''' DROP TABLE IF EXISTS EQUIPEMENT, COULEUR, MORPHOLOGIE, TAILLE, MARQUE,  SPORT, CATEGORIE_SPORT, UTILISATEUR; '''
    mycursor.execute(sql)

    sql='''
    CREATE TABLE UTILISATEUR (
  id_utilisateur INT AUTO_INCREMENT,
  login varchar(255),
  email varchar(255),
  password varchar(255),
  role varchar(255),
  nom varchar(255),
  est_actif tinyint(1),
  PRIMARY KEY (id_utilisateur)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;  
    '''
    mycursor.execute(sql)
    sql=''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE CATEGORIE_SPORT(
    id_categorie_sport INT AUTO_INCREMENT,
    libelle_categorie_sport VARCHAR(255),
    PRIMARY KEY(id_categorie_sport)
    );
    '''
    mycursor.execute(sql)
    sql=''' 
    LOAD DATA LOCAL INFILE '../CATEGORIE.csv' INTO TABLE CATEGORIE_SPORT FIELDS TERMINATED BY ',';
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE SPORT(
    id_sport INT AUTO_INCREMENT,
    libelle_sport VARCHAR(255),
    categorie_sport INT,
    PRIMARY KEY(id_sport),
    CONSTRAINT fk_sport_categorie_sport FOREIGN KEY (categorie_sport) REFERENCES CATEGORIE_SPORT(id_categorie_sport)
);
    '''
    mycursor.execute(sql)
    sql = ''' 
    LOAD DATA LOCAL INFILE '../SPORT.csv' INTO TABLE SPORT FIELDS TERMINATED BY ',';
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE COULEUR(
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(255),
    PRIMARY KEY(id_couleur)
);
     '''
    mycursor.execute(sql)
    sql = ''' 
    LOAD DATA LOCAL INFILE '../COULEUR.csv' INTO TABLE COULEUR FIELDS TERMINATED BY ',';
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE MORPHOLOGIE(
    id_morphologie INT AUTO_INCREMENT,
    libelle_morphologie VARCHAR(255),
    PRIMARY KEY(id_morphologie)
); 
     '''
    mycursor.execute(sql)
    sql = ''' 
    LOAD DATA LOCAL INFILE '../MORPHOLOGIE.csv' INTO TABLE MORPHOLOGIE FIELDS TERMINATED BY ',';
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE MARQUE(
    id_marque INT AUTO_INCREMENT,
    libelle_marque VARCHAR(255),
    PRIMARY KEY(id_marque)
);
         '''
    mycursor.execute(sql)
    sql = ''' 
    LOAD DATA LOCAL INFILE '../MARQUE.csv' INTO TABLE MARQUE FIELDS TERMINATED BY ',';
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE TAILLE(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY(id_taille)
);
         '''
    mycursor.execute(sql)
    sql = '''
    LOAD DATA LOCAL INFILE '../TAILLE.csv' INTO TABLE TAILLE FIELDS TERMINATED BY ',';
          '''
    mycursor.execute(sql)
     
    sql = '''
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
          '''
    mycursor.execute(sql)
    
    sql = '''
    LOAD DATA LOCAL INFILE '../EQUIPEMENT.csv' INTO TABLE EQUIPEMENT FIELDS TERMINATED BY ',';
     '''
    
    mycursor.execute(sql)
    

    get_db().commit()
    return redirect('/')
