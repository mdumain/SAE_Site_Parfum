#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    id_commande = request.args.get('id_commande', '')

    commandes=[]


    sql = '''
    SELECT utilisateur.login, commande.id_etat AS etat_id, commande.date_achat, 
        COUNT(ligne_commande.id_commande) AS nbr_articles, etat.libelle_etat AS libelle,
        SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total , commande.id_commande
    FROM commande
    JOIN ligne_commande ON commande.id_commande = ligne_commande.id_commande
    JOIN etat ON commande.id_etat = etat.id_etat
    JOIN utilisateur ON commande.id_utilisateur=utilisateur.id_utilisateur
    GROUP BY commande.id_commande, commande.id_etat, commande.date_achat, etat.libelle_etat
    ORDER BY  commande.id_etat ASC, commande.date_achat ASC
    '''

    mycursor.execute(sql, commandes)

    commandes=mycursor.fetchall()
    commande_adresses = None
    if id_commande != None:
        sql = '''  
        SELECT prix_declinaison, nom_parfum, nom_volume, quantite, id_volume, ligne_commande.quantite * declinaison_parfum.prix_declinaison AS prix_ligne,
        (SELECT COUNT(declinaison_parfum.id_declinaison_parfum) FROM declinaison_parfum WHERE declinaison_parfum.id_parfum = parfum.id_parfum) AS nb_declinaison
        FROM commande
        JOIN ligne_commande ON commande.id_commande = ligne_commande.id_commande
        JOIN declinaison_parfum ON ligne_commande.declinaison_id = declinaison_parfum.id_declinaison_parfum
        JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
        JOIN volume ON declinaison_parfum.volume_id = volume.id_volume
        WHERE commande.id_commande = %s;
        '''
        mycursor.execute(sql, id_commande)
        articles_commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''     UPDATE commande
        SET id_etat = 2
        WHERE %s=id_commande'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
