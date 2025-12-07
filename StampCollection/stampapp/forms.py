from django.forms import ModelForm
from .models import *

class StampPinForm(ModelForm):
    class Meta:
        model = StampPin
        # 入力するフィールド
        fields = [
            "name",
            "latitude",
            "longitude",
            "stamp_image"
        ]