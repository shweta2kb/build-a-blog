from flask import Flask, request, redirect, render_template ,session ,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) 

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/", methods=['POST','GET'])
def blog():
    
    if request.method =='POST':
        #id = request.form[id]    
        title = request.form['title']
        body = request.form['body']

        new_bolg = Blog(title,body)
        db.session.add(new_bolg)
        db.session.commit()
        print("commit")

    blogs=Blog.query.all() 
    print("query........")   
    return render_template('main.html',blogs=blogs)   
        

@app.route("/addblog", methods=['POST','GET'])
def addblog():
    title_error =''
    body_error =''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == "" or body =="":
            title_error="please fill title of blog" 
            body_error ="Please Fill the body of the blog"   
            return render_template("addpost.html", title_error = title_error,body_error=body_error) 
        else:        
            add_blog = Blog(title,body)
            db.session.add(add_blog)
            db.session.commit()
            print("addblog....")
            return redirect('/')
        
    return render_template('addpost.html')  


@app.route("/displayblog", methods=['POST','GET'])
def displayblog():
    
    blog_id=request.args.get("id")
    print("blog_id......... ",blog_id)
    blogs = Blog.query.all()
    if blog_id:

        blog=Blog.query.get(blog_id)
        return render_template("displayblog.html",blog=blog)
    else:
        return render_template("main.html",blogs=blogs)
        
    

if __name__ == '__main__':
    app.run()    