from beanie import Document, Indexed


class Category(Document):
    name: Indexed(str, unique=True)
    description: str

    class Settings:
        name = "categories"
