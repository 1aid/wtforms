from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, URL, AnyOf, NumberRange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(db.String(200))
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)


class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[InputRequired()])
    species = StringField('Species', validators=[InputRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30)])
    notes = StringField('Notes')
    

class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators=[URL()])
    notes = StringField('Notes')
    available = BooleanField('Available')


@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_pet.html', form=form, pet=pet)


if __name__ == '__main__':
    app.run(debug=True)