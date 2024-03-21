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
    sql = '''
    
           '''
    # mycursor.execute(sql)
    # datas_show = mycursor.fetchall()
    # labels = [str(row['libelle']) for row in datas_show]
    # values = [int(row['nbr_articles']) for row in datas_show]

    # sql = '''
    #         
    #        '''
    datas_show=[]
    labels=[]
    values=[]

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


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
        print(row['id_equipement'])
        sql = ''' SELECT COUNT(id_commentaire) as nb_commentaire FROM commentaire WHERE equipement_id = %s;'''
        mycursor.execute(sql, (id, ))
        values[i]['nb_commentaire'] = mycursor.fetchall()[0]['nb_commentaire']
        sql= ''' SELECT COUNT(id_note) as nb_note FROM note WHERE id_equipement = %s;'''
        mycursor.execute(sql, (id,))
        values[i]['nb_note'] = mycursor.fetchall()[0]['nb_note']

        i += 1
    
    print(values)
    
    return render_template('admin/dataviz/dataviz_commentaire.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)
