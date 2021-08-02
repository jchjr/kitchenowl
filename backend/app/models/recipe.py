from app import db
from app.helpers import DbModelMixin, TimestampMixin
from .item import Item


class Recipe(db.Model, DbModelMixin, TimestampMixin):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String())
    photo = db.Column(db.String())
    planned = db.Column(db.Boolean)

    recipe_history = db.relationship(
        "RecipeHistory", back_populates="recipe", cascade="all, delete-orphan")
    items = db.relationship(
        'RecipeItems', back_populates='recipe', cascade="all, delete-orphan")

    def obj_to_full_dict(self):
        res = super().obj_to_dict()
        items = RecipeItems.query.filter(RecipeItems.recipe_id == self.id).join(
            RecipeItems.item).order_by(
            Item.name).all()
        res['items'] = [e.obj_to_item_dict() for e in items]
        return res

    def obj_to_export_dict(self):
        items = RecipeItems.query.filter(RecipeItems.recipe_id == self.id).join(
            RecipeItems.item).order_by(
            Item.name).all()
        res = {
            "name": self.name,
            "description": self.description,
            "items": [{"name": e.item.name, "description": e.description, "optional": e.optional} for e in items],
        }
        return res

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def search_name(cls, name):
        if '*' in name or '_' in name:
            looking_for = name.replace('_', '__')\
                .replace('*', '%')\
                .replace('?', '_')
        else:
            looking_for = '%{0}%'.format(name)
        return cls.query.filter(cls.name.ilike(looking_for)).all()


class RecipeItems(db.Model, DbModelMixin, TimestampMixin):
    __tablename__ = 'recipe_items'

    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    description = db.Column('description', db.String())
    optional = db.Column('optional', db.Boolean)

    item = db.relationship("Item", back_populates='recipes')
    recipe = db.relationship("Recipe", back_populates='items')

    def obj_to_item_dict(self):
        res = self.item.obj_to_dict()
        res['description'] = getattr(self, 'description')
        res['optional'] = getattr(self, 'optional')
        res['created_at'] = getattr(self, 'created_at')
        res['updated_at'] = getattr(self, 'updated_at')
        return res

    @classmethod
    def find_by_ids(cls, recipe_id, item_id):
        return cls.query.filter(cls.recipe_id == recipe_id, cls.item_id == item_id).first()
