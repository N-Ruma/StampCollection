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
    
    description = models.TextField(
        verbose_name="説明",
        blank=True,
    )
    '''スタンプの場所の説明'''
    
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

class Bingo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    '''ビンゴを所有しているユーザ'''

    #  0  1  2  3  4
    #  5  6  7  8  9
    # 10 11 12 13 14
    # 15 16 17 18 19
    # 20 21 22 23 24
    bingo_id0 = models.BooleanField(default=False)
    bingo_id1 = models.BooleanField(default=False)
    bingo_id2 = models.BooleanField(default=False)
    bingo_id3 = models.BooleanField(default=False)
    bingo_id4 = models.BooleanField(default=False)
    bingo_id5 = models.BooleanField(default=False)
    bingo_id6 = models.BooleanField(default=False)
    bingo_id7 = models.BooleanField(default=False)
    bingo_id8 = models.BooleanField(default=False)
    bingo_id9 = models.BooleanField(default=False)
    bingo_id10 = models.BooleanField(default=False)
    bingo_id11 = models.BooleanField(default=False)
    bingo_id12 = models.BooleanField(default=False)
    bingo_id13 = models.BooleanField(default=False)
    bingo_id14 = models.BooleanField(default=False)
    bingo_id15 = models.BooleanField(default=False)
    bingo_id16 = models.BooleanField(default=False)
    bingo_id17 = models.BooleanField(default=False)
    bingo_id18 = models.BooleanField(default=False)
    bingo_id19 = models.BooleanField(default=False)
    bingo_id20 = models.BooleanField(default=False)
    bingo_id21 = models.BooleanField(default=False)
    bingo_id22 = models.BooleanField(default=False)
    bingo_id23 = models.BooleanField(default=False)
    bingo_id24 = models.BooleanField(default=False)

    def get_bingo_data(self) -> list[bool]:
        return [
            bool(self.bingo_id0),
            bool(self.bingo_id1),
            bool(self.bingo_id2),
            bool(self.bingo_id3),
            bool(self.bingo_id4),
            bool(self.bingo_id5),
            bool(self.bingo_id6),
            bool(self.bingo_id7),
            bool(self.bingo_id8),
            bool(self.bingo_id9),
            bool(self.bingo_id10),
            bool(self.bingo_id11),
            bool(self.bingo_id12),
            bool(self.bingo_id13),
            bool(self.bingo_id14),
            bool(self.bingo_id15),
            bool(self.bingo_id16),
            bool(self.bingo_id17),
            bool(self.bingo_id18),
            bool(self.bingo_id19),
            bool(self.bingo_id20),
            bool(self.bingo_id21),
            bool(self.bingo_id22),
            bool(self.bingo_id23),
            bool(self.bingo_id24),
        ]

    def change_true(self, num: int) -> bool:
        match num:
            case 0:
                self.bingo_id0 = True
            case 1:
                self.bingo_id1 = True
            case 2:
                self.bingo_id2 = True
            case 3:
                self.bingo_id3 = True
            case 4:
                self.bingo_id4 = True
            case 5:
                self.bingo_id5 = True
            case 6:
                self.bingo_id6 = True
            case 7:
                self.bingo_id7 = True
            case 8:
                self.bingo_id8 = True
            case 9:
                self.bingo_id9 = True
            case 10:
                self.bingo_id10 = True
            case 11:
                self.bingo_id11 = True
            case 12:
                self.bingo_id12 = True
            case 13:
                self.bingo_id13 = True
            case 14:
                self.bingo_id14 = True
            case 15:
                self.bingo_id15 = True
            case 16:
                self.bingo_id16 = True
            case 17:
                self.bingo_id17 = True
            case 18:
                self.bingo_id18 = True
            case 19:
                self.bingo_id19 = True
            case 20:
                self.bingo_id20 = True
            case 21:
                self.bingo_id21 = True
            case 22:
                self.bingo_id22 = True
            case 23:
                self.bingo_id23 = True
            case 24:
                self.bingo_id24 = True
            case _:
                return False
        return True
    
    def reset(self):
        self.bingo_id0 = False
        self.bingo_id1 = False
        self.bingo_id2 = False
        self.bingo_id3 = False
        self.bingo_id4 = False
        self.bingo_id5 = False
        self.bingo_id6 = False
        self.bingo_id7 = False
        self.bingo_id8 = False
        self.bingo_id9 = False
        self.bingo_id10 = False
        self.bingo_id11 = False
        self.bingo_id12 = False
        self.bingo_id13 = False
        self.bingo_id14 = False
        self.bingo_id15 = False
        self.bingo_id16 = False
        self.bingo_id17 = False
        self.bingo_id18 = False
        self.bingo_id19 = False
        self.bingo_id20 = False
        self.bingo_id21 = False
        self.bingo_id22 = False
        self.bingo_id23 = False
        self.bingo_id24 = False