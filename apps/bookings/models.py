from django.db import models


class Booking(models.Model):
    # Foreign keys with cascade deletion
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Номер"
    )
    # Booking dates and cost details
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(verbose_name="Дата выезда")
    rent_days = models.IntegerField(verbose_name="Количество дней проживания")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    # String representation for admin panel
    def __str__(self):
        return f"Бронирование #{self.id} — Номер {self.room.room_number} ({self.user})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
