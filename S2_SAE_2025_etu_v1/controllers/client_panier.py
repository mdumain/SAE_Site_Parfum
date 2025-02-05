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
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article
    sql = '''SELECT * FROM ligne_panier WHERE parfum_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql,(id_article,id_client))
    article_panier = mycursor.fetchone()
    if not (article_panier is None) and article_panier['quantite'] >=1 :
        tuple_update = (quantite, id_client,id_article)
        sql = '''UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id = %s AND parfum_id=%s'''
        mycursor.execute(sql,tuple_update)

    else:
        tuple_insert = (id_client,id_article,quantite)
        sql = '''INSERT INTO ligne_panier(utilisateur_id,parfum_id,quantite, date_ajout) VALUES (%s,%s,%s, current_timestamp)'''
        mycursor.execute(sql,tuple_insert)
    sql = '''UPDATE parfum SET stock = stock - %s WHERE id_parfum = %s'''
    mycursor.execute(sql, (quantite, id_article))

    get_db().commit()


    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id=%s'''
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()
    print(article_panier)
    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier SET quantite = quantite-1 WHERE utilisateur_id = %s AND parfum_id=%s'''
    else:
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id=%s'''
    mycursor.execute(sql, (id_client, id_article))
    sql = '''UPDATE parfum SET stock = stock + 1 WHERE id_parfum = %s'''
    mycursor.execute(sql, (id_article))
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (client_id))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
        mycursor.execute(sql, (client_id, item['parfum_id']))

        sql='''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
        mycursor.execute(sql, (item['quantite'], item['parfum_id']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    quantite = mycursor.fetchone()['quantite']
    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    sql='''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
    mycursor.execute(sql, (quantite, id_article))
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
