from controllers.userController import User

def define_user_router(app):
    app.add_url_rule(
        '/api/user/registration',
        view_func = User().registration,
        methods=['POST']
    )

def create_routes(app):
    define_user_router(app)