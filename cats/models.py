from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement, through='AchievementCat')

    def __str__(self):
        return self.name

 
    
    class Meta:
        # как вариант для валидатора уникального значения в модели. 
        # unique_together = ('name', 'owner',)
        # Но Django предлагает следующее (Такую же проверку нужно реализовать и на уровне сериализатора.)
        constraints = [models.UniqueConstraint(
            fields=['name', 'owner'],
            name='unique_name_together'
            )
        ]

class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'
