from flask import Flask,jsonify,request
from models import db,BlogPost,Comment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)
@app.route('/')
def index():
    return 'Welcome to blog API!'

@app.route('/api/blog_posts',methods=['GET'])
def get_blog_posts():
    posts = BlogPost.query.all()
    posts_list = [{'id':post.id,'title':post.title,'content': post.content, 'author':post.author} for post in posts]
    return jsonify(posts_list),200

@app.route('/api/blog_posts',methods=['POST'])
def create_blog_post():
    data = request.get_json()
    new_post = BlogPost(title=data['title'],author=data['author'],content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({
        'id':new_post.id,
        'title' : new_post.title,
        'content': new_post.content,
        'author': new_post.author
    }), 201
    
@app.route('/api/blog_posts/<int:id>',methods=['DELETE'])
def delete_blog_post(id):
    post = BlogPost.query.get(id)
    if post is None:
        return jsonify({
            'error': 'Blog post does not exist!'
        }),404
    db.session.delete(post)
    db.session.commit()
    return jsonify({
        'message': 'Post was deleted successfully'
        }),200

@app.route('/api/blog_posts/<int:id>',methods=['PUT'])
def update_blog_post(id):
    post = BlogPost.query.get(id)
    if post is None:
        return jsonify({'error':'Blog post does not exist!'}),404
    
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.author = data.get('author', post.author)
    db.session.commit()
    return jsonify({'message': 'Blog post updated successfully'}),200


if __name__ =='__main__':
    app.run(debug=True)