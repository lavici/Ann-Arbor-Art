from flask import Flask, render_template
import extensions
import controllers
import config
import api
# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
app.register_blueprint(controllers.main, url_prefix = '')
app.register_blueprint(controllers.search, url_prefix = '')
app.register_blueprint(controllers.user, url_prefix = '')
app.register_blueprint(controllers.art, url_prefix = '')
app.register_blueprint(controllers.artist, url_prefix = '')
app.register_blueprint(controllers.location, url_prefix = '')
app.register_blueprint(controllers.artists, url_prefix = '')
app.register_blueprint(controllers.mapview, url_prefix = '')
app.register_blueprint(controllers.create, url_prefix='')

app.register_blueprint(api.art_api, url_prefix = '')
app.register_blueprint(api.artist_api, url_prefix = '')
app.register_blueprint(api.location_api, url_prefix = '')
app.register_blueprint(api.all_artists_api, url_prefix = '')
app.register_blueprint(api.all_locations_api, url_prefix = '')
app.register_blueprint(api.all_artworks_api, url_prefix = '')
app.register_blueprint(api.all_bids_api, url_prefix = '')
app.register_blueprint(api.login_api, url_prefix = '')
app.register_blueprint(api.search_api, url_prefix = '')

# set the secret key:
# app.secret_key = ''

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
