#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import date
import datetime
from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                        template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    myDate = datetime.date.today()
    sql = ''' SELECT COUNT(id_liste_envie) as nb_ordre FROM liste_envie WHERE id_utilisateur = %s'''
    mycursor.execute(sql, id_client)
    nb_ordre = mycursor.fetchone()['nb_ordre']
    
    sql = '''
    INSERT INTO liste_envie (id_utilisateur, id_equipement, date_ajout, ordre)
    VALUES (%s, %s, %s, %s)
    '''
    mycursor.execute(sql, (id_client, id_article, myDate, nb_ordre + 1))
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
    date = datetime.date.today()
    sql = '''
    SELECT h.id_historique, h.date_consultation as date FROM historique h WHERE id_utilisateur = %s;
    '''
    mycursor.execute(sql, (id_client, ))
    historique = mycursor.fetchall()
    for article in historique:
        if (date - article['date']).days > 30:
            sql = '''
            DELETE FROM historique WHERE id_historique = %s;
            '''
            mycursor.execute(sql, (article['id_historique'], ))
            get_db().commit()
    
    sql = '''
    SELECT e.id_equipement as id_article, e.libelle_equipement as nom, e.prix_equipement as prix, e.image_equipement as image,
    COUNT(d.id_declinaison) as nb_declinaisons, SUM(d.stock) as stock, l.date_ajout as date_create, ordre
    FROM liste_envie l
    LEFT JOIN equipement e ON l.id_equipement = e.id_equipement
    LEFT JOIN declinaison d ON e.id_equipement = d.id_equipement
    WHERE l.id_utilisateur = %s
    GROUP BY e.id_equipement, e.libelle_equipement, e.prix_equipement, e.image_equipement, date_create, ordre
    ORDER BY ordre DESC, date_create DESC;
    '''
    mycursor.execute(sql, (id_client, ))
    articles_liste_envies = mycursor.fetchall()
    
    sql = ''' SELECT COUNT(id_liste_envie) as nb_liste_envies FROM liste_envie WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client, ))
    nb_liste_envies = mycursor.fetchone()['nb_liste_envies']
    
    sql = ''' SELECT e.id_equipement as id_article, e.libelle_equipement as nom,  e.prix_equipement as prix, e.image_equipement as image
    FROM historique LEFT JOIN equipement e ON historique.id_equipement = e.id_equipement 
    WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client, ))
    articles_historique = mycursor.fetchall()

    return render_template('client/liste_envies/liste_envies_show.html'
                           ,articles_liste_envies=articles_liste_envies
                           , articles_historique=articles_historique
                           , nb_liste_envies= nb_liste_envies
                           )
    


def client_historique_add(article_id, client_id):
    mycursor = get_db().cursor()
    client_id = session['id_user']
    date = datetime.date.today()
    print(type(date))
    # rechercher si l'article pour cet utilisateur est dans l'historique
    # si oui mettre
    sql =''' 
    SELECT 
        CASE 
            WHEN EXISTS (SELECT 1 FROM historique WHERE id_utilisateur = %s AND id_equipement = %s) THEN FALSE 
            ELSE TRUE 
    END AS resultat;
    '''
    mycursor.execute(sql, (client_id, article_id))
    test = mycursor.fetchone()['resultat']
    if(test):
        sql = ''' 
        SELECT 
            CASE 
                WHEN (SELECT COUNT(id_historique) as count FROM historique WHERE id_utilisateur = %s) > 5 THEN FALSE 
                ELSE TRUE
        END AS resultat;
        '''
        mycursor.execute(sql, (client_id, ))
        test2 = mycursor.fetchone()['resultat']
        if(test2):
            sql = '''
            INSERT INTO historique (id_utilisateur, id_equipement, date_consultation)
            VALUES (%s, %s, %s)
            '''
            mycursor.execute(sql, (client_id, article_id, date))
            get_db().commit()
        else:
            sql = '''
            SELECT MIN(date_consultation) as date_plus_ancienne FROM historique WHERE id_utilisateur = %s;
            '''
            mycursor.execute(sql, (client_id, ))
            ancien = mycursor.fetchone()
            sql = '''
            SELECT MIN(id_historique) as id_historique FROM historique WHERE id_utilisateur = %s AND date_consultation = %s;
            '''
            mycursor.execute(sql, (client_id, ancien['date_plus_ancienne']))
            id_ancien = mycursor.fetchone()
            sql = '''
            UPDATE historique SET id_equipement = %s, date_consultation = %s
            WHERE id_historique = %s AND id_utilisateur = %s;
            '''
            mycursor.execute(sql, (article_id, date, id_ancien['id_historique'], client_id))
            get_db().commit()
    else:
        sql = '''
        SELECT id_historique FROM historique WHERE id_utilisateur = %s AND id_equipement = %s;
        '''
        mycursor.execute(sql, (client_id, article_id))
        id_historique = mycursor.fetchone()
        sql = '''
        UPDATE historique SET date_consultation = %s, nombre_consultation = nombre_consultation + 1
        WHERE id_historique = %s AND id_utilisateur = %s;
        '''
        mycursor.execute(sql, (date, id_historique['id_historique'], client_id))
        get_db().commit()


@client_liste_envies.route('/client/envies/down', methods=['get'])
def client_liste_envies_article_move_down():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = ''' SELECT ordre FROM liste_envie WHERE id_utilisateur = %s AND id_equipement = %s;'''
    mycursor.execute(sql, (id_client, id_article))
    ordre = mycursor.fetchone()['ordre']
    print(ordre)
    sql = '''
    UPDATE liste_envie SET ordre = ordre + 1
    WHERE id_utilisateur = %s AND ordre = %s;
    '''
    mycursor.execute(sql, (id_client, ordre - 1))
    
    sql = '''
    UPDATE liste_envie SET ordre = ordre - 1
    WHERE id_utilisateur = %s AND id_equipement = %s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    
    
    get_db().commit()
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/up', methods=['get'])
def client_liste_envies_article_move_up():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = ''' SELECT ordre FROM liste_envie WHERE id_utilisateur = %s AND id_equipement = %s;'''
    mycursor.execute(sql, (id_client, id_article))
    ordre = mycursor.fetchone()['ordre']
    
    sql = '''
    UPDATE liste_envie SET ordre = ordre - 1
    WHERE id_utilisateur = %s AND ordre = %s;
    '''
    mycursor.execute(sql, (id_client, ordre + 1))
    
    sql = '''
    UPDATE liste_envie SET ordre = ordre + 1
    WHERE id_utilisateur = %s AND id_equipement = %s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    
    
    get_db().commit()
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/last', methods=['get'])
def client_liste_envies_article_move_last():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    
    sql = ''' SELECT min(ordre) as min_ordre FROM liste_envie WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client, ))
    min_ordre = mycursor.fetchone()['min_ordre']
    
    sql = '''
    SELECT ordre FROM liste_envie WHERE id_utilisateur = %s AND id_equipement = %s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    ordre = mycursor.fetchone()['ordre']
    
    sql = ''' SELECT * FROM liste_envie WHERE id_utilisateur = %s AND ordre < %s;'''
    mycursor.execute(sql, (id_client, ordre))
    liste = mycursor.fetchall()
    
    
    for article in liste:
        sql = '''
        UPDATE liste_envie SET ordre = ordre + 1
        WHERE id_utilisateur = %s AND id_equipement = %s
        '''
        mycursor.execute(sql, (id_client, article['id_equipement']))
        
    sql = '''
        UPDATE liste_envie SET ordre = %s
        WHERE id_utilisateur = %s AND id_equipement = %s
    '''
    
    mycursor.execute(sql, (min_ordre, id_client, id_article))
    get_db().commit()
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_article_move_first():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = ''' SELECT max(ordre) as min_ordre FROM liste_envie WHERE id_utilisateur = %s;'''
    mycursor.execute(sql, (id_client, ))
    max_ordre = mycursor.fetchone()['min_ordre']
    
    sql = '''
    SELECT ordre FROM liste_envie WHERE id_utilisateur = %s AND id_equipement = %s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    ordre = mycursor.fetchone()['ordre']
    
    sql = ''' SELECT * FROM liste_envie WHERE id_utilisateur = %s AND ordre > %s;'''
    mycursor.execute(sql, (id_client, ordre))
    liste = mycursor.fetchall()
    
    
    for article in liste:
        sql = '''
        UPDATE liste_envie SET ordre = ordre - 1
        WHERE id_utilisateur = %s AND id_equipement = %s
        '''
        mycursor.execute(sql, (id_client, article['id_equipement']))
        
    sql = '''
        UPDATE liste_envie SET ordre = %s
        WHERE id_utilisateur = %s AND id_equipement = %s
    '''
    mycursor.execute(sql, (max_ordre, id_client, id_article))
    
    get_db().commit()
    return redirect('/client/envies/show')
