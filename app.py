from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

def add_log(username, action):

    cur = mysql.connection.cursor()

    cur.execute(
        """
        INSERT INTO activity_logs(
            username,
            action_text
        )
        VALUES(%s, %s)
        """,
        (username, action)
    )

    mysql.connection.commit()

    cur.close()
    
def can_edit():
    return session.get('role') in ['admin', 'manager']

def access_denied():
    return render_template(
        'access_denied.html',
        title='Доступ запрещён'
    )

@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            if user[4] == 'blocked':
                error = 'Пользователь заблокирован'

            else:
            
                session['user'] = username
                session['role'] = user[3]

                add_log(username, 'Вход в систему')

                return redirect('/dashboard')

        else:
            error = 'Неверный логин или пароль'

    return render_template(
        'login.html',
        error=error
    )


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM doctors")
    doctors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM patients")
    patients = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointments")
    appointments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM services")
    services = cur.fetchone()[0]

    cur.execute(
        """
        SELECT action_text, created_at
        FROM activity_logs
        ORDER BY id DESC
        LIMIT 5
        """
    )

    logs = cur.fetchall()

    cur.close()

    return render_template(
        'dashboard.html',
        title='Главная',
        doctors=doctors,
        patients=patients,
        appointments=appointments,
        services=services,
        logs=logs
    )
    

@app.route('/doctors')
def doctors():
    if 'user' not in session:
        return redirect('/login')

    search = request.args.get('search', '')

    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            """
            SELECT * FROM doctors
            WHERE full_name LIKE %s OR specialization LIKE %s
            """,
            (
                '%' + search + '%',
                '%' + search + '%'
            )
        )
    else:
        cur.execute("SELECT * FROM doctors")

    doctors = cur.fetchall()

    cur.close()

    return render_template(
        'doctors.html',
        title='Врачи',
        doctors=doctors,
        search=search
    )


@app.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():

    if 'user' not in session:
        return redirect('/login')

    if not can_edit():
        return access_denied()

    if request.method == 'POST':

        full_name = request.form['full_name']
        specialization = request.form['specialization']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO doctors(
                full_name,
                specialization,
                phone,
                email
            )
            VALUES(%s, %s, %s, %s)
            """,
            (
                full_name,
                specialization,
                phone,
                email
            )
        )

        mysql.connection.commit()

        cur.close()

        add_log(session['user'], 'Добавлен врач')
        
        flash('Врач успешно добавлен')

        return redirect('/doctors')

    return render_template(
        'add_doctor.html',
        title='Добавление врача'
    )


@app.route('/edit-doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):

    if 'user' not in session:
        return redirect('/login')
    
    if not can_edit():
        return access_denied()

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        specialization = request.form['specialization']
        phone = request.form['phone']
        email = request.form['email']

        cur.execute(
            """
            UPDATE doctors
            SET
                full_name=%s,
                specialization=%s,
                phone=%s,
                email=%s
            WHERE id=%s
            """,
            (
                full_name,
                specialization,
                phone,
                email,
                id
            )
        )

        mysql.connection.commit()

        cur.close()
        
        add_log(session['user'], 'Изменены данные врача')
        
        flash('Данные врача обновлены')

        return redirect('/doctors')

    cur.execute(
        "SELECT * FROM doctors WHERE id=%s",
        (id,)
    )

    doctor = cur.fetchone()

    cur.close()

    return render_template(
        'edit_doctor.html',
        title='Редактирование врача',
        doctor=doctor
    )


@app.route('/delete-doctor/<int:id>')
def delete_doctor(id):
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM doctors WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    add_log(session['user'], 'Удалён врач')
    
    flash('Врач удалён')

    return redirect('/doctors')


@app.route('/patients')
def patients():
    if 'user' not in session:
        return redirect('/login')

    search = request.args.get('search', '')

    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            """
            SELECT * FROM patients
            WHERE full_name LIKE %s
               OR phone LIKE %s
               OR address LIKE %s
            """,
            (
                '%' + search + '%',
                '%' + search + '%',
                '%' + search + '%'
            )
        )
    else:
        cur.execute("SELECT * FROM patients")

    patients = cur.fetchall()

    cur.close()

    return render_template(
        'patients.html',
        title='Пациенты',
        patients=patients,
        search=search
    )


@app.route('/add-patient', methods=['GET', 'POST'])
def add_patient():

    if 'user' not in session:
        return redirect('/login')
    
    if not can_edit():
        return access_denied()

    if request.method == 'POST':

        full_name = request.form['full_name']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO patients(
                full_name,
                birth_date,
                phone,
                address
            )
            VALUES(%s, %s, %s, %s)
            """,
            (
                full_name,
                birth_date,
                phone,
                address
            )
        )

        mysql.connection.commit()

        cur.close()
        
        add_log(session['user'], 'Добавлен пациент')
        
        flash('Пациент успешно добавлен')

        return redirect('/patients')

    return render_template(
        'add_patient.html',
        title='Добавление пациента'
    )

@app.route('/edit-patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    if 'user' not in session:
        return redirect('/login')
    
    if not can_edit():
        return access_denied()

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']

        cur.execute(
            """
            UPDATE patients
            SET
                full_name=%s,
                birth_date=%s,
                phone=%s,
                address=%s
            WHERE id=%s
            """,
            (
                full_name,
                birth_date,
                phone,
                address,
                id
            )
        )

        mysql.connection.commit()

        cur.close()

        add_log(session['user'], 'Изменены данные пациента')
        
        flash('Данные пациента обновлены')

        return redirect('/patients')

    cur.execute(
        "SELECT * FROM patients WHERE id=%s",
        (id,)
    )

    patient = cur.fetchone()

    cur.close()

    return render_template(
        'edit_patient.html',
        title='Редактирование пациента',
        patient=patient
    )

@app.route('/delete-patient/<int:id>')
def delete_patient(id):
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM patients WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    add_log(session['user'], 'Удалён пациент')
    
    flash('Пациент удалён')

    return redirect('/patients')


@app.route('/services')
def services():
    if 'user' not in session:
        return redirect('/login')

    search = request.args.get('search', '')

    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            """
            SELECT * FROM services
            WHERE title LIKE %s OR description LIKE %s
            """,
            (
                '%' + search + '%',
                '%' + search + '%'
            )
        )
    else:
        cur.execute("SELECT * FROM services")

    services = cur.fetchall()

    cur.close()

    return render_template(
        'services.html',
        title='Услуги',
        services=services,
        search=search
    )


@app.route('/add-service', methods=['GET', 'POST'])
def add_service():

    if 'user' not in session:
        return redirect('/login')
    
    if not can_edit():
        return access_denied()

    if request.method == 'POST':

        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO services(
                title,
                price,
                description
            )
            VALUES(%s, %s, %s)
            """,
            (
                title,
                price,
                description
            )
        )

        mysql.connection.commit()

        cur.close()
        
        add_log(session['user'], 'Добавлена услуга')
        
        flash('Услуга успешно добавлена')

        return redirect('/services')

    return render_template(
        'add_service.html',
        title='Добавление услуги'
    )
    

@app.route('/edit-service/<int:id>', methods=['GET', 'POST'])
def edit_service(id):
    if 'user' not in session:
        return redirect('/login')

    if not can_edit():
        return access_denied()

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        cur.execute(
            """
            UPDATE services
            SET title=%s, price=%s, description=%s
            WHERE id=%s
            """,
            (title, price, description, id)
        )

        mysql.connection.commit()

        cur.close()

        add_log(session['user'], 'Изменена услуга')
        
        flash('Услуга обновлена')

        return redirect('/services')

    cur.execute(
        "SELECT * FROM services WHERE id=%s",
        (id,)
    )

    service = cur.fetchone()

    cur.close()

    return render_template(
        'edit_service.html',
        title='Редактирование услуги',
        service=service
    )
    

@app.route('/delete-service/<int:id>')
def delete_service(id):
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM services WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    add_log(session['user'], 'Удалена услуга')
    
    flash('Услуга удалена')

    return redirect('/services')


@app.route('/appointments')
def appointments():
    if 'user' not in session:
        return redirect('/login')

    search = request.args.get('search', '')

    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            """
            SELECT 
                appointments.id,
                doctors.full_name,
                patients.full_name,
                appointments.appointment_date,
                appointments.appointment_time,
                appointments.status
            FROM appointments
            LEFT JOIN doctors ON appointments.doctor_id = doctors.id
            LEFT JOIN patients ON appointments.patient_id = patients.id
            WHERE doctors.full_name LIKE %s
               OR patients.full_name LIKE %s
               OR appointments.status LIKE %s
               OR appointments.appointment_date LIKE %s
            """,
            (
                '%' + search + '%',
                '%' + search + '%',
                '%' + search + '%',
                '%' + search + '%'
            )
        )
    else:
        cur.execute(
            """
            SELECT 
                appointments.id,
                doctors.full_name,
                patients.full_name,
                appointments.appointment_date,
                appointments.appointment_time,
                appointments.status
            FROM appointments
            LEFT JOIN doctors ON appointments.doctor_id = doctors.id
            LEFT JOIN patients ON appointments.patient_id = patients.id
            """
        )

    appointments = cur.fetchall()

    cur.close()

    return render_template(
        'appointments.html',
        title='Записи',
        appointments=appointments,
        search=search
    )


@app.route('/add-appointment', methods=['GET', 'POST'])
def add_appointment():

    if 'user' not in session:
        return redirect('/login')
    
    if not can_edit():
        return access_denied()

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        doctor_id = request.form['doctor_id']
        patient_id = request.form['patient_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        status = request.form['status']

        cur.execute(
            """
            INSERT INTO appointments(
                doctor_id,
                patient_id,
                appointment_date,
                appointment_time,
                status
            )
            VALUES(%s, %s, %s, %s, %s)
            """,
            (
                doctor_id,
                patient_id,
                appointment_date,
                appointment_time,
                status
            )
        )

        mysql.connection.commit()

        cur.close()
        
        add_log(session['user'], 'Создана запись на приём')
        
        flash('Запись успешно создана')

        return redirect('/appointments')

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    cur.close()

    return render_template(
        'add_appointment.html',
        title='Создание записи',
        doctors=doctors,
        patients=patients
    )
    
    
@app.route('/edit-appointment/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    if 'user' not in session:
        return redirect('/login')

    if not can_edit():
        return access_denied()

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        patient_id = request.form['patient_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        status = request.form['status']

        cur.execute(
            """
            UPDATE appointments
            SET doctor_id=%s,
                patient_id=%s,
                appointment_date=%s,
                appointment_time=%s,
                status=%s
            WHERE id=%s
            """,
            (
                doctor_id,
                patient_id,
                appointment_date,
                appointment_time,
                status,
                id
            )
        )

        mysql.connection.commit()

        cur.close()

        add_log(session['user'], 'Изменена запись на приём')
        
        flash('Запись обновлена')

        return redirect('/appointments')

    cur.execute(
        "SELECT * FROM appointments WHERE id=%s",
        (id,)
    )

    appointment = cur.fetchone()

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    cur.close()

    return render_template(
        'edit_appointment.html',
        title='Редактирование записи',
        appointment=appointment,
        doctors=doctors,
        patients=patients
    )


@app.route('/delete-appointment/<int:id>')
def delete_appointment(id):
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM appointments WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    add_log(session['user'], 'Удалена запись на приём')
    
    flash('Запись удалена')

    return redirect('/appointments')


@app.route('/users')
def users():
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()

    return render_template(
        'users.html',
        title='Пользователи',
        users=users
    )
    
    
@app.route('/toggle-user/<int:id>')
def toggle_user(id):
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT status FROM users WHERE id=%s",
        (id,)
    )

    user = cur.fetchone()

    if user[0] == 'active':
        new_status = 'blocked'
    else:
        new_status = 'active'

    cur.execute(
        "UPDATE users SET status=%s WHERE id=%s",
        (new_status, id)
    )

    mysql.connection.commit()

    cur.close()

    add_log(session['user'], 'Изменён статус пользователя')
    
    flash('Статус пользователя изменён')

    return redirect('/users')


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return access_denied()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO users(username, password, role, status)
            VALUES(%s, %s, %s, %s)
            """,
            (
                username,
                password,
                role,
                'active'
            )
        )

        mysql.connection.commit()

        cur.close()

        add_log(session['user'], 'Добавлен пользователь')
        
        flash('Пользователь успешно добавлен')

        return redirect('/users')

    return render_template(
        'add_user.html',
        title='Добавление пользователя'
    )


@app.route('/activity-logs')
def activity_logs():
    if 'user' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT * FROM activity_logs
        ORDER BY id DESC
        """
    )

    logs = cur.fetchall()

    cur.close()

    return render_template(
        'activity_logs.html',
        title='Журнал действий',
        logs=logs
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)