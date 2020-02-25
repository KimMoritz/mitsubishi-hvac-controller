from flask import render_template, url_for, flash, redirect, request
from hvac_ircontrol.hvac import HVAC
from hvac_ircontrol.mitsubishi import ClimateMode, VanneHorizontalMode, FanMode, VanneVerticalMode
from hvac_ircontrol import app, db, bcrypt
from hvac_ircontrol.forms import RegistrationForm, LoginForm, ResetPasswordForm
from hvac_ircontrol.models import User
from flask_login import login_user, current_user, logout_user, login_required

# from hvac_ircontrol import Display


def get_hvac_variables():
    temps = {'16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23}
    fan_modes = {'Auto': FanMode.Auto,
                 'Speed1': FanMode.Speed1,
                 'Speed2': FanMode.Speed2,
                 'Speed3': FanMode.Speed3}
    climate_modes = {'Hot': ClimateMode.Hot,
                     'Cold': ClimateMode.Cold,
                     'Auto': ClimateMode.Auto,
                     'Dry': ClimateMode.Dry}
    vanne_horizontal_modes = {'Left': VanneHorizontalMode.Left,
                              'MiddleLeft': VanneHorizontalMode.MiddleLeft,
                              'Middle': VanneHorizontalMode.Middle,
                              'MiddleRight': VanneHorizontalMode.MiddleRight,
                              'Right': VanneHorizontalMode.Right,
                              'Swing': VanneHorizontalMode.Swing,
                              'NotSet': VanneHorizontalMode.NotSet}
    vanne_vertical_modes = {'Auto': VanneVerticalMode.Auto,
                            'Bottom': VanneVerticalMode.Bottom,
                            'MiddleBottom': VanneVerticalMode.MiddleBottom,
                            'Middle': VanneVerticalMode.Middle,
                            'MiddleTop': VanneVerticalMode.MiddleTop,
                            'Top': VanneVerticalMode.Top}
    variables = {'temps': temps,
                 'fan_modes': fan_modes,
                 'climate_modes': climate_modes,
                 'vanne_horizontal_modes': vanne_horizontal_modes,
                 'vanne_vertical_modes': vanne_vertical_modes}
    return variables


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

        print(temp + fan_mode + climate_mode + vanne_horizontal_mode + vanne_vertical_mode)

        hvac_variables = get_hvac_variables()
        print(request.form.get(hvac_variables.get('temps').get(temp)))

        hvac.set_heat(
            hvac_variables.get('temps').get(temp),
            hvac_variables.get('fan_modes').get(fan_mode),
            hvac_variables.get('climate_modes').get(climate_mode),
            hvac_variables.get('vanne_horizontal_modes').get(vanne_horizontal_mode),
            hvac_variables.get('vanne_vertical_modes').get(vanne_vertical_mode)
        )
        # display = Display()
        # display.show_settings(temp=request.form.get('temp'), speed=request.form.get('fan_mode'))

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
    # display = Display()
    # display.show_settings(temp=request.form.get('temp'), speed=request.form.get('fan_mode'))
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
    hvac_variables = get_hvac_variables()
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
