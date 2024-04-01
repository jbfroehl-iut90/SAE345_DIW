#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    article=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None

    sql = ''' SELECT * FROM equipement WHERE id_equipement = %s '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    sql = ''' SELECT * FROM couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = ''' SELECT * FROM taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    sql = ''' SELECT id_taille, libelle_taille FROM taille WHERE id_taille NOT IN (SELECT id_taille FROM declinaison WHERE id_equipement = %s) '''
    mycursor.execute(sql, (id_article,))
    d_taille_uniq = mycursor.fetchall()

    sql = ''' SELECT id_couleur, libelle_couleur FROM couleur WHERE id_couleur NOT IN (SELECT id_couleur FROM declinaison WHERE id_equipement = %s) '''
    mycursor.execute(sql, (id_article,))
    d_couleur_uniq = mycursor.fetchall()

    return render_template('admin/article/add_declinaison_article.html'
                           , article=article
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    sql = ''' INSERT INTO declinaison (id_equipement, stock, taille_declinaison, couleur_declinaison) VALUES (%s, %s, %s, %s) '''
    mycursor.execute(sql, (id_article, stock, taille, couleur))
    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_article = request.args.get('article_id')
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()
    declinaison_article=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None

    sql = ''' SELECT * FROM declinaison LEFT JOIN equipement ON equipement.id_equipement = declinaison.id_equipement WHERE id_declinaison = %s'''
    mycursor.execute(sql, (id_declinaison_article, ))
    declinaison_article = mycursor.fetchone()

    sql = ''' SELECT * FROM couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = ''' SELECT * FROM taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    sql = ''' SELECT id_taille, libelle_taille FROM taille WHERE id_taille NOT IN (SELECT id_taille FROM declinaison WHERE id_equipement = %s) '''
    mycursor.execute(sql, (id_article,))
    d_taille_uniq = mycursor.fetchall()

    sql = ''' SELECT * FROM couleur WHERE id_couleur NOT IN (SELECT id_couleur FROM declinaison WHERE id_equipement = %s)'''
    mycursor.execute(sql, (id_article,))
    d_couleur_uniq = mycursor.fetchall()

    return render_template('admin/article/edit_declinaison_article.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_article=declinaison_article
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article','')
    id_article = request.form.get('id_article','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')

    mycursor = get_db().cursor()

    sql = ''' UPDATE declinaison SET stock = %s, taille_declinaison = %s, couleur_declinaison = %s WHERE id_declinaison = %s '''
    mycursor.execute(sql, (stock, taille_id, couleur_id, id_declinaison_article))
    get_db().commit()

    message = u'declinaison_article modifié , id:' + str(id_declinaison_article) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article','')
    id_article = request.args.get('id_article','')
    mycursor = get_db().cursor()

    # Ne peux pas supprimer si il y a des commandes en cours avec cette declinaison
    sql = ''' SELECT * FROM ligne_commande WHERE declinaison_id = %s '''
    mycursor.execute(sql, (id_declinaison_article,))
    ligne_commande = mycursor.fetchone()

    if ligne_commande:
        flash(u'Impossible de supprimer cette declinaison, des commandes sont en cours avec cette declinaison', 'alert-danger')
        return redirect('/admin/article/edit?id_article=' + str(id_article))
    else: 
        sql = ''' DELETE FROM declinaison WHERE id_declinaison = %s '''
        mycursor.execute(sql, (id_declinaison_article,))
        get_db().commit()

    flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_article),  'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))
