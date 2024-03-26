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
    
    sql = '''
    DELETE FROM liste_envie
    WHERE id_utilisateur = %s AND id_equipement = %s'''
    mycursor.execute(sql, (id_client, id_article))
    get_db().commit()
    
    # Regroupement par couleur (ex pour la couleur rouge : 3 tailles différentes)
    declinaisons2 = {}
    for declinaison in declinaisons:
        if declinaison['libelle_couleur'] in declinaisons2:
            declinaisons2[declinaison['libelle_couleur']].append(declinaison)
        else:
            declinaisons2[declinaison['libelle_couleur']] = [declinaison]

    if len(declinaisons) == 1:
        sql = ''' SELECT * FROM equipement WHERE id_equipement = %s'''
        mycursor.execute(sql, (id_article))
        article = mycursor.fetchone()
        
        return render_template('client/boutique/declinaison_article.html',
                                declinaisons=declinaisons,
                                quantite=quantite,
                                article=article, declinaisons2=declinaisons2)
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
    id_declinaison_article = request.form.get('id_declinaison', None)
    prix = request.form.get('prix', None)
    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = ''' SELECT * FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_declinaison_article, id_client))
    article_panier = mycursor.fetchone()

    if article_panier is None:
        sql = ''' INSERT INTO ligne_panier (quantite, prix, id_declinaison, id_utilisateur) VALUES (%s, %s, %s, %s) '''
        mycursor.execute(sql, (quantite, prix, id_declinaison_article, id_client))
        
        # Retirer stock de la déclinaison
        sql2=''' UPDATE declinaison SET stock = stock - %s WHERE id_declinaison = %s '''
        mycursor.execute(sql2, (quantite, id_declinaison_article))
    else:
        sql = ''' UPDATE ligne_panier 
        SET quantite = quantite + %s 
        WHERE id_declinaison = %s AND id_utilisateur = %s '''
        mycursor.execute(sql, (quantite, id_declinaison_article, id_client))
        
        # Retirer stock de la déclinaison
        sql2=''' UPDATE declinaison SET stock = stock - %s WHERE id_declinaison = %s '''
        mycursor.execute(sql2, (quantite, id_declinaison_article))

    get_db().commit()
    return redirect('/client/article/show')

# Ajouter 1 à la quantité dans le panier
@client_panier.route('/client/panier/addqty', methods=['GET', 'POST'])
def add_qty():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ligne_panier = request.form.get('id_ligne_panier','')
    
    sql = ''' SELECT * FROM ligne_panier WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_ligne_panier, id_client))
    ligne_panier = mycursor.fetchone()
    
    mysql = ''' UPDATE ligne_panier SET quantite = quantite + 1 WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
    mycursor.execute(mysql, (id_ligne_panier, id_client))
    
    # Retirer stock de la déclinaison
    sql2=''' UPDATE declinaison SET stock = stock - 1 WHERE id_declinaison = %s '''
    mycursor.execute(sql2, (ligne_panier['id_declinaison']))
    
    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ligne_panier = request.form.get('id_ligne_panier')
    qtycommande = request.form.get('quantite')

    sql = ''' SELECT * FROM ligne_panier WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_ligne_panier, id_client))
    ligne_panier = mycursor.fetchone()
    
    if int(qtycommande) > 1:
        mysql = ''' UPDATE ligne_panier SET quantite = quantite - 1 WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
        mycursor.execute(mysql, (id_ligne_panier, id_client))
        
        sql2=''' UPDATE declinaison SET stock = stock + 1 WHERE id_declinaison = %s '''
        mycursor.execute(sql2, (ligne_panier['id_declinaison']))
    else:
        mysql = ''' DELETE FROM ligne_panier WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
        mycursor.execute(mysql, (id_ligne_panier, id_client))
        
        sql2=''' UPDATE declinaison SET stock = stock + 1 WHERE id_declinaison = %s '''
        mycursor.execute(sql2, (ligne_panier['id_declinaison']))
        
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    # sélection des lignes de panier
    sql = ''' SELECT * FROM ligne_panier WHERE id_utilisateur = %s '''
    mycursor.execute(sql, (client_id, ))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        # suppression de la ligne de panier de l'article pour l'utilisateur connecté
        sql = ''' DELETE FROM ligne_panier WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
        mycursor.execute(sql, (item['id_ligne_panier'], client_id))
        # mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
        sql2=''' UPDATE declinaison SET stock = stock + %s WHERE id_declinaison = %s '''
        mycursor.execute(sql2, (item['quantite'], item['id_declinaison']))
        
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ligne_panier = request.form.get('id_ligne_panier')
    print("id_ligne_panier", id_ligne_panier)
    sql = ''' SELECT * FROM ligne_panier WHERE id_ligne_panier = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_ligne_panier, id_client))
    ligne_panier = mycursor.fetchone()
    
    sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_ligne_panier = %s'''
    mycursor.execute(sql, (id_client, id_ligne_panier))


    sql2=''' UPDATE declinaison SET stock = stock + %s WHERE id_declinaison = %s '''
    mycursor.execute(sql2, (ligne_panier['quantite'], ligne_panier['id_declinaison']))    

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
