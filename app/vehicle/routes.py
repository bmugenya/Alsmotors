from app.vehicle import blueprint
from flask import render_template, request
from flask_login import login_required
from app.authentication.models import Car,Image
from app import db,login_manager
import cloudinary.uploader


@blueprint.route('/table')
def table():
    cars =  Car.query.all()
    return render_template('vehicle/table.html',cars=cars)

@blueprint.route('/vehicle/<int:id>', methods=['GET'])
def vehicle(id):
    car =  db.session.get(Car, id)
    images = Image.query.filter(Image.cars_id == id)
    return render_template('vehicle/vehicle.html',images=images,car=car)


@blueprint.route('/collection', methods=['GET','POST'])
def collection():
    if request.method == 'POST':
        category = request.form['category']
        brand = request.form['brand']
        location = request.form['location']
        fuel = request.form['fuel']
        transmission = request.form['transmission']
        cars = 'searching'

        if brand:
            cars =  Car.query.filter(Car.brand.like(brand))
        if category:
            cars =  Car.query.filter(Car.category.like(category))
        if location:
            cars =  Car.query.filter(Car.location.like(location))
        if fuel:
            cars =  Car.query.filter(Car.fuel_type.like(fuel))
        if transmission:
            cars =  Car.query.filter(Car.transmission.like(transmission))

        return render_template('vehicle/collection.html',cars=cars)

    cars =  Car.query.all()
    return render_template('vehicle/collection.html',item_length="true",cars=cars)
 
 
@blueprint.route('/update/vehicle/<int:id>', methods=['POST','GET'])
def update_vehicle(id):
    """Update a new vehicle"""

    if request.method == 'POST':
       
        file = request.files['image']
        upload_data = cloudinary.uploader.upload(file)
        photo = upload_data['secure_url']
        
        data = {
            'images':photo,
            'body_type' : request.form['body'],
            'description' : request.form['description'],
            'cars_id' : id,
        }
        
        car = Image(**data)
        db.session.add(car)
        db.session.commit()
        return render_template('vehicle/add_vehicle.html',id=id)

    return render_template('vehicle/update_vehicle.html',id=id)


@blueprint.route('/register/vehicle', methods=['POST','GET'])
def register_vehicle():
    """Register a new car"""
  
    if request.method == 'POST':
        file = request.files['image']
        upload_data = cloudinary.uploader.upload(file)
        photo = upload_data['secure_url']
        
        data = {
            'image_url':photo,
            'name' : request.form['name'],
            'year' : request.form['year'],
            'engine' : request.form['engine'],
            'drive_type' : request.form['drive_type'],
            'brand' : request.form['brand'],
            'category' : request.form['category'],
            'model' : request.form['model'],
            'location' : request.form['location'],
            'fuel_type' : request.form['fuel'],
            'transmission' : request.form['transmission'],
            # 'promotion' : request.form.getlist('promotion'),
            # 'used' : request.form.getlist('used')
        }
    
        car = Car(**data)
        db.session.add(car)
        db.session.commit()
        msg = "Car created successfully."

        return render_template('vehicle/add_vehicle.html',msg=msg,success=True)

    return render_template('vehicle/add_vehicle.html')
