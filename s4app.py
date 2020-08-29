from flask import Flask, render_template, request


#User objet to store user name, password, email and points
class User:
  def __init__(self, uname, pwd, email, points):
    self.uname = uname
    self.pwd = pwd
    self.email = email
    self.points = points
  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)

#activity object to store activity details
class Activity:
  def __init__(self, category, activity, points):
    self.activity = activity
    self.category = category
    self.points = points
  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)

#init Flask server
app = Flask(__name__)

#create list of users
users=[]

#create admin user
admin=User("admin","admin","admin@competewithme.com",0)

#check is username or email already exist in our user list
def is_duplicate(uname,email):
    error=None
    for u in users:
        if u.uname == uname:
           error="Username already taken. Please try again"
        elif u.email == email:
           error="email is used for a differnent account. Please try again"
    return error

#check is username and pwd is in our user list
def is_valid_login(uname,pwd):
    for u in users:
        if u.uname == uname and u.pwd == pwd:
           return True
    return False


#check id password and confirm match
#check if password or username len is less than 4
#check if valid email format
def valid_account(uname,pwd,confirm_pwd,email):
    error=None
    if pwd!=confirm_pwd:
        error='Password does not match. Please try again.'
    elif len(pwd)<4:
        error = 'Password len has to be 4. Please try again.'
    elif len(uname)<4:
        error = 'User name len has to be 4. Please try again.'
    elif uname=="admin":
        error = 'Cannot use admin usename. Please try again.'
    elif email.find('@') == -1 and email.find('.') == -1:
        error = 'Invalid email. Please try again.'
    return error


#handle admin login and match user name and password on post
@app.route('/admin_login', methods=['POST'])
def admin_welcome():
   error = None
   if request.method=="POST": 
      pwd=request.form['pwd']
      uname=request.form['uname']
      if pwd != admin.pwd and uname != admin.uname:
         error = 'Invalid Credentials. Please try again.'
   if error is None:   
      return render_template('admin.html')
   else:
      print(error)
      return render_template('home.html', error=error)

#handle home page
@app.route('/')
def home():
   return render_template('home.html')

#handle user page
@app.route('/user')
def instructions():
   return render_template('user.html')

#handle user login
@app.route('/user_login',methods=['GET', 'POST'])
def user_login():
   error = None
   valid=False
   if request.method== "POST":
      pwd=request.form ['pwd']
      uname=request.form['uname']

      if len(pwd)<4 or len(uname)<4:
         error = 'Invalid user name or password. Please try again.'

      if error is None:
         valid = is_valid_login(uname,pwd)

      if valid is False:
         error = 'Invalid user name or password. Please try again.'
        
   #there is no error go to user.html
   if error is None:
      return render_template('user.html')
   else:
      return render_template('home.html', error=error)


#handle create_account action
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
   error = None
   if request.method=="POST":
      pwd=request.form['pwd']
      uname=request.form['uname']
      confirm_pwd=request.form['confirm_pwd']
      email=request.form['email']
      #validate account
      error = valid_account(uname,pwd,confirm_pwd,email)
      if error is None:
         #check if duplicate
         error = is_duplicate(uname,email)
   if error is None:  
      #create user 
      user=User(uname,pwd,email,0)
      #add user to list
      users.append(user)
      #print users for debug
      for u in users:
          print(u)
      #tell user create accout is successful
      return "<a href=\"/\">User Created Successfull</a>"
   else:
      #on error return error to user
      print(error)
      return render_template('home.html', error=error)




if __name__ == "__main__":
   #start flask web server
   app.run(host='0.0.0.0', port=80, debug=True)
