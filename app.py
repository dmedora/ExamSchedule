from flask import Flask, render_template, request, json
import schedule_table

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
    exams = []
    for i in range(0, num_classes)
        day = request.form["Day" + i]
        time = request.form["Time" + i]
        exams.append(search(day, time))

    return render_template('schedule.html', exams=exams)

row_data = schedule_table.main()



def search(day, time):
    day = day.replace(",", " ").replace("&", " ").replace(";", " ").split()
    day = day[0]

    if day == "Foreign":
        return (row_data[13][1], row_data[13][3])
    if day == "Econ":
        return (row_data[2][1], row_data[2][3])
    if day == "Chem":
        return (row_data[8][1], row_data[8][3])

    for row in row_data:
        if day in row[4] and time in row[4]:
            return (row[1], row[3])




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

