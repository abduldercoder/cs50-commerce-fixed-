from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing_view"),
    path("listing/<int:listing_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("mylistings/", views.my_listings, name="my_listings"),
    path("category/<str:category_name>/", views.category_listings, name="category_listings"),
    path("reopen/<int:listing_id>/", views.reopen_auction, name="reopen_auction"),



]
