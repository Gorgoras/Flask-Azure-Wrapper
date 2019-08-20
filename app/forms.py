from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask import session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class CreateResGroupForm(FlaskForm):
    rg_name = StringField('Resource Group Name')
    subscriptionID = StringField('SubscriptionId')
    region = SelectField('Region', choices=[('eastasia','East Asia'),
        ('southeastasia','Southeast Asia'),
        ('centralus','Central US'),
        ('eastus','East US'),
        ('eastus2','East US 2'),
        ('westus','West US'),
        ('northcentralus','North Central US'),
        ('southcentralus','South Central US'),
        ('northeurope','North Europe'),
        ('westeurope','West Europe'),
        ('japanwest','Japan West'),
        ('japaneast','Japan East'),
        ('brazilsouth','Brazil South'),
        ('australiaeast','Australia East'),
        ('australiasoutheast','Australia Southeast'),
        ('southindia','South India'),
        ('centralindia','Central India'),
        ('westindia','West India'),
        ('canadacentral','Canada Central'),
        ('canadaeast','Canada East'),
        ('uksouth','UK South'),
        ('ukwest','UK West'),
        ('westcentralus','West Central US'),
        ('westus2','West US 2'),
        ('koreacentral','Korea Central'),
        ('koreasouth','Korea South'),
        ('francecentral','France Central'),
        ('francesouth','France South'),
        ('australiacentral','Australia Central'),
        ('australiacentral2','Australia Central 2'),
        ('uaecentral','UAE Central'),
        ('uaenorth','UAE North'),
        ('southafricanorth','South Africa North'),
        ('southafricawest','South Africa West')])
    submit = SubmitField('Create Resource Group!')

class CreateSqlServerForm(FlaskForm):
    rg_name = StringField('Resource Group Name')
    subscriptionID = StringField('SubscriptionId')
    sql_svname = StringField('Sql Server Name')
    admin_user = StringField('Admin Username')
    admin_pass = PasswordField('Admin Password')
    sql_dbname = StringField('Database Name')
    submit = SubmitField('Create Sql Server!')
    region = SelectField('Region', choices=[('eastasia','East Asia'),
        ('southeastasia','Southeast Asia'),
        ('centralus','Central US'),
        ('eastus','East US'),
        ('eastus2','East US 2'),
        ('westus','West US'),
        ('northcentralus','North Central US'),
        ('southcentralus','South Central US'),
        ('northeurope','North Europe'),
        ('westeurope','West Europe'),
        ('japanwest','Japan West'),
        ('japaneast','Japan East'),
        ('brazilsouth','Brazil South'),
        ('australiaeast','Australia East'),
        ('australiasoutheast','Australia Southeast'),
        ('southindia','South India'),
        ('centralindia','Central India'),
        ('westindia','West India'),
        ('canadacentral','Canada Central'),
        ('canadaeast','Canada East'),
        ('uksouth','UK South'),
        ('ukwest','UK West'),
        ('westcentralus','West Central US'),
        ('westus2','West US 2'),
        ('koreacentral','Korea Central'),
        ('koreasouth','Korea South'),
        ('francecentral','France Central'),
        ('francesouth','France South'),
        ('australiacentral','Australia Central'),
        ('australiacentral2','Australia Central 2'),
        ('uaecentral','UAE Central'),
        ('uaenorth','UAE North'),
        ('southafricanorth','South Africa North'),
        ('southafricawest','South Africa West')])

class CreateStorageAccountForm(FlaskForm):
    rg_name = StringField('Resource Group Name')
    subscriptionID = StringField('SubscriptionId')
    storageName = StringField('Storage Name')
    region = SelectField('Region', choices=[('eastasia','East Asia'),
        ('southeastasia','Southeast Asia'),
        ('centralus','Central US'),
        ('eastus','East US'),
        ('eastus2','East US 2'),
        ('westus','West US'),
        ('northcentralus','North Central US'),
        ('southcentralus','South Central US'),
        ('northeurope','North Europe'),
        ('westeurope','West Europe'),
        ('japanwest','Japan West'),
        ('japaneast','Japan East'),
        ('brazilsouth','Brazil South'),
        ('australiaeast','Australia East'),
        ('australiasoutheast','Australia Southeast'),
        ('southindia','South India'),
        ('centralindia','Central India'),
        ('westindia','West India'),
        ('canadacentral','Canada Central'),
        ('canadaeast','Canada East'),
        ('uksouth','UK South'),
        ('ukwest','UK West'),
        ('westcentralus','West Central US'),
        ('westus2','West US 2'),
        ('koreacentral','Korea Central'),
        ('koreasouth','Korea South'),
        ('francecentral','France Central'),
        ('francesouth','France South'),
        ('australiacentral','Australia Central'),
        ('australiacentral2','Australia Central 2'),
        ('uaecentral','UAE Central'),
        ('uaenorth','UAE North'),
        ('southafricanorth','South Africa North'),
        ('southafricawest','South Africa West')])