import json

from tinydb import TinyDB
from tinydb.table import Document


class Manager:

    def __init__(self, item_type):
        self.items = {}
        self.item_type = item_type
        db = TinyDB("db.json", sort_keys=True, indent=4)
        self.table = db.table(self.item_type.__name__.lower() + "s")
        for item_data in self.table:
            self.create(**item_data)

    def create(self, save=False, **kwargs):  # Ajout de données à la base de donnée
        if "id" not in kwargs:
            kwargs["id"] = self.get_next_id()

        item = self.item_type(**kwargs)
        self.items[item.id] = item
        if save:
            self.save_item(item.id)
        return item

    def get_next_id(self):  # Récupère l'id suivant dans la base de donnée
        try:
            return self.table.all()[-1].doc_id + 1
        except IndexError:
            return 1

    def search(self, filter_key=lambda x: x,
               sort_key=lambda x: x.id):  # Accède aux données voulues dans la base de donnée de façon générique
        return list(sorted(filter(filter_key, self.items.values()),
                    key=sort_key))

    def search_by_id(self, id):  # Recherche par ID
        return self.items[id]

    def all(self):  # Retourne toute les données voulues
        return list(self.items.values())

    def save_item(self, id):  # Permet de sauvegarder une nouvelle donnée en écrasant l'ancienne
        item = self.search_by_id(id)
        self.table.upsert(Document(json.loads(item.json()), doc_id=id))
