class Paginator:
    def __init__(self, items: list, page: int = 1):
        self.items = items
        self.page = page
        self.per_page = 1

        self.pages = max(1, (len(items) + self.per_page - 1) // self.per_page)

        # защита от выхода за границы
        if self.page < 1:
            self.page = 1
        if self.page > self.pages:
            self.page = self.pages

    def get_page(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]

    def has_next(self):
        return self.page < self.pages

    def has_previous(self):
        return self.page > 1