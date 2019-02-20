from flask import Flask, render_template, request
import json
import time
import datetime

def get_status():
    with open("status.json", "r") as f:
        status_dict = json.load(f)
    return status_dict

home_status = True

app = Flask(__name__)

@app.route("/")
def home():
    status = get_status()
    last_update = status["lastFileUpdate"]
    temp = status["thermometer"]["temperature"]


    is_open = status["compass"]["isOpen"]
    t_open = status["lastFileUpdate"]
    t = int(time.time()) - int(t_open)
    t_open = datetime.timedelta(seconds=t)
    shaker = status["accelerometer"]["isShook"]
  

    #time_ago = last_update - time.time
    #print(time_ago)
    return render_template("paloma.html", temp=temp, t_open= t_open, is_open=is_open, shake=shaker,home_status= home_status, system_status="connected")

@app.route('/home', methods=['POST'])
def update_home_status():
    if(home):
        home = False
    else:
        home = True
    return render_template("paloma.html", temp=temp, t_open= t_open, is_open=is_open, shake=shaker,home_status= home_status, system_status="connected")

@app.route('/home', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    print("HELLOOOOO")
    if request.method == 'GET':
        """return the information for <user_id>"""
          
    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        # you can use <user_id>, which is a str but could
        # changed to be int or whatever you want, along
        # with your lxml knowledge to make the required
        # changes
        data = request.form # a multidict containing POST data   
        print("HELLOOOOO")
    if request.method == 'DELETE':
        """delete user with ID <user_id>""" 
    
        # POST Error 405 Method Not Allowed
#def status_change():        
#    new_status = get_status()
#    if new_status is status:
#        return False
#    return True

#print(status)
#starttime=time.time()
#stat_change = status_change()
#while True:
 # if(stat_change):
  #    home()
    #new_status = get_status()
    #temp = new_status["thermometer"]["temperature"]
    #status=get_status()
    #return render_template("paloma.html", temp=temp)
  #app = AppReloader(get_app)
  #time.sleep(30.0 - ((time.time() - starttime) % 30.0))


if __name__ == "__main__":
    app.run(debug=True)




