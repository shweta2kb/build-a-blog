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
    
    # check for query paramter named id
    # if you find it render displayblog.html
    
    id =  request.args.get('id')

    if id:
        blog = Blog.query.get(id)
        return render_template('displayblog.html',blog=blog)
    # if no id paramter, then render main.html


    blogs=Blog.query.all() 
    return render_template('main.html',blogs=blogs)   
        

@app.route("/addblog", methods=['POST','GET'])
def addblog():
    title_error =''
    body_error =''
    print('WE MADE IT')

    if request.method == 'POST':
        print('in POST part')
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
            return redirect('/?id=' + str(add_blog.id))

    #if request.args:
    #    print('in request.args part')
    #    print(request.args)
    #    id_number = request.args['id']
    #    post = Blog .query.filter_by(id=id_number).first()
    #    return render_template('displayblog.html',blog=post)

    # this displays the form   
    return render_template('addpost.html')  


@app.route("/displayblog", methods=['POST','GET'])
def displayblog():
    
    blog_id=request.args.get("id")
    blogs = Blog.query.all()
    if blog_id:

        blog=Blog.query.get(blog_id)
        return render_template("displayblog.html",blog=blog)
    else:
        return render_template("main.html",blogs=blogs)
        
    

if __name__ == '__main__':
    app.run()    