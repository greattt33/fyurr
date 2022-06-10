#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# from crypt import methods
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate=Migrate(app,db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120)) 
    talent = db.Column(db.Boolean)
    description = db.Column(db.String(120))
    show = db.relationship('Show', backref='Venue', lazy=True)


    def __init__(self,name,city,state,phone,genre,image_link,facebook_link):
      self.id= id
      self.name= name
      self.city= city
      self.state= state
      self.phone= phone
      self.genre= genre
      self.image_link= image_link
      self.facebook_link= facebook_link

    def __repr__(self):
      return f'done'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    description= db.Column(db.String(200))
    shows = db.relationship('Show', backref='Artist', lazy=True)
    website = db.Column(db.String(120)) 
    talent = db.Column(db.Boolean)
    

    def __init__(self,name,city,state,phone,genre,image_link,facebook_link):
      self.id= id
      self.name= name
      self.city= city
      self.state= state
      self.phone= phone
      self.genre= genre
      self.image_link= image_link
      self.facebook_link= facebook_link

    def __repr__(self):
      return f'done'
  


class Show(db.Model):
  __tablename__ = 'Show'
  id= db.Column(db.Integer, primary_key=True)
  artist_id=db.Column(db.Integer, db.ForeignKey('Artist.id'))
  venue_id=db.Column(db.Integer, db.ForeignKey('Venue.id'))
  start_time=db.Column(db.String(120))
  artist_name=db.column(db.String(50),db.ForeignKey('Artist.name'))
  artist_image=db.column(db.String(120), db.ForeignKey('Artist.image_link'))

  def __init__(self,id,artist_id,venue_id,start_time,artist_name,artist_image):
      self.id= id
      self.artist_id= artist_id
      self.venue_id= venue_id
      self.start_time= start_time
      self.artist_name= artist_name
      self.artist_image= artist_image

  def __repr__(self):
      return f'done'
  
db.create_all()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    realareas = []

    areas = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

    for area in areas:
      realvenues = []

      venues = Venue.query.filter_by(city=area.city).filter_by(state=area.state).all()

      for venue in venues:
        upcoming_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.date > datetime.now()).all()

      realvenues.append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': len(upcoming_shows)
        })
    
    realareas.append({
      'city': area.city,
      'state': area.state,
      'venues': realvenues
      })

    return render_template('pages/venues.html',area= realareas)

 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  if request.methods== 'POST':
    data = []
  count = 0
  search_term=request.form.get('search_term', '')
  places = Venue.query.with_entities(Venue.name).distinct().all() 
  for names in places:
    name = names[0]
    if search_term.lower() in name.lower():
      venues = Venue.query.filter_by(name=name).all()
      for venue in venues:
        count += 1
        show = Show.query.filter_by(id=venue.id).all()
        data.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(show)
        }) 
  response={
    "count": count,
    "data": data
  }
 
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  venue = Venue.query.filter(Venue.id == venue_id).first()

  future_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.date > datetime.now()).all()

  if len(future_shows) > 0:
    upcoming_shows_arr = []

    for future_show in future_shows:
      artist = Artist.query.filter(Artist.id == future_show.artist).first()

      upcoming_shows_arr.append({
          'artist_id': artist.id,
          'artist_name': artist.name,
          'artist_image_link': artist.image_link,
          'start_time': str(future_show.date) 
        })

      venue.upcoming_shows = upcoming_shows_arr
      venue.upcoming_shows_count = len(upcoming_shows_arr)
    else:
      venue.upcoming_shows = []
      venue.upcoming_shows_count = 0

  past_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.date < datetime.now()).all()

  if len(past_shows) > 0 :
    past_shows_arr = []

    for past_show in past_shows:
      artist = Artist.query.filter(Artist.id == past_show.artist).first()

      past_shows_arr.append(
        {
          'artist_id': artist.id,
          'artist_name': artist.name,
          'artist_image_link': artist.image_link,
          'start_time': str(future_show.date) 
        }
      )
      venue.upcoming_shows = past_shows_arr
      venue.upcoming_shows_count = len(past_shows_arr)
  else:
      venue.upcoming_shows = []
      venue.upcoming_shows_count = 0
  
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try: 
    venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website = request.form['website'],
      talent = True if 'talent' in request.form else False, 
      description = request.form['seeking_description']
    )
    db.session.add(venue)
    db.session.commit()
  except: 
    error = True
    db.session.rollback()
  finally: 
    db.session.close()
  if error: 
    flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  if not error: 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error=False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally: 
    db.session.close()
  
  if error: 
    flash('An error occurred. Deletion failed')
  if not error: 
    flash('Deleted')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  persons = Artist.query.with_entities(Artist.name, Artist.id).distinct().all()  
  for person in persons:
    name = person[0]
    id = person[1] 
    data.append({
      "name": name,
      "id": id
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term')
  search = "%{}%".format(search_term.replace(" ", "\ "))

  artists = Artist.query.filter(Artist.name.match(search)).order_by('name').all()
  data = []
  for artist in artists:

    data.append(
      {
        'id': artist.id,
        'name': artist.name,
        'num_upcoming_shows': len(artist.shows)
      }
    )

  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = Artist.query.filter_by(id=artist_id).all()[0]  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter(Artist.id == artist_id).first()

  form.name.data = artist.name
  form.genres.data = artist.genres
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website_link.data = artist.website
  form.facebook_link.data = artist.facebook_link
  form.venue.data = artist.venue
  form.description.data = artist.description
  form.image_link.data = artist.image_link

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  error = False
  try:
    artist = Artist.query.get(artist_id)
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']
    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.genres = genres
    artist.image_link = image_link
    artist.facebook_link = facebook_link
    artist.website = website
    artist.talent = seeking_talent
    artist.description = seeking_description
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  place = Venue.query.filter_by(id = venue_id).all()[0]
  venue={
    "id": place.id,
    "name": place.name,
    "genres": place.genres,
    "address": place.address,
    "city": place.city,
    "state": place.state,
    "phone": place.phone,
    "website": place.website_link,
    "facebook_link": place.facebook_link,
    "seeking_talent": place.seeking_talent,
    "seeking_description": place.seeking_description,
    "image_link": place.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    error = False
    try: 
      artist = Artist(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        genres = request.form.getlist('genres'),
        image_link = request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        website_link = request.form['website_link'],
        seeking_talent = True if 'seeking_talent' in request.form else False, 
        seeking_description = request.form['seeking_description']
      	)
      db.session.add(artist)
      db.session.commit()
    except: 
        error = True
        db.session.rollback()
    finally: 
        db.session.close()
    if error: 
        flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
    if not error: 
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  shows = Show.query.all()

  for show in shows:
    data.append({
          'venue_name': show.venue.name,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'venue_id': show.venue_id,
          'artist_id': show.artist_id,
          'start_time':str(show.date)
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try: 
    show = Show(
      artist_id = request.form['artist_id'],
      venue_id = request.form['venue_id'],
      start_time = request.form['start_time']
    )
    db.session.add(show)
    db.session.commit()
  except: 
    error = True
    db.session.rollback()
  finally: 
    db.session.close()
  if error: 
    flash('An error occurred. Show ' + ' could not be listed.')
  if not error: 
    flash('Show ' + ' was successfully listed!')

  # on successful db insert, flash success
 
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))


    
    app.run(host='0.0.0.0', port=port)
'''
