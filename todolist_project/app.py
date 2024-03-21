from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime as dt
import json
from database import Database

app = Flask(__name__ , template_folder='templates')
dbo = Database()

ls = dbo.get_data()


# home
@app.route('/')
def index():
    return render_template('index.html',message=ls)


#adding item in the list
@app.route('/add', methods = ['post'])
def add():
    #list of task items from ls dic items
    # getting the value of task field using below code line
    #if list is empty this will result in empty dic_task
    dic_task = [i['Task'] for i in ls]

    todo = request.form.get('item').strip().capitalize()
    date = request.form.get('date')
    cur_date = dt.now().date()
    due_date = dt.strptime(date,'%Y-%m-%d').date()
    # rem_days = (due_date - cur_date).days

    if todo == "":
        return render_template('index.html',error='enter valid text',message = ls)

    elif todo in dic_task:
        return render_template('index.html', info= f'text already exist',message = ls)

    else:
        item = {'Task':todo,'Status':False,'Date':date,'Due_date':str(due_date)}
        ls.append(item)
        dbo.create_data(item)
        return render_template('index.html',confirm = 'added', message = ls)


@app.route('/edit/<int:index0>', methods=['POST', 'GET'])
def edit(index0):
    #for edit form values to function as per case
    if request.method == 'POST':

        updated_item = request.form.get('updated_item').strip().capitalize()
        date = request.form.get('updated_date')

        dic_lst = [i['Task'] for i in ls]

        #need to defined item and index in all conditional cases otherwise when it will redirect to edit.html it wont have any value for them

        if updated_item == dic_lst[index0]:
            return render_template('edit.html', info2='No changes made', index0=index0, item=ls[index0]['Task'])

        #using list of dictionary
        elif updated_item in dic_lst:
            return render_template('edit.html', info2=f'Task already exists', index0=index0, item=ls[index0]['Task'])

        elif updated_item == "":
            return render_template('edit.html', error2='Enter valid text', index0=index0, item=ls[index0]['Task'])

        else:
            ls[index0]['Task'] = updated_item
            ls[index0]['Status'] = False
            return redirect('/')
    else:
        #for edit button to get values for edit form using GET method
        return render_template('edit.html', index0=index0, item=ls[index0]['Task'])

@app.route('/delete/<int:index0>',methods=['GET'])
def delete(index0):
    task = ls[index0]
    ls.remove(task)
    return render_template('index.html', message=ls, confirm='task deleted' )

@app.route('/done/<int:index0>', methods=['GET'])
def done(index0):
    ls[index0]['Status'] = not ls[index0]['Status']
    dbo.done_data(index0)

    if ls[index0]['Status']:
        return render_template('index.html',message=ls, confirm='task completed')
    else:
        return render_template('index.html', message=ls, confirm='task unchecked')







app.run(debug=True, port=5001 )
