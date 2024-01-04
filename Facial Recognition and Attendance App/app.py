from flask import Flask, render_template, Response
from image_rec import generate_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Dashboard')
def dashboard():
    return render_template('DashBoard.html', title = 'Dashboard')

@app.route('/Logs')
def logs():
    return render_template('Logs.html', title = 'Logs')

@app.route('/Intruders')
def intruders():
    return render_template('Intruders.html', title = 'Intruders')

@app.route('/ManageUsers')
def manageusers():
    return render_template('Manageusers.html', title = 'Manage Users')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
