#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    # Drop les tazbles en commençant par la fin pour éviter les erreurs de contraintes
    sql=''' DROP TABLE IF EXISTS historique, liste_envie, commentaires, ligne_panier, ligne_commande, declinaison, note, commentaire, commande, adresse, etat, equipement, utilisateur, marque, taille, morphologie, couleur, categorie_sport;'''
    mycursor.execute(sql)

    sql='''
    CREATE TABLE utilisateur (
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
    CREATE TABLE categorie_sport(
    id_categorie_sport INT AUTO_INCREMENT,
    libelle_categorie_sport VARCHAR(255),
    PRIMARY KEY(id_categorie_sport)
    );
    '''
    mycursor.execute(sql)
    
    sql=''' 
    INSERT INTO categorie_sport (libelle_categorie_sport) VALUES
        ('Sport de combat'),
        ('Sport collectif'),
        ('Sport de raquettes'),
        ('Sport d endurance'),
        ('Sport aquatique'),
        ('Cyclisme'),
        ('Renforcement Musculaire'),
        ('Autre'),
        ('Sans catégorie');
    ;
    '''
    
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE couleur(
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(255),
    couleur_anglais VARCHAR(255),
    PRIMARY KEY(id_couleur)
);
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO couleur(libelle_couleur, couleur_anglais) VALUES
    ('Rouge', 'red'),
    ('Bleu', 'blue'),
    ('Vert', 'green'),
    ('Violet', 'violet'),
    ('Noir', 'black'),
    ('Blanc', 'white'),
    ('Rose', 'pink'),
    ('Jaune', 'yellow'),
    ('Gris', 'grey'),
    ('Marron', 'brown'),
    ('Orange', 'orange'),
    ('Kaki', 'khaki'),
    ('Aucune', 'grey');
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE morphologie(
    id_morphologie INT AUTO_INCREMENT,
    libelle_morphologie VARCHAR(255),
    PRIMARY KEY(id_morphologie)
);
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO morphologie (libelle_morphologie) VALUES
    ('Homme'),
    ('Femme'),
    ('Enfant'),
    ('Unisexe');
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE marque(
    id_marque INT AUTO_INCREMENT,
    libelle_marque VARCHAR(255),
    PRIMARY KEY(id_marque)
);
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO marque (libelle_marque) VALUES
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
    CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY(id_taille)
);
         '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO taille (libelle_taille) VALUES
    ('XS'),
    ('S'),
    ('M'),
    ('L'),
    ('XL'),
    ('XXL'),
    ('XXXL'),
    ('Article seul'),
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
    CREATE TABLE equipement(
    id_equipement INT AUTO_INCREMENT,
    libelle_equipement VARCHAR(10000),
    prix_equipement INT,
    description_equipement VARCHAR(1000),
    image_equipement VARCHAR(1000),
    marque_equipement_id INT,
    sport_equipement_id INT,
    morphologie_equipement_id INT,
    PRIMARY KEY(id_equipement),
    CONSTRAINT fk_equipement_marque FOREIGN KEY (marque_equipement_id) REFERENCES marque(id_marque),
    CONSTRAINT fk_equipement_sport FOREIGN KEY (sport_equipement_id) REFERENCES categorie_sport(id_categorie_sport),
    CONSTRAINT fk_equipement_morphologie FOREIGN KEY (morphologie_equipement_id) REFERENCES morphologie(id_morphologie)
);
          '''
    mycursor.execute(sql)

    
    sql = '''
    INSERT INTO equipement (libelle_equipement, prix_equipement, description_equipement, image_equipement, marque_equipement_id, sport_equipement_id, morphologie_equipement_id) VALUES
    ( 'Gants  de  MMA  Venum  Impact  2.0' , 80,  'Ces  gants  en  cuir  Skintex  sont  ergonomiques    confortables  et  de  haute  qualité.  La  mousse  triple  densite  permet  de  garder  votre  main  à  l  abris  des  chocs.  Forme  incurvée  permettant  au  gant  de  parfaitement  épouser  la  forme  de  votre  main.  Le  système  de  fermeture  fournit  un  meilleur  serrage  et  la  possibilité  de  fermer  avec  une  seule  main.' , 'gantsMMA.webp', 1, 1, 4),
    ( 'Gants  de  boxe  Venum  Elite' , 90,  'Gants  pour  Boxe  Anglaise    Kick  Boxing  et  Muay  Thai.  Doté  d  une  mousse  à  quadruple  densité    ces  gants  sont  designés  pour  absorber  au  mieux  les  impacts  lors  des  frappes.  Les  coutures  renforcées  et  les  panneaux  en  maille  combinés  à  leur  forme  ergonomique  vous  apporteront  un  ajustement  confortable  et  vous  aurez  l  impression  de  ne  faire  qu  un  avec  le  gant.' , 'gantsBoxe.webp', 1, 1, 4),
    ( 'Kimono  JJB  Venum  Elite  4.0' , 200,  'Ce  Kimono  est  fabriqué  en  coton  Pearl  Wave  450  g/m²  et  est  renforcé  sur  tous  les  points  de  tension  pour  une  plus  grande  durabilité.  Le  col  en  mousse  EVA  rigide  résistera  aux  prises  de  vos  adversaires  et  à  vos  ruptures  de  prise  les  plus  puissantes.  Confortable  et  robuste    il  est  conçu  pour  résister  à  l  usure  des  séances  d  entraînement  intenses.  Le  pantalon  est  fabriqué  en  tissu  Ripstop  285  g/m²  et  est  renforcé  aux  chevilles    aux  genoux  et  à  l  entrejambe.  Les  coutures  renforcées  aux  poignets  assurent  une  plus  grande  longévité' , 'kimonoJJB.webp', 1, 3, 1),
    ('Nunchaku', 40,  'Découvrez  l  élégance  et  la  puissance  du  Nunchaku    un  instrument  emblématique  dans  le  monde  des  arts  martiaux.  Notre  Nunchaku  est  fabriqué  avec  un  artisanat  exceptionnel    offrant  une  combinaison  parfaite  de  durabilité  et  de  performance.  Conçu  pour  les  pratiquants  de  tous  niveaux    cet  article  incarne  la  tradition  tout  en  intégrant  des  éléments  modernes  pour  une  expérience  optimale' , 'nunchaku.jpg', 19, 1, 4),
    ( 'Kimono  de  Judo' , 70,  'Explorez  l  excellence  du  judo  avec  notre  Kimono  de  haute  qualité.  Conçu  pour  répondre  aux  exigences  rigoureuses  des  pratiquants  de  judo    notre  Kimono  allie  confort    durabilité  et  performance  exceptionnelle.  Fabriqué  à  partir  de  matériaux  résistants    il  offre  une  coupe  précise  qui  permet  une  liberté  de  mouvement  maximale  tout  en  conservant  une  élégance  traditionnelle.  Que  vous  soyez  un  débutant  passionné  ou  un  judoka  expérimenté    notre  Kimono  est  un  choix  fiable  pour  vos  séances  d  entraînement  et  compétitions.' , 'kimonoJudo.jpg', 19, 1, 1),
    ( 'Jordan  Zion  3  Pink  Lotus  Enfants  GS' , 110,  'Chaussure  de  basket  Jordan  rose  pour  enfant' , 'chaussureBasket1.webp', 10, 2, 3),
    ( 'Résine  Kempa  200ml  [Taille  200  ml]' , 16,  'résine  en  pot  pour  plus  d  adhérence  en  match' , 'potResineHand1.jpg', 11, 2, 1),
    ( 'filet  de  volley  ball  d  entrainement' , 45,  'filet  de  10*1m  sera  parfait  pour  vos  entrainement' , 'filetVolley1.jpg', 12, 2, 1),
    ( 'pince  nez  flottant  de  natation  bleu  cyan' , 4,  'peur  de  perdre  votre  pince  nez celui  ci  flotte  ' , 'pinceNezNatation1.jpg', 13, 5, 4),
    ( 'Palmes  Cressi  Frog  Plus  Noir/silver' , 65,  'Palmage  fluide  effort  réduit  peu  fatiguant' , 'palmPlongée1.jpg', 14, 5, 4),
    ( 'Soft  flask  250mL  -  28mm' , 18,  'Gourde  accessible facilement  transportable' , 'gourdeCoursePied1.jpg', 15, 4, 4),
    ( 'flash  carbon' , 76,  'léger  transportable  en  fibre  de  carbone' , 'batonTrail1.jpg', 16, 4, 4),
    ( 'Kettlebell  de  musculation  en  fonte  et  base  caoutchouc' , 55,  'kettelbell  de  55kg  a  base  en  caoutchouc  pour  moins  de  dégat' , 'bouleMuscu.jpg', 17, 7, 4),
    ( 'Barre  Olympique  -  Entrainement  2.0  -  20kg' , 207,  'barre  de  crossfit  de  20kg  avec  un  bon  grip' , 'barreCrossfit1.jpg', 18, 7, 4),
    ( 'GYM  BALL  RÉSISTANT  TAILLE  2  /  65  cm  -  BLEU' , 20,  'gymball  avec  une  structure  résitante      peut  etre  utilisé  pour  toutes  exercices' , 'gymballPilat1.jpg', 17, 7, 4),
    ( 'Spectral  29  CF  8' , 4600,  'Du  rapide  et  fluide  au  rugueux  et  technique    le  Spectral  CF  8  est  prêt  à  affronter  tous  les  sentiers  que  vous  lui  indiquerez.' , 'veloEnduro1.webp', 20, 6, 4),
    ( 'Vélo  de  Route  BMC  Teammachine  SLR  Five  Shimano  105  Di2  12V  700  mm  Argent  Arctic  2023' , 3300,  'Vélo  de  course  parfait  pour  rouler  sur  route  et  la  vitesse' , 'veloCourse1.jpg', 21, 6, 4),
    ( 'Electra  Loft  7i  EQ  Step  Thru' , 440,  'La  technologie  Flat  Foot  d  Electra  signifie  un  confort  et  un  contrôle  brevetés  sur  un  vélo  Electra.' , 'veloVille.jpg', 22, 6, 4),
    ( 'X  Crazyfast  Elite  LL  FG' , 270,  'chaussure  de  foot  equipé  de  crampon  silouhette  aérodynamique' , 'chaussureFoot1.avif', 2, 2, 4),
    ( 'Protège-dents  Venum  Predator' , 22,  'Ce  protège-dents    est  le  parfait  mix  en  confort    souplesse  et  absorption  des  chocs    afin  de  prévenir  et  réduire  les  besssures  au  niveau  de  vos  dents    lèvres  et  gencives.  Cadre  extérieur  en  caoutchouc  asborbant  les  chocs    et  intérieur  en  gel  thermo-formable  afin  de  mouler  parfaitement  votre  dentition  et  permettre  une  meilleure  respiration', 'protegeDents.webp', 1, 1, 4);
     '''
    
    mycursor.execute(sql)
    
    sql='''
CREATE TABLE note(
    id_note INT AUTO_INCREMENT,
    note DECIMAL(2,1),
    id_equipement INT,
    utilisateur_id INT,
    PRIMARY KEY(id_note),
    CONSTRAINT fk_note_equipement FOREIGN KEY(id_equipement) REFERENCES equipement(id_equipement),
    CONSTRAINT fk_note_utilisateur FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur));'''    
    mycursor.execute(sql)
    
    sql='''
    INSERT INTO note (note, id_equipement, utilisateur_id) VALUES 
    (5.0, 1, 3),
    (4.5, 1, 2),
    (4.5, 1, 3),
    (4.5, 2, 2),
    (2.0, 3, 3),
    (3.5, 3, 1),
    (5.0, 4, 3),
    (4.5, 4, 3),
    (4.5, 4, 3),
    (2.0, 4, 1),
    (1.0, 5, 2),
    (1.0, 5, 2),
    (1.0, 5, 2),
    (1.0, 5, 2),
    (3.5, 6, 3),
    (5.0, 6, 3),
    (4.5, 7, 3),
    (3.5, 8, 3),
    (2.0, 9, 3),
    (3.5, 8, 3),
    (2.0, 9, 3),
    (1.0, 10, 3),
    (3.5, 9, 1),
    (2.0, 10, 3),
    (1.0, 10, 2),
    (5.0, 11, 3),
    (4.5, 11, 3),
    (3.5, 11, 3),
    (2.0, 11, 3),
    (1.0, 11, 3),
    (4.5, 12, 3),
    (3.5, 13, 3),
    (3.5, 13, 3),
    (2.0, 15, 3),
    (1.0, 16, 3),
    (4.5, 17, 3),
    (5.0, 17, 3),
    (5.0, 17, 3),
    (5.0, 17, 3),
    (4.5, 18, 3),
    (3.5, 19, 3),
    (3.5, 20, 3),
    (5.0, 1, 3),
    (3.5, 19, 3),
    (3.5, 20, 3)
    ;'''
    mycursor.execute(sql)
    

    sql = '''
    CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY(id_etat)
);
            '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO etat (libelle_etat) VALUES
    ('En cours de traitement'),
    ('Expédié'),
    ('Validé');
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE adresse(
    id_adresse INT AUTO_INCREMENT,
    adresse VARCHAR(255),
    code_postal VARCHAR(255),
    ville VARCHAR(255),
    valide tinyint(1),
    departement INT,
    nom VARCHAR(255),
    id_utilisateur INT,
    PRIMARY KEY(id_adresse),
    CONSTRAINT fk_adresse_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    );'''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO adresse (adresse, code_postal, ville, valide, departement, nom, id_utilisateur) VALUES
    ('1 rue du groudron par terre', '75000', 'Paris',1, 75, 'Jean', 2),
    ('2 rue des petits canards', '69000', 'Lyon',0, 69, 'Jeanne', 2),
    ('4 chemin du pont', '31500', 'Toulouse',1, 31, 'Jeanne', 2),
    ('5 rue du grand mechant loup', '93000', 'Lyon',1, 69, 'Jean', 2),
    ('6 rue des petits canards', '69000', 'Lyon',1, 69, 'Jeanne', 3),
    ('7 chemin du pont', '31500', 'Toulouse',1, 31, 'Jeanne', 3),
    ('8 rue de géplusdinspi', '93000', 'Lyon',1, 69, 'Jean', 3);
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    etat_id INT NOT NULL,
    id_utilisateur INT,
    adresse_id INT,
    billing_address_id INT,
    PRIMARY KEY(id_commande),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    CONSTRAINT fk_commande_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    CONSTRAINT fk_commande_adresse FOREIGN KEY (adresse_id) REFERENCES adresse(id_adresse),
    CONSTRAINT fk_commande_billing_address FOREIGN KEY (billing_address_id) REFERENCES adresse(id_adresse)
);
            '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO commande (date_achat, etat_id, id_utilisateur, adresse_id, billing_address_id) VALUES
    ('2022-11-10', 1, 2, 1, 1),
    ('2022-11-11', 2, 2, 2, 2),
    ('2022-11-13', 3, 2, 3, 2);
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE declinaison(
    id_declinaison INT AUTO_INCREMENT,
    couleur_declinaison INT,
    taille_declinaison INT,
    stock INT,
    id_equipement INT,
    PRIMARY KEY(id_declinaison),
    CONSTRAINT fk_declinaison_equipement FOREIGN KEY (id_equipement) REFERENCES equipement(id_equipement),
    CONSTRAINT fk_declinaison_taille FOREIGN KEY (taille_declinaison) REFERENCES taille(id_taille),
    CONSTRAINT fk_declinaison_couleur FOREIGN KEY (couleur_declinaison) REFERENCES couleur(id_couleur)
);
            '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO declinaison (couleur_declinaison, taille_declinaison, stock, id_equipement) VALUES
    (1, 1, 10, 1),
    (2, 2, 10, 1),
    (3, 3, 10, 1),
    (1, 4, 10, 2),
    (1, 5, 10, 2),
    (1, 6, 10, 2),
    (1, 7, 10, 3),
    (1, 8, 10, 3),
    (1, 9, 10, 3),
    (1, 10, 10, 4),
    (1, 11, 10, 4),
    (1, 12, 10, 4),
    (1, 13, 10, 5),
    (1, 14, 10, 5),
    (1, 15, 10, 5),
    (1, 16, 10, 6),
    (1, 17, 10, 6),
    (1, 18, 10, 6),
    (3, 1, 10, 7),
    (2, 1, 10, 7),
    (1, 1, 10, 7),
    (3, 2, 10, 8),
    (2, 2, 10, 8),
    (1, 2, 10, 8),
    (3, 3, 10, 9),
    (2, 3, 10, 9),
    (1, 3, 10, 9),
    (3, 4, 10, 10),
    (2, 4, 10, 10),
    (1, 4, 10, 10),
    (3, 5, 10, 11),
    (2, 5, 10, 11),
    (1, 5, 10, 11),
    (3, 6, 10, 12),
    (2, 6, 10, 12),
    (1, 6, 10, 12),
    (3, 7, 10, 13),
    (2, 7, 10, 13),
    (1, 7, 10, 13),
    (3, 8, 10, 14),
    (2, 8, 10, 14),
    (1, 8, 10, 14),
    (3, 9, 10, 15),
    (2, 9, 10, 15),
    (1, 9, 10, 15),
    (3, 10, 10, 16),
    (2, 10, 10, 16),
    (1, 10, 10, 16),
    (3, 11, 10, 17),
    (2, 11, 10, 17),
    (1, 11, 10, 17),
    (3, 12, 10, 18),
    (2, 12, 10, 18),
    (1, 12, 10, 18),
    (3, 13, 10, 19),
    (2, 13, 10, 19),
    (1, 13, 10, 19),
    (3, 14, 10, 20),
    (2, 14, 10, 20),
    (1, 14, 10, 20);
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande(
    commande_id INT,
    declinaison_id INT,
    prix INT,
    quantite INT,
    PRIMARY KEY(commande_id, declinaison_id),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    CONSTRAINT fk_ligne_commande_declinaison FOREIGN KEY (declinaison_id) REFERENCES declinaison(id_declinaison)
    );'''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_commande (commande_id, declinaison_id, prix, quantite) VALUES
    (1, 1, 80, 1),
    (1, 2, 80, 1),
    (2, 7, 200, 2),
    (3, 11, 40, 4);
    '''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE ligne_panier(
    id_ligne_panier INT AUTO_INCREMENT,
    quantite INT,
    prix INT,
    id_declinaison INT,
    id_utilisateur INT,
    PRIMARY KEY(id_ligne_panier),
    CONSTRAINT fk_ligne_panier_declinaison FOREIGN KEY (id_declinaison) REFERENCES declinaison(id_declinaison),
    CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
); 
            '''
    mycursor.execute(sql)

    sql='''CREATE TABLE commentaire(
    id_commentaire INT AUTO_INCREMENT,
    commentaire VARCHAR(511),
    statut INT,
    date_publication DATE,
    equipement_id INT,
    utilisateur_id INT,
    PRIMARY KEY(id_commentaire),
    CONSTRAINT fk_commentaire_equipement FOREIGN KEY (equipement_id) REFERENCES equipement(id_equipement),
    CONSTRAINT fk_commentaire_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
    );'''
    
    mycursor.execute(sql)

    sql='''INSERT INTO commentaire (commentaire, statut, date_publication, equipement_id, utilisateur_id) VALUES
('Super produit (publié le 17/11)', 1, '2022-11-17', 1, 3),
('Bonne qualité (publié le 15/11)', 1, '2022-11-15', 1, 2),
('Je suis satisfait', 1, '2022-11-19', 2, 2),
('A acheter', 0, '2022-11-12 10:15:15', 5, 2),
('Super nickel', 1, '2022-10-11', 4, 2),
('Mauvaise qualité', 0, '2022-11-11', 3, 3),
('Déjà cassé', 0, '2022-11-11', 1, 2),
('A éviter', 0, '2022-11-11', 1, 3),
('Je suis déçu', 1, '2022-11-11', 1, 2),
('Je recommande', 1, '2022-11-11', 1, 2),
('Je suis satisfait', 1, '2022-11-11', 5, 2),
('Abimé', 0, '2022-11-11', 5, 2),
('Je suis satisfait', 0, '2022-11-11', 5, 2),
('Acheter pour mon fils', 1, '2022-11-11', 6, 3),
('Bonne qualité', 1, '2022-11-11', 7, 3),
('Je suis satisfait', 1, '2022-11-11', 7, 3),
('Je recommande', 1, '2022-11-11', 8, 2),
('Je suis satisfait', 0, '2022-11-11', 9, 2),
('Je recommande', 0, '2022-11-11', 10, 2),
('Je suis satisfait', 1, '2022-11-11', 11, 2),
('Je recommande', 1, '2022-11-11', 14, 2),
('Je suis satisfait', 1, '2022-11-11', 15, 2),
('Je recommande', 0, '2022-11-11', 16, 2),
('Je suis satisfait', 1, '2022-11-11', 17, 2),
('Je recommande', 0, '2022-11-11', 18, 2),
('Je suis satisfait', 1, '2022-11-11', 19, 2),
('Je recommande', 1, '2022-11-11', 20, 2),
('Je suis satisfait', 1, '2022-11-11', 19, 2),
('Je recommande', 1, '2022-11-11', 20, 2);
'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE liste_envie(
    id_liste_envie INT AUTO_INCREMENT,
    id_utilisateur INT,
    id_equipement INT,
    date_ajout DATE,
    ordre INT,
    PRIMARY KEY(id_liste_envie, id_utilisateur, id_equipement),
    CONSTRAINT fk_liste_envie_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    CONSTRAINT fk_liste_envie_equipement FOREIGN KEY (id_equipement) REFERENCES equipement(id_equipement)
    );
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO liste_envie (id_utilisateur, id_equipement, date_ajout, ordre) VALUES
    (2, 1, '2022-11-10',1),
    (2, 2, '2022-11-11',3),
    (2, 3, '2022-11-13',3),
    (2, 4, '2022-11-14',4),
    (2, 14, '2023-12-12', 5),
    (3, 15, '2021-12-10', 1),
    (3, 3, '2023-10-10', 2),
    (3, 1, '2020-08-10', 3),
    (3, 8, '2021-11-06', 4);    '''
    mycursor.execute(sql)
    
    sql=  '''
    CREATE TABLE historique(
        id_historique INT AUTO_INCREMENT,
        id_utilisateur INT,
        id_equipement INT,
        date_consultation DATE,
        nombre_consultation INT,
        PRIMARY KEY(id_historique),
        CONSTRAINT fk_historique_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_historique_equipement FOREIGN KEY (id_equipement) REFERENCES equipement(id_equipement)
        );
        '''
    mycursor.execute(sql)
    
    sql = '''
    INSERT INTO historique (id_utilisateur, id_equipement, date_consultation, nombre_consultation) VALUES
    (2, 1, '2024-02-04', 2),
    (2, 2, '2024-03-04', 1),
    (2, 3, '2024-03-02', 1),
    (2, 4, '2024-03-05', 1),
    (3, 15, '2024-03-07', 3),
    (3, 3, '2024-03-09', 4),
    (3, 1, '2024-03-11', 5),
    (3, 8, '2024-03-12', 8);
    '''
    mycursor.execute(sql)
    
    get_db().commit()
    return redirect('/')