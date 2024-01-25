from controllers.userController import User

def define_user_router(app):
    app.add_url_rule(
        '/api/user/registration',
        view_func = User().registration,
        methods=['POST']
    )
    app.add_url_rule(
        '/api/user/login',
        view_func = User().login,
        methods=['POST']
    )
    app.add_url_rule(
        '/api/user/auth',
        view_func = User().check,
        methods=['GET']
    )
    app.add_url_rule(
        '/api/user/get',
        view_func = User().get_user,
        methods=['GET']
    )

def create_routes(app):
    define_user_router(app)