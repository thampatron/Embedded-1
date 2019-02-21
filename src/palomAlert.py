from flask import Flask, render_template, request, redirect, url_for
import json
import time
from API_network import send, initSender

client = initSender("PalomAlert/run")

#read last status from status.json
def get_status():
    with open("status.json", "r") as f:
        status_dict = json.load(f)
    return status_dict

#read logged events from log.txt
def get_log():
  with open("log.txt") as f:
    content = f.readlines()
  #to remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content] 
  return content

#get relevant information from log to display on Events Log
def get_logStatus(log):
  output = []
  t_output = [] 
  for m_event in log:

    event = json.loads(m_event)
    t_stamp = event["timeStamp"]
  
    #check what changed in the event by comparing event update-time and component update-time
    if time.ctime(event["status"]["compass"]["lastUpdate"]) == t_stamp:
      if event["status"]["compass"]["isOpen"] == 'yes':
        was_open = "opened"
      else :
        was_open = "closed"
      output.append("Door was "+was_open)
      t_output.append(t_stamp)
    elif time.ctime(event["status"]["accelerometer"]["lastIntrusion"]) == t_stamp:
      output.append("Door was shaken ")
      t_output.append(t_stamp)
  return output, t_output
    


app = Flask(__name__)

#route called when "AT HOME?" is changed to update at_home status and turn RUN/HALT the pi
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
    your_list = list(reversed(your_list[(len(your_list)-4):]))

    status = get_status()
    
    last_update = time.ctime(status["lastFileUpdate"])
    temp = status["thermometer"]["temperature"]
   
    is_open = status["compass"]["isOpen"]
  
    log, t_log = get_logStatus(your_list)

    
    return  render_template("paloma.html", temp=temp, is_open=is_open, your_list=log, t_log = t_log , t_open = last_update, at_home=app.at_home, system_status="connected") 

#home route which renders html 
@app.route("/")
def home():
    your_list = get_log()
    status = get_status()
    your_list = list(reversed(your_list[(len(your_list)-4):]))
    last_update = time.ctime(status["lastFileUpdate"])
    temp = status["thermometer"]["temperature"]
    
    is_open = status["compass"]["isOpen"]
    log, t_log = get_logStatus(your_list)
    

    return render_template("paloma.html", temp=temp, is_open=is_open,your_list=log,t_log=t_log,t_open = last_update, at_home=app.at_home, system_status="connected") 


if __name__ == "__main__":
    at_home="no"
    app.at_home=at_home
    app.run(debug=True)




