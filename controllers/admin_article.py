#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  SELECT e.id_equipement, e.libelle_equipement, e.prix_equipement, e.description_equipement, e.image_equipement, 
    e.marque_equipement_id, e.sport_equipement_id, e.morphologie_equipement_id,
    COUNT(CASE WHEN c.statut = 0 THEN c.id_commentaire ELSE NULL END) as nb_commentaires_nouveaux, 
    SUM(d.stock) as stock 
    FROM equipement e
    LEFT JOIN commentaire c ON e.id_equipement = c.equipement_id 
    LEFT JOIN declinaison d ON e.id_equipement = d.id_equipement
    GROUP BY e.id_equipement, e.libelle_equipement, e.prix_equipement, e.description_equipement, 
    e.image_equipement, e.marque_equipement_id,e.sport_equipement_id, e.morphologie_equipement_id;
'''
    mycursor.execute(sql)
    equipement = mycursor.fetchall()
    
    
    return render_template('admin/article/show_article.html', articles=equipement)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    sql = ''' SELECT * FROM categorie_sport'''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()

    sql = ''' SELECT * FROM couleur'''
    mycursor.execute(sql)
    colors = mycursor.fetchall()

    sql = ''' SELECT * FROM taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()


    return render_template('admin/article/add_article.html'
                           ,types_article=type_article,
                           couleurs=colors
                           ,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')
    couleur = request.form.get('id_couleur', '')
    taille = request.form.get('taille_id', '')
    print(taille)
    stock = request.form.get('nb_stock', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    # Ajoute l'article nouvellement crée dans equipement
    sql = '''  INSERT INTO equipement (libelle_equipement, image_equipement, prix_equipement, sport_equipement_id, description_equipement) VALUES (%s, %s, %s, %s, %s)'''

    tuple_add = (nom, filename, prix, type_article_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'Nouvel equipement ajouté , nom: ', nom, ' - Catégorie :', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'Nouvel equipement ajouté , nom:' + nom + '- Catégorie:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    # Sélectionne le nombre de déclinaisons pour un article donné 
    sql = ''' SELECT COUNT(*) as nb_declinaison FROM declinaison WHERE id_equipement = %s'''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    print(nb_declinaison)
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT * FROM equipement WHERE id_equipement = %s '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image_equipement']

        sql = ''' DELETE FROM equipement WHERE id_equipement = %s '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM equipement WHERE id_equipement = %s    
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)
    sql = '''
    SELECT * FROM categorie_sport
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''
    SELECT * FROM declinaison 
    LEFT JOIN couleur ON couleur.id_couleur = declinaison.couleur_declinaison
    LEFT JOIN taille ON taille.id_taille = declinaison.taille_declinaison
    WHERE id_equipement = %s
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
    SELECT image FROM equipement WHERE id_equipement = %s
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image_equipement']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    # UPdate de la table equipement avec les changements effectués
    sql = ''' UPDATE TABLE equipement SET libelle_equipement = %s, image_equipement = %s, prix_equipement = %s, sport_equipement_id = %s, description = %s WHERE id_equipement = %s'''
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
