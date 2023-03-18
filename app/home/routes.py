import os
from app.home import blueprint
from flask import render_template, request,flash,redirect,url_for,current_app
from jinja2 import TemplateNotFound
from app.authentication.models import Car,Contact, Subscribe
from app import db
from flask_mail import Message
from app import mail

@blueprint.route('/subscribe', methods=['GET','POST'])
def subscription():
    cars =  Car.query.all()
    
    if request.method == 'POST':
        data = { 'email' : request.form['email']  }
        msg = "Thank you for subscribing."
        send_msg = Message(msg,sender=os.getenv('MAIL_USERNAME'),recipients=[data['email']])
        send_msg.html = render_template('home/message.html')
        mail.send(send_msg)
        
        notification = Subscribe(**data)
        db.session.add(notification)
        db.session.commit()
        flash(msg)
        redirect(url_for('home_blueprint.index'))
    return render_template('home/index.html',cars=cars,segment='index')


@blueprint.route('/contact', methods=['GET','POST'])
def Contact():
    if request.method == "POST":
        data = {
                    'name' : request.form['first'] + " " + request.form['last'],
                    'email' : request.form['email'],
                    'mobile' : request.form['phone'],
                    'message' : request.form['message'],
        }
                
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()

        flash("Thank you for reaching out to Alsmotors.")
    redirect(url_for('home_blueprint.index'))


@blueprint.route('/',methods=['GET','POST'])
def index():
    
    if request.method == 'GET':    
        cars =  Car.query.all()
        return render_template('home/index.html',cars=cars,segment='index')

    if request.method == 'POST':
        category = request.form['category']
        brand = request.form['brand']
        location = request.form['location']
        fuel = request.form['fuel']
        transmission = request.form['transmission']
        cars = 'searching'

        if brand:
            cars =  Car.query.filter(Car.brand.like(brand))
            return render_template('home/index.html',cars=cars, category="brand", segment='index')
        if category:
            cars =  Car.query.filter(Car.category.like(category))
            return render_template('home/index.html',cars=cars, category="category", segment='index')
        if location:
            cars =  Car.query.filter(Car.location.like(location))
        if fuel:
            cars =  Car.query.filter(Car.fuel_type.like(fuel))
        if transmission:
            cars =  Car.query.filter(Car.transmission.like(transmission))

        return render_template('home/index.html',cars=cars,segment='index')
              


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
