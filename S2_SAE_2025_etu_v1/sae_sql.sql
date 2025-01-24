DROP TABLE IF EXISTS parfum;
DROP TABLE IF EXISTS conditionnement;
DROP TABLE IF EXISTS volume;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;


CREATE TABLE utilisateur
(
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(255),
    role VARCHAR(50),
    nom VARCHAR(50),
    est_actif BOOLEAN
);


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


CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT PRIMARY KEY,
    libelle_etat VARCHAR(50)
);

CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT PRIMARY KEY,
    date_achat DATE,
    id_utilisateur INT,
    id_etat INT,

    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_etat) REFERENCES etat(id_etat)
    );

CREATE TABLE ligne_commande(
    id_commande INT,
    id_parfum INT,
    prix NUMERIC(10,2),
    quantite INT,
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
    FOREIGN KEY (id_parfum) REFERENCES parfum(id_parfum)

);

CREATE TABLE ligne_panier(
    id_utilisateur INT,
    id_parfum INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (id_utilisateur,id_parfum,date_ajout),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_parfum) REFERENCES parfum(id_parfum)
);

CREATE TABLE conditionnement(
    id_conditionnement INT AUTO_INCREMENT PRIMARY KEY,
    libelle_conditionnement VARCHAR(50)
);

CREATE TABLE volume(
    id_volume INT AUTO_INCREMENT PRIMARY KEY,
    nom_volume VARCHAR(25)
);

CREATE TABLE genre(
    id_genre INT AUTO_INCREMENT PRIMARY KEY,
    nom_genre VARCHAR(25)
);

CREATE TABLE parfum(
    id_parfum INT AUTO_INCREMENT PRIMARY KEY ,
    nom_parfum VARCHAR(50),
    prix_parfum DECIMAL(10,2),
    conditionnement_id INT,
    volume_id INT,
    genre_id INT,
    description VARCHAR(500),
    fournisseur VARCHAR(50),
    marque VARCHAR(25),
    image VARCHAR(50),
    CONSTRAINT fk_parfum_conditionnement FOREIGN KEY (conditionnement_id) REFERENCES conditionnement(id_conditionnement),
    CONSTRAINT fk_parfum_volume FOREIGN KEY (volume_id) REFERENCES volume(id_volume),
    CONSTRAINT fk_parfum_genre FOREIGN KEY (genre_id) REFERENCES genre(id_genre)
);

INSERT INTO conditionnement VALUES (Null,'Verre'),
                                   (Null,'Alluminium');

INSERT INTO volume VALUES(Null,'30ml'),
                         (Null,'50ml'),
                         (Null,'60ml'),
                         (Null,'100ml'),
                         (Null,'125ml'),
                         (Null,'200ml');


INSERT INTO genre VALUES (Null,'Homme');
INSERT INTO genre VALUES (Null,'Femme');
INSERT INTO genre VALUES (Null,'Mixte');

INSERT INTO parfum VALUE (Null,'Spider_man',10,1,3,1,'parfum Spider man','ParfumCo','KIDS','spiderman.jpg'),
                            (Null,'patt patrouille',10,1,1,1,'parfum pat patrouille','ParfumCo','KIDS','patpatrouille.jpg'),
                            (Null,'Barbaparfum',15,1,3,3,'Le parfum Barbapapa','ParfumCo','ARZER','barbaparfum.jpg'),
                            (Null,'Barbie',5,1,1,2,'le parfum de Barbie','ParfumCo','KIDS','barbie.jpg'),
                            (Null,'Sauvage',60,1,4,1,'Le parfum sauvage','ParfumCo','Dior','sauvage.jpg'),
                            (Null,'Invictus',95,1,4,1,'Parfum Invictus','ParfumCo','Rabane','invictus.jpg'),
                            (Null,'Flora Gorgeous Magnolia',170,2,4,2,'Le parfum a l odeur de magnolia','ParfumCo','Gucci','gucci.jpg'),
                            (Null,'Spice-Bomb',90,1,2,1,'le parfum qui explose','ParfumCo','VIKTOR&ROLF','spiceBomb.jpg'),
                            (Null,'BORN IN ROMA UOMO',60,1,3,1,'Le parfum italien','ParfumCo','Valentino','valentino.jpg'),
                            (Null,'Coco ma demoiselle',90,1,1,2,'parfum qui sent bon','ParfumCo','Coco chanel','coco-mademoiselle.jpg'),
                            (Null,'The most wanted',54,1,2,1,'Parfum de brigand','ParfumCo','AZZARO','mostWanted.jpg'),
                            (Null,'Black opium',74,1,2,2,'parfum black opium','ParfumCo','Yves Saint Laurent','blackopium.jpg'),
                            (Null,'Le Beau',104.99,1,5,1,'Parfum pour homme beau','ParfumCo','Jean-Paul Gaultier','leBeau.jpg'),
                            (Null,'Eau d\'ombré Leather',116,1,2,1,'Parfum eau d\'ombré Leather','ParfumCo','Tom Ford','eauDombréLeather.jpg'),
                            (Null,'1 million',106.89,2,6,1,'Parfum de riche','ParfumCo','RABANNE','1_million.jpg');


SELECT * FROM parfum;
SELECT * FROM conditionnement;
SELECT * FROM volume;
SELECT * FROM genre;
