DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur (
  id_utilisateur INT AUTO_INCREMENT,
  login varchar(255),
  email varchar(255),
  password varchar(255),
  role varchar(255),
  nom varchar(255),
  est_actif tinyint(1),
  PRIMARY KEY (id_utilisateur)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 ;

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(NULL,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(NULL,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(NULL,'client3','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');