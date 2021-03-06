from flask import render_template, flash, redirect, session, request
from flask_login import current_user, login_user
from app import app
from app.forms import LoginForm, CreateResGroupForm, CreateSqlServerForm, CreateStorageAccountForm, CreateDataFactoryForm
import azure.common.credentials as cred
import azure.mgmt.subscription as subs
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient as blobacc
from azure.mgmt.storage.models import StorageAccountCreateParameters as blob_model
from azure.mgmt.storage.models import (Sku, SkuName, Kind)
from azure.mgmt.datafactory import DataFactoryManagementClient as adf
from azure.mgmt.datafactory.models import Factory as adf_model

@app.route('/')
@app.route('/index')
def index():
    try:
        logged = session['loggedIn']
    except:
        logged = 'F'
    if logged == 'T':
        s = session['subscription_id']
        subscription = {'subs_id': s}
        return render_template('index.html', title='Home', user={'username': session['user'] }, subscription = subscription)

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
                credentials = cred.UserPassCredentials(user, pasw, verify=True)
                session['user'] = user
                session['pasw'] = pasw
                session['loggedIn'] = 'T'
                #Get subscriptions
                su = subs.SubscriptionClient(credentials=credentials)
                subsList = [sub.as_dict() for sub in su.subscriptions.list()]
                session['subscription_id'] = subsList[0]['subscription_id']
                #Get resource groups
                #resource_client = ResourceManagementClient(credentials, session['subscription_id'])
                #resGroups = [resC.as_dict()['name'] for resC in resource_client.resource_groups.list()]
                #session['resource_groups'] = resGroups
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
            form.subscriptionID.data = session['subscription_id']
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

@app.route('/createsqlserver', methods=['GET', 'POST'])
def createSqlServer():
    if request.method == 'GET':
        try:
            logged = session['loggedIn']
        except:
            logged = 'F'
        if logged == 'T':
            form = CreateSqlServerForm()
            user = session['user']
            pasw = session['pasw']
            credentials = cred.UserPassCredentials(user, pasw, verify=True)
            resource_client = ResourceManagementClient(credentials, session['subscription_id'])
            resGroups = []
            for resC in resource_client.resource_groups.list():
                resGroups.append((resC.as_dict()['name'], resC.as_dict()['name']))
            form.rg_name.choices = resGroups
            form.subscriptionID.data = session['subscription_id']
            return render_template('sqlserver.html', title='Create Sql Server', form=form)
        else:
            flash("You must login before creating resources!!")
            return redirect('/index')
    else:
        try:
            form = CreateSqlServerForm()
            credentials = cred.UserPassCredentials(session['user'], session['pasw'], verify=True)
            subsID = form.subscriptionID.data
            RGName = form.rg_name.data
            location = form.region.data
            sql_svname = form.sql_svname.data
            sql_dbname = form.sql_dbname.data
            dbuser = form.admin_user.data
            dbpass = form.admin_pass.data

            sql_client = SqlManagementClient(credentials=credentials, subscription_id=subsID)
            sql_client.servers.create_or_update(
                    RGName,
                    sql_svname,
                    {
                        'location': location,
                        'version': '12.0',  # Required for create
                        'administrator_login': dbuser,  # Required for create
                        'administrator_login_password': dbpass  # Required for create
                    }
                )
            async_db_create = sql_client.databases.create_or_update(
                    RGName,
                    sql_svname,
                    sql_dbname,
                    {
                        'location': location
                    }
                )
            async_db_create.result()
            flash("Sql Server created successfully")
            return redirect('/index')
        except Exception as ex:
            errorMessage = repr(ex)
            flash("Cannot create sql server with those settings. " + errorMessage)
    return redirect('/index')

@app.route('/createresources')
def createResources():
    try:
        logged = session['loggedIn']
    except:
        logged = 'F'
    if logged == 'T':
        return render_template('createresources.html', title='Create Resources')
    else:
        flash("You must login before creating resources!!")
        return redirect('/index')

@app.route('/createstorageaccount', methods=['GET', 'POST'])
def createStorageAccount():
    if request.method == 'GET':
        try:
            logged = session['loggedIn']
        except:
            logged = 'F'
        if logged == 'T':
            form = CreateStorageAccountForm()
            user = session['user']
            pasw = session['pasw']
            credentials = cred.UserPassCredentials(user, pasw, verify=True)
            resource_client = ResourceManagementClient(credentials, session['subscription_id'])
            resGroups = []
            for resC in resource_client.resource_groups.list():
                resGroups.append((resC.as_dict()['name'], resC.as_dict()['name']))
            form.rg_name.choices = resGroups
            form.subscriptionID.data = session['subscription_id']
            return render_template('storageaccount.html', title='Create Storage Account', form=form)
        else:
            flash("You must login before creating resources!!")
            return redirect('/index')
    else:
        try:
            form = CreateStorageAccountForm()
            
            credentials = cred.UserPassCredentials(session['user'], session['pasw'], verify=True)
            subsID = form.subscriptionID.data
            RGName = form.rg_name.data
            location = form.region.data
            storageName = form.storageName.data
            storage_client = blobacc(credentials,subsID)
            availability = storage_client.storage_accounts.check_name_availability(storageName)
            if availability.name_available:
                storage_client.storage_accounts.create(RGName, storageName, blob_model(sku=Sku(name=SkuName.standard_ragrs),
                        kind=Kind.storage,
                        location=location))
            else:
                flash("Name not available!")
                return redirect('/index')
            flash("Storage Account created successfully")
            return redirect('/index')
        except Exception as ex:
            errorMessage = repr(ex)
            flash("Cannot create storage account with those settings. " + errorMessage)
    return redirect('/index')

@app.route('/createdatafactory', methods=['GET', 'POST'])
def createDataFactory():
    if request.method == 'GET':
        try:
            logged = session['loggedIn']
        except:
            logged = 'F'
        if logged == 'T':
            form = CreateDataFactoryForm()
            user = session['user']
            pasw = session['pasw']
            credentials = cred.UserPassCredentials(user, pasw, verify=True)
            resource_client = ResourceManagementClient(credentials, session['subscription_id'])
            resGroups = []
            for resC in resource_client.resource_groups.list():
                resGroups.append((resC.as_dict()['name'], resC.as_dict()['name']))
            form.rg_name.choices = resGroups
            form.subscriptionID.data = session['subscription_id']
            return render_template('datafactory.html', title='Create Data Factory', form=form)
        else:
            flash("You must login before creating resources!!")
            return redirect('/index')
    else:
        try:
            form = CreateStorageAccountForm()
            credentials = cred.UserPassCredentials(session['user'], session['pasw'], verify=True)
            subsID = form.subscriptionID.data
            RGName = form.rg_name.data
            location = form.region.data
            datafactoryName = form.datafactoryName.data
            adf_client = adf(credentials, subsID)
            model = adf_model(location=location)
            adf_client.factories.create_or_update(resource_group_name=RGName, factory_name=datafactoryName, factory=model)
            flash("Data Factory created successfully!!")
            return redirect('/index')
        except Exception as ex:
            errorMessage = repr(ex)
            flash("Cannot create data factory with those settings. " + errorMessage)
    return redirect('/index')