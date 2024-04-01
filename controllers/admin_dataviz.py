#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()

    # Equipements join couleur et taille
    sql = ''' SELECT * FROM equipement 
    JOIN declinaison ON equipement.id_equipement = declinaison.id_equipement
    JOIN couleur ON declinaison.couleur_declinaison = couleur.id_couleur
    JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
    JOIN taille ON declinaison.taille_declinaison = taille.id_taille;'''
    mycursor.execute(sql)
    equipement = mycursor.fetchall()

    sql = ''' SELECT COUNT(id_equipement) as nbr_articles, libelle_categorie_sport FROM equipement
              JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
              GROUP BY libelle_categorie_sport;'''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle_categorie_sport']) for row in datas_show]
    values = [int(row['nbr_articles']) for row in datas_show]


    sql = ''' SELECT COUNT(id_equipement) as nbr_articles FROM equipement;'''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()

    sql = ''' SELECT COUNT(equipement.id_equipement) as nbr_articles, categorie_sport.id_categorie_sport, categorie_sport.libelle_categorie_sport 
    FROM equipement JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport 
    GROUP BY categorie_sport.id_categorie_sport, categorie_sport.libelle_categorie_sport; '''
    mycursor.execute(sql)
    types_article_nb = mycursor.fetchall()

    # Nombre d'equipements par type d'equipement
    sql = ''' SELECT COUNT(id_equipement) as nbr_articles, libelle_categorie_sport FROM equipement
              JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
              GROUP BY libelle_categorie_sport;'''
    mycursor.execute(sql)
    equipement_par_type = mycursor.fetchall()

    # Nombre de déclinaisons par equipement
    sql = ''' SELECT COUNT(id_declinaison) as nbr_declinaisons, libelle_equipement FROM declinaison LEFT JOIN equipement ON declinaison.id_equipement = equipement.id_equipement GROUP BY libelle_equipement;'''
    mycursor.execute(sql)
    datas = mycursor.fetchall()
    nb_declinaisons = [int(row['nbr_declinaisons']) for row in datas]
    labels_decli = [str(row['libelle_equipement']) for row in datas]
    print(nb_declinaisons)
    print(labels_decli)

    # Couts des equipements par type d'equipement et en fonction des stocks
    sql = ''' SELECT SUM(prix_equipement * stock) as prix_total, libelle_categorie_sport FROM equipement 
              JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
              JOIN declinaison ON equipement.id_equipement = declinaison.id_equipement
              GROUP BY libelle_categorie_sport;'''
    mycursor.execute(sql)
    datas = mycursor.fetchall()
    prix_total_cat = [int(row['prix_total']) for row in datas]
    labels_prix = [str(row['libelle_categorie_sport']) for row in datas]

    total = 0
    for prix in prix_total_cat:
        total += prix

    return render_template('admin/dataviz/dataviz_stocks.html'
                           , equipement=equipement
                           , datas_show=datas_show
                           , labels=labels
                           , values=values
                           , types_articles_nb=types_article_nb
                           ,equipement_par_type=equipement_par_type
                           ,nb_declinaisons=nb_declinaisons
                           ,labels_decli=labels_decli
                           ,prix_total_cat=prix_total_cat
                           ,labels_prix=labels_prix
                           ,total=total)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    mycursor = get_db().cursor()
    # Compte le nombre de d'adresses par département
    sql = ''' SELECT COUNT(id_adresse) as nbr_dept, departement FROM adresse GROUP BY departement;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    print(adresses)

    # total des adresses
    total = 0
    for element in adresses:
        total += element['nbr_dept']

    # recherche de la valeur maxi "nombre" dans les départements
    maxAddress = 0
    for element in adresses:
        if element['nbr_dept'] > maxAddress:
            maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    if maxAddress != 0:
        for element in adresses:
            indice = element['nbr_dept'] / maxAddress
            element['indice'] = round(indice,2)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                            , total=total)


@admin_dataviz.route('/admin/dataviz/dataviz_commentaire')
def show_commentaire_data():
    datas_show=[]
    labels=[]
    values=[]
    mycursor = get_db().cursor()
    sql = '''
            SELECT COUNT(id_commentaire) as nb_commentaire_total from commentaire;
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    print(datas_show)
    
    sql = '''
            SELECT id_equipement, libelle_equipement FROM equipement;
            '''
    
    mycursor.execute(sql)
    values = mycursor.fetchall()
    i = 0
    for row in values:
        id = row['id_equipement']
        sql = ''' SELECT COUNT(id_commentaire) as nb_commentaire FROM commentaire WHERE equipement_id = %s;'''
        mycursor.execute(sql, (id, ))
        values[i]['nb_commentaire'] = mycursor.fetchall()[0]['nb_commentaire']
        sql= ''' SELECT COUNT(id_note) as nb_note FROM note WHERE id_equipement = %s;'''
        mycursor.execute(sql, (id,))
        values[i]['nb_note'] = mycursor.fetchall()[0]['nb_note']

        i += 1
    
    
    values_graph = []
    sql = '''
            SELECT libelle_categorie_sport FROM categorie_sport;
           '''    
    mycursor.execute(sql)
    labels_val = mycursor.fetchall()
    labels = [str(row['libelle_categorie_sport']) for row in labels_val]
    
    sql = ''' SELECT id_categorie_sport FROM categorie_sport;'''
    mycursor.execute(sql)
    ids = mycursor.fetchall()
    
    temp_values = []
    for id in ids:
        sql = ''' SELECT COUNT(id_note) as nb_note FROM note
                    JOIN equipement ON note.id_equipement = equipement.id_equipement
                    JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
                    WHERE categorie_sport.id_categorie_sport = %s AND note > 3.9;'''
        mycursor.execute(sql, (id['id_categorie_sport'],))
        temp_values.append(mycursor.fetchall()[0]['nb_note'])
    
    values_graph = [int(row) for row in temp_values]
    
    temp_values = []
    for id in ids:
        sql = ''' SELECT COUNT(id_note) as nb_note FROM note
                    JOIN equipement ON note.id_equipement = equipement.id_equipement
                    JOIN categorie_sport ON equipement.sport_equipement_id = categorie_sport.id_categorie_sport
                    WHERE categorie_sport.id_categorie_sport = %s AND note < 3;'''
        mycursor.execute(sql, (id['id_categorie_sport'],))
        temp_values.append(mycursor.fetchall()[0]['nb_note'])
    
    values_graph2 = [int(row) for row in temp_values]
    print(values_graph)
    
    labels_2 = ['Commentaires invalidés', 'Commentaires validés']
    temp_values = []
    sql = ''' SELECT COUNT(id_commentaire) as nb_commentaire_invalider FROM commentaire WHERE statut=0;'''
    mycursor.execute(sql)
    temp_values.append(mycursor.fetchall()[0]['nb_commentaire_invalider'])
    sql = ''' SELECT COUNT(id_commentaire) as nb_commentaire_valider FROM commentaire WHERE statut=1;'''
    mycursor.execute(sql)
    temp_values.append(mycursor.fetchall()[0]['nb_commentaire_valider'])
    values_graph3 = [int(row) for row in temp_values]
    print(values_graph3)
    return render_template('admin/dataviz/dataviz_commentaire.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values,
                           values_graph = values_graph,
                           values_graph2 = values_graph2,
                           values_graph3 = values_graph3,
                            labels_2 = labels_2
                           )
