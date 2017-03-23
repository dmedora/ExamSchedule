from flask import Flask, render_template, request, json
import schedule_table
import pandas as pd
import random

################# NOTES #################
# add alerts for exam schedule conflicts
# 
#########################################


app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.errorhandler(Exception)
def handle_invalid_usage(response):
    return response

@app.route("/showSchedule", methods=["POST"])
def showSchedule():
	# call search function, get values to return
    # exams = []
    # for i in range(0, num_classes)
        # day = request.form["Day" + i]
        # time = request.form["Time" + i]
        # classname = request.form["ClassName" + i]
    #     exams.append(search(day, time, classname))

    day = request.form["Day"]
    time = request.form["Time"]
    classname = request.form["ClassName"]
    exams = []
    for i in range(0, num_classes)
        day = request.form["Day" + i]
        time = request.form["Time" + i]
        exams.append(search(day, time))

    return render_template('schedule.html', exams=exams)

    # return render_template('schedule.htmal', exams=exams)

row_data = schedule_table.main()


covered = {}
def color(s):
    global covered
    boolsq = s != " "
    if boolsq == True:
        if s in covered.keys():
            # print(s, 'COVERED AGAIN')
            return 'background-color: '+ covered[s]
        else:
            # print(s, 'FINDING COLOR AND GIVING TO COVERED')
            colors = ['#BBE3FF', '#ff6347', 'rgb(187,227,255)', 'rgb(220,170,225)', 'rgb(188,255,166)', 
                  'rgb(255,231,166)', 'rgb(139,211,178)', 'rgb(164,195,243)', 'rgb(252,157,145)',
                 'rgb(255,214,163)', 'rgb(205,206,255)', 'rgb(228,215,246)']
            randindex = int(random.random() * len(colors) // 1)
            randcolor = colors[randindex]
            colors.remove(randcolor)
            # print(randcolor, '\n')
            covered[s] = randcolor
            return 'background-color: ' + randcolor + ';'
    else:
        return ''


def search(day, time, classname):
    day = day.replace(",", " ").replace("&", " ").replace(";", " ").split()
    day = day[0]

    if day == "Foreign":
        return (row_data[13][1], row_data[13][3], classname)
    if day == "Econ":
        return (row_data[2][1], row_data[2][3], classname)
    if day == "Chem":
        return (row_data[8][1], row_data[8][3], classname)

    if time == "--":
        raise Exception("OH SHIT YOU DONE FUCKED UP")
    
    for row in row_data:
        if day in row[4] and time in row[4]:
            return (row[1], row[3], classname)
    # easygui.msgbox("Classes filled out incorrectly", title="ERROR")


# @app.route("/signUp", methods=["POST"])
# def signUp():
# 	# read posted values from the UI
# 	_name = request.form["inputName"]
# 	_email = request.form["inputEmail"]
# 	_password = request.form["inputPassword"]

# 	# validate received values
# 	if _name and _email and _password:
# 		return json.dumps({"html":"<span>All fields good!</span>"})
# 	else:
# 		return json.dumps({"html":"<span>Fields not completed.</span>"})

if __name__ == "__main__":
	app.run(debug=True)

