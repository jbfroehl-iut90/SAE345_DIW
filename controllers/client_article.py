#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/article/filtre/del', methods=['POST'])
def client_article_filtre_del():
    session.pop('filtre', None)
    return redirect('/client/article/show')

@client_article.route('/client/index')
@client_article.route('/client/article/show', methods=['GET', 'POST'])              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' select * from equipement '''
    
    
    filter_word = request.form.get('filter_word')
    filter_prix_min = request.form.get('filter_prix_min')
    filter_prix_max = request.form.get('filter_prix_max')
    filter_types = request.form.getlist('filter_types')
    
    conditions = []
    params = []

    if filter_word:
        conditions.append("libelle_equipement LIKE %s")
        params.append(("%" + filter_word + "%"))
        
    if filter_prix_min:
        conditions.append("prix_equipement >= %s")
        params.append(filter_prix_min)
        
    if filter_prix_max:
        conditions.append("prix_equipement <= %s")
        params.append(filter_prix_max)
        
    if filter_types:
        placeholders = ','.join(['%s'] * len(filter_types))
        conditions.append(f"sport_equipement_id IN ({placeholders})")
        params.extend(filter_types)
        
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    mycursor.execute(sql, tuple(params))
    articles = mycursor.fetchall()
        
    for article in articles:
        sql = ''' select sum(stock) as stock from declinaison where id_equipement = %s'''
        mycursor.execute(sql, (article["id_equipement"], ))
        # Ajout de la clé stock dans le dictionnaire article
        article["stock"] = mycursor.fetchone()["stock"]
        
        # Calculer la moyenne des notes s'il y'en a 1
        sql = ''' SELECT ROUND(SUM(note)/(COUNT(id_note)), 1) as moy_note FROM note WHERE id_equipement=%s;'''
        mycursor.execute(sql, (article["id_equipement"], ))
        article["moy_notes"] = mycursor.fetchone()["moy_note"]
        
        sql = ''' SELECT COUNT(note) as nb_notes FROM note WHERE id_equipement=%s;'''
        mycursor.execute(sql, (article["id_equipement"], ))
        article["nb_notes"] = mycursor.fetchone()["nb_notes"]
        
        # Calculer le nombre de commentaires
        sql = '''SELECT COUNT(id_commentaire) as nb_commentaires FROM commentaire WHERE equipement_id=%s AND statut=1 AND utilisateur_id <> 1;'''
        mycursor.execute(sql, (article["id_equipement"], ))
        article["nb_avis"] = mycursor.fetchone()["nb_commentaires"]
        print(article["nb_avis"])
        
        sql = '''
        SELECT 
            CASE 
                WHEN COUNT(*) > 0 THEN 1 
                ELSE 0 
            END AS liste_envie
        FROM liste_envie
        WHERE id_utilisateur = %s AND id_equipement = %s;
        '''
        mycursor.execute(sql, (id_client, article["id_equipement"]))
        article["liste_envie"] = mycursor.fetchone()["liste_envie"]
        print(article["liste_envie"])
        
        
    # utilisation du filtre
    sql3=''' select * from categorie_sport '''
    mycursor.execute(sql3)
    categories = mycursor.fetchall()


    # pour le filtre

    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    session['filtre'] = True

    articles_panier = []
    sql = ''' select * from ligne_panier where id_utilisateur = %s '''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()
    print(articles_panier)

    print("len : ",len(articles_panier))

    if len(articles_panier) >= 1:
        sql = ''' SELECT * FROM ligne_panier 
        LEFT JOIN declinaison ON ligne_panier.id_declinaison = declinaison.id_declinaison
        LEFT JOIN couleur ON declinaison.couleur_declinaison = couleur.id_couleur
        LEFT JOIN taille ON declinaison.taille_declinaison = taille.id_taille
        LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement 
        WHERE id_utilisateur = %s''' 
        mycursor.execute(sql, id_client)
        articles_panier = mycursor.fetchall()

        # Total de tout les éléments dans le panier (donc stock * prix + stock * prix + ...)
        sql = ''' SELECT sum(prix * quantite) as prix_total FROM ligne_panier WHERE id_utilisateur = %s'''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()['prix_total']

    else:
        sql = ''' select * from ligne_panier where id_utilisateur = %s '''
        mycursor.execute(sql, id_client)
        articles_panier = mycursor.fetchall()

        sql = ''' SELECT sum(prix * quantite) as prix_total FROM ligne_panier WHERE id_utilisateur = %s'''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()['prix_total']

    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=categories
                           )