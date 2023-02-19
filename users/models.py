from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.validators import check_birth_date


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположение"

    def __str__(self):
        return self.name


class UserRoles(models.TextChoices):
    MEMBER = "member", _("member")
    MODERATOR = "moderator", _("moderator")
    ADMIN = "admin", _("admin")


class Users(AbstractUser):
    role = models.CharField(choices=UserRoles.choices, default=UserRoles.MEMBER, max_length=9)
    age = models.SmallIntegerField(null=True)
    location = models.ManyToManyField(Location)
    email = models.EmailField(unique=True, null=True, blank=True,
                              validators=[RegexValidator(
                                  regex="@rambler.ru",
                                  inverse_match=True,
                                  message="Регистрация с домена 'rambler.ru' запрещена"
                              )])
    birth_date = models.DateField(null=True, blank=True, validators=[check_birth_date])

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
