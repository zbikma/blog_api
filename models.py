from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(100),nullable=False)
    content= db.Column(db.Text,nullable=False)
    author= db.Column(db.String(50),nullable=False)
    created_date= db.Column(db.DateTime,default= lambda: datetime.now(timezone.utc))
    comments = db.relationship('Comment',backref='post',lazy=True)
    
class Comment(db.Model):
    __tablename__ = 'Comments'
    id=db.Column(db.Integer,primary_key=True)
    post_id= db.Column(db.Integer,db.ForeignKey("blog_posts.id"),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default= lambda: datetime.now(timezone.utc))
