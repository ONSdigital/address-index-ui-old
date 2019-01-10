from flask import Blueprint, render_template, request
from flask_login import login_required
from ai_ui.forms.filters import FilterForm
from ai_ui.utilities.classifications import get_classification_list

filter_bp = Blueprint('filter_bp', __name__, static_folder='static', template_folder='templates')


@filter_bp.route('/filters')
@filter_bp.route('/filters/<start_point>')
@login_required
def filters(start_point=None):
    form = FilterForm()

    called_from = request.args.get('called_from')
    existing_filters = request.args.get('existing_filters')

    class_list = get_classification_list(start_point)

    return render_template('filters.html', class_list=class_list, form=form,
                           existing_filters=existing_filters, called_from=called_from)


