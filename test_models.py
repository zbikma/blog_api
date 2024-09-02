import unittest
from app import app,db
from models import BlogPost,Comment

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a temporary database for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_blog_post(self):  # sourcery skip: class-extract-method
        post= BlogPost(title="Test Post",content="This is a test blog post",author="Test Author")
        db.session.add(post)
        db.session.commit()
        # fetch the post and check if it was successfully created
        out_post = BlogPost.query.first()
        self.assertIsNotNone(out_post)
        self.assertEqual(out_post.title,"Test Post")
    
    def test_create_comment(self):
        post= BlogPost(title="Test Post",content="This is a test blog post",author="Test Author")
        db.session.add(post)
        db.session.commit()
        
        comment = Comment(content = "This is a test comment on Test Post",author="Test Comment Author",post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        # now check if the comment is create 
        out_comment = Comment.query.first()
        self.assertIsNotNone(out_comment)
        self.assertEqual(out_comment.post_id ,post.id)
        self.assertEqual(out_comment.content,"This is a test comment on Test Post")
        
        
        
if __name__ == '__main__':
    unittest.main()