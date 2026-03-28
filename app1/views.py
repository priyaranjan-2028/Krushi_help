import random
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import BuyerChatForm, ChatReplyForm, LoginForm, ProductForm, ProfileForm, RegistrationForm
from .models import BuyerDemand, ChatMessage, Order, Product, UserProfile
from .sms import SMSDeliveryError, send_otp_sms


OTP_SESSION_PREFIX = "registration_otp_"
PENDING_DATA_PREFIX = "registration_data_"
VERIFIED_OTP_PREFIX = "verified_otp_"
DEMO_OTP_PREFIX = "demo_otp_"


MANDI_PRICE_DATA = [
    {"crop": "Rice", "price": 2380, "trend": "up", "change": "+4.2%", "suggestion": "Sell now"},
    {"crop": "Wheat", "price": 2250, "trend": "down", "change": "-1.3%", "suggestion": "Wait for better price"},
    {"crop": "Vegetables", "price": 1480, "trend": "up", "change": "+2.1%", "suggestion": "Sell now"},
]


NEARBY_DEMAND_DEFAULTS = [
    {"crop_name": "Tomatoes", "quantity_needed": "120 kg", "distance_km": Decimal("2.4")},
    {"crop_name": "Rice", "quantity_needed": "15 quintals", "distance_km": Decimal("5.1")},
]


CHAT_DEFAULTS = [
    {"buyer_name": "Anil Traders", "message": "Can you supply 50 kg by tomorrow morning?", "is_unread": True},
    {"buyer_name": "Fresh Basket Store", "message": "Your wheat quality looks great. Can we discuss pricing?", "is_unread": False},
]


ORDER_DEFAULTS = [
    {"buyer_name": "Anil Traders", "quantity": Decimal("40.00"), "status": "pending", "delivery_mode": "Transport partner"},
    {"buyer_name": "Maa Mangala Retail", "quantity": Decimal("25.00"), "status": "accepted", "delivery_mode": "Self delivery"},
    {"buyer_name": "Green Basket", "quantity": Decimal("18.00"), "status": "delivered", "delivery_mode": "Transport partner"},
]


def index(request):
    return render(request, "index.html")


def terms_page(request):
    return render(request, "terms.html")


def farmer_login(request):
    return _handle_login(request, "farmer")


def farmer_register(request):
    return _handle_register(request, "farmer")


def buyer_login(request):
    return _handle_login(request, "buyer")


def buyer_register(request):
    return _handle_register(request, "buyer")


def _handle_register(request, role):
    role_label = role.title()
    otp_key = f"{OTP_SESSION_PREFIX}{role}"
    pending_key = f"{PENDING_DATA_PREFIX}{role}"
    verified_key = f"{VERIFIED_OTP_PREFIX}{role}"
    demo_otp_key = f"{DEMO_OTP_PREFIX}{role}"

    if request.method == "GET":
        request.session.pop(otp_key, None)
        request.session.pop(pending_key, None)
        request.session.pop(verified_key, None)
        request.session.pop(demo_otp_key, None)

    otp_sent = bool(request.session.get(otp_key))
    otp_verified = bool(request.session.get(verified_key))

    if otp_verified:
        stage = "complete"
    elif otp_sent:
        stage = "verify"
    else:
        stage = "start"

    form = RegistrationForm(
        role=role,
        stage=stage,
        initial=request.session.get(pending_key, {}),
    )

    if request.method == "POST":
        action = request.POST.get("action")
        stage = "start"
        if action == "verify_otp":
            stage = "verify"
        elif action == "register":
            stage = "complete"

        form = RegistrationForm(request.POST, role=role, stage=stage)

        if form.is_valid():
            if action == "send_otp":
                otp = f"{random.randint(100000, 999999)}"
                basic_data = form.get_basic_data()

                if UserProfile.objects.filter(phone_number=basic_data["phone_number"]).exists():
                    messages.error(request, "An account with this phone number already exists.")
                else:
                    sms_sent = False
                    try:
                        send_otp_sms(basic_data["phone_number"], otp)
                    except SMSDeliveryError as exc:
                        messages.warning(request, f"{exc} Using demo OTP on screen for testing.")
                    else:
                        sms_sent = True
                        messages.success(request, f"OTP sent successfully to {basic_data['phone_number']}.")

                    request.session[otp_key] = otp
                    request.session[pending_key] = basic_data
                    request.session[verified_key] = False
                    request.session[demo_otp_key] = otp
                    request.session.modified = True
                    otp_sent = True
                    otp_verified = False
                    if not sms_sent:
                        messages.info(request, "Demo OTP is shown below on this page.")
                    form = RegistrationForm(role=role, stage="verify", initial=basic_data)
            elif action == "verify_otp":
                stored_otp = request.session.get(otp_key)
                basic_data = request.session.get(pending_key)

                if not stored_otp or not basic_data:
                    messages.error(request, "Enter name and phone number first, then send OTP.")
                elif form.cleaned_data["phone_number"] != basic_data["phone_number"] or form.cleaned_data["full_name"] != basic_data["full_name"]:
                    messages.error(request, "Name or mobile number changed after OTP send. Please send OTP again.")
                    request.session.pop(otp_key, None)
                    request.session.pop(pending_key, None)
                    request.session.pop(verified_key, None)
                    otp_sent = False
                    otp_verified = False
                    form = RegistrationForm(role=role, stage="start")
                elif form.cleaned_data["otp"] != stored_otp:
                    messages.error(request, "The OTP you entered is incorrect.")
                else:
                    request.session[verified_key] = True
                    request.session.modified = True
                    otp_verified = True
                    otp_sent = True
                    messages.success(request, "Mobile number verified. Now complete the remaining details.")
                    form = RegistrationForm(role=role, stage="complete", initial=basic_data)
            elif action == "register":
                basic_data = request.session.get(pending_key)
                otp_verified = bool(request.session.get(verified_key))

                if not basic_data or not otp_verified:
                    messages.error(request, "Verify your mobile number first.")
                elif UserProfile.objects.filter(phone_number=basic_data["phone_number"]).exists():
                    messages.error(request, "An account with this phone number already exists.")
                else:
                    profile_data = form.get_profile_data()
                    with transaction.atomic():
                        user = User.objects.create(
                            username=_build_username(role, basic_data["phone_number"]),
                            first_name=basic_data["full_name"],
                            email=profile_data.get("email", ""),
                        )
                        user.set_password(profile_data["password"])
                        user.save()

                        profile = UserProfile.objects.create(
                            user=user,
                            role=role,
                            full_name=basic_data["full_name"],
                            phone_number=basic_data["phone_number"],
                            email=profile_data.get("email", ""),
                            location_name=profile_data["location_name"],
                            latitude=profile_data["latitude"],
                            longitude=profile_data["longitude"],
                            farmer_type=profile_data.get("farmer_type", ""),
                            is_phone_verified=True,
                        )

                        if role == "farmer":
                            _seed_farmer_dashboard(profile)

                    request.session.pop(otp_key, None)
                    request.session.pop(pending_key, None)
                    request.session.pop(verified_key, None)
                    request.session.pop(demo_otp_key, None)
                    messages.success(request, f"{role_label} registration completed successfully.")
                    return redirect(f"{role}_login")

    basic_data = request.session.get(pending_key, {})
    context = {
        "role": role_label,
        "page_title": f"{role_label} Register",
        "heading": f"Create your {role} account",
        "subtext": "Enter name and mobile number, verify OTP, then complete the remaining details on the same page.",
        "button_text": f"Register as {role_label}",
        "alternate_text": "Already have an account?",
        "alternate_link": f"{role}_login",
        "alternate_label": "Login here",
        "is_register": True,
        "form": form,
        "otp_sent": otp_sent,
        "otp_verified": otp_verified,
        "basic_data": basic_data,
        "demo_otp": request.session.get(demo_otp_key, ""),
    }
    return render(request, "auth_form.html", context)


def _handle_login(request, role):
    role_label = role.title()
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        phone_number = form.cleaned_data["phone_number"]
        password = form.cleaned_data["password"]

        try:
            profile = UserProfile.objects.select_related("user").get(phone_number=phone_number, role=role)
        except UserProfile.DoesNotExist:
            messages.error(request, f"No {role} account found with that phone number.")
        else:
            user = authenticate(request, username=profile.user.username, password=password)
            if user is None:
                messages.error(request, "Incorrect password. Please try again.")
            else:
                login(request, user)
                messages.success(request, f"{role_label} login successful.")
                if role == "farmer":
                    return redirect("farmer_dashboard")
                if role == "buyer":
                    return redirect("buyer_dashboard")
                return redirect("index")

    context = {
        "role": role_label,
        "page_title": f"{role_label} Login",
        "heading": f"Welcome back, {role_label}",
        "subtext": f"Log in to continue your {role.lower()} journey on Krushi Settu with your registered phone number and password.",
        "button_text": f"Login as {role_label}",
        "alternate_text": "Need an account first?" if role == "buyer" else "New to Krushi Settu?",
        "alternate_link": f"{role}_register",
        "alternate_label": f"Create a {role} account",
        "is_register": False,
        "login_form": form,
    }
    return render(request, "auth_form.html", context)


@login_required
def farmer_dashboard(request):
    context = _build_farmer_portal_context(request, active_page="dashboard")
    if not isinstance(context, dict):
        return context
    return render(request, "dashboard.html", context)


@login_required
def farmer_crops(request):
    context = _build_farmer_portal_context(request, active_page="crops")
    if not isinstance(context, dict):
        return context
    return render(request, "crops.html", context)


@login_required
def farmer_add_crop(request):
    context = _build_farmer_portal_context(request, active_page="sell")
    if not isinstance(context, dict):
        return context
    return render(request, "add_crop.html", context)


@login_required
def farmer_orders(request):
    context = _build_farmer_portal_context(request, active_page="orders")
    if not isinstance(context, dict):
        return context
    return render(request, "orders.html", context)


@login_required
def farmer_messages(request):
    context = _build_farmer_portal_context(request, active_page="messages")
    if not isinstance(context, dict):
        return context
    return render(request, "chat.html", context)


@login_required
def farmer_prices(request):
    context = _build_farmer_portal_context(request, active_page="prices")
    if not isinstance(context, dict):
        return context
    return render(request, "prices.html", context)


@login_required
def farmer_profile(request):
    context = _build_farmer_portal_context(request, active_page="profile")
    if not isinstance(context, dict):
        return context
    profile = context["profile"]

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = profile.full_name
            profile.user.save(update_fields=["first_name"])
            messages.success(request, "Profile updated successfully.")
            return redirect("farmer_profile")
        context["profile_form"] = form
        return render(request, "profile.html", context)

    return render(request, "profile.html", context)


@login_required
def buyer_dashboard(request):
    context = _build_buyer_portal_context(request, active_page="dashboard")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_dashboard.html", context)


@login_required
def buyer_marketplace(request):
    context = _build_buyer_portal_context(request, active_page="marketplace")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_marketplace.html", context)


@login_required
def buyer_buy(request):
    context = _build_buyer_portal_context(request, active_page="buy")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_buy.html", context)


@login_required
def buyer_farmers(request):
    context = _build_buyer_portal_context(request, active_page="farmers")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_farmers.html", context)


@login_required
def buyer_messages(request):
    context = _build_buyer_portal_context(request, active_page="messages")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_messages.html", context)


@login_required
def buyer_prices(request):
    context = _build_buyer_portal_context(request, active_page="prices")
    if not isinstance(context, dict):
        return context
    return render(request, "buyer_prices.html", context)


@login_required
def buyer_profile(request):
    context = _build_buyer_portal_context(request, active_page="profile")
    if not isinstance(context, dict):
        return context
    profile = context["profile"]

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = profile.full_name
            profile.user.save(update_fields=["first_name"])
            messages.success(request, "Buyer profile updated successfully.")
            return redirect("buyer_profile")
        context["profile_form"] = form
        return render(request, "buyer_profile.html", context)

    return render(request, "buyer_profile.html", context)


@login_required
@require_POST
def save_product(request):
    profile = _get_farmer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    product_id = request.POST.get("product_id")
    instance = None
    if product_id:
        instance = get_object_or_404(Product, id=product_id, farmer=profile)

    form = ProductForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        product = form.save(commit=False)
        product.farmer = profile
        product.save()
        messages.success(request, "Product saved successfully.")
    else:
        messages.error(request, "Please correct the product details and try again.")
    return _redirect_to_next(request, "farmer_crops")


@login_required
@require_POST
def delete_product(request, product_id):
    profile = _get_farmer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    product = get_object_or_404(Product, id=product_id, farmer=profile)
    product.delete()
    messages.success(request, "Product removed successfully.")
    return _redirect_to_next(request, "farmer_crops")


@login_required
@require_POST
def update_order_status(request, order_id, status):
    profile = _get_farmer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    if status not in {"accepted", "rejected", "delivered"}:
        messages.error(request, "Invalid order action.")
        return redirect("farmer_dashboard")

    order = get_object_or_404(Order, id=order_id, farmer=profile)
    order.status = status
    order.save(update_fields=["status"])
    messages.success(request, f"Order marked as {order.get_status_display().lower()}.")
    return _redirect_to_next(request, "farmer_orders")


@login_required
@require_POST
def send_chat_message(request):
    profile = _get_farmer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    form = ChatReplyForm(request.POST)
    if form.is_valid():
        ChatMessage.objects.create(
            farmer=profile,
            buyer_name=form.cleaned_data["buyer_name"],
            message=form.cleaned_data["message"],
            is_unread=False,
        )
        messages.success(request, f"Message sent to {form.cleaned_data['buyer_name']}.")
    else:
        messages.error(request, "Please choose a buyer and enter a message before sending.")
    return redirect(f"{reverse('farmer_messages')}?chat={request.POST.get('buyer_name', '')}")


@login_required
@require_POST
def send_buyer_message(request):
    profile = _get_buyer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    form = BuyerChatForm(request.POST)
    if form.is_valid():
        farmer = get_object_or_404(UserProfile, id=form.cleaned_data["farmer_id"], role="farmer")
        ChatMessage.objects.create(
            farmer=farmer,
            buyer_name=profile.full_name,
            message=form.cleaned_data["message"],
            is_unread=True,
        )
        messages.success(request, f"Message sent to {farmer.full_name}.")
        return redirect(f"{reverse('buyer_messages')}?farmer={farmer.id}")

    messages.error(request, "Choose a farmer and type a message before sending.")
    return redirect("buyer_messages")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("index")


def _get_farmer_profile(request):
    profile = getattr(request.user, "profile", None)
    if not profile or profile.role != "farmer":
        return HttpResponseForbidden("Farmer access only.")
    return profile


def _get_buyer_profile(request):
    profile = getattr(request.user, "profile", None)
    if not profile or profile.role != "buyer":
        return HttpResponseForbidden("Buyer access only.")
    return profile


def _build_farmer_portal_context(request, active_page="dashboard"):
    profile = _get_farmer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    _seed_farmer_dashboard(profile)

    products = profile.products.all()
    orders = profile.orders.select_related("product").all()
    chats = list(profile.chat_messages.all()[:12])
    demands = profile.nearby_demands.all()[:4]
    recent_products = products[:3]

    earnings_today = (
        orders.filter(status="delivered").aggregate(total=Sum("total_amount")).get("total")
        or Decimal("0.00")
    )
    active_orders = orders.filter(status__in=["pending", "accepted"]).count()
    total_products = products.count()
    unread_count = profile.chat_messages.filter(is_unread=True).count()
    notifications_count = active_orders + unread_count + 2

    new_orders = orders.filter(status="pending")
    ongoing_orders = orders.filter(status="accepted")
    completed_orders = orders.filter(status="delivered")

    product_form = ProductForm()
    edit_product_id = request.GET.get("edit")
    edit_product = None
    if edit_product_id:
        edit_product = get_object_or_404(Product, id=edit_product_id, farmer=profile)
        product_form = ProductForm(instance=edit_product)

    profile_form = ProfileForm(instance=profile)
    selected_chat_name = request.GET.get("chat")
    selected_chat = None
    if selected_chat_name:
        selected_chat = next((chat for chat in chats if chat.buyer_name == selected_chat_name), None)
    if selected_chat is None and chats:
        selected_chat = chats[0]
    chat_form = ChatReplyForm(initial={"buyer_name": selected_chat.buyer_name if selected_chat else ""})

    return {
        "profile": profile,
        "active_page": active_page,
        "notifications_count": notifications_count,
        "earnings_today": earnings_today,
        "active_orders": active_orders,
        "total_products": total_products,
        "market_prices": MANDI_PRICE_DATA,
        "products": products,
        "recent_products": recent_products,
        "new_orders": new_orders,
        "ongoing_orders": ongoing_orders,
        "completed_orders": completed_orders,
        "completed_orders_count": completed_orders.count(),
        "chats": chats,
        "selected_chat": selected_chat,
        "unread_count": unread_count,
        "demands": demands,
        "product_form": product_form,
        "profile_form": profile_form,
        "chat_form": chat_form,
        "edit_product": edit_product,
        "chart_points": [42, 58, 50, 76, 68, 84, 96],
        "profile_map_url": _build_map_url(profile.latitude, profile.longitude),
    }


def _build_buyer_portal_context(request, active_page="dashboard"):
    profile = _get_buyer_profile(request)
    if not isinstance(profile, UserProfile):
        return profile

    farmers = UserProfile.objects.filter(role="farmer").prefetch_related("products").all()
    products = Product.objects.select_related("farmer").all()
    buyer_chats = list(
        ChatMessage.objects.filter(buyer_name=profile.full_name).select_related("farmer")[:12]
    )

    selected_farmer = None
    selected_farmer_id = request.GET.get("farmer")
    if selected_farmer_id:
        selected_farmer = next((farmer for farmer in farmers if str(farmer.id) == str(selected_farmer_id)), None)
    if selected_farmer is None and buyer_chats:
        selected_farmer = buyer_chats[0].farmer
    if selected_farmer is None and farmers:
        selected_farmer = farmers[0]

    profile_form = ProfileForm(instance=profile)
    chat_form = BuyerChatForm(initial={"farmer_id": selected_farmer.id if selected_farmer else ""})

    return {
        "profile": profile,
        "active_page": active_page,
        "notifications_count": max(len(buyer_chats), 1),
        "total_market_crops": products.count(),
        "total_farmers": len(farmers),
        "featured_products": products[:6],
        "farmer_profiles": farmers[:8],
        "selected_farmer": selected_farmer,
        "buyer_chats": buyer_chats,
        "market_prices": MANDI_PRICE_DATA,
        "profile_form": profile_form,
        "chat_form": chat_form,
        "profile_map_url": _build_map_url(profile.latitude, profile.longitude),
    }


def _redirect_to_next(request, fallback_name):
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect(fallback_name)


def _build_map_url(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"


def _seed_farmer_dashboard(profile):
    if not profile.products.exists():
        products = [
            {"crop_name": "Rice", "price": Decimal("2380.00"), "quantity_available": Decimal("35.00"), "unit": "quintal", "status": "available"},
            {"crop_name": "Wheat", "price": Decimal("2250.00"), "quantity_available": Decimal("22.00"), "unit": "quintal", "status": "available"},
            {"crop_name": "Vegetables", "price": Decimal("42.00"), "quantity_available": Decimal("120.00"), "unit": "kg", "status": "sold_out"},
        ]
        for item in products:
            Product.objects.create(farmer=profile, **item)

    if not profile.orders.exists():
        product_list = list(profile.products.all())
        for order_data, product in zip(ORDER_DEFAULTS, product_list, strict=False):
            Order.objects.create(
                farmer=profile,
                product=product,
                buyer_name=order_data["buyer_name"],
                quantity=order_data["quantity"],
                status=order_data["status"],
                total_amount=(product.price * order_data["quantity"]) if product else Decimal("0.00"),
                delivery_mode=order_data["delivery_mode"],
            )

    if not profile.chat_messages.exists():
        for item in CHAT_DEFAULTS:
            ChatMessage.objects.create(farmer=profile, **item)

    if not profile.nearby_demands.exists():
        for item in NEARBY_DEMAND_DEFAULTS:
            BuyerDemand.objects.create(farmer=profile, **item)

    if not profile.bank_upi_details:
        profile.bank_upi_details = "UPI: krushisettu@upi"
        profile.save(update_fields=["bank_upi_details"])


def _build_username(role, phone_number):
    base_username = slugify(f"{role}-{phone_number}")
    candidate = base_username
    counter = 1

    while User.objects.filter(username=candidate).exists():
        counter += 1
        candidate = f"{base_username}-{counter}"

    return candidate
