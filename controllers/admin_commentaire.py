#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    sql = ''' SELECT id_commentaire, commentaire, statut, date_publication, equipement_id, utilisateur_id, nom
    FROM commentaire LEFT JOIN utilisateur ON utilisateur_id=utilisateur.id_utilisateur where equipement_id=%s;  '''
    mycursor.execute(sql, (id_article,))
    commentaires = mycursor.fetchall()
    print(commentaires)
    sql = '''   SELECT * FROM equipement WHERE id_equipement=%s;   '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    print(article)
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , article=article
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST', 'GET'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_commentaire = request.form.get('id_commentaire')
    id_utilisateur = request.form.get('id_utilisateur')
    id_article = request.form.get('id_article')
    date_publication = request.form.get('date_publication')
    sql = ''' DELETE FROM commentaire WHERE id_commentaire=%s AND utilisateur_id=%s AND equipement_id=%s AND date_publication=%s;'''
    tuple_delete=(id_commentaire, id_utilisateur,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    print(tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html',id_utilisateur=id_utilisateur,id_article=id_article,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_article_3   '''
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()
    sql = '''   UPDATE commentaire SET statut=1 WHERE statut=0 and equipement_id=%s;   '''
    mycursor.execute(sql, (id_article,))
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)