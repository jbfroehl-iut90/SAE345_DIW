#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' select * from EQUIPEMENT '''
    list_param = []
    condition_and = " where "
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # utilisation du filtre
    sql3=''' select * from CATEGORIE_SPORT '''
    # articles =[]
    mycursor.execute(sql3)
    categories = mycursor.fetchall()

    # pour le filtre
    types_article = []


    articles_panier = []

    # Nos types de sport

    sqleu =  ''' select * from SPORT '''
    mycursor.execute(sqleu)
    sports = mycursor.fetchall()

    sqleu2 = ''' select * from CATEGORIE_SPORT '''
    mycursor.execute(sqleu2)
    categories_sport = mycursor.fetchall()
    print(categories_sport)

    if len(articles_panier) >= 1:
        sql = '''  select * from EQUIPEMENT'''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article, sports=sports, categories=categories_sport
                           )
