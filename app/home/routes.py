from app.home import blueprint
from flask import render_template, request,flash,redirect,url_for
from jinja2 import TemplateNotFound
from app.authentication.models import Car,Contact, Subscribe
from app import db


@blueprint.route('/subscribe', methods=['GET','POST'])
def subscription():
    cars =  Car.query.all()
    
    if request.method == 'POST':
        data = { 'email' : request.form['email']  }
        
        notification = Subscribe(**data)
        db.session.add(notification)
        db.session.commit()
        flash("Thank you for subscribing to Alsmotors newsletter.")
        redirect(url_for('home_blueprint.index'))
    return render_template('home/index.html',cars=cars,segment='index')



@blueprint.route('/',methods=['GET','POST'])
def index():
    cars =  Car.query.all()

    if request.method == 'POST':
        data = {
            'name' : request.form['name'],
            'mobile' : request.form['phone'],
            'message' : request.form['message'],
        }
        
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()

        flash("Thank you for reaching out to Alsmotors.")
        redirect(url_for('home_blueprint.index'))

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
