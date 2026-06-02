from .models import Room


# Retrieves rooms from the catalog filtered by category
def get_catalog_data():
    return list(Room.objects.all())


# Retrieves all rooms from the catalog
def get_catalog_by_category(category):
    return list(Room.objects.filter(category=category))