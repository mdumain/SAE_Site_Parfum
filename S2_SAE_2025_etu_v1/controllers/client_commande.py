#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    SELECT * FROM ligne_panier 
    JOIN declinaison_parfum ON ligne_panier.declinaison_id = declinaison_parfum.id_declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    WHERE utilisateur_id = %s
    '''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' 
        SELECT SUM(prix_parfum * quantite) AS prix_total
        FROM ligne_panier 
            JOIN declinaison_parfum ON ligne_panier.declinaison_id = declinaison_parfum.id_declinaison_parfum
            JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum 
        WHERE utilisateur_id = %s 
        '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()["prix_total"]
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = '''
    SELECT * 
    FROM ligne_panier 
    JOIN declinaison_parfum ON ligne_panier.declinaison_id = declinaison_parfum.id_declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    WHERE utilisateur_id = %s'''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')
                                          #https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    date = datetime.now()
    a = datetime.strptime(f"{date.month} {date.day} {date.year} {date.hour}:{date.minute}", "%m %d %Y %H:%M")

    sql = ''' 
    INSERT INTO commande VALUE (NULL, %s, %s, 1);
    '''
    mycursor.execute(sql, (a, id_client))
    sql = '''SELECT id_commande FROM commande WHERE id_commande=LAST_INSERT_ID();'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()['id_commande']
    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_id = %s'''
        mycursor.execute(sql, (id_client, item['declinaison_id']))
        sql = '''INSERT INTO ligne_commande VALUE (%s, %s, %s, %s)'''
        mycursor.execute(sql, (last_insert_id, item['declinaison_id'], item['prix_parfum'], item['quantite']))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  
    SELECT commande.id_commande, commande.id_etat, etat.libelle_etat, date_achat, SUM(prix_parfum * quantite) AS prix_total, SUM(quantite) AS nbr_articles
    FROM commande 
    JOIN ligne_commande ON commande.id_commande = ligne_commande.id_commande 
    JOIN declinaison_parfum ON ligne_commande.declinaison_id = declinaison_parfum.id_declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    JOIN etat ON commande.id_etat = etat.id_etat
    WHERE id_utilisateur = %s 
    GROUP BY commande.id_commande, id_etat, date_achat
    ORDER BY commande.id_etat, date_achat DESC; 
    '''
    mycursor.execute(sql, id_client)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = '''
        SELECT nom_parfum, nom_volume, prix_parfum, quantite, SUM(quantite * prix_parfum) AS prix_ligne,
       (SELECT COUNT(declinaison_parfum.id_declinaison_parfum) FROM declinaison_parfum WHERE declinaison_parfum.id_parfum = parfum.id_parfum) AS nb_dec
        FROM ligne_commande
            JOIN declinaison_parfum ON ligne_commande.declinaison_id = declinaison_parfum.id_declinaison_parfum
            JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
            JOIN volume ON declinaison_parfum.volume_id = volume.id_volume
        WHERE id_commande = %s
        GROUP BY nom_parfum, prix_parfum, quantite, nom_volume, nb_dec
        '''
        mycursor.execute(sql, id_commande)
        articles_commande = mycursor.fetchall()
        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

