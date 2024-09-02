import unittest
from app import app,db
from models import BlogPost,Comment
class BlogPostAPITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_blog_posts(self):
        # create some blog posts in the database
        post1 = BlogPost(title="Women In Tech",content="In this post I 'd like to talk about the presence of women in the tech.",author="Someone")
        post2 = BlogPost(title="Diversity In Tech",content="In this post I 'd like to talk about inclusion and diversity in the tech.",author="Someone Else")
        db.session.add_all([post1,post2])
        db.session.commit()
        # now we have to call the api end point to ge the list of posts: we would need a Http Get request in such scenario
        response = self.app.get('/api/blog_posts')
        self.assertEqual(response.status_code,200)
        
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(len(data),2)
        self.assertEqual(data[0]['title'],"Women In Tech")
        self.assertEqual(data[1]['title'],"Diversity In Tech")
        
    def test_create_blog_post(self):
        new_blog_post ={
            'title': 'new blog post',
            'content': 'this is a new blog post about how flat an organization must be',
            'author': 'Test Author'
        }
        response = self.app.post('/api/blog_posts',json=new_blog_post)
        # Check that the request was successful (status code 201 Created)
        self.assertEqual(response.status_code,201)
        # verify the response contains correct data
        data= response.get_json()
        self.assertEqual(data['title'],'new blog post')
        self.assertEqual(data['content'],'this is a new blog post about how flat an organization must be')
        self.assertEqual(data['author'],'Test Author')
        
    def test_delete_blog_post(self):
        
        blog_post= BlogPost(title="test post",author="test author",content=" this is a blog to be deleted")
        db.session.add(blog_post)
        db.session.commit()
        # create the delete request
        response = self.app.delete(f'/api/blog_posts/{blog_post.id}')
        # Check that the request was successful (status code 201 Created)
        self.assertEqual(response.status_code,200)
        # verify the response contains correct data
       
        self.assertEqual(response.get_json(),{'message':'Post was deleted successfully'})
        deleted_post = BlogPost.query.get(blog_post.id)
        self.assertIsNone(deleted_post)
        
    def test_modify_blog_post(self):
        
        blog_post= BlogPost(title="test post",author="test author",content=" this is a blog to be deleted")
        db.session.add(blog_post)
        db.session.commit()
        # create the update request
        # New data for update
        updated_data = {
        'title': "New Title",
        'content': "New Content",
        'author': "New Author"
        }
        response = self.app.put(f'/api/blog_posts/{blog_post.id}',json=updated_data)
        # Check that the request was successful (status code 201 Created)
        self.assertEqual(response.status_code,200)
        # verify the response contains correct data
       
        self.assertEqual(response.get_json(), {'message': 'Blog post updated successfully'})

        # Verify the post was updated
        updated_post = BlogPost.query.get(blog_post.id)
        self.assertEqual(updated_post.title, "New Title")
        self.assertEqual(updated_post.content, "New Content")
        self.assertEqual(updated_post.author, "New Author")
        
if __name__ == '__main__':
    unittest.main()