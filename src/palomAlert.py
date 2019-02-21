from flask import Flask, render_template, request, redirect, url_for
import json
import time
from API_network import send, initSender



client = initSender("PalomAlert/run")

def get_status():
    with open("status.json", "r") as f:
        status_dict = json.load(f)
    return status_dict

def get_log():
  with open("log.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace 
# characters like `\n` at the end of each line
  content = [x.strip() for x in content] 
  return content

def get_logStatus(log):
  output = []
  t_output = [] 
  for m_event in log:

    event = json.loads(m_event)
    t_stamp = event["timeStamp"]
    
    if time.ctime(event["status"]["compass"]["lastUpdate"]) == t_stamp:
      if event["status"]["compass"]["isOpen"] == 'yes':
        was_open = "opened"
      else :
        was_open = "closed"
      output.append("Door was "+was_open)
      t_output.append( t_stamp)
    elif time.ctime(event["status"]["accelerometer"]["lastIntrusion"]) == t_stamp:
      output.append("Door was shaken ")
      t_output.append(t_stamp)
  return output, t_output
    


app = Flask(__name__)
@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    if jsdata == "no":
      app.at_home = "yes"
      send(client, None, "PalomAlert/halt", qos=2)
    else:
      app.at_home="no"
      send(client, None, "PalomAlert/run", qos=2)


    your_list = get_log()
    print(your_list[0])
    your_list = your_list[:3]


    print (app.at_home)
    status = get_status()
  
    
    last_update = status["lastFileUpdate"]
    temp = status["thermometer"]["temperature"]
    print(your_list)
    is_open = status["compass"]["isOpen"]
    #time_ago = last_update - time.time
    #print(time_ago)
    log, t_log = get_logStatus(your_list)

    print(app.at_home)
    return  render_template("paloma.html", temp=temp, is_open=is_open,your_list=log,t_log = t_log , t_open = last_update, at_home=app.at_home, system_status="connected") 

@app.route("/")
def home():
    your_list = get_log()
    status = get_status()
    your_list = your_list[:3]
    last_update = status["lastFileUpdate"]
    temp = status["thermometer"]["temperature"]
    print(your_list)
    is_open = status["compass"]["isOpen"]
    log, t_log = get_logStatus(your_list)
    #time_ago = last_update - time.time
    #print(time_ago)
   
    print(app.at_home)
    return render_template("paloma.html", temp=temp, is_open=is_open,your_list=log,t_log=t_log,t_open = last_update, at_home=app.at_home, system_status="connected") # last_update, sysON, #, opendoor, door-shake


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




