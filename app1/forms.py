from django import forms

from .models import ChatMessage, Product, UserProfile


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your full name"}),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "Enter your mobile number"}),
    )
    otp = forms.CharField(
        max_length=6,
        required=False,
        label="OTP Verification",
        widget=forms.TextInput(attrs={"placeholder": "Enter 6-digit OTP"}),
    )
    password = forms.CharField(
        min_length=8,
        required=False,
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Create a password"}),
    )
    confirm_password = forms.CharField(
        min_length=8,
        required=False,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email Address (Optional)",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email (optional)"}),
    )
    location_name = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={"placeholder": "Search your village, town, or market"}),
    )
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    farmer_type = forms.ChoiceField(
        required=False,
        label="Farmer Type",
        choices=UserProfile.FARMER_TYPE_CHOICES,
    )

    def __init__(self, *args, role="buyer", stage="start", **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role
        self.stage = stage

        if role != "farmer":
            self.fields.pop("farmer_type")
        else:
            self.fields["farmer_type"].widget.attrs.update({"class": "auth-select"})

        for field_name, field in self.fields.items():
            if field_name not in {"latitude", "longitude", "farmer_type"}:
                field.widget.attrs.setdefault("class", "auth-input")

        if self.stage == "start":
            self._configure_start_stage()
        elif self.stage == "verify":
            self._configure_verify_stage()
        else:
            self._configure_complete_stage()

    def _configure_start_stage(self):
        self.fields["full_name"].required = True
        self.fields["phone_number"].required = True
        self.fields["otp"].required = False
        self.fields["password"].required = False
        self.fields["confirm_password"].required = False
        self.fields["email"].required = False
        self.fields["location_name"].required = False
        if "farmer_type" in self.fields:
            self.fields["farmer_type"].required = False

    def _configure_verify_stage(self):
        self._configure_start_stage()
        self.fields["otp"].required = True

    def _configure_complete_stage(self):
        self.fields["full_name"].required = False
        self.fields["phone_number"].required = False
        self.fields["otp"].required = False
        self.fields["password"].required = True
        self.fields["confirm_password"].required = True
        self.fields["location_name"].required = True
        if "farmer_type" in self.fields:
            self.fields["farmer_type"].required = self.role == "farmer"

    def clean_phone_number(self):
        phone_number = "".join(filter(str.isdigit, self.cleaned_data["phone_number"]))
        if len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone_number

    def clean_otp(self):
        otp = self.cleaned_data.get("otp", "").strip()
        if self.stage == "verify" and (not otp or len(otp) != 6 or not otp.isdigit()):
            raise forms.ValidationError("Enter the 6-digit OTP.")
        return otp

    def clean(self):
        cleaned_data = super().clean()

        if self.stage == "complete":
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")
            location_name = (cleaned_data.get("location_name") or "").strip()
            latitude = cleaned_data.get("latitude")
            longitude = cleaned_data.get("longitude")

            if password and confirm_password and password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match.")

            if not location_name:
                self.add_error("location_name", "Search and select your location.")

            if latitude in (None, "") or longitude in (None, ""):
                raise forms.ValidationError("Select your location from search results so coordinates can be saved.")

            if self.role == "farmer" and "farmer_type" in self.fields and not cleaned_data.get("farmer_type"):
                self.add_error("farmer_type", "Select your farmer type.")

        return cleaned_data

    def get_basic_data(self):
        return {
            "full_name": self.cleaned_data["full_name"],
            "phone_number": self.cleaned_data["phone_number"],
        }

    def get_profile_data(self):
        return {
            "password": self.cleaned_data["password"],
            "email": self.cleaned_data.get("email", ""),
            "location_name": self.cleaned_data["location_name"],
            "latitude": self.cleaned_data["latitude"],
            "longitude": self.cleaned_data["longitude"],
            "farmer_type": self.cleaned_data.get("farmer_type", ""),
        }


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="Registered Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "Enter your registered phone number"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "auth-input")

    def clean_phone_number(self):
        phone_number = "".join(filter(str.isdigit, self.cleaned_data["phone_number"]))
        if len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone_number


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["crop_name", "price", "quantity_available", "unit", "product_image", "status"]
        widgets = {
            "crop_name": forms.TextInput(attrs={"placeholder": "Crop name"}),
            "price": forms.NumberInput(attrs={"placeholder": "Price in rupees", "step": "0.01"}),
            "quantity_available": forms.NumberInput(attrs={"placeholder": "Quantity", "step": "0.01"}),
            "unit": forms.TextInput(attrs={"placeholder": "kg / quintal / piece"}),
            "product_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "auth-input")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "phone_number",
            "location_name",
            "bank_upi_details",
            "preferred_language",
            "profile_image",
        ]
        widgets = {
            "profile_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "auth-input")
            if name == "preferred_language":
                field.widget.attrs["class"] = "auth-select"

    def clean_phone_number(self):
        phone_number = "".join(filter(str.isdigit, self.cleaned_data["phone_number"]))
        if len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        qs = UserProfile.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number is already used by another account.")
        return phone_number


class ChatReplyForm(forms.Form):
    buyer_name = forms.CharField(widget=forms.HiddenInput())
    message = forms.CharField(
        label="Message",
        widget=forms.TextInput(attrs={"placeholder": "Type your message here..."}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "auth-input")

    def clean_buyer_name(self):
        buyer_name = self.cleaned_data["buyer_name"].strip()
        if not buyer_name:
            raise forms.ValidationError("Choose a buyer before sending a message.")
        return buyer_name


class BuyerChatForm(forms.Form):
    farmer_id = forms.IntegerField(widget=forms.HiddenInput())
    message = forms.CharField(
        label="Message",
        widget=forms.TextInput(attrs={"placeholder": "Ask about price, quality, or delivery..."}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "auth-input")
