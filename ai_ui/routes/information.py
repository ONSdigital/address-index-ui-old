from flask import Blueprint, render_template
from flask_login import login_required

information_bp = Blueprint('information_bp', __name__, static_folder='static', template_folder='templates')


@information_bp.route('/help', methods=['GET'])
@login_required
def help():
    return render_template('help.html')


