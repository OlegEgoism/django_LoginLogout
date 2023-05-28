from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    photo = models.ImageField(verbose_name='Фотография', upload_to='user/%Y/%m/', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)
