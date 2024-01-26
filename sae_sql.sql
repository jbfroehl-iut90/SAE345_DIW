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

INSERT INTO MORPHOLOGIE (libelle_morphologie) VALUES
    ('Homme'),
    ('Femme'),
    ('Enfant'),
    ('Unisexe');

INSERT INTO CATEGORIE_SPORT (libelle_categorie_sport) VALUES
        ('Sport de combat'),
        ('Sport collectif'),
        ('Sport de raquettes'),
        ('Sport d endurance'),
        ('Sport aquatique'),
        ('Cyclisme'),
        ('Renforcement Musculaire')
    ;

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

INSERT INTO SPORT (libelle_sport, categorie_sport) VALUES
    ('Muay Thai', 1),
    ('Mixed Martial Art', 1),
    ('Jiu Jitsu Brésilien', 1),
    ('Karate', 1),
    ('Judo', 1),
    ('Football', 2),
    ('Handball', 2),
    ('Volleyball', 2),
    ('Basketball', 2),
    ('Badminton', 3),
    ('Tennis', 3),
    ('Tennis de table', 3),
    ('Squash', 3),
    ('Course à pieds', 4),
    ('Trail', 4),
    ('Natation', 5),
    ('Plongée', 5),
    ('Enduro', 6),
    ('Ville', 6),
    ('Course à vélo', 6),
    ('Musculation', 7),
    ('Crossfit', 7),
    ('Pilate', 7)
    ;

INSERT INTO EQUIPEMENT (libelle_equipement, prix_equipement, description_equipement, image_equipement, taille_equipement, marque_equipement, sport_equipement, couleur_equipement, morphologie_equipement) VALUES
    ( 'Gants  de  MMA  Venum  Impact  2.0' , 80,  'Ces  gants  en  cuir  Skintex  sont  ergonomiques    confortables  et  de  haute  qualité.  La  mousse  triple  densite  permet  de  garder  votre  main  à  l  abris  des  chocs.  Forme  incurvée  permettant  au  gant  de  parfaitement  épouser  la  forme  de  votre  main.  Le  système  de  fermeture  fournit  un  meilleur  serrage  et  la  possibilité  de  fermer  avec  une  seule  main.' , 'gantsMMA.webp', 4, 1, 2, 5, 4),
    ( 'Gants  de  boxe  Venum  Elite' , 90,  'Gants  pour  Boxe  Anglaise    Kick  Boxing  et  Muay  Thai.  Doté  d  une  mousse  à  quadruple  densité    ces  gants  sont  designés  pour  absorber  au  mieux  les  impacts  lors  des  frappes.  Les  coutures  renforcées  et  les  panneaux  en  maille  combinés  à  leur  forme  ergonomique  vous  apporteront  un  ajustement  confortable  et  vous  aurez  l  impression  de  ne  faire  qu  un  avec  le  gant.' , 'gantsBoxe.webp', 4, 1, 1, 1, 4),
    ( 'Kimono  JJB  Venum  Elite  4.0' , 200,  'Ce  Kimono  est  fabriqué  en  coton  Pearl  Wave  450  g/m²  et  est  renforcé  sur  tous  les  points  de  tension  pour  une  plus  grande  durabilité.  Le  col  en  mousse  EVA  rigide  résistera  aux  prises  de  vos  adversaires  et  à  vos  ruptures  de  prise  les  plus  puissantes.  Confortable  et  robuste    il  est  conçu  pour  résister  à  l  usure  des  séances  d  entraînement  intenses.  Le  pantalon  est  fabriqué  en  tissu  Ripstop  285  g/m²  et  est  renforcé  aux  chevilles    aux  genoux  et  à  l  entrejambe.  Les  coutures  renforcées  aux  poignets  assurent  une  plus  grande  longévité' , 'kimonoJJB.webp', 3, 1, 3, 2, 1),
    ('Nunchaku', 40,  'Découvrez  l  élégance  et  la  puissance  du  Nunchaku    un  instrument  emblématique  dans  le  monde  des  arts  martiaux.  Notre  Nunchaku  est  fabriqué  avec  un  artisanat  exceptionnel    offrant  une  combinaison  parfaite  de  durabilité  et  de  performance.  Conçu  pour  les  pratiquants  de  tous  niveaux    cet  article  incarne  la  tradition  tout  en  intégrant  des  éléments  modernes  pour  une  expérience  optimale' , 'nunchaku.jpg', 4, 19, 4, 5, 4),
    ( 'Kimono  de  Judo' , 70,  'Explorez  l  excellence  du  judo  avec  notre  Kimono  de  haute  qualité.  Conçu  pour  répondre  aux  exigences  rigoureuses  des  pratiquants  de  judo    notre  Kimono  allie  confort    durabilité  et  performance  exceptionnelle.  Fabriqué  à  partir  de  matériaux  résistants    il  offre  une  coupe  précise  qui  permet  une  liberté  de  mouvement  maximale  tout  en  conservant  une  élégance  traditionnelle.  Que  vous  soyez  un  débutant  passionné  ou  un  judoka  expérimenté    notre  Kimono  est  un  choix  fiable  pour  vos  séances  d  entraînement  et  compétitions.' , 'kimonoJudo.jpg', 3, 19, 5, 6, 1),
    ( 'Jordan  Zion  3  Pink  Lotus  Enfants  GS' , 110,  'Chaussure  de  basket  Jordan  rose  pour  enfant' , 'chaussureBasket1.webp', 16, 10, 9, 7, 3),
    ( 'Résine  Kempa  200ml  [Taille  200  ml]' , 16,  'résine  en  pot  pour  plus  d  adhérence  en  match' , 'potResineHand1.jpg', 27, 11, 7, 2, 1),
    ( 'filet  de  volley  ball  d  entrainement' , 45,  'filet  de  10*1m  sera  parfait  pour  vos  entrainement' , 'filetVolley1.jpg', 30, 12, 8, 6, 1),
    ( 'pince  nez  flottant  de  natation  bleu  cyan' , 4,  'peur  de  perdre  votre  pince  nez celui  ci  flotte  ' , 'pinceNezNatation1.jpg', 1, 13, 16, 2, 4),
    ( 'Palmes  Cressi  Frog  Plus  Noir/silver' , 65,  'Palmage  fluide  effort  réduit  peu  fatiguant' , 'palmPlongée1.jpg', 1, 14, 17, 5, 4),
    ( 'Soft  flask  250mL  -  28mm' , 18,  'Gourde  accessible facilement  transportable' , 'gourdeCoursePied1.jpg', 27, 15, 14, 2, 4),
    ( 'flash  carbon' , 76,  'léger  transportable  en  fibre  de  carbone' , 'batonTrail1.jpg', 1, 16, 15, 5, 4),
    ( 'Kettlebell  de  musculation  en  fonte  et  base  caoutchouc' , 55,  'kettelbell  de  55kg  a  base  en  caoutchouc  pour  moins  de  dégat' , 'bouleMuscu.jpg', 31, 17, 21, 5, 4),
    ( 'Barre  Olympique  -  Entrainement  2.0  -  20kg' , 207,  'barre  de  crossfit  de  20kg  avec  un  bon  grip' , 'barreCrossfit1.jpg', 32, 18, 22, 9, 4),
    ( 'GYM  BALL  RÉSISTANT  TAILLE  2  /  65  cm  -  BLEU' , 20,  'gymball  avec  une  structure  résitante      peut  etre  utilisé  pour  toutes  exercices' , 'gymballPilat1.jpg', 1, 17, 23, 2, 4),
    ( 'Spectral  29  CF  8' , 4600,  'Du  rapide  et  fluide  au  rugueux  et  technique    le  Spectral  CF  8  est  prêt  à  affronter  tous  les  sentiers  que  vous  lui  indiquerez.' , 'veloEnduro1.webp', 3, 20, 18, 5, 4),
    ( 'Vélo  de  Route  BMC  Teammachine  SLR  Five  Shimano  105  Di2  12V  700  mm  Argent  Arctic  2023' , 3300,  'Vélo  de  course  parfait  pour  rouler  sur  route  et  la  vitesse' , 'veloCourse1.jpg', 3, 21, 19, 6, 4),
    ( 'Electra  Loft  7i  EQ  Step  Thru' , 440,  'La  technologie  Flat  Foot  d  Electra  signifie  un  confort  et  un  contrôle  brevetés  sur  un  vélo  Electra.' , 'veloVille.jpg', 3, 22, 20, 10, 4),
    ( 'X  Crazyfast  Elite  LL  FG' , 270,  'chaussure  de  foot  equipé  de  crampon  silouhette  aérodynamique' , 'chaussureFoot1.avif', 26, 2, 6, 8, 4),
    ( 'Protège-dents  Venum  Predator' , 22,  'Ce  protège-dents    est  le  parfait  mix  en  confort    souplesse  et  absorption  des  chocs    afin  de  prévenir  et  réduire  les  besssures  au  niveau  de  vos  dents    lèvres  et  gencives.  Cadre  extérieur  en  caoutchouc  asborbant  les  chocs    et  intérieur  en  gel  thermo-formable  afin  de  mouler  parfaitement  votre  dentition  et  permettre  une  meilleure  respiration', 'protegeDents.webp', 5, 1, 1, 11, 4),
    ( 'Protège-dents  Venum  Predator' , 22,  'Ce  protège-dents    est  le  parfait  mix  en  confort    souplesse  et  absorption  des  chocs    afin  de  prévenir  et  réduire  les  besssures  au  niveau  de  vos  dents    lèvres  et  gencives.  Cadre  extérieur  en  caoutchouc  asborbant  les  chocs    et  intérieur  en  gel  thermo-formable  afin  de  mouler  parfaitement  votre  dentition  et  permettre  une  meilleure  respiration', 'ProtegeDentKaki.webp', 5, 1, 1, 12, 4);
SELECT libelle_equipement FROM EQUIPEMENT;