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
    sql=''' DROP TABLE IF EXISTS NOTE, EQUIPEMENT, CATEGORIE_SPORT, COULEUR, MORPHOLOGIE, MARQUE, TAILLE, UTILISATEUR; '''
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
    INSERT INTO UTILISATEUR(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(NULL,'admin','admin@admin.fr',
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
    INSERT INTO CATEGORIE_SPORT (libelle_categorie_sport) VALUES
        ('Sport de combat'),
        ('Sport collectif'),
        ('Sport de raquettes'),
        ('Sport d endurance'),
        ('Sport aquatique'),
        ('Cyclisme'),
        ('Renforcement Musculaire')
    ;
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
    INSERT INTO COULEUR(libelle_couleur) VALUES
    ('Rouge'),
    ('Bleu'),
    ('Vert'),
    ('Violet'),
    ('Noir'),
    ('Blanc'),
    ('Rose'),
    ('Jaune'),
    ('Gris'),
    ('Marron'),
    ('Orange'),
    ('Kaki');
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
    INSERT INTO MORPHOLOGIE (libelle_morphologie) VALUES
    ('Homme'),
    ('Femme'),
    ('Enfant'),
    ('Unisexe');
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
    INSERT INTO MARQUE (libelle_marque) VALUES
    ('Venum'),
    ('Adidas'),
    ('Nike'),
    ('Kipsta'),
    ('Puma'),
    ('Asics'),
    ('Le coq sportif'),
    ('The North Face'),
    ('Metal'),
    ('Jordan'),
    ('Kempa'),
    ('Power Shot'),
    ('Nabaiji'),
    ('cressi_sub'),
    ('salomon'),
    ('Kemi'),
    ('Domyos'),
    ('Fit & Rack'),
    ('Decathlon'),
    ('canyon'),
    ('Bmc'),
    ('electra');
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
    INSERT INTO TAILLE (libelle_taille) VALUES
    ('XS'),
    ('S'),
    ('M'),
    ('L'),
    ('XL'),
    ('XXL'),
    ('XXXL'),
    ('Lot 2'),
    ('Lot 4'),
    ('Lot 6'),
    ('Lot 8'),
    ('Lot 10'),
    ('Lot 12'),
    ('Lot 14'),
    ('Lot 16'),
    ('36'),
    ('37'),
    ('38'),
    ('39'),
    ('40'),
    ('41'),
    ('42'),
    ('43'),
    ('44'),
    ('45'),
    ('46'),
    ('0, 5(L)'),
    ('1(L)'),
    ('2(L)'),
    ('10(m)'),
    ('55(kg)'),
    ('20(kg)');
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
    CONSTRAINT fk_equipement_sport FOREIGN KEY (sport_equipement) REFERENCES CATEGORIE_SPORT(id_categorie_sport),
    CONSTRAINT fk_equipement_couleur FOREIGN KEY (couleur_equipement) REFERENCES COULEUR(id_couleur),
    CONSTRAINT fk_equipement_morphologie FOREIGN KEY (morphologie_equipement) REFERENCES MORPHOLOGIE(id_morphologie)
);
          '''
    mycursor.execute(sql)
    
    sql = '''
    INSERT INTO EQUIPEMENT (libelle_equipement, prix_equipement, description_equipement, image_equipement, taille_equipement, marque_equipement, sport_equipement, couleur_equipement, morphologie_equipement) VALUES
    ( 'Gants  de  MMA  Venum  Impact  2.0' , 80,  'Ces  gants  en  cuir  Skintex  sont  ergonomiques    confortables  et  de  haute  qualité.  La  mousse  triple  densite  permet  de  garder  votre  main  à  l  abris  des  chocs.  Forme  incurvée  permettant  au  gant  de  parfaitement  épouser  la  forme  de  votre  main.  Le  système  de  fermeture  fournit  un  meilleur  serrage  et  la  possibilité  de  fermer  avec  une  seule  main.' , 'gantsMMA.webp', 4, 1, 1, 5, 4),
    ( 'Gants  de  boxe  Venum  Elite' , 90,  'Gants  pour  Boxe  Anglaise    Kick  Boxing  et  Muay  Thai.  Doté  d  une  mousse  à  quadruple  densité    ces  gants  sont  designés  pour  absorber  au  mieux  les  impacts  lors  des  frappes.  Les  coutures  renforcées  et  les  panneaux  en  maille  combinés  à  leur  forme  ergonomique  vous  apporteront  un  ajustement  confortable  et  vous  aurez  l  impression  de  ne  faire  qu  un  avec  le  gant.' , 'gantsBoxe.webp', 4, 1, 1, 1, 4),
    ( 'Kimono  JJB  Venum  Elite  4.0' , 200,  'Ce  Kimono  est  fabriqué  en  coton  Pearl  Wave  450  g/m²  et  est  renforcé  sur  tous  les  points  de  tension  pour  une  plus  grande  durabilité.  Le  col  en  mousse  EVA  rigide  résistera  aux  prises  de  vos  adversaires  et  à  vos  ruptures  de  prise  les  plus  puissantes.  Confortable  et  robuste    il  est  conçu  pour  résister  à  l  usure  des  séances  d  entraînement  intenses.  Le  pantalon  est  fabriqué  en  tissu  Ripstop  285  g/m²  et  est  renforcé  aux  chevilles    aux  genoux  et  à  l  entrejambe.  Les  coutures  renforcées  aux  poignets  assurent  une  plus  grande  longévité' , 'kimonoJJB.webp', 3, 1, 3, 2, 1),
    ('Nunchaku', 40,  'Découvrez  l  élégance  et  la  puissance  du  Nunchaku    un  instrument  emblématique  dans  le  monde  des  arts  martiaux.  Notre  Nunchaku  est  fabriqué  avec  un  artisanat  exceptionnel    offrant  une  combinaison  parfaite  de  durabilité  et  de  performance.  Conçu  pour  les  pratiquants  de  tous  niveaux    cet  article  incarne  la  tradition  tout  en  intégrant  des  éléments  modernes  pour  une  expérience  optimale' , 'nunchaku.jpg', 4, 19, 1, 5, 4),
    ( 'Kimono  de  Judo' , 70,  'Explorez  l  excellence  du  judo  avec  notre  Kimono  de  haute  qualité.  Conçu  pour  répondre  aux  exigences  rigoureuses  des  pratiquants  de  judo    notre  Kimono  allie  confort    durabilité  et  performance  exceptionnelle.  Fabriqué  à  partir  de  matériaux  résistants    il  offre  une  coupe  précise  qui  permet  une  liberté  de  mouvement  maximale  tout  en  conservant  une  élégance  traditionnelle.  Que  vous  soyez  un  débutant  passionné  ou  un  judoka  expérimenté    notre  Kimono  est  un  choix  fiable  pour  vos  séances  d  entraînement  et  compétitions.' , 'kimonoJudo.jpg', 3, 19, 1, 6, 1),
    ( 'Jordan  Zion  3  Pink  Lotus  Enfants  GS' , 110,  'Chaussure  de  basket  Jordan  rose  pour  enfant' , 'chaussureBasket1.webp', 16, 10, 2, 7, 3),
    ( 'Résine  Kempa  200ml  [Taille  200  ml]' , 16,  'résine  en  pot  pour  plus  d  adhérence  en  match' , 'potResineHand1.jpg', 27, 11, 2, 2, 1),
    ( 'filet  de  volley  ball  d  entrainement' , 45,  'filet  de  10*1m  sera  parfait  pour  vos  entrainement' , 'filetVolley1.jpg', 30, 12, 2, 6, 1),
    ( 'pince  nez  flottant  de  natation  bleu  cyan' , 4,  'peur  de  perdre  votre  pince  nez celui  ci  flotte  ' , 'pinceNezNatation1.jpg', 1, 13, 5, 2, 4),
    ( 'Palmes  Cressi  Frog  Plus  Noir/silver' , 65,  'Palmage  fluide  effort  réduit  peu  fatiguant' , 'palmPlongée1.jpg', 1, 14, 5, 5, 4),
    ( 'Soft  flask  250mL  -  28mm' , 18,  'Gourde  accessible facilement  transportable' , 'gourdeCoursePied1.jpg', 27, 15, 4, 2, 4),
    ( 'flash  carbon' , 76,  'léger  transportable  en  fibre  de  carbone' , 'batonTrail1.jpg', 1, 16, 4, 5, 4),
    ( 'Kettlebell  de  musculation  en  fonte  et  base  caoutchouc' , 55,  'kettelbell  de  55kg  a  base  en  caoutchouc  pour  moins  de  dégat' , 'bouleMuscu.jpg', 31, 17, 7, 5, 4),
    ( 'Barre  Olympique  -  Entrainement  2.0  -  20kg' , 207,  'barre  de  crossfit  de  20kg  avec  un  bon  grip' , 'barreCrossfit1.jpg', 32, 18, 7, 9, 4),
    ( 'GYM  BALL  RÉSISTANT  TAILLE  2  /  65  cm  -  BLEU' , 20,  'gymball  avec  une  structure  résitante      peut  etre  utilisé  pour  toutes  exercices' , 'gymballPilat1.jpg', 1, 17, 7, 2, 4),
    ( 'Spectral  29  CF  8' , 4600,  'Du  rapide  et  fluide  au  rugueux  et  technique    le  Spectral  CF  8  est  prêt  à  affronter  tous  les  sentiers  que  vous  lui  indiquerez.' , 'veloEnduro1.webp', 3, 20, 6, 5, 4),
    ( 'Vélo  de  Route  BMC  Teammachine  SLR  Five  Shimano  105  Di2  12V  700  mm  Argent  Arctic  2023' , 3300,  'Vélo  de  course  parfait  pour  rouler  sur  route  et  la  vitesse' , 'veloCourse1.jpg', 3, 21, 6, 6, 4),
    ( 'Electra  Loft  7i  EQ  Step  Thru' , 440,  'La  technologie  Flat  Foot  d  Electra  signifie  un  confort  et  un  contrôle  brevetés  sur  un  vélo  Electra.' , 'veloVille.jpg', 3, 22, 6, 10, 4),
    ( 'X  Crazyfast  Elite  LL  FG' , 270,  'chaussure  de  foot  equipé  de  crampon  silouhette  aérodynamique' , 'chaussureFoot1.avif', 26, 2, 2, 8, 4),
    ( 'Protège-dents  Venum  Predator' , 22,  'Ce  protège-dents    est  le  parfait  mix  en  confort    souplesse  et  absorption  des  chocs    afin  de  prévenir  et  réduire  les  besssures  au  niveau  de  vos  dents    lèvres  et  gencives.  Cadre  extérieur  en  caoutchouc  asborbant  les  chocs    et  intérieur  en  gel  thermo-formable  afin  de  mouler  parfaitement  votre  dentition  et  permettre  une  meilleure  respiration', 'protegeDents.webp', 5, 1, 1, 11, 4),
    ( 'Protège-dents  Venum  Predator' , 22,  'Ce  protège-dents    est  le  parfait  mix  en  confort    souplesse  et  absorption  des  chocs    afin  de  prévenir  et  réduire  les  besssures  au  niveau  de  vos  dents    lèvres  et  gencives.  Cadre  extérieur  en  caoutchouc  asborbant  les  chocs    et  intérieur  en  gel  thermo-formable  afin  de  mouler  parfaitement  votre  dentition  et  permettre  une  meilleure  respiration', 'ProtegeDentKaki.webp', 5, 1, 1, 12, 4);
     '''
    
    mycursor.execute(sql)
    
    sql='''
    CREATE TABLE NOTE(
    id_note INT AUTO_INCREMENT,
    note INT,
    id_equipement INT,
    PRIMARY KEY(id_note),
    CONSTRAINT fk_note_equipement FOREIGN KEY(id_equipement) REFERENCES EQUIPEMENT(id_equipement)
    );'''
    
    mycursor.execute(sql)
    
    sql='''
    INSERT INTO NOTE (note, id_equipement) VALUES 
    (4, 1),
    (2, 1),
    (5, 1),
    (3, 1),
    (4, 1);
    '''
    mycursor.execute(sql)
    
    get_db().commit()
    return redirect('/')
