from django.forms import ModelForm
from .models import StampPin

class StampPinForm(ModelForm):
    class Meta:
        model = StampPin
        # 入力するフィールド
        fields = [
            "name",
            "latitude",
            "longitude",
        ]
        