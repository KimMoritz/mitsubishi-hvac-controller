import logging
from flask import render_template, url_for, flash, redirect, request
from mitsubishi_hvac_controller.hvac import HVAC
from mitsubishi_hvac_controller import app, db, bcrypt
from mitsubishi_hvac_controller.forms import RegistrationForm, LoginForm, ResetPasswordForm
from mitsubishi_hvac_controller.models import User, Setting, Power
from flask_login import login_user, current_user, logout_user, login_required

def write_settings_to_db(setting, temp, fan_mode, climate_mode, vanne_horizontal_mode, vanne_vertical_mode):
    logging.info('Writing settings to db: ' + setting + temp + fan_mode + climate_mode + vanne_horizontal_mode + vanne_vertical_mode)
    setting = Setting(
        setting=setting,
        temp=temp,
        fan_mode=fan_mode,
        climate_mode=climate_mode,
        vanne_horizontal_mode=vanne_horizontal_mode,
        vanne_vertical_mode=vanne_vertical_mode
    )
    last = db.session.query(Setting).get('last')
    if last is not None:
        logging.info('Deleting last setting from db.')
        db.session.delete(last)
    logging.info('Adding new setting to db.')
    db.session.add(setting)
    logging.info('Committing changes')
    db.session.commit()


def build_settings_page(power, message):
    hvac = HVAC()
    hvac_variables = hvac.get_hvac_variables()
    setting = db.session.query(Setting).get('last')
    if setting is None:
        setting = db.session.query(Setting).get('default')

    return render_template('settings.html',
                           temps=hvac_variables.get('temps').keys(),
                           temp_presel=setting.temp,
                           fan_modes=hvac_variables.get('fan_modes').keys(),
                           fan_mode_presel=setting.fan_mode,
                           climate_modes=hvac_variables.get('climate_modes').keys(),
                           climate_mode_presel=setting.climate_mode,
                           vanne_horizontal_modes=hvac_variables.get('vanne_horizontal_modes').keys(),
                           vanne_horizontal_mode_presel=setting.vanne_horizontal_mode,
                           vanne_vertical_modes=hvac_variables.get('vanne_vertical_modes').keys(),
                           vanne_vertical_mode_presel=setting.vanne_vertical_mode,
                           message=message,
                           power=power
                           )


def build_req_form_variables(form, hvac_variables):
    req_form_variables = {'temp': hvac_variables.get('temps').get(form.get('temp')),
                          'fan_mode': hvac_variables.get('fan_modes').get(form.get('fan_mode')),
                          'climate_mode': hvac_variables.get('climate_modes').get(form.get('climate_mode')),
                          'vanne_horizontal_mode': hvac_variables.get('vanne_horizontal_modes').get(
                              form.get('vanne_horizontal_mode')),
                          'vanne_vertical_mode': hvac_variables.get('vanne_vertical_modes').get(
                              form.get('vanne_vertical_mode'))}
    return req_form_variables


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        logging.info('GET /settings')
        power = db.session.query(Power).get(0)
        return build_settings_page(power=power.power, message='')
    if request.method == 'POST':
        hvac = HVAC()
        hvac_variables = hvac.get_hvac_variables()
        form = request.form
        req_form_variables = build_req_form_variables(form, hvac_variables)

        write_settings_to_db(setting='last', temp=form.get('temp'), fan_mode=form.get('fan_mode'),
                             climate_mode=form.get('climate_mode'),
                             vanne_horizontal_mode=form.get('vanne_horizontal_mode'),
                             vanne_vertical_mode=form.get('vanne_vertical_mode'))

        hvac.set_heat(**req_form_variables)

        return build_settings_page(power=True, message='Temperature set!')


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')


@app.route('/power', methods=['GET', 'POST'])
@login_required
def power():
    hvac = HVAC()
    power = db.session.query(Power).get(0)

    if power.power:
        logging.info("Turning off")
        hvac.turn_off()
        db.session.delete(power)
        power_new = Power(id=0, power=not power.power)
        db.session.add(power_new)
        db.session.commit()
        message = 'Turned off!'
    else:
        setting = db.session.query(Setting).get("last")
        logging.info("Turning on")
        hvac_variables = hvac.get_hvac_variables()
        setting_variables = {'temp': hvac_variables.get('temps').get(setting.temp),
                             'fan_mode': hvac_variables.get('fan_modes').get(setting.fan_mode),
                             'climate_mode': hvac_variables.get('climate_modes').get(setting.climate_mode),
                             'vanne_horizontal_mode': hvac_variables.get('vanne_horizontal_modes').get(setting.vanne_horizontal_mode),
                             'vanne_vertical_mode': hvac_variables.get('vanne_vertical_modes').get(setting.vanne_vertical_mode)}

        hvac.set_heat(**setting_variables)
        db.session.delete(power)
        power_new = Power(id=0, power=not power.power)
        db.session.add(power_new)
        db.session.commit()
        message = 'Turned on!'

    logging.info(message)
    return build_settings_page(power=not power.power, message=message)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        logging.info('User not authenticated.')
        return redirect(url_for('home'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        user = User(
            username=registration_form.username.data,
            email=registration_form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        logging.info('Account created.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registration_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logging.info('User not authenticated.')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            session.permanent = True 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!')
    logging.info('Logged out.')
    return redirect(url_for('home'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
