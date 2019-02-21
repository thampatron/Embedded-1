from flask import Flask, render_template, request, redirect, url_for
import json
import time

def get_status():
    with open("status.json", "r") as f:
        status_dict = json.load(f)
    return status_dict



app = Flask(__name__)
@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    if jsdata == "no":
      app.at_home = "yes"
    else:
      app.at_home="no"

    print (app.at_home)
    status = get_status()
    last_update = status["lastFileUpdate"]
    temp = status["thermometer"]["temperature"]
    print(temp)
    is_open = status["compass"]["isOpen"]
    #time_ago = last_update - time.time
    #print(time_ago)
    your_list=["1.20","2.40","3.40"]
    print(app.at_home)
    return  render_template("paloma.html", temp=temp, is_open=is_open,your_list=your_list,  t_open = last_update, at_home=app.at_home, system_status="connected") 

@app.route("/")
def home():
    status = get_status()
    last_update = status["lastFileUpdate"]
    temp = status["thermometer"]["temperature"]
    print(temp)
    is_open = status["compass"]["isOpen"]
    #time_ago = last_update - time.time
    #print(time_ago)
    your_list=["1.20","2.40","3.40"]
    print(app.at_home)
    return render_template("paloma.html", temp=temp, is_open=is_open,your_list=your_list,t_open = last_update, at_home=app.at_home, system_status="connected") # last_update, sysON, #, opendoor, door-shake


def status_change():
    new_status = get_status()
    if new_status is status:
        return False
    return True
status = get_status()

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
    at_home="no"
    app.at_home=at_home
    app.run(debug=True)




