from controllers.userController import User

def test():
    return 'hello world'

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
    app.add_url_rule(
        '/api/user/set',
        view_func = User().save_user,
        methods=['PUT']
    )
    app.add_url_rule(
        '/api/test',
        view_func = test,
        methods=['GET']
    )

def create_routes(app):
    define_user_router(app)