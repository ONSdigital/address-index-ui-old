from ai_ui import app
from ai_ui.routes.authentication import authentication_bp
# from ai_ui.routes.errors import error_bp
# from ai_ui.routes.unit_pages import search_bp


app.register_blueprint(authentication_bp, url_prefix='/')
# app.register_blueprint(error_bp, url_prefix='/error')
# app.register_blueprint(search_bp)
