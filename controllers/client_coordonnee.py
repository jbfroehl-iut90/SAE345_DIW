#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    utilisateur=[]

    sql = ''' SELECT * FROM utilisateur WHERE id_utilisateur = %s '''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    sql = ''' SELECT * FROM adresse LEFT JOIN utilisateur ON adresse.id_utilisateur = utilisateur.id_utilisateur WHERE utilisateur.id_utilisateur = %s '''
    mycursor.execute(sql, (id_client,))
    adresses = mycursor.fetchall()
    nb_adresses = mycursor.rowcount

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                          , adresses=adresses
                          , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' select * from utilisateur where id_utilisateur = %s '''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    utilisateur = None

    if utilisateur :
        flash(u'cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               #, user=user
                               )
    
    sql = ''' UPDATE utilisateur SET nom = %s, login = %s, email = %s WHERE id_utilisateur = %s '''
    mycursor.execute(sql, (nom, login, email, id_client))

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    # Si l'adresse n'est pas utilisée dans une commande
    sql = ''' SELECT * FROM commande WHERE adresse_id = %s OR billing_address_id = %s '''
    mycursor.execute(sql, (id_adresse, id_adresse))
    commande = mycursor.fetchone()

    if commande is None:
        sql = ''' DELETE FROM adresse where id_adresse = %s '''
        mycursor.execute(sql, (id_adresse,))
        get_db().commit()
    else:
        flash(u'Adresse utilisée dans une commande, passage en inactive', 'alert-warning')
        sql = ''' UPDATE adresse SET valide = 0 WHERE id_adresse = %s '''
        mycursor.execute(sql, (id_adresse,))
        get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' SELECT * FROM utilisateur
    LEFT JOIN adresse ON utilisateur.id_utilisateur = adresse.id_utilisateur
    WHERE utilisateur.id_utilisateur = %s '''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    dept = request.form.get('dept')

    sql = ''' INSERT INTO adresse (adresse,code_postal,ville,valide, departement, nom, id_utilisateur) VALUES (%s, %s, %s, %s, %s, %s, %s) '''
    mycursor.execute(sql, (rue, code_postal, ville, 0, dept, nom, id_client))
    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql = ''' SELECT * FROM utilisateur WHERE id_utilisateur=%s '''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    sql = ''' SELECT * FROM adresse WHERE id_adresse=%s '''
    mycursor.execute(sql, (id_adresse,))
    adresse = mycursor.fetchone()

    return render_template('/client/coordonnee/edit_adresse.html'
                           ,utilisateur=utilisateur
                           ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')
    dept = request.form.get('dept')

    sql = ''' UPDATE adresse SET adresse = %s, code_postal = %s, ville = %s, departement = %s, nom = %s WHERE id_adresse = %s '''
    mycursor.execute(sql, (rue, code_postal, ville, dept, nom, id_adresse))
    get_db().commit()

    return redirect('/client/coordonnee/show')
