# Azure-Resource-Creator
 Just an excuse to learn flask framework, and save time at work easily creating the most common Azure resources.

To run this. simply clone the repo and run
	
	cd C:/path/to/clonedRepo
	pip install -r requirements.txt
	SET FLASK_APP=mainPage.py
	flask run

# Using docker container
 You can also get this to work using docker:

	docker pull gorgoras/flask-azurerct
	docker run -p 5000:5000 gorgoras/flask-azurerct

After using any of the options, just go to localhost:5000 and login with your Azure account!! (soon it will support Service Principal too!)