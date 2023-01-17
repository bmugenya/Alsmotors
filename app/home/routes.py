from app.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from app.authentication.models import Car
from app import db,login_manager
from sqlalchemy import or_
import cloudinary.uploader


@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/inventory')
def inventory():
    cars =  Car.query.all()
    return render_template('home/inventory.html',item_length="true",cars=cars, segment='index')



@blueprint.route('/filter', methods=['POST'])
def filter():

    s_type = request.form['type']
    brand = request.form['brand']
    make = request.form['make']
    # price = request.form['price']
    models = request.form['models']
    location = request.form['location']
    fuel = request.form['fuel']
    transmission = request.form['transmission']
    cars = 'searching'


    if brand:
        cars =  Car.query.filter(Car.brand.like(brand))
    if s_type:
        cars =  Car.query.filter(Car.type.like(s_type))
    if make:
        cars =  Car.query.filter(Car.make.like(make))
    if models:
        cars =  Car.query.filter( Car.models.like(models))
    if location:
        cars =  Car.query.filter(Car.location.like(location))
    if fuel:
        cars =  Car.query.filter(Car.fuel.like(fuel))
    if transmission:
        cars =  Car.query.filter(Car.transmission.like(transmission))

    return render_template('home/inventory.html',cars=cars, segment='index')
 

@blueprint.route('/car')
def car():
    return render_template('home/car.html', segment='index')


@blueprint.route('/add/car', methods=['POST'])
def add_car():
    """Register a new car"""
  
    # file = request.files['image']
    # upload_data = cloudinary.uploader.upload(file)
    # photo = upload_data['secure_url']
    
    data = {
        # 'image_url':photo,
        'name' : request.form['name'],
        'type' : request.form['type'],
        'brand' : request.form['brand'],
        'make' : request.form['make'],
        'price' : request.form['price'],
        'models' : request.form['models'],
        'location' : request.form['location'],
        'fuel' : request.form['fuel'],
        'transmission' : request.form['transmission'],
        'featured' : request.form.getlist('featured')[0],
        'promotion' : request.form.getlist('promotion')[0],
        'used' : request.form.getlist('used')[0]
    }
 
    car = Car(**data)
    db.session.add(car)
    db.session.commit()

  

    return render_template('home/car.html',
                               msg='Car created successfully.',
                               success=True)


@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
