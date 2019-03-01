from flask import *

from extensions import connect_to_database

create = Blueprint('create', __name__, template_folder='templates')

@create.route('/admin/menu', methods=['GET', 'POST'])
def menu_route():
    return render_template("admin_create_menu.html")
