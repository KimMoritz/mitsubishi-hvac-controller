from flask import render_template, url_for, flash, redirect, request
from mitsubishi_hvac_controller.hvac import HVAC
from hvac_ircontrol.mitsubishi import ClimateMode, VanneHorizontalMode, FanMode, VanneVerticalMode
from mitsubishi_hvac_controller import app, db, bcrypt
from mitsubishi_hvac_controller.forms import RegistrationForm, LoginForm, ResetPasswordForm
from mitsubishi_hvac_controller.models import User, Setting
from flask_login import login_user, current_user, logout_user, login_required


def write_settings_to_db(setting, temp, fan_mode, climate_mode, vanne_horizontal_mode, vanne_vertical_mode):
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
        db.session.delete(last)
    db.session.add(setting)
    db.session.commit()


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        return build_render_template(message='')
    if request.method == 'POST':
        hvac = HVAC()

        temp = request.form.get('temp')
        fan_mode = request.form.get('fan_mode')
        climate_mode = request.form.get('climate_mode')
        vanne_horizontal_mode = request.form.get('vanne_horizontal_mode')
        vanne_vertical_mode = request.form.get('vanne_vertical_mode')

        req_form_variables = {'temp': temp,
                              'fan_mode': fan_mode,
                              'climate_mode': climate_mode,
                              'vanne_horizontal_mode': vanne_horizontal_mode,
                              'vanne_vertical_mode': vanne_vertical_mode}

        write_settings_to_db(setting='last', **req_form_variables)

        hvac_variables = hvac.get_hvac_variables()
        print(request.form.get(hvac_variables.get('temps').get(temp)))

        hvac.set_heat(**req_form_variables)

        return build_render_template(message='Temperature set!')


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')


@app.route('/off', methods=['GET', 'POST'])
@login_required
def turn_off():
    hvac = HVAC()
    hvac.turn_off()
    print('Turned off!')
    return build_render_template(message='Turned off!')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registration_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('home'))


def build_render_template(message):
    hvac = HVAC()
    hvac_variables = hvac.get_hvac_variables()
    temp_presel = hvac_variables.get('temps').get('20')
    fan_mode_presel = hvac_variables.get('fan_modes').get(FanMode.Speed1)
    climate_mode_presel = hvac_variables.get('climate_modes').get(ClimateMode.Hot)
    vanne_horizontal_mode_presel = hvac_variables.get('vanne_horizontal_modes').get(VanneHorizontalMode.Middle)
    vanne_vertical_mode_presel = hvac_variables.get('vanne_vertical_modes').get(VanneVerticalMode.Middle)

    return render_template('settings.html',
                           temps=hvac_variables.get('temps').keys(),
                           temp_presel=temp_presel,
                           fan_modes=hvac_variables.get('fan_modes').keys(),
                           fan_mode_presel=fan_mode_presel,
                           climate_modes=hvac_variables.get('climate_modes').keys(),
                           climate_mode_presel=climate_mode_presel,
                           vanne_horizontal_modes=hvac_variables.get('vanne_horizontal_modes').keys(),
                           vanne_horizontal_mode_presel=vanne_horizontal_mode_presel,
                           vanne_vertical_modes=hvac_variables.get('vanne_vertical_modes').keys(),
                           vanne_vertical_mode=vanne_vertical_mode_presel,
                           message=message
                           )


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
