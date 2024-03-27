#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    try:
        id_article = int(request.args.get('id_article'))
    except (TypeError, ValueError):
        abort(400, "Invalid or missing id_equipement parameter")

    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_article, id_client)

    sql = ''' SELECT * FROM equipement WHERE id_equipement=%s;''' 
    
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()

    commandes_articles=[]
    nb_commentaires=[]
    if article is None:
        abort(404, "pb id article")
        
    sql = ''' SELECT ROUND(SUM(note)/(COUNT(id_note)), 1) as moy_note, COUNT(id_note) as nb_note FROM note WHERE id_equipement=%s;'''
    mycursor.execute(sql, id_article)
    moyenne = mycursor.fetchone()
    print('moyenne',moyenne)
        
    sql = ''' SELECT nom, id_commentaire, commentaire, statut, date_publication, equipement_id, utilisateur_id FROM commentaire 
    LEFT JOIN utilisateur ON utilisateur_id = utilisateur.id_utilisateur WHERE equipement_id=%s and statut=1 ORDER BY date_publication DESC, id_commentaire;'''
    mycursor.execute(sql, id_article)
    commentaires = mycursor.fetchall()
    
    sql = ''' SELECT COUNT(commande_id) AS nb_commandes_article FROM commande 
    LEFT JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    WHERE commande.id_utilisateur=%s AND ligne_commande.equipement_id=%s;'''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()
    print('commandes_articles',commandes_articles)
    
    sql = ''' SELECT note FROM note WHERE utilisateur_id=%s AND id_equipement=%s;'''
    mycursor.execute(sql, (id_client, id_article))
    note = mycursor.fetchone()
    print('note',note)
    # if note:
    #    note=note['note']
    sql = '''SELECT COUNT(id_commentaire) as nb_commentaires_utilisateur FROM commentaire WHERE utilisateur_id=%s AND equipement_id=%s AND statut=%s ORDER BY date_publication;'''
    mycursor.execute(sql, (id_client, id_article, 1))
    nb_commentaires_utilisateur = mycursor.fetchone()
    print('nb_commentaires_utilisateur',nb_commentaires_utilisateur)
    
    sql='''SELECT COUNT(id_commentaire) as nb_commentaires_total FROM commentaire WHERE equipement_id=%s AND utilisateur_id <> 1;'''
    mycursor.execute(sql, id_article)
    nb_commentaires = mycursor.fetchone()
    
    client_historique_add(id_article, id_client)
    
    print('nb_commentaires',nb_commentaires)
    return render_template('client/article_info/article_details.html'
                           , article=article
                           , commandes_articles=commandes_articles
                           , commentaires=commentaires
                           , note=note
                           , nb_commentaires_utilisateur=nb_commentaires_utilisateur
                            , nb_commentaires=nb_commentaires
                            , moyenne=moyenne
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    tuple_insert = (commentaire, id_client, id_article)
    print(tuple_insert)
    sql = ''' INSERT INTO commentaire (commentaire, statut, utilisateur_id, equipement_id) VALUES (%s, 0, %s, %s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    id_commentaire = request.form.get('id_commentaire', None)
    sql = ''' DELETE FROM commentaire WHERE id_commentaire = %s AND utilisateur_id=%s AND equipement_id=%s AND date_publication=%s;'''
    tuple_delete=(id_commentaire, id_client,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_insert = (note, id_article, id_client)
    print(tuple_insert)
    sql = ''' INSERT INTO note (note, id_equipement, utilisateur_id) VALUES (%s, %s, %s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_article, id_client)
    print(tuple_update)
    sql = ''' UPDATE note SET note=%s WHERE id_equipement=%s AND utilisateur_id=%s;'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    sql = ''' DELETE FROM note WHERE utilisateur_id=%s AND id_equipement=%s;'''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
