from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StampPin(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    
    latitude = models.FloatField(
        verbose_name="latitude",
    )
    
    longitude = models.FloatField(
        verbose_name="longitude",
    )
    
    # スタンプを獲得したユーザ
    users = models.ManyToManyField(
        to=User,
        verbose_name="users_own_stamp",
    )

    class Meta:
        constraints = [
            # 緯度と経度による重複を許可しない
            models.UniqueConstraint(
                fields=[
                    "latitude",
                    "longitude",
                ],
                name="stamp_pin_unique",
            ),
        ]
    
    def __str__(self) -> str:
        return self.name
