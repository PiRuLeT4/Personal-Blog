from flask import Flask, request, render_template, session, redirect, url_for
from utils import load_all_posts, load_post, save_post, delete_post, add_post, save_user, validate_user
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #.. here we validate the credentials
        if validate_user(username, password):
            #.. ADMIN
            if (username == 'admin') and (password == 'chocolate'):
                session['loged_in'] = True
                session['is_admin'] = True
                return redirect(url_for('admin'))
            #.. USER
            elif (username != 'admin') and password:
                session['loged_in'] = True
                session['is_admin'] = False

            return redirect(url_for('home'))
        else:
            return 'User not found, Create a new account to log in'
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('loged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('loged_in') or not session.get('is_admin'):
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return wrapper




@app.route('/home_admin')
@admin_required
def admin():
    posts = load_all_posts()
    return render_template('home_admin.html', posts=posts)

@app.route('/home')
@login_required
def home():
    posts = load_all_posts()
    return render_template('home.html', posts=posts)

    
@app.route('/article/<string:id>')
@login_required
def blog_details(id):
    blog = load_post(id)
    title = blog['title']
    content = blog['content'] 
    return render_template('blog.html', title=title, content=content)

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
@admin_required
def edit(id):
    if request.method == 'POST':
        updated = {}

        title = request.form['title']
        date = request.form['date']
        content = request.form['content']

        updated['title'] = title
        updated['date'] = date 
        updated['content'] = content
        updated['id'] = id

        save_post(updated)

        return redirect(url_for('admin'))
        
    return render_template('edit_blog.html')

@app.route('/new', methods=['GET', 'POST'])
@admin_required
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        content = request.form['content']

        new_blog = {
            'title': title, 
            'content': content,
            'date': date,
            'id': None, 
        }
        add_post(new_blog)
        return redirect(url_for('admin'))

    return render_template('add_blog.html')

@app.route('/delete_blog/<string:id>')
@admin_required
def delete(id):
    delete_post(id)
    return redirect(url_for('admin'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #.. save the new user in users
        if save_user(username, password):
            return redirect(url_for('login'))
        else:
            return 'User alredy exists'
        
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)


 