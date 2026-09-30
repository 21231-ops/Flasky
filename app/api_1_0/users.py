from flask import jsonify

from app.api_1_0 import api
from app.api_1_0.authentication import auth
from app.models import User


@api.route('/users/<int:id>/')
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())



