from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Pet
from forms import AddPet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "adopt"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

#Routes

@app.route('/')
def home_page():
    '''Render home page'''
    pets = Pet.query.all()
    return render_template('pet_list.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def show_add_pet_form():
    '''Renders form to add a new pet and handles submissions'''
    form = AddPet()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        if form.photo_url.data:    
            photo_url = form.photo_url.data
        else:
            photo_url = "https://midlandbrewing.com/wp-content/uploads/2018/04/Photo-Coming-Soon.png"
        age = form.age.data
        notes = form.notes.data
        available = bool(form.available.data)
        
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_pet_form.html', form=form)
    
@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPet(obj=pet)
    if form.validate_on_submit():
        if form.photo_url.data:    
            photo_url = form.photo_url.data
        else:
            photo_url = "https://midlandbrewing.com/wp-content/uploads/2018/04/Photo-Coming-Soon.png"
        
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.photo_url = photo_url
        pet.notes = form.notes.data
        pet.available = bool(form.available.data)
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit_pet.html', form=form, pet=pet)