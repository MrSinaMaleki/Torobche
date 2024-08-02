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
            callback=Callback('users.callbacks', 'login')
        ),
        Route(
            "Register(User)",
            condition=lambda: Auth.user_login_status is False and Auth.admin_login_status is False,
            callback=Callback('users.callbacks', 'register')
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

        Route(
            "Search By Category",
            condition=lambda: Auth.user_login_status or Auth.admin_login_status,
            callback=Callback('users.callbacks', "find_by_category")
        ),

        Route(
            "See my Favorites",
            condition=lambda: Auth.user_login_status,
            callback=Callback('users.callbacks', 'see_favorites')
        ),

        Route(
            "Add to Favorites",
            condition=lambda: Auth.user_login_status,
            callback=Callback('users.callbacks', 'add_favorite')
        )

    ])
)
