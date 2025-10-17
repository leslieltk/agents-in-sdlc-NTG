from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate the publisher name.
        
        Args:
            key (str): The attribute name being validated.
            name (str): The publisher name to validate.
            
        Returns:
            str: The validated publisher name.
            
        Raises:
            ValueError: If the name fails validation.
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validate the publisher description.
        
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
        Return string representation of the Publisher object.
        
        Returns:
            str: A string representation showing the publisher name.
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Convert the Publisher object to a dictionary suitable for JSON serialization.
        
        Returns:
            dict: A dictionary containing publisher data including game count.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }