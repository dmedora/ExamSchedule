from flask import Flask, render_template, request, json
import schedule_table
import pandas as pd
import random

################# NOTES ##################
# add alerts for exam schedule conflicts #
##########################################

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/showSchedule", methods=["GET"])
def refreshGet():
    return render_template('index.html')

@app.errorhandler(Exception)
def handle_invalid_usage(response):
    return response

@app.errorhandler(404)
def not_found(e):
    return Response('Page not found!')

@app.route("/showSchedule", methods=["POST"])
def showSchedule():
    exams = []
    num_vals = len(request.form)
    form_vals = []

    i = 0
    while (3*i) < (num_vals - 1): # -1 to exclude the submit button
        temp_name = request.form["ClassName" + str(i)] # works fine
        temp_day = request.form["Day" + str(i)] # don't work fine
        temp_time = request.form["Time" + str(i)]

        temp_trio = (temp_name, temp_day, temp_time)
        form_vals.append(temp_trio)
    
        i += 1

    for triplet in form_vals:
        try:
            toappend = search(triplet[1], triplet[2], triplet[0])
        except Exception as e:
            # return render_template('test_page.html', test_var=e)
            return render_template('index.html', error="Classes filled out incorrectly")

        exams.append(toappend)
        exams = [val for val in exams if val != None]

    # to handle exams at the same time
    seen = [None for i in range(0, len(exams))]
    for i in range(0, len(exams)):
        flag = False
        for j in range(0, len(seen)):
            if (seen[j] != None) and (exams[i][0] == seen[j][0] and exams[i][1] == seen[j][1]):
                if "Time conflict" in seen[j][2]:
                    seen[j][2] = seen[j][2] + " / " + exams[i][2]
                else: 
                    seen[j][2] = "Time conflict: " + seen[j][2] + " / " + exams[i][2]
                flag = True
                break
                
        if flag == False:
            seen[i] = list(exams[i]) #because outside loop... 


    exams = [val for val in seen if val != None]

    df = pd.DataFrame(index = ["8-11am", "11:30-2:30pm", "3-6pm", "7-10pm"], columns = ["Mon", "Tues", "Weds", "Thurs", "Fri"]).fillna(" ")
    for exam_tup in exams:
        # df.loc[exam_tup[1], exam_tup[0]] = classname
        df.loc[exam_tup[1], exam_tup[0]] = exam_tup[2]
    df.columns = ["Mon 5/8", "Tues 5/9", "Weds 5/10", "Thurs 5/11", "Fri 5/12"]
    # df.style.applymap(color)

    return render_template("index.html", data=df.style.applymap(color).render())
    # return render_template("schedule.html", name=showSchedule, data=df.style.applymap(color).render())

    ############################################
    

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

    if time == "--" and day == "--":
        return None
    
    for row in row_data:
        if day in row[4] and time in row[4]:
            return [row[1], row[3], classname]
    # easygui.msgbox("Classes filled out incorrectly", title="ERROR")


# @app.route("/signUp", methods=["POST"])
# def signUp():
#   # read posted values from the UI
#   _name = request.form["inputName"]
#   _email = request.form["inputEmail"]
#   _password = request.form["inputPassword"]

#   # validate received values
#   if _name and _email and _password:
#       return json.dumps({"html":"<span>All fields good!</span>"})
#   else:
#       return json.dumps({"html":"<span>Fields not completed.</span>"})

if __name__ == "__main__":
    app.run(debug=True)



#################### SCRAPYARD ####################
    # for i in range(0, len(request.form)+1):
    #     day = request.form["Day" + i]
    #     time = request.form["Time" + i]
    #     classname = request.form["ClassName" + i]
    #     exams.append(search(day, time, classname))

    # day = request.form["Day0"]
    # time = request.form["Time0"]
    # classname = request.form["ClassName0"]

    # original working try-except
    # try:
    #     toappend = search(day, time, classname)
    # except Exception as e:
    #     return render_template('index.html', error = "Classes filled out incorrectly")
    # exams.append(toappend)


    # except Exception as e:
    #     # list index out of range... 
    #     return render_template('test_page.html', test_var=e, test2=exams, test3=seen)
    # # return render_template('test_page.html', test2=exams, test3=seen)


