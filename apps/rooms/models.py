from django.db import models


class Room(models.Model):
    # Room category (standard / comfort / superior / imperial)
    CATEGORY_CHOICES = [
        ('standard', 'Стандарт'),
        ('comfort', 'Комфорт'),
        ('superior', 'Улучшенный'),
        ('imperial', 'Империал')
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='standard',
        verbose_name="Категория"
    )
    room_number = models.CharField(
        max_length=10,
        verbose_name="Номер комнаты",
        help_text="Например: 101, 205, 310",
    )
    # Date added
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    # Room photos (gallery)
    photo1 = models.ImageField(upload_to="rooms/", verbose_name="Фото 1")
    photo2 = models.ImageField(upload_to="rooms/", verbose_name="Фото 2", blank=True, null=True)
    photo3 = models.ImageField(upload_to="rooms/", verbose_name="Фото 3", blank=True, null=True)
    # Room description
    description = models.TextField(verbose_name="Описание")
    # Room  price
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # String representation for admin panel
    def __str__(self):
        return f"{self.get_category_display()} #{self.room_number}"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
