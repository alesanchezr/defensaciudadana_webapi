from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os


path = "./pdf_store"
if os.path.isfile(path) == True:
    os.mkdir(path)
else:
    print("")

app = Flask(__name__) #instancio la aplicación Flask

#configuraciones de la app Flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://defensaciudadana:Guillermo174027447@localhost/defensaciudadana_webapi'

db = SQLAlchemy(app) #instancio el objeto SQLAlchemy, pues estos son instancias de clases de los frameworck


class Clients(db.Model):
    clients_id = db.Column(db.Integer, primary_key=True)
    clients_name = db.Column(db.String(50), unique=True, nullable=False)
    clients_rut = db.Column(db.String(16), unique=True, nullable=False)
    clients_nationality = db.Column(db.String(20), unique=False, nullable=True)
    clients_civilStatus = db.Column(db.String(30), unique=True, nullable=True)
    clients_job = db.Column(db.String(30), unique=True, nullable=True)
    clients_address = db.Column(db.String(100), unique=False, nullable=True)
    clients_contact = db.Column(db.String(40), unique=False, nullable=True)

    clients_relationship_cases = db.relationship('Cases', backref='case_client')
    clients_relationship_corporations = db.relationship('Corporations', backref='corporation_client')


    def __repr__(self):
        return '<Clients %r>' % self.clients_id, self.clients_name, self.clients_rut, self.clients_nationality, self.clients_civilStatus, self.clients_job, self.clients_address, self.clients_contact

    def serialize(self):
        return {
            "clients_id": self.clients_id,
            "clients_name": self.clients_name,
            "clients_rut": self.clients_rut,
            "clients_nationality": self.clients_nationality,
            "clients_civilStatus": self.clients_civilStatus,
            "clients_job": self.clients_job,
            "clients_address": self.clients_address,
            "clients_contact": self.clients_contact,
        }

class Cases(db.Model):
    __tablename__ ='cases'
    cases_id = db.Column(db.Integer, primary_key=True)
    cases_description = db.Column(db.String(200), unique=False, nullable=False)
    cases_rol_rit_ruc = db.Column(db.String(50), unique=False, nullable=True)
    cases_trial_entity = db.Column(db.String(60), unique=False, nullable=False)
    cases_legalIssue = db.Column(db.String(20), unique=False, nullable=True)
    cases_procedure = db.Column(db.String(60), unique=False, nullable=True)
    cases_objetive = db.Column(db.String(100), unique=False, nullable=False)
    cases_update = db.Column(db.String(300), unique=False, nullable=True)
    cases_updateDate = db.Column(db.DateTime, unique=False, nullable = True)
    cases_activeCase = db.Column(db.Boolean(60), unique=False, nullable=True)
    cases_incomeDate = db.Column(db.DateTime, unique=False, nullable = False, default=datetime.datetime.utcnow)
    cases_deadLine = db.Column(db.DateTime, unique=False, nullable = True)

    #se pone minuscula la tabla clients pues mira directamente a la base de datos y no a la clase de python
    cases_client_id = db.Column(db.Integer, db.ForeignKey('clients.clients_id'), nullable=False)
    # establece relacion con tabla documents
    cases_relationship_documents = db.relationship('Documents', backref='case_document')


    def __repr__(self):
       return '<Cases %r>' %  self.cases_id, self.cases_description, self.cases_rol_rit_ruc, self.cases_trial_entity, self.cases_legalIssue, self.cases_procedure, self.cases_objetive, self.cases_update, self.cases_updateDate, self.cases_activeCase, self.cases_incomeDate, self.cases_deadLine, 


class Documents(db.Model):
    __tablename__='documents'
    documents_id = db.Column(db.Integer, primary_key=True) 
    documents_type = db.Column(db.String(100), unique=False, nullable=True)
    documents_date = db.Column(db.DateTime, unique=False, nullable = False, default=datetime.datetime.utcnow)

    documents_cases_id = db.Column(db.Integer, db.ForeignKey('cases.cases_id'))

    def __repr__(self):
        return '<Document %r>' % self.documents_id, self.documents_type, self.documents_date



class Corporations(db.Model):
    __tablename__='corporations'
    corporation_id = db.Column(db.Integer, primary_key=True)
    corporation_name = db.Column(db.String(200), unique=False, nullable=False)
    corporation_type = db.Column(db.String(50), unique=False, nullable=True)    
    corporation_CBR = db.Column(db.String(50), unique=False, nullable=False)
    corporation_rolSII = db.Column(db.String(16), unique=False, nullable=True)
    corporation_taxType = db.Column(db.String(15), unique=False, nullable=True)

    corporation_client_id = db.Column(db.ForeignKey('clients.clients_id'))
    
    

    def __repr__(self):
        return '<Message %r>' % self.corporation_id, self.corporation_name, self.corporation_type, self.corporation_CBR, self.corporation_rolSII, self.corporation_taxType
 


@app.route('/')
def user():
    return "HOLA MUNDO"

@app.route('/clientes/<string:rut>', methods = ['GET','POST', 'PUT', 'DELETE'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def clients(rut):
    if request.method == 'GET':
        list=[]
        if rut == "17.402.744-7" or rut == "20.968.696-1":
            resp = db.session.query(Clients).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS
            for item in resp:
                list.append({
            "clients_id": item.clients_id,
            "clients_name": item.clients_name,
            "clients_rut": item.clients_rut,
            "clients_nationality": item.clients_nationality,
            "clients_civilStatus": item.clients_civilStatus,
            "clients_job": item.clients_job,
            "clients_address": item.clients_address,
            "clients_contact": item.clients_contact
        })
            return jsonify({"resp": list}),200
        else:
            resp = db.session.query(Clients).filter_by(clients_rut=rut).all()
            for item in resp:
                list.append({
            "clients_id": item.clients_id,
            "clients_name": item.clients_name,
            "clients_rut": item.clients_rut,
            "clients_nationality": item.clients_nationality,
            "clients_civilStatus": item.clients_civilStatus,
            "clients_job": item.clients_job,
            "clients_address": item.clients_address,
            "clients_contact": item.clients_contact
        })
            return jsonify({"resp": list}),200

    if request.method == 'POST':
        incomingData = request.get_json()
        insertedData= Clients(clients_name=incomingData['name'], clients_rut=incomingData['rut'], clients_nationality=incomingData['nationality'], clients_civilStatus=incomingData['civilStatus'], clients_job=incomingData['job'], clients_address=incomingData['address'], clients_contact=incomingData['contact'] )
        db.session.add(insertedData)
        db.session.commit()
        return "data inserted",200

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Clients.query.filter_by(clients_rut=rut).first()
        if incomingData['name'] != "":
            updateData.name = incomingData['name']
            db.session.commit()
            return "updated"

        if incomingData['rut'] != "":
            updateData.clients_rut = incomingData['rut']
            db.session.commit()
            return "updated"

        if incomingData['nationality'] != "":
            updateData.clients_nationality = incomingData['nationality']
            db.session.commit()
            return "updated"
        
        if incomingData['civilStatus'] != "":
            updateData.clients_civilStatus = incomingData['civilStatus'] 
            db.session.commit()
            return "updated"

        if incomingData['job'] != "":
            updateData.clients_job = incomingData['job']
            db.session.commit()
            return "updated"
        
        if incomingData['address'] != "":
            updateData.clients_address = incomingData['address'] 
            db.session.commit()
            return "updated"

        if incomingData['contact'] != "":
            updateData.clients_contact = incomingData['contact']
            db.session.commit()
            return "updated"     
        

    if request.method == 'DELETE':
        deletedRow= Clients.query.filter_by(clients_rut=rut).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200


@app.route('/casos/<string:rut>', methods = ['GET','POST', 'PUT', 'DELETE'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def cases(rut):
    if request.method == 'GET':
        list=[]
        if rut == "17.402.744-7" or rut == "20.968.696-1":
            resp = db.session.query(Cases).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS
            for item in resp:
                list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id
        })
            return jsonify({"resp": list}),200
        else:
            resp = db.session.query(Clients).filter_by(clients_rut=rut).first()
            client_id= resp.clients_id
            cases = db.session.query(Cases).filter_by(cases_client_id=client_id).all()

            for item in cases:
                list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id
        })

            return jsonify({"resp": list}),200

    if request.method == 'POST':
        incomingData = request.get_json()
        insertedData= Cases(cases_description=incomingData['cases_description'], cases_rol_rit_ruc=incomingData['cases_rol_rit_ruc'], cases_trial_entity=incomingData['cases_trial_entity'], cases_legalIssue=incomingData['cases_legalIssue'], cases_procedure=incomingData['cases_procedure'], cases_objetive=incomingData['cases_objetive'], cases_update=incomingData['cases_update'], cases_activeCase=incomingData['cases_activeCase'], cases_client_id=incomingData['cases_client_id'] )
        db.session.add(insertedData)
        db.session.commit()
        return "data inserted",200

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["cases_rol_rit_ruc"]).first()
        if incomingData['cases_description'] != " ":
            updateData.cases_description = incomingData['cases_description'] 
            db.session.commit()
            return "updated"
        

    if request.method == 'DELETE':
        incomingData = request.get_json()
        deletedRow= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["cases_rol_rit_ruc"]).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200
        
        