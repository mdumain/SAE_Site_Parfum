DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS parfum;
DROP TABLE IF EXISTS conditionnement;
DROP TABLE IF EXISTS volume;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS marque;


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
    libelle_genre VARCHAR(25)
);

CREATE TABLE fournisseur(
    id_fournisseur INT AUTO_INCREMENT PRIMARY KEY,
    nom_fournisseur VARCHAR(25)
);

CREATE TABLE marque(
    id_marque INT AUTO_INCREMENT PRIMARY KEY,
    nom_marque VARCHAR(25)
);

CREATE TABLE parfum(
    id_parfum INT AUTO_INCREMENT PRIMARY KEY ,
    nom_parfum VARCHAR(50),
    prix_parfum DECIMAL(10,2),
    conditionnement_id INT,
    volume_id INT,
    genre_id INT,
    marque_id INT,
    fournisseur_id INT,
    description VARCHAR(1000),
    image VARCHAR(50),
    CONSTRAINT fk_parfum_marque FOREIGN KEY (marque_id) REFERENCES marque(id_marque),
    CONSTRAINT fk_parfum_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    CONSTRAINT fk_parfum_conditionnement FOREIGN KEY (conditionnement_id) REFERENCES conditionnement(id_conditionnement),
    CONSTRAINT fk_parfum_volume FOREIGN KEY (volume_id) REFERENCES volume(id_volume),
    CONSTRAINT fk_parfum_genre FOREIGN KEY (genre_id) REFERENCES genre(id_genre)
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

INSERT INTO conditionnement VALUES
                                (Null,'Verre'),
                                (Null,'Alluminium');

INSERT INTO volume VALUES(Null,'30ml'),
                         (Null,'50ml'),
                         (Null,'60ml'),
                         (Null,'100ml'),
                         (Null,'125ml'),
                         (Null,'200ml'),
                         (Null, '150ml'),
                         (Null, '250ml');


INSERT INTO genre VALUES (Null,'Homme'),
                         (Null,'Femme'),
                         (Null,'Mixte');

INSERT INTO fournisseur VALUES
                            (1, 'ParfumCo'),
                            (2, 'LuxeParfums'),
                            (3, 'EcoScents');

INSERT INTO marque VALUES
    (1, 'KIDS'),
    (2, 'Dior'),
    (3, 'Gucci'),
    (4, 'Coco Chanel'),
    (5, 'Yves Saint Laurent'),
    (6, 'Jean-Paul Gaultier'),
    (7, 'Tom Ford'),
    (8, 'Paco Rabanne'),
    (9, 'Creed'),
    (10, 'Viktor&Rolf'),
    (11, 'Valentino'),
    (12, 'Azzaro'),
    (13, 'Lancôme'),
    (14, 'Dolce & Gabana'),
    (15, 'Carolina Herrera'),
    (16, 'Elizabeth Arden'),
    (17, 'Birkholz');

INSERT INTO parfum VALUES
                       (NULL, 'Spider-Man', 10, 1, 3, 1, 1, 1, 'Un parfum dynamique et énergisant, inspiré par l\'agilité et l\'héroïsme de Spider-Man. Notes de citron, de gingembre et de bois.', 'spiderman.jpg'),
                       (NULL, 'Pat\' Patrouille', 10, 1, 1, 1, 1, 1, 'Un parfum joyeux et ludique, parfait pour les enfants. Notes de fruits rouges, de vanille et de sucre.', 'patpatrouille.jpg'),
                       (NULL, 'Barbaparfum', 15, 1, 3, 3, 9, 1, 'Un parfum doux et réconfortant, inspiré par l\'univers coloré de Barbapapa. Notes de miel, de fleurs blanches et de musc.', 'barbaparfum.jpg'),
                       (NULL, 'Barbie', 5, 1, 1, 2, 1, 1, 'Un parfum féminin et glamour, capturant l\'essence de Barbie. Notes de fleurs roses, de framboise et de vanille.', 'barbie.jpg'),
                       (NULL, 'Sauvage', 60, 2, 4, 1, 2, 2, 'Un parfum sauvage et intense, pour l\'homme moderne et audacieux. Notes de bergamote, de poivre et d\'ambroxan.', 'sauvage.jpg'),
                       (NULL, 'Invictus', 95, 1, 4, 1, 8, 2, 'Un parfum victorieux et puissant, pour ceux qui repoussent les limites. Notes de pamplemousse, de laurier et de bois ambré.', 'invictus.jpg'),
                       (NULL, 'Flora Gorgeous Magnolia', 170, 1, 4, 2, 3, 2, 'Un parfum floral et élégant, inspiré par la beauté éclatante du magnolia. Notes de magnolia, de jasmin et de bois de santal.', 'gucci.jpg'),
                       (NULL, 'Spicebomb', 90, 1, 2, 1, 10, 3, 'Un parfum explosif et épicé, pour les hommes qui osent. Notes de piment, de tabac et de cuir.', 'spiceBomb.jpg'),
                       (NULL, 'Born in Roma Uomo', 60, 1, 3, 1, 11, 3, 'Un parfum italien sophistiqué, capturant l\'esprit de Rome. Notes de lavande, de géranium et de bois de vétiver.', 'valentino.jpg'),
                       (NULL, 'Coco Mademoiselle', 90, 1, 1, 2, 4, 2, 'Un parfum intemporel et féminin, pour la femme moderne. Notes de rose, de patchouli et de vanille.', 'coco_mademoiselle.jpg'),
                       (NULL, 'The Most Wanted', 54, 1, 2, 1, 12, 3, 'Un parfum audacieux et séduisant, pour les hommes qui attirent tous les regards. Notes de cardamome, de bois précieux et d\'ambre.', 'mostWanted.jpg'),
                       (NULL, 'Black Opium', 74, 1, 2, 2, 5, 2, 'Un parfum addictif et mystérieux, pour les femmes qui aiment briller dans l\'ombre. Notes de café, de vanille et de fleurs blanches.', 'black_opium.jpg'),
                       (NULL, 'Le Beau', 104.99, 1, 5, 1, 6, 2, 'Un parfum frais et ensoleillé, pour l\'homme moderne et élégant. Notes de noix de coco, de bergamote et de bois de cèdre.', 'le_beau.jpg'),
                       (NULL, 'Ombre Leather', 116, 1, 2, 1, 7, 2, 'Un parfum sombre et sensuel, inspiré par le cuir et les ombres mystérieuses. Notes de cuir, de violette et de patchouli.', 'ombre_leather.jpg'),
                       (NULL, '1 Million', 106.89, 1, 6, 1, 8, 2, 'Un parfum luxueux et audacieux, pour ceux qui vivent sans limites. Notes de sangria, de rose et de cuir.', '1_million.jpg'),
                       (NULL, 'J\'adore', 120, 2, 4, 2, 2, 2, 'Un parfum floral et ensoleillé, symbole de féminité et de grâce. Notes de jasmin, de rose et de ylang-ylang.', 'j_adore.jpg'),
                       (NULL, 'Light Blue', 85, 1, 2, 3, 14, 2, 'Un parfum frais et lumineux, inspiré par la Méditerranée. Notes de citron, de pomme et de cèdre.', 'light_blue.jpg'),
                       (NULL, 'La Vie Est Belle', 160, 1, 7, 2, 13, 2, 'Un parfum gourmand et optimiste, célébrant le bonheur de vivre. Notes de patchouli, d\'iris et de vanille.', 'la_vie_est_belle.jpg'),
                       (NULL, 'Acqua di Gio', 95, 1, 4, 1, 5, 2, 'Un parfum aquatique et rafraîchissant, inspiré par la mer Méditerranée. Notes de bergamote, de jasmin et de bois de santal.', 'acqua_di_gio.jpg'),
                       (NULL, 'Le Male', 100, 1, 5, 1, 6, 2, 'Un parfum iconique et viril, pour l\'homme moderne et séduisant. Notes de lavande, de vanille et de menthe.', 'le_male.jpg'),
                       (NULL, 'Black Orchid', 150, 1, 6, 2, 7, 2, 'Un parfum intense et mystérieux, pour les femmes qui osent être différentes. Notes de truffe, d\'orchidée noire et de patchouli.', 'black_orchid.jpg'),
                       (NULL, 'Good Girl', 110, 1, 4, 2, 15, 2, 'Un parfum audacieux et sensuel, pour la femme qui sait ce qu\'elle veut. Notes de café, de tubéreuse et de vanille.', 'good_girl.jpg'),
                       (NULL, 'Aventus', 300, 1, 8, 1, 9, 2, 'Un parfum légendaire et puissant, pour les hommes qui dominent le monde. Notes d\'ananas, de bouleau et de musc.', 'aventus.jpg'),
                       (NULL, 'Green Tea', 30, 1, 4, 3, 16, 3, 'Un parfum frais et naturel, inspiré par la sérénité du thé vert. Notes de thé vert, de citron et de fleurs blanches.', 'green_tea.jpg'),
                       (NULL, 'Citrus Splash', 25, 1, 4, 3, 17, 3, 'Un parfum énergisant et pétillant, parfait pour un regain de vitalité. Notes de citron, de mandarine et de bergamote.', 'citrus_splash.jpg');

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

SELECT parfum.id_parfum, parfum.nom_parfum, parfum.prix_parfum, conditionnement.libelle_conditionnement, volume.nom_volume, genre.libelle_genre, marque.nom_marque, fournisseur.nom_fournisseur, parfum.description, parfum.image
FROM parfum JOIN conditionnement ON conditionnement_id = id_conditionnement
JOIN fournisseur ON id_fournisseur = fournisseur_id
JOIN genre ON id_genre = genre_id
JOIN marque  ON marque_id = id_marque
JOIN volume ON volume_id = id_volume
ORDER BY prix_parfum;
