from flask import *
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hp7584*529903*",
    database="web"
)

mycursor = mydb.cursor()


def get_key(dict, pkey):
    values = []
    for key, value in dict.items():
        if pkey == value:
            values.append(int(key) - 1)
    return values


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("index.html")


@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    mycursor.execute("SELECT nota FROM tareas WHERE usuario='root' ")
    result = mycursor.fetchall()
    tasks = [i[0] for i in result]
    if request.method == "POST":
        values = request.form.to_dict()
        if "bt_add" in request.form:
            sql = "INSERT INTO tareas (usuario, nota) VALUES (%s, %s)"
            val = ("root", values["task_to_add"])
            mycursor.execute(sql,val)
        else:
            keys = get_key(values, "on")
            for index in keys:
                del_val = tasks[index]
                mycursor.execute(f"DELETE FROM tareas WHERE nota='{del_val}'")
        mydb.commit()
        return redirect(url_for("tareas"))
    else:
        return render_template("Tareas.html", tasks=tasks)


def main():
    mycursor.execute("SELECT nota FROM tareas WHERE usuario='root' ")
    result = mycursor.fetchall()
    tasks = []
    for i in result:
        tasks.append(i[0])


if __name__ == '__main__':
    app.run(debug=True)
    # main()
