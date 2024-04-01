#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    try :
        id_commande = request.args.get('id_commande', None)
    except:
        id_commande = None
    if id_commande != None:
        sql = ''' SELECT * FROM ligne_commande 
        LEFT JOIN declinaison ON ligne_commande.declinaison_id = declinaison.id_declinaison
        LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
        LEFT JOIN couleur ON declinaison.couleur_declinaison = couleur.id_couleur
        LEFT JOIN taille ON declinaison.taille_declinaison = taille.id_taille
        LEFT JOIN (SELECT id_equipement, COUNT(*) as nb_declinaisons FROM declinaison GROUP BY id_equipement) as nb_declinaisons 
        ON equipement.id_equipement = nb_declinaisons.id_equipement
        WHERE commande_id = %s'''
        articles_commande = []
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()
    else:
        sql = ''' SELECT 
            ligne_commande.*,
            equipement.*,
            nb_declinaisons.nb_declinaisons
        FROM ligne_commande
        LEFT JOIN declinaison ON ligne_commande.declinaison_id = declinaison.id_declinaison
        LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
        LEFT JOIN (
            SELECT id_equipement, COUNT(*) as nb_declinaisons 
            FROM declinaison 
            GROUP BY id_equipement
        ) as nb_declinaisons ON equipement.id_equipement = nb_declinaisons.id_equipement;
'''
        articles_commande = []
        mycursor.execute(sql)
        articles_commande = mycursor.fetchall()

    sql = ''' SELECT * FROM commande
    LEFT JOIN etat ON commande.etat_id = etat.id_etat
    LEFT JOIN utilisateur ON commande.id_utilisateur = utilisateur.id_utilisateur
    LEFT JOIN (SELECT commande_id, SUM(quantite) as nb_articles FROM ligne_commande GROUP BY commande_id) as nb_articles
    ON commande.id_commande = nb_articles.commande_id
    LEFT JOIN (SELECT commande_id, SUM(prix_equipement * quantite) as total_commande
    FROM ligne_commande LEFT JOIN declinaison ON ligne_commande.declinaison_id = declinaison.id_declinaison
    LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement
    GROUP BY commande_id) as total_commande
    ON commande.id_commande = total_commande.commande_id;
    '''
    commandes=[]
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    commande_adresses = []
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = ''' SELECT * FROM ligne_commande WHERE commande_id = %s '''
        mycursor.execute(sql, (id_commande))

        commande_adresses = []
        sql = ''' SELECT * FROM commande WHERE id_commande = %s '''
        mycursor.execute(sql, (id_commande))
        commande = mycursor.fetchone()
        sql = ''' SELECT * FROM adresse WHERE id_adresse = %s '''
        mycursor.execute(sql, (commande['adresse_id']))
        commande_adresse = mycursor.fetchone()
        commande_adresses.append(commande_adresse)
        sql = ''' SELECT * FROM adresse WHERE id_adresse = %s '''
        mycursor.execute(sql, (commande['billing_address_id']))
        commande_adresse = mycursor.fetchone()
        commande_adresses.append(commande_adresse)

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = ''' UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
