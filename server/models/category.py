from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Category(BaseModel):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one category has many games
    games = relationship("Game", back_populates="category")
    
    @validates('name')
    def validate_name(self, key, name):
        """
        Validate the category name.
        
        Args:
            key (str): The attribute name being validated.
            name (str): The category name to validate.
            
        Returns:
            str: The validated category name.
            
        Raises:
            ValueError: If the name fails validation.
        """
        return self.validate_string_length('Category name', name, min_length=2)
        
    @validates('description')
    def validate_description(self, key, description):
        """
        Validate the category description.
        
        Args:
            key (str): The attribute name being validated.
            description (str or None): The description to validate.
            
        Returns:
            str or None: The validated description.
            
        Raises:
            ValueError: If the description fails validation.
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)
    
    def __repr__(self):
        """
        Return string representation of the Category object.
        
        Returns:
            str: A string representation showing the category name.
        """
        return f'<Category {self.name}>'
        
    def to_dict(self):
        """
        Convert the Category object to a dictionary suitable for JSON serialization.
        
        Returns:
            dict: A dictionary containing category data including game count.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }