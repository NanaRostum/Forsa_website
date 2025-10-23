from flask import Flask, render_template, request, redirect, url_for, session, flash
from connection import conn 

app = Flask(__name__)
app.secret_key = 'nananananan'


@app.route('/')
def index():
    return  redirect(url_for('base'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    messaggio = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        # gia_registrato = False

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            gia_registrato = cursor.fetchone()

            if gia_registrato:
                messaggio = ' Utente già registrato. Vai al login.'
                return redirect(url_for('login'))
            else:
                cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                           (name, email, password))
                conn.commit()
                messaggio = ' Registrazione completata! Ora puoi accedere.'
                session["messaggio"]=messaggio
                return redirect(url_for('login'))
            
        except Exception as error:
            messaggio = f'Errore: {str(error)}'

    return render_template('register.html', messaggio=messaggio)


@app.route('/login', methods=['GET', 'POST'])
def login():
    messaggio = ''
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        # trovato = False
      

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            trovato = cursor.fetchone()
            # trovato = True
                    
            if trovato: 
                session['email'] = email
                if email == 'forsadmin@gmail.com':
                    return redirect(url_for('dashboard'))
                return redirect(url_for('home'))
            

            else:
                messaggio = ' Email o password errate o you need to register'
            

        except Exception as error:
            messaggio = f'Errore: {str(error)}'
    # if 'messaggio' in session:
    #         messaggio =session['messaggio']
    return render_template('login.html', messaggio=messaggio)




@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', email=session['email'])


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Hai effettuato il logout con successo.')
    return redirect(url_for('base'))


@app.route('/courses')
def courses():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    return render_template('courses.html', courses=data)

@app.route('/scholarships')
def scholarships():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scholarships")
    data_scholarship = cursor.fetchall()
    return render_template('scholarships.html', scholarships=data_scholarship)

@app.route('/consulting', methods=['POST', "GET"])
def consulting():
    messaggio =""

    
    if request.method =="POST":
        topic = request.form['topic']
        details = request.form['details']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consulting_requests (user_email, topic, details) VALUES(%s,%s,%s)", (session['email'], topic, details))

        conn.commit()
        messaggio = "Your consulting request has been submitted"
        return render_template('consulting.html', messaggio=messaggio)
    
    if "email"  not in session:
        messaggio = "You must login to access the consulting service."
    return render_template('consulting.html', messaggio=messaggio)

@app.route('/admin')
def admin():
    messaggio =""
    if "email" not in session or session.get('email') != "forsadmin@gmail.com":
        messaggio = "Access denied: Admins only."
    return render_template("admin.html", messaggio=messaggio)


@app.route('/dashboard')
def dashboard():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scholarships")
    total_scholarships = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM consulting_requests")
    total_consults = cursor.fetchone()[0]

    return render_template('dashboard.html', 
                           total_users=total_users,
                           total_courses = total_courses,
                           total_scholarships = total_scholarships,
                           total_consults = total_consults
                           )


@app.route('/base')
def base():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scholarships ORDER BY id DESC LIMIT 3")
    latest_scholarships = cursor.fetchall()

    cursor.execute("SELECT * FROM courses ORDER BY id DESC LIMIT 3")
    latest_courses = cursor.fetchall()
    return render_template('base.html', 
                           latest_scholarships = latest_scholarships,
                           latest_courses=latest_courses)

if __name__ == '__main__':
    app.run(debug=True)
