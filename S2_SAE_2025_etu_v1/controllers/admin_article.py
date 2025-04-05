#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db
from networkx.algorithms.cuts import volume

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  SELECT parfum.nom_parfum AS nom, parfum.id_parfum AS id_article, genre.nom_genre AS libelle, parfum.genre_id AS type_article_id ,prix_parfum AS prix, SUM(stock) AS stock, parfum.image AS image,
     (SELECT COUNT(declinaison_parfum.id_declinaison_parfum) FROM declinaison_parfum WHERE declinaison_parfum.id_parfum = parfum.id_parfum) AS nb_declinaisons
    FROM parfum
    JOIN genre ON parfum.genre_id = genre.id_genre
    JOIN declinaison_parfum ON parfum.id_parfum = declinaison_parfum.id_parfum
    GROUP BY parfum.nom_parfum, parfum.id_parfum, genre.nom_genre, parfum.genre_id, prix_parfum, parfum.image 
    ORDER BY parfum.nom_parfum;
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():

    mycursor = get_db().cursor()
    sql = ''' SELECT id_genre AS id_type_article, nom_genre AS libelle FROM genre; '''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()

    sql = '''SELECT * FROM volume'''
    mycursor.execute(sql)
    volumes = mycursor.fetchall()

    return render_template('admin/article/add_article.html'
                           ,types_article=type_article
                           ,volumes=volumes
                           #,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')
    volume = request.form.get('volume_id', '')
    stock = request.form.get('stock', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('/home/sae345g14/sae2.345suj14/S2_SAE_2025_etu_v1/static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = ''' INSERT INTO parfum(nom_parfum,image,prix_parfum,genre_id,description) VALUES (%s,%s,%s,%s,%s);'''

    tuple_add = (nom, filename, float(prix), int(type_article_id), description)
    mycursor.execute(sql, tuple_add)

    sql = ''' SELECT last_insert_id() as last_insert_id '''
    mycursor.execute(sql)
    id_parfum = mycursor.fetchone()['last_insert_id']

    tuple_add = (id_parfum, stock, volume)
    sql = ''' INSERT INTO declinaison_parfum(id_parfum, stock, volume_id) VALUES (%s, %s, %s);'''
    mycursor.execute(sql, tuple_add)

    get_db().commit()

    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' -stock:' + stock + '- image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(id_declinaison_parfum) FROM parfum JOIN declinaison_parfum ON parfum.id_parfum = declinaison_parfum.id_parfum GROUP BY parfum.id_parfum '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()

    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT * from parfum WHERE id_parfum = %s '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        image = request.files.get('image')

        sql = ''' DELETE FROM parfum WHERE parfum.id_parfum =%s  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('/home/sae345g14/sae2.345suj14/S2_SAE_2025_etu_v1/static/images/' + image)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_parfum AS id_article, nom_parfum AS nom, prix_parfum AS prix, image, description from parfum where id_parfum = %s
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)
    sql = '''
    SELECT id_genre AS id_type_article, nom_genre AS libelle FROM genre; 
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''
    SELECT *
    FROM declinaison_parfum
    JOIN volume ON declinaison_parfum.volume_id = volume.id_volume
    WHERE id_parfum = %s
    '''
    mycursor.execute(sql, id_article)
    declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                           ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       SELECT image FROM parfum WHERE id_parfum = %s
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/home/sae345g14/sae2.345suj14/S2_SAE_2025_etu_v1/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/home/sae345g14/sae2.345suj14/S2_SAE_2025_etu_v1/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('/home/sae345g14/sae2.345suj14/S2_SAE_2025_etu_v1/static/images/', filename))
            image_nom = filename

    sql = ''' UPDATE parfum SET nom_parfum = %s , image = %s ,prix_parfum = %s, genre_id = %s, description = %s WHERE id_parfum = %s '''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
