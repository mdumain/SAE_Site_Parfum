#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

client_boutique_filtre = Blueprint('client_boutique_filtre', __name__,
                         template_folder='templates')

@client_boutique_filtre.route('/client/boutique/filtre', methods=['GET'])
def filtre_client():
    mycursor = get_db().cursor()

    # Récupération des genres de types d'article
    sql = ''' SELECT * FROM genre ORDER BY libelle_genre'''
    mycursor.execute(sql)
    items_filtre = mycursor.fetchall()

    filtres = { 'filter_word' : '', 'filter_prix_max': [] , 'filter_prix_min':'' , 'filter_types': ''}

    return render_template('client/boutique/_filtre.html' 
                           , items_filtre=items_filtre 
                           , filtres=filtres)

@client_boutique_filtre.route('/client/boutique/filtre', methods=['POST'])
def valid_filtre_client():
    mycursor = get_db().cursor()

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('min', None)
    filter_prix_max = request.form.get('max', None)
    filter_types = request.form.getlist('filter_types', None)

    param = []

    filtres = {'filter_word': filter_word, 'filter_types': filter_types,
               'filter_prix_min': filter_prix_min, 'filter_prix_max': filter_prix_max}

    print(filtres)

# Requete SQL
    sql = ''' SELECT id_parfum, nom_parfum, prix_parfum, conditionnement_id, 
    volume_id, genre_id, marque_id, FROM parfum 
    JOIN libelle_genre ON parfum.genre_id = libelle_genre.id_genre WHERE 1=1'''

# pour filter_word
    if filter_word == '' or filter_word:
        if len(filter_word) > 1:
            if filter_word.isalpha():
                sql += " AND nom_parfum LIKE %s"
                param.append(f"%{filter_word}%")
            else:
                flash(u'Le Mot doit être composé uniquement de lettre')
        else:
            if len(filter_word) == 1:
                flash(u'Le Mot doit être composé doit être composé de au moins 2 lettres')
                return redirect('/client/boutique/filtre')


# FILTRE SUR LES PRIX
    if filter_prix_min and filter_prix_max:
        if int(filter_prix_min) < int(filter_prix_max):
            sql += " AND prix_parfum BETWEEN %s AND %s"
            param.append(filter_prix_min)
            param.append(filter_prix_max)
        else:
            flash(u'min et max doivent être des numériques')
    elif not filter_prix_min and filter_prix_max:
        filter_prix_min = 0
        sql += " AND prix_parfum BETWEEN %s AND %s"
        param.append(filter_prix_min)
        param.append(filter_prix_max)
    elif filter_prix_min and not filter_prix_max:
        filter_prix_max = 99999999999999999
        sql += " AND prix_parfum BETWEEN %s AND %s"
        param.append(filter_prix_min)
        param.append(filter_prix_max)


# FILTRE SUR LES TYPES
    if filter_types and filter_types != []:
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
    sql += " ORDER BY parfum.nom_parfum;"
    mycursor.execute(sql, param)
    parfums = mycursor.fetchall()

    mycursor.execute("SELECT * FROM parfum ORDER BY parfum.nom_parfum")
    items_filtre = mycursor.fetchall()

    return render_template('client/boutique/_filtre.html'
                           , parfums=parfums
                           , items_filtre=items_filtre
                           , filtres=filtres)

@client_boutique_filtre.route('/client/boutique/supprimer', methods=['POST'])
def reset_filtre_client():
    filtres = {'filter_word': '', 'filter_types': [], 'filter_prix_min': '', 'filter_prix_max': ''}
    return render_template('client/boutique/_filtre.html', items_filtre=[], filtres=filtres)
