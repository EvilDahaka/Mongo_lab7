from beanie import Document, Indexed


class Category(Document):
    name: str = Indexed(unique=True)
    description: str

    class Settings:
        name = "categories"
