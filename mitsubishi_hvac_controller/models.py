from mitsubishi_hvac_controller import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return str(self.username) + str(self.email)


class Setting(db.Model):
    setting = db.Column(db.String(8), primary_key=True)
    temp = db.Column(db.String(2), nullable=False)
    fan_mode = db.Column(db.String(8), nullable=False)
    climate_mode = db.Column(db.String(4), nullable=False)
    vanne_horizontal_mode = db.Column(db.String(16), nullable=False)
    vanne_vertical_mode = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return "Settings saved as " +  str(self.setting) + ": (" + \
               str(self.temp) + ", " + \
               str(self.fan_mode) + ", " + \
               str(self.climate_mode) + ", " + \
               str(self.vanne_horizontal_mode) + ", " + \
               str(self.vanne_vertical_mode) + ")"


class Power(db.Model):
    id = db.Column(db.SmallInteger(), primary_key=True)
    power = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return "Id: " + str(self.id) + ", power: " + str(self.power)
