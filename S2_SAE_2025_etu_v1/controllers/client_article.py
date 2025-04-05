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

    filter_word=''
    filter_prix_min, filter_prix_max = None, None
    filter_types = []

    if "filter_word" in session.keys():
        filter_word = session['filter_word']
    if "filter_prix_min" in session.keys():
        filter_prix_min = session['filter_prix_min']
    if "filter_prix_max" in session.keys():
        filter_prix_max = session['filter_prix_max']
    if "filter_types" in session.keys():
        filter_types = session['filter_types']

    param = []

    sql = ''' 
    SELECT parfum.*, genre.*, SUM(stock) AS stock, COUNT(id_declinaison_parfum) AS nb_dec,prix_parfum
    FROM parfum
    JOIN declinaison_parfum ON parfum.id_parfum = declinaison_parfum.id_parfum
    JOIN genre ON parfum.genre_id = genre.id_genre WHERE 1=1
    '''

    if "filter_word" in session.keys() and filter_word != '':
        if len(filter_word) > 1:
            if filter_word.isalpha():
                sql += " AND nom_parfum LIKE %s"
                param.append(f"%{filter_word}%")
            else:
                flash(u'Le Mot doit être composé uniquement de lettre')
        else:
            if len(filter_word) == 1:
                flash(u'Le Mot doit être composé doit être composé de au moins 2 lettres')



    if "filter_types" in session.keys() and filter_types != []:
        sql += " AND ("
        i = 0
        for type_article in filter_types:
            sql += " genre_id = %s"
            param.append(type_article)
            if i == len(filter_types) - 1:
                sql += ")"
            else:
                sql += " OR"
                i += 1

    sql += '''GROUP BY parfum.id_parfum, parfum.nom_parfum, parfum.conditionnement_id, parfum.genre_id, parfum.marque_id, parfum.fournisseur_id, parfum.description, parfum.image, genre.id_genre, genre.nom_genre'''

    if "filter_prix_min" in session.keys() and filter_prix_min != "":
        if "filter_prix_max" in session.keys() and filter_prix_max != "":
            if int(filter_prix_min) < int(filter_prix_max):
                sql += ''' HAVING prix_parfum BETWEEN %s AND %s'''
                param.append(int(filter_prix_min))
                param.append(int(filter_prix_max))
            else:
                flash(u'min et max doivent être des numériques')
        else:
            sql += ''' HAVING prix_parfum >= %s'''
            param.append(int(filter_prix_min))
    elif "filter_prix_max" in session.keys() and filter_prix_max != "":
        sql += ''' HAVING prix_parfum <= %s'''
        param.append(int(filter_prix_max))

    mycursor.execute(sql, param)
    articles = mycursor.fetchall()

    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''

    sql1 = ''' SELECT * FROM genre '''
    mycursor.execute(sql1)

    # pour le filtre
    types_article = mycursor.fetchall()



    articles_panier = []
    sql = '''SELECT *, CONCAT(parfum.nom_parfum, ' (', volume.nom_volume, ')') AS nom 
    FROM ligne_panier JOIN declinaison_parfum ON ligne_panier.declinaison_id = declinaison_parfum.id_declinaison_parfum 
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    JOIN volume ON declinaison_parfum.volume_id = volume.id_volume
    '''
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()


    if len(articles_panier) >= 1:
        sql = ''' 
        SELECT SUM(prix_parfum * quantite) AS prix_total
        FROM ligne_panier 
            JOIN declinaison_parfum ON ligne_panier.declinaison_id = declinaison_parfum.id_declinaison_parfum
            JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum 
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
