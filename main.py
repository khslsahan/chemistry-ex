from distutils.log import debug
import pymysql
from app import app
from tables import Results ,Experiments
from db_config import mysql
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/new_user')
def add_user_view():
	return render_template('add.html')


@app.route('/new_experiment')
def add_experiment_view():
	return render_template('addExperiment.html' )	

@app.route('/new_experiment_calculated/<value>')
def add_experiment_view_caculated(value):
	return render_template('addExperiment.html',hello=value)	

@app.route('/calculate')
def view_calculate_experiment():
	return render_template('calculation.html',rf_value="")	

@app.route('/tlc_calucation', methods=['POST'])
def calculate_experiment():
	conn = None
	cursor = None
	try:		
		_a_val = request.form['a_val']
		_r_val = request.form['r_val'] 
		# validate the received values
		if _a_val and _r_val   and request.method == 'POST':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# save edits
			rf_value = round(  float(_a_val)/float(_r_val), 4)
			return render_template('calculation.html',rf_value=rf_value)
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		print("N") 	
 

@app.route('/addExperiment', methods=['POST'])
def add_experiment():
	conn = None
	cursor = None
	try:		
		_name = request.form['inputName']
		_calculated_value = request.form['inputCalculatedValue']
		_experiment_date = request.form['inputExperimentDate']
		# validate the received values
		if _name and _calculated_value and _experiment_date and request.method == 'POST':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# save edits
			sql = "insert  into `experiments`(`name`,`calculated_value`,`experiment_date`)  values (%s , %s , %s )"
			data = (_name, _calculated_value, _experiment_date,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('EXPERIMENT added successfully!')
			return redirect('/')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

		
 

@app.route('/')
def experiments():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM  experiments where is_deleted=0;")
		rows = cursor.fetchall()
		table = Experiments(rows)
		table.border = True
		return render_template('experiments.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()




 

@app.route('/editExperiment/<int:id>')
def edit_experiment_view(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM experiments WHERE experiment_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('editExperiment.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


 
		
@app.route('/updateExperiment', methods=['POST'])
def update_experiment():
	conn = None
	cursor = None
	try:		
		_name = request.form['inputName']
		_calculated_value = request.form['inputCalculatedValue']
		_experiment_date = request.form['inputExperimentDate']
		_id = request.form['id']
		# validate the received values
		if _name and _calculated_value and _experiment_date and _id and request.method == 'POST':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# print(_hashed_password)
			# save edits  `name`,`calculated_value`,`experiment_date`
			sql = "UPDATE experiments SET name=%s, calculated_value=%s, experiment_date=%s WHERE experiment_id=%s"
			data = (_name, _calculated_value, _experiment_date, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Experiment updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

 
		
@app.route('/deleteExperiment/<int:id>')
def delete_experiment(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM experiments WHERE experiment_id=%s", (id,))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


if __name__ == "__main__":
    app.run(port=5005,debug=True)