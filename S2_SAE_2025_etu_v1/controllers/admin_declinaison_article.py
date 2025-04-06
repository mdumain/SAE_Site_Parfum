#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT * FROM parfum WHERE id_parfum = %s
    '''
    mycursor.execute(sql, id_article)
    article=mycursor.fetchone()

    sql = '''
    SELECT * FROM volume
    '''
    mycursor.execute(sql)
    volumes = mycursor.fetchall()

    sql = '''
    SELECT * FROM couleur
    '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = '''
    SELECT * 
    FROM declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    WHERE parfum.id_parfum = %s AND couleur_id = 1;
    '''
    mycursor.execute(sql, id_article)
    declinaisons = mycursor.fetchall()
    if declinaisons is not None and len(declinaisons) >= 1:
        d_couleur_uniq = 1
    else:
        d_couleur_uniq=None
        sql = '''
        SELECT *
        FROM declinaison_parfum
        WHERE id_parfum = %s
        '''
        mycursor.execute(sql, id_article)
        declinaisons = mycursor.fetchall()
        if declinaisons is not None and len(declinaisons) >= 1:
            couleurs = couleurs[1:]

    return render_template('admin/article/add_declinaison_article.html'
                           , article=article
                           , volumes = volumes
                           , couleurs = couleurs
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    volume = request.form.get('volume')
    couleur = request.form.get('couleur', 1)

    sql = '''SELECT * FROM declinaison_parfum WHERE id_parfum = %s AND volume_id = %s AND couleur_id = %s'''
    mycursor.execute(sql, (id_article, volume, couleur))
    declinaison = mycursor.fetchone()

    if declinaison is not None:
        flash("Declinaison déjà existante")
        return redirect('/admin/article/edit?id_article=' + id_article)

    sql = '''INSERT INTO declinaison_parfum(id_parfum, stock, volume_id, couleur_id) VALUES (%s, %s, %s, %s)'''
    mycursor.execute(sql, (id_article, stock, volume, couleur))

    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()

    sql = '''
    SELECT declinaison_parfum.*, parfum.image, parfum.nom_parfum, parfum.id_parfum
    FROM declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    WHERE declinaison_parfum.id_declinaison_parfum = %s
    '''
    mycursor.execute(sql, id_declinaison_article)
    declinaison_article = mycursor.fetchone()
    id_article = declinaison_article['id_parfum']

    sql = '''
    SELECT * FROM volume
    '''
    mycursor.execute(sql)
    volumes = mycursor.fetchall()

    sql = '''
    SELECT * FROM couleur
    '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = '''
    SELECT * 
    FROM declinaison_parfum
    JOIN parfum ON declinaison_parfum.id_parfum = parfum.id_parfum
    WHERE parfum.id_parfum = %s AND couleur_id = 1;
    '''
    mycursor.execute(sql, id_article)
    declinaisons = mycursor.fetchall()

    if declinaisons is not None and len(declinaisons) >= 1:
        d_couleur_uniq = 1
    else:
        d_couleur_uniq=None
        sql = '''
        SELECT *
        FROM declinaison_parfum
        WHERE id_parfum = %s
        '''
        mycursor.execute(sql, id_article)
        declinaisons = mycursor.fetchall()
        if declinaisons is not None and len(declinaisons) > 1:
            couleurs = couleurs[1:]

    return render_template('admin/article/edit_declinaison_article.html'
                           , volumes=volumes
                           , couleurs=couleurs
                           , declinaison_article=declinaison_article
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article','')
    id_article = request.form.get('id_article','')
    stock = request.form.get('stock','')
    volume_id = request.form.get('id_volume','')
    couleur = request.form.get('id_couleur', 1)
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM declinaison_parfum WHERE id_parfum = %s AND volume_id = %s AND couleur_id = %s'''
    mycursor.execute(sql, (id_article, volume_id, couleur))
    declinaison = mycursor.fetchone()

    if declinaison is not None:
        flash("Declinaison déjà existante")
        return redirect('/admin/article/edit?id_article=' + id_article)

    sql = '''
    UPDATE declinaison_parfum
    SET volume_id = %s, stock = %s, couleur_id = %s
    WHERE id_declinaison_parfum = %s
    '''
    mycursor.execute(sql, (volume_id, stock, couleur, id_declinaison_article))
    get_db().commit()
    message = u'declinaison_article modifié , id:' + str(id_declinaison_article) + '- stock :' + str(stock) + ' - volume_id:' + str(volume_id)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article','')
    id_article = request.args.get('id_article','')

    mycursor = get_db().cursor()
    sql = '''
    DELETE FROM declinaison_parfum
    WHERE id_declinaison_parfum = %s
    '''
    mycursor.execute(sql, id_declinaison_article)
    get_db().commit()

    flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_article),  'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))
