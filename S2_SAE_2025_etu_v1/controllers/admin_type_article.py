#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()

    sql = '''SELECT genre.nom_genre AS libelle, genre.id_genre AS id_type_article, COUNT(parfum.id_parfum) AS nbr_articles
    FROM genre
    LEFT JOIN parfum ON parfum.genre_id = genre.id_genre
    GROUP BY genre.nom_genre, genre.id_genre
    ORDER BY genre.id_genre ASC;'''

    mycursor.execute(sql)
    types_article = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', types_article=types_article)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():

    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()

    sql = ''' INSERT INTO genre (nom_genre) VALUES (%s)  '''
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''SELECT COUNT(parfum.id_parfum) AS nbr_articles
                   FROM parfum
                   WHERE parfum.genre_id = %s'''
    mycursor.execute(sql, (id_type_article,))
    result = mycursor.fetchone()
    nbr_articles = result['nbr_articles']

    if nbr_articles > 0:
        flash(u'Impossible de supprimer le type d\'article car il y a encore des articles associés.', 'alert-danger')
    else:
        sql_delete = '''DELETE FROM genre WHERE id_genre = %s'''
        mycursor.execute(sql_delete, (id_type_article,))
        get_db().commit()
        flash(u'Suppression du type d\'article réussie, id : ' + id_type_article, 'alert-success')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''SELECT id_genre AS id_type_article, nom_genre AS libelle FROM genre WHERE id_genre = %s'''
    mycursor.execute(sql, (id_type_article,))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id_type_article', '')
    tuple_update = (libelle, id_type_article)
    mycursor = get_db().cursor()
    sql = '''UPDATE genre SET nom_genre = %s WHERE id_genre = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')
