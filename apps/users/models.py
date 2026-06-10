from django.db import models


class User(models.Model):
    # Telegram ID
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")

    # User name (first name and last name)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")

    #  Phone number
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")

    # Date of registration
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    # String representation for admin panel
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
