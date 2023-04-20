from app.vehicle import blueprint
from flask import render_template, request,flash,redirect,url_for,jsonify,make_response
from flask_login import login_required
from app.authentication.models import Car,Image,Notification,Contact, Subscribe
from app import db,login_manager
import cloudinary.uploader




@blueprint.route('/delete/vehicle/<int:id>', methods=['GET','POST','DELETE'])
@login_required
def delete_vehicle(id):
    car =  db.session.get(Car, id)
    # db.session.delete(car)
    # db.session.commit()
    flash('Vehicle deleted successfully')
    return redirect(url_for('vehicle_blueprint.collection')) 

@blueprint.route('/table')
@login_required
def table():
    cars =  Car.query.all()
    contacts =  Contact.query.all()
    subscribers =   Subscribe.query.all()
    return render_template('vehicle/table.html',contacts=contacts,subscribers=subscribers,cars=cars)

@blueprint.route('/vehicle/<int:id>', methods=['GET','POST'])
def vehicle(id):
    car =  db.session.get(Car, id)
    images = Image.query.filter(Image.cars_id == id)
    
    
    if request.method == 'POST':
        data = {
        
            'name' : request.form['name'],
            'mobile' : request.form['phone'],
            'email' : request.form['email'],
            'message' : request.form['message'],
            'cars_id' : id,
        }
        
        notification = Notification(**data)
        db.session.add(notification)
        db.session.commit()
        msg = "Thank you for your inquiry regarding %s we will get back to you shortly" % (car.name)
        flash(msg)
        redirect(url_for('vehicle_blueprint.vehicle',id=id))

    return render_template('vehicle/vehicle.html',id=id,images=images,car=car)


@blueprint.route('/collection', methods=['GET','POST'])
def collection():
    if request.args.get('location'):
        cars =  Car.query.filter(Car.location.like(request.args.get('location')))
        return render_template('vehicle/collection.html',cars=cars)


    if request.args.get('brand'):
        cars =  Car.query.filter(Car.location.like(request.args.get('brand')))
        return render_template('vehicle/collection.html',cars=cars)

    if request.args.get('type'):
        cars =  Car.query.filter(Car.category.like(request.args.get('type')))
        return render_template('vehicle/collection.html',cars=cars)

    if request.method == 'POST':
        category = request.form['category']
        brand = request.form['brand']
        location = request.form['location']
        fuel = request.form['fuel']
        transmission = request.form['transmission']
        print(request.form)
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
 



@blueprint.route('/vehicles/api', methods=['GET','POST'])
def vehicle_api():
    if request.method == 'POST':
        data =request.get_json()
        print(data)
        if data:
            category = data.get('category')
            brand = data.get('brand')
            location = data.get('location')
            fuel = data.get('fuel')
            transmission = data.get('transmission')
            used = data.get('used')
            cars = 'searching'

            if brand:
                cars =  Car.query.filter(Car.brand.like(brand))
            if category:
                cars =  Car.query.filter(Car.category.like(category))
            if location:
                cars =  Car.query.filter(Car.location.like(location))
            if fuel:
                cars =  Car.query.filter(Car.fuel_type.like(fuel))
            if used:
                cars =  Car.query.filter(Car.used.like(used))
            if transmission:
                cars =  Car.query.filter(Car.transmission.like(transmission))

            return [{
             "id":car.id,
                'name':car.name,
                'image_url':car.image_url,
                'year':car.year,
                'engine':car.engine,
                'drive_type':car.drive_type,
                'brand':car.brand,
                'category':car.category,
                'model':car.model,
                'location':car.location,
                'fuel_type':car.fuel_type,
                'transmission':car.transmission,
                'promotion':car.promotion,
                'used':car.used
                } for car in cars]

    cars =  Car.query.all()
    return [{
    "id":car.id,
        'name':car.name,
        'image_url':car.image_url,
        'year':car.year,
        'engine':car.engine,
        'drive_type':car.drive_type,
        'brand':car.brand,
        'category':car.category,
        'model':car.model,
        'location':car.location,
        'fuel_type':car.fuel_type,
        'transmission':car.transmission,
        'promotion':car.promotion,
        'used':car.used
        }for car in cars]
 
@blueprint.route('/update/vehicle/<int:id>', methods=['POST','GET'])
@login_required
def update_vehicle(id):
    """Update a new vehicle"""
   
    if request.method == 'POST':
       
        file = request.files['image']
        upload_data = cloudinary.uploader.upload(file,width=560,height=316)
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
        
        flash("Image added successfully.")
        redirect(url_for('vehicle_blueprint.update_vehicle',id=id))
    
    car =  db.session.get(Car, id)
    images = Image.query.filter(Image.cars_id == id)
    requests = images.count()
    
    notifications = Notification.query.filter(Notification.cars_id == id)
    return render_template('vehicle/update_vehicle.html',id=id,requests=requests,notifications=notifications,images=images,car=car)



@blueprint.route('/register/vehicle', methods=['POST','GET'])
@login_required
def register_vehicle():
    """Register a new car"""
  
    if request.method == 'POST':
        file = request.files['image']
        upload_data = cloudinary.uploader.upload(file,width=560,height=316)
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
        msg = "%s created successfully." % (request.form['name'])
        flash(msg)
        redirect(url_for('vehicle_blueprint.register_vehicle'))

    return render_template('vehicle/add_vehicle.html')
