from flask import Flask,render_template,request,redirect,session
import pandas as pd
import os
import mysql.connector
import joblib
import shap

app = Flask(__name__)
app.secret_key="employee_secret"


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_system",
        charset="utf8"
    )

DATASET_PATH="dataset/employee_layoff_dataset.csv"

def load_model():
    model = joblib.load("model.pkl")
    encoder = joblib.load("encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    cat_cols = joblib.load("cat_cols.pkl")
    num_cols = joblib.load("num_cols.pkl")

    return model, encoder, scaler, cat_cols, num_cols

def read_dataset():
    return pd.read_csv(DATASET_PATH)

@app.route('/',methods=['GET','POST'])
def index():

    return render_template("index.html")

@app.route('/admin',methods=['GET','POST'])
def admin():

    if request.method=='POST':

        username=request.form['username']
        password=request.form['password']

        if username=="admin" and password=="admin":
            session['admin']="admin"
            return redirect('/dashboard')

    return render_template("admin_login.html")

@app.route('/dashboard')
def dashboard():

    if 'admin' not in session:
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM hr_users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction=1")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction=0")
    low_risk = cursor.fetchone()[0]

    if total_predictions > 0:
        retention_rate = round((low_risk / total_predictions) * 100, 2)
    else:
        retention_rate = 0

    cursor.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM predictions
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) DESC
        LIMIT 7
    """)

    rows = cursor.fetchall()

    dates = []
    values = []

    for row in rows[::-1]:
        dates.append(str(row[0]))
        values.append(row[1])

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions,
        high_risk=high_risk,
        retention_rate=retention_rate,
        chart_labels=dates,
        chart_values=values
    )

@app.route('/view_users')
def view_users():

    if 'admin' not in session:
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM hr_users")
    users = cursor.fetchall()

    return render_template("view_users.html", users=users)


@app.route('/train_model')
def train_model():

    if 'admin' not in session:
        return redirect('/admin')

    return render_template("train_model.html")


@app.route('/process1')
def process1():

    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    df_view = df.head(20)

    data = df_view.values.tolist()
    columns = df_view.columns.tolist()

    return render_template(
        'process1.html',
        data=data,
        columns=columns
    )


@app.route('/process2')
def process2():

    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    summary=[]

    for col in df.columns:

        summary.append([
            col,
            df[col].count(),
            str(df[col].dtype)
        ])

    return render_template(
        'process2.html',
        summary=summary
    )

NUMERICAL_FEATURES=[
"Age",
"Total_Work_Experience",
"Years_At_Company",
"Years_In_Current_Role",
"Monthly_Salary",
"Salary_Hike_Percent",
"Work_Life_Balance",
"Job_Satisfaction",
"Environment_Satisfaction",
"Relationship_With_Manager",
"Training_Hours_Last_Year",
"Performance_Rating",
"Distance_From_Home",
"Absenteeism_Rate"
]

CATEGORICAL_FEATURES=[
"Gender",
"Department",
"Job_Role",
"Education_Level",
"Marital_Status",
"Job_Level",
"Overtime",
"Promotion_Last_5_Years",
"Company_Stock_Option"
]

TARGET=["Attrition"]



@app.route('/process3')
def process3():

    if 'admin' not in session:
        return redirect('/admin')

    return render_template(
        'process3.html',
        numerical=NUMERICAL_FEATURES,
        categorical=CATEGORICAL_FEATURES,
        target=TARGET
    )


@app.route('/process4')
def process4():

    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    df = df.head(40)

    data=df.values.tolist()
    columns=df.columns.tolist()

    return render_template(
        'process4.html',
        data=data,
        columns=columns
    )

@app.route('/process5')
def process5():

    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    counts=df['Attrition'].value_counts().to_dict()

    exit_count=counts.get(1,0)
    stay_count=counts.get(0,0)

    return render_template(
        "process5.html",
        exit_count=exit_count,
        stay_count=stay_count
    )

@app.route('/admin_predictions')
def admin_predictions():

    if 'admin' not in session:
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()

    query = """
    SELECT id, username, input_data, prediction, probability, created_at
    FROM predictions
    ORDER BY id DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    return render_template("admin_predictions.html", data=rows)


@app.route('/register', methods=['GET','POST'])
def hr_register():

    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        query = "INSERT INTO hr_users (name,mobile,email,username,password) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(name,mobile,email,username,password))
        db.commit()

        return redirect('/login')

    return render_template('hr_register.html')


@app.route('/login', methods=['GET','POST'])
def hr_login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        query = "SELECT * FROM hr_users WHERE username=%s AND password=%s"
        cursor.execute(query,(username,password))
        user = cursor.fetchone()

        if user:
            session['hr'] = username
            return redirect('/hr_dashboard')

    return render_template('hr_login.html')

@app.route('/hr_dashboard')
def hr_dashboard():

    if 'hr' not in session:
        return redirect('/hr_login')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction=1")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction=0")
    low_risk = cursor.fetchone()[0]

    if total_predictions > 0:
        retention_rate = round((low_risk / total_predictions) * 100, 2)
    else:
        retention_rate = 0

    cursor.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM predictions
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) DESC
        LIMIT 7
    """)

    rows = cursor.fetchall()

    dates = []
    values = []

    for row in rows[::-1]:
        dates.append(str(row[0]))
        values.append(row[1])

    return render_template(
        'hr_dashboard.html',
        total_predictions=total_predictions,
        high_risk=high_risk,
        low_risk=low_risk,
        retention_rate=retention_rate,
        chart_labels=dates,
        chart_values=values
    )

@app.route('/predict', methods=['GET','POST'])
def predict():

    if 'hr' not in session:
        return redirect('/hr_login')

    if request.method == 'POST':

        model, encoder, scaler, cat_cols, num_cols = load_model()
        prediction_type = request.form.get("prediction_type")

        # =====================================
        # 🔵 SINGLE EMPLOYEE
        # =====================================
        if prediction_type == "single":

            data = request.form.to_dict()
            data.pop("prediction_type", None)

            input_df = pd.DataFrame([data])

            # -------- NUMERIC CLEAN --------
            for col in num_cols:
                value = input_df[col].iloc[0]
                try:
                    input_df[col] = float(value)
                except:
                    input_df[col] = 0

            # -------- CATEGORICAL CLEAN --------
            for col in cat_cols:
                val = input_df[col].iloc[0]
                if val == "" or val is None:
                    val = "Unknown"

                val = str(val)

                # 🔥 HANDLE UNKNOWN CATEGORY
                if hasattr(encoder, "categories_"):
                    known = encoder.categories_[cat_cols.index(col)]
                    if val not in known:
                        val = "Unknown"

                input_df[col] = val

            # -------- TRANSFORM --------
            input_df[cat_cols] = encoder.transform(input_df[cat_cols])
            input_df[num_cols] = scaler.transform(input_df[num_cols])

            # -------- PREDICT --------
            pred = model.predict(input_df)[0]
            prob = model.predict_proba(input_df)[0][1]
            prob_percent = round(prob * 100, 2)

            # -------- SHAP --------
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(input_df)

            contributions = dict(zip(input_df.columns, shap_values[1][0]))

            sorted_features = sorted(contributions.items(),
                                     key=lambda x: abs(x[1]),
                                     reverse=True)[:5]

            positive_factors, negative_factors = [], []

            for f, val in sorted_features:
                name = f.replace("_", " ")
                if val > 0:
                    positive_factors.append(name)
                else:
                    negative_factors.append(name)

            # -------- RISK --------
            if prob >= 0.5:
                risk_level = "High Exit Risk"
                result_title = "Employee is likely to LEAVE"
                hr_action = "Salary revision, workload balance, counseling"
            else:
                risk_level = "Low Exit Risk"
                result_title = "Employee will STAY"
                hr_action = "No immediate action required"

            summary = f"{risk_level} detected with {prob_percent}% probability."

            explanation = f"The model predicts {risk_level.lower()} with a probability of {prob_percent}%. "

            if positive_factors:
                explanation += "Risk increasing factors include: " + ", ".join(positive_factors) + ". "

            if negative_factors:
                explanation += "Retention supporting factors include: " + ", ".join(negative_factors) + ". "

            explanation += "These features contributed most using SHAP."

            # -------- SAVE --------
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO predictions (username,input_data,prediction,probability)
                VALUES (%s,%s,%s,%s)
            """, (session['hr'], str(data), int(pred), float(prob)))
            db.commit()

            return render_template(
                "result.html",
                mode="single",
                prediction=pred,
                prob=prob_percent,
                risk_level=risk_level,
                result_title=result_title,
                summary=summary,
                explanation=explanation,
                positive=positive_factors,
                negative=negative_factors,
                hr_action=hr_action
            )

        # =====================================
        # 🟣 BULK EMPLOYEE (FIXED)
        # =====================================
        else:

            file = request.files['file']
            df = pd.read_excel(file)

            # 🔥 GLOBAL CLEAN (IMPORTANT)
            df = df.fillna("Unknown")

            # Ensure all columns exist
            for col in num_cols:
                if col not in df.columns:
                    df[col] = 0

            for col in cat_cols:
                if col not in df.columns:
                    df[col] = "Unknown"

            # Type fix
            for col in num_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            for col in cat_cols:
                df[col] = df[col].astype(str)

            results = []
            explainer = shap.TreeExplainer(model)

            for i in range(len(df)):

                row = df.iloc[[i]].copy()

                # 🔥 SAFE CATEGORY FIX
                for col in cat_cols:
                    val = str(row[col].iloc[0])

                    if hasattr(encoder, "categories_"):
                        known = encoder.categories_[cat_cols.index(col)]
                        if val not in known:
                            val = "Unknown"

                    row[col] = val

                # -------- TRANSFORM --------
                row[cat_cols] = encoder.transform(row[cat_cols])
                row[num_cols] = scaler.transform(row[num_cols])

                pred = model.predict(row)[0]
                prob = model.predict_proba(row)[0][1]
                prob_percent = round(prob * 100, 2)

                # -------- SHAP --------
                shap_values = explainer.shap_values(row)
                contributions = dict(zip(row.columns, shap_values[1][0]))

                sorted_features = sorted(contributions.items(),
                                         key=lambda x: abs(x[1]),
                                         reverse=True)[:5]

                positive, negative = [], []

                for f, val in sorted_features:
                    name = f.replace("_", " ")
                    if val > 0:
                        positive.append(name)
                    else:
                        negative.append(name)

                # -------- RISK --------
                if prob >= 0.5:
                    risk = "High Exit Risk"
                    action = "Salary revision, workload balance, counseling"
                else:
                    risk = "Low Exit Risk"
                    action = "No immediate action required"

                results.append({
                    "id": i+1,
                    "prob": prob_percent,
                    "risk": risk,
                    "summary": f"{risk} with {prob_percent}%",
                    "positive": positive,
                    "negative": negative,
                    "explanation": f"Prediction: {risk} ({prob_percent}%)",
                    "action": action
                })

            return render_template(
                "result.html",
                mode="bulk",
                results=results
            )

    return render_template("predict.html")

@app.route('/history')
def history():

    if 'hr' not in session:
        return redirect('/hr_login')

    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM predictions WHERE username=%s ORDER BY id DESC"
    cursor.execute(query, (session['hr'],))
    rows = cursor.fetchall()

    return render_template("history.html", data=rows)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
