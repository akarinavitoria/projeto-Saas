from .database import db

# Modelo de Academia
class Gym(db.Model):
    __tablename__ = 'gyms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    plans = db.relationship('Plan', backref='gym', lazy=True)

# Modelo de Cliente
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Modelo de Profissional
class Professionals(db.Model):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=False)

# Modelo de Planos de Academia
class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=False)

# Modelo de Registro 
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    gym_id = db.Column(db.Integer, nullable=False)
    plan = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Registration {self.id}>"