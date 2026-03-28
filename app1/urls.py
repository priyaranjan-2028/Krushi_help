'''Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""'''

from django.contrib import admin
from django.urls import path, include
from app1 import views

urlpatterns = [
   path("", views.index, name="index"),
   path("terms/", views.terms_page, name="terms"),
   path("farmer/login/", views.farmer_login, name="farmer_login"),
   path("farmer/register/", views.farmer_register, name="farmer_register"),
   path("farmer/dashboard/", views.farmer_dashboard, name="farmer_dashboard"),
   path("farmer/crops/", views.farmer_crops, name="farmer_crops"),
   path("farmer/sell/", views.farmer_add_crop, name="farmer_add_crop"),
   path("farmer/orders/", views.farmer_orders, name="farmer_orders"),
   path("farmer/messages/", views.farmer_messages, name="farmer_messages"),
   path("farmer/messages/send/", views.send_chat_message, name="send_chat_message"),
   path("farmer/prices/", views.farmer_prices, name="farmer_prices"),
   path("farmer/profile/", views.farmer_profile, name="farmer_profile"),
   path("farmer/products/save/", views.save_product, name="save_product"),
   path("farmer/products/<int:product_id>/delete/", views.delete_product, name="delete_product"),
   path("farmer/orders/<int:order_id>/<str:status>/", views.update_order_status, name="update_order_status"),
   path("buyer/login/", views.buyer_login, name="buyer_login"),
   path("buyer/register/", views.buyer_register, name="buyer_register"),
   path("buyer/dashboard/", views.buyer_dashboard, name="buyer_dashboard"),
   path("buyer/marketplace/", views.buyer_marketplace, name="buyer_marketplace"),
   path("buyer/buy/", views.buyer_buy, name="buyer_buy"),
   path("buyer/farmers/", views.buyer_farmers, name="buyer_farmers"),
   path("buyer/messages/", views.buyer_messages, name="buyer_messages"),
   path("buyer/messages/send/", views.send_buyer_message, name="send_buyer_message"),
   path("buyer/prices/", views.buyer_prices, name="buyer_prices"),
   path("buyer/profile/", views.buyer_profile, name="buyer_profile"),
   path("logout/", views.logout_view, name="logout"),
]
