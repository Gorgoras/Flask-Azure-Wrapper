from flask import render_template, flash, redirect, session, request
from flask_login import current_user, login_user
from app import app
from app.forms import LoginForm, CreateResGroupForm
import azure.common.credentials as cred
from azure.mgmt.resource import ResourceManagementClient

@app.route('/')
@app.route('/index')
def index():
    try:
        logged = session['loggedIn']
    except:
        logged = 'F'
    if logged == 'T':
        return render_template('index.html', title='Home', user={'username': session['user'] })

    return render_template('index.html', title='Home', user={'username': 'Random User' })

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        logged = session['loggedIn']
    except:
        logged = 'F'
    if logged == 'F':
        form = LoginForm()
        if form.validate_on_submit():
            user = form.username.data
            pasw = form.password.data
            try:
                cred.UserPassCredentials(user, pasw, verify=True)
                session['user'] = user
                session['pasw'] = pasw
                session['loggedIn'] = 'T'
                return redirect('/index')
            except Exception:
                flash('Login failed for user {}.'.format(
                    form.username.data))
                return redirect('/login')
        return render_template('login.html', title='Sign In', form=form)
    else:
        return redirect('/index')

@app.route('/logout')
def logout():
    session['loggedIn'] = 'F'
    flash('Successfully logged out')
    return render_template('index.html', title='Home', user={'username': 'Random User' })

@app.route('/createResourceGroup', methods=['GET', 'POST'])
def createResourceGroup():
    if request.method == 'GET':
        try:
            logged = session['loggedIn']
        except:
            logged = 'F'
        if logged == 'T':
            form = CreateResGroupForm()
            return render_template('resourcegroup.html', title='Create Resource Group', form=form)
        else:
            flash("You must login before creating resources!!")
            return redirect('/index')
    else:
        try:
            form = CreateResGroupForm()
            credentials = cred.UserPassCredentials(session['user'], session['pasw'], verify=True)
            subsID = form.subscriptionID.data
            RGName = form.rg_name.data
            location = form.region.data
            resource_client = ResourceManagementClient(credentials, subsID)
            resource_client.resource_groups.create_or_update(resource_group_name=RGName, parameters={'location': location})
            flash("Resource Group created successfully")
            return redirect('/index')
        except Exception as ex:
            errorMessage = repr(ex)
            flash("Cannot create resource group with those settings" + errorMessage)
    return redirect('/index')

@app.route('/createsqlserver')
def createSqlServer():
    if request.method == 'GET':
        try:
            logged = session['loggedIn']
        except:
            logged = 'F'
        if logged == 'T':
            #Logic to create Sql Server
        else:
            flash("You must login before creating resources!!")
            return redirect('/index')