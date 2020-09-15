import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy() #instancio el objeto SQLAlchemy, pues estos son instancias de clases de los frameworck

class Clients(db.Model):
    clients_id = db.Column(db.Integer, primary_key=True)
    clients_name = db.Column(db.String(300), unique=True, nullable=False)
    clients_rut = db.Column(db.String(16), unique=True, nullable=False)
    clients_nationality = db.Column(db.String(300), unique=False, nullable=True)
    clients_civilStatus = db.Column(db.String(300), unique=False, nullable=True)
    clients_job = db.Column(db.String(300), unique=False, nullable=True)
    clients_address = db.Column(db.String(300), unique=False, nullable=True)
    clients_contact = db.Column(db.String(300), unique=False, nullable=True)

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
    cases_description = db.Column(db.String(300), unique=False, nullable=False)
    cases_rol_rit_ruc = db.Column(db.String(300), unique=False, nullable=True)
    cases_trial_entity = db.Column(db.String(300), unique=False, nullable=False)
    cases_legalIssue = db.Column(db.String(300), unique=False, nullable=True)
    cases_procedure = db.Column(db.String(300), unique=False, nullable=True)
    cases_objetive = db.Column(db.String(300), unique=False, nullable=False)
    cases_update = db.Column(db.String(300), unique=False, nullable=True)
    cases_pendingTask = db.Column(db.String(300), unique=False, nullable=True)
    cases_updateDate = db.Column(db.DateTime, unique=False, nullable = True)
    cases_activeCase = db.Column(db.Boolean, unique=False, nullable=True)
    cases_incomeDate = db.Column(db.DateTime, unique=False, nullable = False, default=datetime.datetime.utcnow)
    cases_deadLine = db.Column(db.DateTime, unique=False, nullable = True)

    #se pone minuscula la tabla clients pues mira directamente a la base de datos y no a la clase de python
    cases_client_id = db.Column(db.Integer, db.ForeignKey('clients.clients_id'), nullable=False)
    cases_lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.lawyers_id'), nullable=False)
    # establece relacion con tabla documents
    cases_relationship_documents = db.relationship('Documents', backref='case_document')


    def __repr__(self):
       return '<Cases %r>' %  self.cases_id, self.cases_description, self.cases_rol_rit_ruc, self.cases_trial_entity, self.cases_legalIssue, self.cases_procedure, self.cases_objetive, self.cases_update, self.cases_updateDate, self.cases_pendingTask, self.cases_activeCase, self.cases_incomeDate, self.cases_deadLine,

class Lawyers(db.Model):
    __tablename__ ='lawyers'
    lawyers_id = db.Column(db.Integer, primary_key=True)
    lawyers_name = db.Column(db.String(300), unique=True, nullable=False)
    lawyers_field = db.Column(db.String(300), unique=False, nullable=False)
    lawyers_rut = db.Column(db.String(300), unique=True, nullable=False)
    lawyers_password = db.Column(db.String(300), unique=False, nullable=False)

    lawyers_relationship_cases = db.relationship('Cases', backref='case_lawyer')


    def __repr__(self):
        return '<Lawyers %r>' % self.lawyers_id, self.lawyers_name, self.lawyers_field, self.lawyers_rut, self.lawyers_password

    def serialize(self):
        return {
            "lawyers_id": self.lawyers_id,
            "lawyers_name": self.lawyers_name,
            "lawyers_field": self.lawyers_field,
            "lawyers_rut": self.lawyers_rut,
            "lawyers_password": self.lawyers_password
        }


class Documents(db.Model):
    __tablename__='documents'
    documents_id = db.Column(db.Integer, primary_key=True)
    documents_type = db.Column(db.String(100), unique=False, nullable=True)
    documents_date = db.Column(db.DateTime, unique=False, nullable = False, server_default=func.now())

    documents_cases_id = db.Column(db.Integer, db.ForeignKey('cases.cases_id'))

    def __repr__(self):
        return '<Document %r>' % self.documents_id, self.documents_type, self.documents_date



class Corporations(db.Model):
    __tablename__='corporations'
    corporation_id = db.Column(db.Integer, primary_key=True)
    corporation_name = db.Column(db.String(300), unique=False, nullable=False)
    corporation_type = db.Column(db.String(300), unique=False, nullable=True)
    corporation_CBR = db.Column(db.String(300), unique=False, nullable=False)
    corporation_rolSII = db.Column(db.String(300), unique=False, nullable=True)
    corporation_taxType = db.Column(db.String(300), unique=False, nullable=True)

    corporation_client_id = db.Column(db.ForeignKey('clients.clients_id'))



    def __repr__(self):
        return '<Corporations %r>' % self.corporation_id, self.corporation_name, self.corporation_type, self.corporation_CBR, self.corporation_rolSII, self.corporation_taxType
