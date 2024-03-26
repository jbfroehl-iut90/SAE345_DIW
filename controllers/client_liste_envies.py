#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import os
from datetime import datetime

from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                        template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    myDate = datetime.now()
    print(myDate)
    sql = '''
    INSERT INTO liste_envie (id_utilisateur, id_equipement, date_ajout)
    VALUES (%s, %s, %s)
    '''
    mycursor.execute(sql, (id_client, id_article, myDate))
    get_db().commit()
    return redirect('/client/article/show')

@client_liste_envies.route('/client/envie/delete', methods=['get'])
def client_liste_envies_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = '''
    DELETE FROM liste_envie
    WHERE id_utilisateur = %s AND id_equipement = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    get_db().commit()
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envie/delete_view', methods=['get'])
def client_liste_envies_delete_view():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = '''
    DELETE FROM liste_envie
    WHERE id_utilisateur = %s AND id_equipement = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    get_db().commit()
    return redirect('/client/article/show')
    
@client_liste_envies.route('/client/envies/show', methods=['get'])
def client_liste_envies_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    articles_liste_envies = []
    articles_historique = []
    sql = '''
    SELECT e.id_equipement as id_article, e.libelle_equipement as nom, e.prix_equipement as prix, e.image_equipement as image,
    COUNT(d.id_declinaison) as nb_declinaisons, SUM(d.stock) as stock, date_ajout 
    FROM liste_envie l
    LEFT JOIN equipement e ON l.id_equipement = e.id_equipement
    LEFT JOIN declinaison d ON e.id_equipement = d.id_equipement
    WHERE l.id_utilisateur = %s
    GROUP BY e.id_equipement
    '''
    mycursor.execute(sql, (id_client, ))
    articles_liste_envies = mycursor.fetchall()
    return render_template('client/liste_envies/liste_envies_show.html'
                           ,articles_liste_envies=articles_liste_envies
                           , articles_historique=articles_historique
                           #, nb_liste_envies= nb_liste_envies
                           )
    


def client_historique_add(article_id, client_id):
    mycursor = get_db().cursor()
    client_id = session['id_user']
    # rechercher si l'article pour cet utilisateur est dans l'historique
    # si oui mettre
    sql ='''   '''
    mycursor.execute(sql, (article_id, client_id))
    historique_produit = mycursor.fetchall()
    sql ='''   '''
    mycursor.execute(sql, (client_id))
    historiques = mycursor.fetchall()


@client_liste_envies.route('/client/envies/up', methods=['get'])
@client_liste_envies.route('/client/envies/down', methods=['get'])
@client_liste_envies.route('/client/envies/last', methods=['get'])
@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_article_move():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
  
    return redirect('/client/envies/show')
