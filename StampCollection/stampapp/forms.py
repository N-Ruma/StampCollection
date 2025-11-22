from django.forms import ModelForm
from .models import MapPin

class MapPinForm(ModelForm):
    class Meta:
        model = MapPin
        # 入力するフィールド
        fields = [
            "name",
            "latitude",
            "longitude",
        ]
        