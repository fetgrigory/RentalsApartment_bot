class Paginator:
    def __init__(self, items: list, page: int = 1):
        self.items = items
        self.page = page
        self.per_page = 1

        # Calculate the total number of pages
        self.pages = max(1, (len(items) + self.per_page - 1) // self.per_page)

        # Clamp page number to valid range
        if self.page < 1:
            self.page = 1
        if self.page > self.pages:
            self.page = self.pages

    # Get items for the current page
    def get_page(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]

    # Check if a next page exists
    def has_next(self):
        return self.page < self.pages

    # Check if a previous page exists
    def has_previous(self):
        return self.page > 1