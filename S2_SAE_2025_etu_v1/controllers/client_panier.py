#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_parfum')
    quantite = request.form.get('quantite')

    id_declinaison_article=request.form.get('id_declinaison_article',None)

    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    if id_declinaison_article is None:
        sql = '''
        SELECT * FROM declinaison_parfum 
        JOIN volume ON declinaison_parfum.volume_id = volume.id_volume
        WHERE id_parfum = %s'''
        mycursor.execute(sql, id_article)
        declinaisons = mycursor.fetchall()
        if len(declinaisons) == 1:
            id_declinaison_article = declinaisons[0]['id_declinaison_parfum']
        elif len(declinaisons) == 0:
            abort("pb nb de declinaison")
        else:
            sql = '''SELECT * FROM parfum WHERE id_parfum = %s'''
            mycursor.execute(sql, id_article)
            article = mycursor.fetchone()
            return render_template('client/boutique/declinaison_article.html'
                                       , declinaisons=declinaisons
                                       , quantite=quantite
                                       , article=article)

    sql = '''SELECT stock FROM declinaison_parfum WHERE id_declinaison_parfum = %s'''
    mycursor.execute(sql, id_declinaison_article)
    stock = mycursor.fetchone()["stock"]
    if stock <= 0:
        flash("Article plus disponible")
        return redirect("/client/article/show")

    sql = '''SELECT * FROM ligne_panier WHERE declinaison_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql,(id_declinaison_article,id_client))
    article_panier = mycursor.fetchone()
    if  article_panier is not None and article_panier['quantite'] >=1 :
        tuple_update = (quantite, id_client, id_declinaison_article)
        sql = '''UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id = %s AND declinaison_id=%s'''
        mycursor.execute(sql,tuple_update)

    else:
        tuple_insert = (id_client,id_declinaison_article,quantite)
        sql = '''INSERT INTO ligne_panier(utilisateur_id,declinaison_id,quantite, date_ajout) VALUES (%s,%s,%s, current_timestamp)'''
        mycursor.execute(sql,tuple_insert)
    sql = '''UPDATE declinaison_parfum SET stock = stock - %s WHERE id_declinaison_parfum = %s'''
    mycursor.execute(sql, (quantite, id_declinaison_article))

    get_db().commit()


    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id=%s'''
    mycursor.execute(sql, (id_client, id_declinaison_article))
    article_panier = mycursor.fetchone()

    if article_panier is not None and article_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier SET quantite = quantite-1 WHERE utilisateur_id = %s AND declinaison_id=%s'''
    else:
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id=%s'''
    mycursor.execute(sql, (id_client, id_declinaison_article))

    sql = '''UPDATE declinaison_parfum SET stock = stock + 1 WHERE id_declinaison_parfum = %s'''
    mycursor.execute(sql, id_declinaison_article)

    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']

    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, client_id)
    items_panier = mycursor.fetchall()

    for item in items_panier:

        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id = %s'''
        mycursor.execute(sql, (client_id, item['declinaison_id']))

        sql='''UPDATE declinaison_parfum SET stock = stock + %s WHERE id_declinaison_parfum = %s'''
        mycursor.execute(sql, (item['quantite'], item['declinaison_id']))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_article = request.form.get('id_declinaison_article')

    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id = %s'''
    mycursor.execute(sql, (id_client, id_declinaison_article))
    quantite = mycursor.fetchone()['quantite']

    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id = %s'''
    mycursor.execute(sql, (id_client, id_declinaison_article))

    sql='''UPDATE declinaison_parfum SET stock = stock + %s WHERE id_declinaison_parfum = %s'''
    mycursor.execute(sql, (quantite, id_declinaison_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word != '' and not filter_word.isalpha():
        flash(u'Le Mot doit être composé uniquement de lettre')

    elif len(filter_word) == 1:
        flash(u'Le Mot doit être composé doit être composé de au moins 2 lettres')

    elif filter_prix_min != "" and filter_prix_max != "" and int(filter_prix_min) > int(filter_prix_max):
            flash(u'le min doit être plut petit que le max')

    else:
        session['filter_word'] = filter_word
        session['filter_types'] = filter_types
        session['filter_prix_min'] = filter_prix_min
        session['filter_prix_max'] = filter_prix_max

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():

    session['filter_prix_min'] = ''
    session['filter_prix_max'] = ''
    session['filter_types'] = []
    session['filter_word'] = ''

    return redirect('/client/article/show')
