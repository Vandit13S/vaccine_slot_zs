from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class userlist(db.Model):
    srno = db.Column(db.Integer,primary_key=True, autoincrement=True)
    n = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(50),nullable=False)
    filler1 = db.Column(db.String(500), nullable=True)
    filler2 = db.Column(db.String(500), nullable=True)
    filler3 = db.Column(db.String(500), nullable=True)
    filler4 = db.Column(db.String(500), nullable=True)
    filler5 = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<Pincode %r>' % self.n

#db.drop_all()
#db.create_all()
@app.route('/', methods=["GET", "POST"])
def index():
    errors = ""
    if request.method == "POST":
        n = None
        email = None
        dt = None
        try:
            n = int(request.form["n"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["n"])
        try:
            email = str(request.form["email"])
        except:
            errors += "<p>{!r} is not valid.</p>\n".format(request.form["email"])
        '''try:
            dt = str(request.form["dt"])
        except:
            errors += "<p>{!r} is not valid.</p>\n".format(request.form["dt"])'''

        if n is not None and email is not None and errors=="":
            new_srno2 = userlist( n=n, email=email)
            try:
                db.session.add(new_srno2)
                db.session.commit()
                tasks = userlist.query.order_by(userlist.n).all()
            except:
                return 'Error in taking input'
            return render_template('result.html',tasks=tasks)
        else:
            return render_template('index.html').format(errors=errors)
    else:
        #tasks = userlist.query.order_by(userlist.n).all()
        return render_template('index.html').format(errors=errors)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    errors=""
    if request.method == "POST":
        #n = None
        email = None
        try:
            email = str(request.form["email"])
        except:
            errors += "<p>{!r} is not valid.</p>\n".format(request.form["email"])
        if email is not None:
            user_to_delete = userlist.query.filter_by(email=email).all()
            try:
                for i in user_to_delete:
                    db.session.delete(i)
                    db.session.commit()
                tasks = userlist.query.order_by(userlist.n).all()
            except:
                return 'Error in deleting this email'
            return render_template('result.html',tasks=tasks)
    else:
        return render_template('delete.html')


if __name__ == "__main__":
    app.run(debug=True)


