from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mitsubishi_hvac_controller.models import User, Setting, Power
db.create_all()
if len(db.session.query(User).all()) == 0:
    print("Creating default admin user. Please change password ASAP.")
    hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
    user = User(
        username="admin",
        email="admin@admin.com",
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()

if len(db.session.query(Setting).all()) == 0:
    print("Creating default settings.")
    setting = Setting(setting='default',
                      temp='21',
                      fan_mode='Speed2',
                      climate_mode='Hot',
                      vanne_horizontal_mode='Middle',
                      vanne_vertical_mode='Middle')
    db.session.add(setting)
    db.session.commit()
print(db.session.query(Setting).all())


if len(db.session.query(Power).all()) == 0:
    print("Creating default settings.")
    power = Power(id=0, power=False)
    db.session.add(power)
    db.session.commit()
print(db.session.query(Power).all())


from mitsubishi_hvac_controller import routes
