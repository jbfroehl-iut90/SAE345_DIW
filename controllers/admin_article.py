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
    e.marque_equipement_id, e.sport_equipement_id, e.morphologie_equipement_id
    FROM equipement e
    GROUP BY e.id_equipement, e.libelle_equipement, e.prix_equipement, e.description_equipement, 
    e.image_equipement, e.marque_equipement_id,e.sport_equipement_id, e.morphologie_equipement_id;
'''
    mycursor.execute(sql)
    equipement = mycursor.fetchall()
    
    for id_equipement in equipement:
        sql = ''' SELECT SUM(stock) as stock FROM declinaison 
        WHERE id_equipement = %s'''
        mycursor.execute(sql, (id_equipement['id_equipement'], ))
        stock = mycursor.fetchone()
        id_equipement['stock'] = stock['stock']

        # NOmbre de déclinasons
        sql = ''' SELECT COUNT(*) as nb_declinaisons FROM declinaison 
        WHERE id_equipement = %s'''
        mycursor.execute(sql, (id_equipement['id_equipement'], ))
        id_equipement['nb_declinaisons'] = mycursor.fetchone()['nb_declinaisons']
        
        sql = ''' SELECT COUNT(*) as nb_commentaires_nouveaux FROM commentaire
        WHERE equipement_id = %s AND statut = 0;'''
        mycursor.execute(sql, (id_equipement['id_equipement'], ))
        id_equipement['nb_commentaires_nouveaux'] = mycursor.fetchone()['nb_commentaires_nouveaux']
        
        
    
    
    
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
    couleur = request.form.get('couleur_id', '')
    print("couleur :",couleur)
    taille = request.form.get('taille_id', '')
    print("taille : ",taille)
    stock = request.form.get('nb_stock', '')
    print("stock : ",stock)

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

    # Crée une déclinaison par défaut de l'article nouvellement crée
    sql = ''' INSERT INTO declinaison (id_equipement, couleur_declinaison, taille_declinaison, stock) VALUES (%s, %s, %s, %s)'''
    mycursor.execute(sql, (mycursor.lastrowid, couleur, taille, stock))
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
    if nb_declinaison['nb_declinaison'] > 1:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    elif nb_declinaison['nb_declinaison'] == 1:
        
        sql = ''' SELECT * FROM ligne_commande WHERE declinaison_id = (SELECT id_declinaison FROM declinaison WHERE id_equipement = %s)'''
        mycursor.execute(sql, id_article)
        ligne_commande = mycursor.fetchone()

        if ligne_commande:
            message = u'Impossible de supprimer cet article, des commandes sont en cours avec cet article'
            flash(message, 'alert-danger')
            return redirect('/admin/article/show')
        else :
            sql = ''' DELETE FROM declinaison WHERE id_equipement = %s'''
            mycursor.execute(sql, id_article)
            get_db().commit()
            sql = ''' SELECT * FROM equipement WHERE id_equipement = %s '''
            mycursor.execute(sql, id_article)
            article = mycursor.fetchone()
            image = article['image_equipement']

            # Delete de l'article en faisant attention aux contraintes de clés étrangères
            sql  = ''' DELETE FROM commentaire WHERE equipement_id = %s'''
            mycursor.execute(sql, id_article)
            get_db().commit()

            sql = ''' DELETE FROM historique WHERE id_equipement = %s'''
            mycursor.execute(sql, id_article)
            get_db().commit()

            sql = ''' DELETE FROM note WHERE id_equipement = %s'''
            mycursor.execute(sql, id_article)
            get_db().commit()

        # Si l'article est dans des commandes, on ne peut pas le supprimer
        sql = ''' SELECT COUNT(*) as nb_commandes FROM ligne_commande
        LEFT JOIN declinaison ON ligne_commande.declinaison_id = declinaison.id_declinaison
        LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
        WHERE equipement.id_equipement = %s'''
        mycursor.execute(sql, id_article)
        nb_commandes = mycursor.fetchone()
        if nb_commandes['nb_commandes'] > 0:
            message = u'il y a des commandes pour cet article : vous ne pouvez pas le supprimer'
            flash(message, 'alert-warning')
            return redirect('/admin/article/show')

        sql = ''' DELETE FROM equipement WHERE id_equipement = %s '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)


        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    else:
        sql = ''' SELECT * FROM equipement WHERE id_equipement = %s '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        image = article['image_equipement']

        # Delete de l'article en faisant attention aux contraintes de clés étrangères
        sql  = ''' DELETE FROM commentaire WHERE equipement_id = %s'''
        mycursor.execute(sql, id_article)
        get_db().commit()

        sql = ''' DELETE FROM historique WHERE id_equipement = %s'''
        mycursor.execute(sql, id_article)
        get_db().commit()

        sql = ''' DELETE FROM note WHERE id_equipement = %s'''
        mycursor.execute(sql, id_article)
        get_db().commit()

        # Si l'article est dans des commandes, on ne peut pas le supprimer
        sql = ''' SELECT COUNT(*) as nb_commandes FROM ligne_commande
        LEFT JOIN declinaison ON ligne_commande.declinaison_id = declinaison.id_declinaison
        LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
        WHERE equipement.id_equipement = %s'''
        mycursor.execute(sql, id_article)
        nb_commandes = mycursor.fetchone()
        if nb_commandes['nb_commandes'] > 0:
            message = u'il y a des commandes pour cet article : vous ne pouvez pas le supprimer'
            flash(message, 'alert-warning')
            return redirect('/admin/article/show')

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
    SELECT image_equipement FROM equipement WHERE id_equipement = %s
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
    sql = ''' UPDATE equipement SET libelle_equipement = %s, image_equipement = %s, prix_equipement = %s, sport_equipement_id = %s, description_equipement = %s WHERE id_equipement = %s'''
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
