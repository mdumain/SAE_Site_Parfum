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
    sql='''DROP TABLE IF EXISTS utilisateur '''

    mycursor.execute(sql)
    sql='''
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
    sql=''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES (1,'admin','admin@admin.fr','sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf','ROLE_admin','admin','1'), (2,'client','client@client.fr','sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d','ROLE_client','client','1'), (3,'client2','client2@client2.fr','sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422','ROLE_client','client2','1');
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE type_article(
    
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO type_article
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE etat (
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE article (
    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO article (

         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande (
    ) DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_commande(
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande 
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_panier (
    );  
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
