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
    sql = '''DROP TABLE IF EXISTS ligne_panier, ligne_commande, commande, parfum, genre, etat, utilisateur, volume, conditionnement;'''

    mycursor.execute(sql)
    sql = '''
    CREATE TABLE utilisateur(
        id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
        login VARCHAR(50),
        email VARCHAR(50),
        password VARCHAR(255),
        role VARCHAR(50),
        nom VARCHAR(50),
        est_actif BOOLEAN
      )DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES (1,'admin','admin@admin.fr','sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf','ROLE_admin','admin','1'), (2,'client','client@client.fr','sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d','ROLE_client','client','1'), (3,'client2','client2@client2.fr','sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422','ROLE_client','client2','1');
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE genre(
    id_genre INT AUTO_INCREMENT PRIMARY KEY,
    nom_genre VARCHAR(25)
)  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO genre VALUES 
(Null,'Homme'), 
(Null,'Femme'), 
(Null,'Mixte');
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT PRIMARY KEY,
    libelle_etat VARCHAR(50)
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat VALUES (Null,'En attente'), (Null,'Expédié'), (Null,'Validé'), (Null,'Confirmé');
     '''
    mycursor.execute(sql)

    sql = ''' 
        CREATE TABLE conditionnement (
        id_conditionnement INT AUTO_INCREMENT PRIMARY KEY,
        libelle_conditionnement VARCHAR(50)

        )  DEFAULT CHARSET=utf8;  
        '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO conditionnement VALUES (Null,'Verre'),
                                   (Null,'Alluminium');
         '''
    mycursor.execute(sql)

    sql = ''' 
            CREATE TABLE volume (
                id_volume INT AUTO_INCREMENT PRIMARY KEY,
                nom_volume VARCHAR(25)

            )  DEFAULT CHARSET=utf8;  
            '''
    mycursor.execute(sql)
    sql = ''' 
        INSERT INTO volume VALUES(Null,'30ml'),
                         (Null,'50ml'),
                         (Null,'60ml'),
                         (Null,'100ml'),
                         (Null,'125ml'),
                         (Null,'200ml');

             '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE parfum(
    id_parfum INT AUTO_INCREMENT PRIMARY KEY,
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
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO parfum VALUES (Null,'Spider_man',10,1,3,1,'parfum Spider man','ParfumCo','KIDS','spiderman.jpg'),
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
                            (Null,'Eau dombré Leather',116,1,2,1,'Parfum eau dombré Leather','ParfumCo','Tom Ford','eauDombréLeather.jpg'),
                            (Null,'1 million',106.89,2,6,1,'Parfum de riche','ParfumCo','RABANNE','1_million.jpg');



         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT PRIMARY KEY,
    date_achat DATE,
    id_utilisateur INT,
    id_etat INT,

    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_etat) REFERENCES etat(id_etat)
    ) DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande VALUE 
(Null,'2021-06-01',1,1), 
(Null,'2021-06-02',2,1), 
(Null,'2021-06-03',3,1);
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_commande(
    id_commande INT,
    id_parfum INT,
    prix NUMERIC(10,2),
    quantite INT,
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
    FOREIGN KEY (id_parfum) REFERENCES parfum(id_parfum)
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande VALUES (1,1,10,1),( 2,2,10,1),(3,3,15,1);
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_panier(
    id_utilisateur INT,
    id_parfum INT,
    quantite INT,
    date_ajout DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_parfum) REFERENCES parfum(id_parfum)
);

         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
