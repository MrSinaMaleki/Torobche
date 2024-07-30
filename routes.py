from core.state import Auth
from core.router import Route, Router, Callback

router = Router(
    Route("Main", description="Sina - Torobche :)", children=[
        Route(
            "Login",
            condition=lambda: Auth.login_status is False,
            callback=Callback('admin.callbacks', 'login')
        ),
        Route(
            "Register",
            condition=lambda: Auth.login_status is False,
            callback=Callback('admin.callbacks', 'register')
        ),
        Route(
            "Logout",
            condition=lambda: Auth.login_status,
            callback=Callback('admin.callbacks', 'logout')
        ),
        Route("Panel",
              condition=lambda: Auth.login_status,
              children=[
                  Route("Login", callback=Callback('admin.callbacks', 'login')),
                  Route("Register", callback=Callback('admin.callbacks', 'register')),
                  Route("In Panel", children=[
                      Route("Login", callback=Callback('admin.callbacks', 'login')),
                      Route("Register", callback=Callback('admin.callbacks', 'register')),
                  ]),
              ]),

    ])
)
