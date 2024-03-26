#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    # Selection des articles du panier et on récpère le libelle_equipement
    sql = ''' SELECT * FROM ligne_panier 
    LEFT JOIN declinaison ON ligne_panier.id_declinaison = declinaison.id_declinaison 
    LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
    WHERE id_utilisateur = %s
    '''
    articles_panier = []
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' SELECT sum(prix * quantite) as prix_total FROM ligne_panier WHERE id_utilisateur = %s'''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier LEFT JOIN declinaison ON ligne_panier.id_declinaison = declinaison.id_declinaison WHERE id_utilisateur = %s'''
    items_ligne_panier = []
    mycursor.execute(sql, (id_client))
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')
    # Date en Year-Month-Day
    a = datetime.now().strftime('%Y-%m-%d')
    

    sql = ''' INSERT INTO commande (id_utilisateur, date_achat, etat_id) VALUES (%s, %s, %s)'''
    mycursor.execute(sql, (id_client, a, 1))

    sql  = ''' SELECT LAST_INSERT_ID() as last_insert_id'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()['last_insert_id']

    for item in items_ligne_panier:
        sql = "DELETE FROM ligne_panier WHERE id_ligne_panier = %s"
        mycursor.execute(sql, (item['id_ligne_panier']))
        get_db().commit()

    for item in items_ligne_panier:
        sql = ''' INSERT INTO ligne_commande (commande_id, equipement_id, prix, quantite) VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql, (last_insert_id, item['id_equipement'], item['prix'], item['quantite']))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT * FROM commande
    LEFT JOIN etat ON commande.etat_id = etat.id_etat 
    LEFT JOIN (SELECT commande_id, SUM(quantite) as nb_articles FROM ligne_commande GROUP BY commande_id) as nb_articles ON commande.id_commande = nb_articles.commande_id
    LEFT JOIN (SELECT commande_id, SUM(prix_equipement * quantite) as total_commande 
    FROM ligne_commande LEFT JOIN equipement ON ligne_commande.equipement_id = equipement.id_equipement GROUP BY commande_id) as total_commande 
    ON commande.id_commande = total_commande.commande_id
    WHERE id_utilisateur = %s 
    '''
    mycursor.execute(sql, (id_client))
    commandes = []
    commandes = mycursor.fetchall()


    articles_commande = []
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = ''' SELECT * FROM ligne_commande
        LEFT JOIN equipement ON ligne_commande.equipement_id = equipement.id_equipement
        WHERE commande_id = %s
        '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

