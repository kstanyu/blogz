
from flask import Flask, redirect, render_template, request, url_for
#from signup_info_checks import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://blogz:LC101Blogz@localhost:8889/blogz"

app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


#blogz user class
class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref = "owner")
   
    def __init__(self, username, password ):
        self.username = username
        self.password = password

#blog class thats owner by a user
class Blog(db.Model):
        
    id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, blog_title, blog_post, user):
        self.blog_title = blog_title
        self.blog_post = blog_post
        self.user = user

    
@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("newpost.html")
 
@app.route("/login")
def login():

@app.route("/signup")
def signup():

@app.route("/blog", methods = ["POST", "GET"])
def blog():
    blog_posts = Blog.query.all()

    blog_id = request.args.get('id')
    if blog_id is None: 
        return render_template("homepage.html", title = "BUILD A BLOG", blogposts = blog_posts)
    else:
        blog_entry = Blog.query.get(blog_id)
        return render_template("blog-post.html", blog_title = blog_entry.blog_title, blog_content = blog_entry.blog_post)

    #return render_template("homepage.html", title = "BUILD A BLOG", blogposts = blog_posts)

@app.route("/newpost", methods = ["POST", "GET"])
def newpost(): 
    if request.method == "POST":
        blog_title_error = ""
        blog_post_error = ""
        blg_title = ""
        blg_post = ""
        if is_empty(request.form["blog_title"]) or is_empty(request.form["blog_post"]):
            if is_empty(request.form["blog_title"]):
                blog_title_error = "Please fill in the title."
            else:
                blg_title = request.form["blog_title"]
            if is_empty(request.form["blog_post"]):
                blog_post_error = "Please fill in the Body."
            else:
                blg_post = request.form["blog_post"]

        #if (request.form["blog_title"] == "") or (request.form["blog_post"] == ""):
        if blog_title_error or blog_post_error: 
            return render_template("newpost.html", blg_title = blg_title, blg_post = blg_post,  blog_title_error = blog_title_error, body_error = blog_post_error)
        else:
            blog_title = request.form["blog_title"]
            new_post = request.form["blog_post"]
            new_blog = Blog(blog_title, new_post)
            db.session.add(new_blog)
            db.session.commit()
        
            return redirect(url_for("blog", id = [new_blog.id]))
    
    return render_template("newpost.html")

#@app.route("/newpost", methods = ["POST","GET"])
#def newpost():
#    return render_template("newpost.html")

    
if __name__ == "__main__":
    app.run()
