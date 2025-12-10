from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class StampPin(models.Model):    
    def stamp_upload_to(self, filename: str) -> str:
        '''画像パスをUUIDに設定し取得する
        
        :return: カスタマイズしたファイル名を含む画像パス
        '''
        prefix = "stamp_images/"
        new_filename = str(uuid4()).replace("-", "")
        extension = filename.split(".")[-1]
        
        return f"{prefix}{new_filename}.{extension}"
    
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    '''スタンプ名'''
    
    latitude = models.FloatField(
        verbose_name="latitude",
    )
    '''緯度'''
    
    longitude = models.FloatField(
        verbose_name="longitude",
    )
    '''経度'''

    stamp_image = models.ImageField(
        verbose_name="stamp_image",
        upload_to=stamp_upload_to, # type: ignore
        null=True, # データ生成時のnullはOK
        blank=False, # 画像アップロード時のblankはNG
    )
    '''スタンプ画像'''
    
    users = models.ManyToManyField(
        to=User,
        verbose_name="users_own_stamp",
    )
    '''スタンプを獲得したユーザ'''

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "latitude",
                    "longitude",
                ],
                name="stamp_pin_unique",
            ),
        ]
        '''緯度と経度による重複を許可しない'''
    
    def __str__(self) -> str:
        return self.name
