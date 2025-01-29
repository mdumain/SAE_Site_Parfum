#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')

@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   SELECT * FROM parfum  '''
    mycursor.execute(sql,[])

    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    articles = mycursor.fetchall()

    sql1 = ''' SELECT * FROM genre '''
    mycursor.execute(sql1,list_param)

    # pour le filtre
    types_article = mycursor.fetchall()



    articles_panier = []
    sql = '''SELECT * FROM ligne_panier JOIN parfum on ligne_panier.parfum_id = parfum.id_parfum'''
    mycursor.execute(sql,list_param)
    articles_panier = mycursor.fetchall()


    if len(articles_panier) >= 1:
        sql = ''' 
        SELECT SUM(prix_parfum * quantite) AS prix_total
        FROM ligne_panier 
            JOIN parfum ON ligne_panier.parfum_id = parfum.id_parfum 
        WHERE utilisateur_id = %s 
        '''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
