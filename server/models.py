from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(length=10), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        # Ensure that name is not empty
        if not value.strip():
            raise ValueError("Author name cannot be empty.")
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        # Ensure that phone numbers are exactly ten digits if provided
        if value and (len(value) != 10 or not value.isdigit()):
            raise ValueError("Phone number must be exactly ten digits and contain only digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)

    @validates('title')
    def validate_title(self, key, value):
        # Check for clickbait phrases in the title
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("The title must contain at least one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return value
    
    @validates('content')
    def validate_content(self, key, value):
        # Ensure that post content is at least 250 characters long
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        # Ensure that post category is either Fiction or Non-Fiction
        if value not in ('Fiction', 'Non-Fiction'):
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        # Ensure that post summary is a maximum of 250 characters if provided
        if value and len(value) >= 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return value
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
