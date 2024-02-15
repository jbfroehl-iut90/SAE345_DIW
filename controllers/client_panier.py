#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['GET', 'POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    id_declinaison_article=request.form.get('id_declinaison', None)

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = ''' SELECT * FROM declinaison 
    LEFT JOIN couleur ON couleur.id_couleur = declinaison.couleur_declinaison 
    LEFT JOIN taille ON taille.id_taille = declinaison.taille_declinaison
    WHERE id_equipement = %s;'''
    mycursor.execute(sql, (id_article, ))
    declinaisons = mycursor.fetchall()


    # Regroupement par couleur (ex pour la couleur rouge : 3 tailles différentes)
    declinaisons2 = {}
    for declinaison in declinaisons:
        if declinaison['libelle_couleur'] in declinaisons2:
            declinaisons2[declinaison['libelle_couleur']].append(declinaison)
        else:
            declinaisons2[declinaison['libelle_couleur']] = [declinaison]

    if len(declinaisons) == 1:
        id_declinaison_article = declinaisons[0]['id_declinaison']
    elif len(declinaisons) == 0:
        sql = ''' SELECT * FROM equipement WHERE id_equipement = %s'''
        mycursor.execute(sql, (id_article, ))
        article = mycursor.fetchone()
    else:
        sql = ''' SELECT * FROM equipement WHERE id_equipement = %s'''
        mycursor.execute(sql, (id_article))
        article = mycursor.fetchone()
        return render_template('client/boutique/declinaison_article.html'
                                   , declinaisons=declinaisons
                                   , quantite=quantite
                                   , article=article, declinaisons2=declinaisons2)

    return redirect('/client/article/show')

@client_panier.route('/client/panier/add/declinaison', methods=['GET', 'POST'])
def client_panier_add_declinaison():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    id_declinaison_article = request.form.get('item_declinaison.id_declinaison', None)
    prix_unitaire = request.form.get('equipement.prix_equipement', None)

    sql = ''' SELECT * FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if article_panier is None:
        sql = ''' INSERT INTO ligne_panier (quantite, prix, id_declinaison, id_utilisateur) VALUES (%s, %s, %s, %s) '''
        mycursor.execute(sql, (quantite, quantite, id_declinaison_article, id_client))
    else:
        sql = ''' UPDATE ligne_panier 
        SET quantite = quantite + %s 
        WHERE id_declinaison = %s AND id_utilisateur = %s '''
        mycursor.execute(sql, (quantite, id_declinaison_article, id_client))

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
    id_declinaison_article = request.form.get('id_declinaison', None)
    article_panier=[]
    sql = ''' SELECT * FROM ligne_panier WHERE id_equipement = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, id_article)
    article_panier = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        # mise à jour de la quantité dans le panier => -1 article
        sql = ''' UPDATE ligne_panier SET quantite = quantite - 1 WHERE id_equipement = %s AND id_utilisateur = %s '''
    else:
        # suppression de la ligne de panier
        sql = ''' DELETE FROM ligne_panier WHERE id_equipement = %s AND id_utilisateur = %s'''

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    # sélection des lignes de panier
    sql = ''' SELECT * FROM ligne_panier WHERE id_utilisateur = %s '''
    items_panier = []
    for item in items_panier:
        # suppression de la ligne de panier de l'article pour l'utilisateur connecté
        sql = ''' DELETE FROM ligne_panier WHERE id_equipement = %s AND id_utilisateur = %s '''
        # mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
        sql2=''' UPDATE equipement SET stock = stock + %s WHERE id_equipement = %s '''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_article = request.form.get('id_declinaison')
    id_equipment = request.form.get('id_article')
    id_ligne_panier = request.form.get('id_ligne_panier')

    sql = ''' SELECT * FROM ligne_panier WHERE id_utilisateur = %s AND id_ligne_panier = %s '''
    mycursor.execute(sql, (id_client, id_ligne_panier))
    ligne_panier = mycursor.fetchone()

    sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_ligne_panier = %s'''
    mycursor.execute(sql, (id_client, id_ligne_panier))

    sql2='''  UPDATE equipement SET stock = stock + %s WHERE id_equipement = %s'''  
    # mycursor.execute(sql2, (ligne_panier['quantite'], id_declinaison_article))

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
