from core.state import Auth
from core.router import Route, Router, Callback

router = Router(
    Route("Main", description="Sina - Torobche :)", children=[
        Route("test"),
        Route("Login(Admin)",
              condition=lambda: Auth.admin_login_status is False,
              callback=Callback('admin.callbacks', 'login')
              ),

        Route("Add Url",
              condition=lambda: Auth.admin_login_status,
              callback=Callback('admin.callbacks', 'add_url')
              ),

        Route("Remove Url",
              condition=lambda: Auth.admin_login_status,
              callback=Callback('admin.callbacks', 'delete_url')
              ),

        Route("logout(Admin)",
              condition=lambda: Auth.admin_login_status,
              callback=Callback('admin.callbacks', 'logout')
              ),



        Route(
            "Login(User)",
            condition=lambda: Auth.user_login_status is False and Auth.admin_login_status is False,
            callback=Callback('admin.callbacks', 'login')
        ),
        Route(
            "Register",
            condition=lambda: Auth.user_login_status is False and Auth.admin_login_status is False,
            callback=Callback('admin.callbacks', 'register')
        ),
        Route(
            "Logout(User)",
            condition=lambda: Auth.user_login_status,
            callback=Callback('admin.callbacks', 'logout')
        ),

        Route(
            "Search By name",
            condition=lambda: Auth.user_login_status or Auth.admin_login_status,
            callback=Callback('users.callbacks', 'find_products')
        ),

    ])
)
