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
    exams.append(search(day, time, classname))
        
    df = pd.DataFrame(index = ["8-11am", "11:30-2:30pm", "3-6pm", "7-10pm"], columns = ["Mon", "Tues", "Weds", "Thurs", "Fri"]).fillna(" ")
    for exam_tup in exams:
        df.loc[exam_tup[1], exam_tup[0]] = classname
    df.columns = ["Mon 5/8", "Tues 5/9", "Weds 5/10", "Thurs 5/11", "Fri 5/12"]
    df.style.apply(color)
    return render_template("schedule.html", name=showSchedule, data=df.to_html())

    # return render_template('schedule.htmal', exams=exams)

row_data = schedule_table.main()


def color(s):
    boolcol = s != " "
    colors = ['#BBE3FF', '#ff6347', '187,227,255', '220,170,225', '188,255,166', '255,231,166', '252,226,226', ]
    randindex = random.random() * len(colors) // 1
    randcolor = colors[randindex]
    colors.remove(randcolor)
    return ['background-color:' + randcolor if v else '' for v in boolcol]


def search(day, time, classname):
    day = day.replace(",", " ").replace("&", " ").replace(";", " ").split()
    day = day[0]

    if day == "Foreign":
        return (row_data[13][1], row_data[13][3], classname)
    if day == "Econ":
        return (row_data[2][1], row_data[2][3], classname)
    if day == "Chem":
        return (row_data[8][1], row_data[8][3], classname)

    for row in row_data:
        if day in row[4] and time in row[4]:
            return (row[1], row[3], classname)




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

