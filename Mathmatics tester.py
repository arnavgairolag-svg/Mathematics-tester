import tkinter as tk
from tkinter import messagebox
import random
import math

# ---------- Main Window ----------
window = tk.Tk()
window.title("✦ CDY Math Tester ✦")
window.geometry("1000x700")
window.configure(bg="#f2f2f8")

# ---------- Global Variables ----------
score = 0
question_count = 0
total_questions = random.randint(8,20)
current_answer = None
questions_list = []
difficulty = "Easy"
grade_level = "1"
canvas_item = None

# ---------- Question Generators ----------
def generate_arithmetic_question(diff, grade):
    if grade in ["1","2"]:
        n1, n2 = random.randint(1,20), random.randint(1,20)
    elif grade in ["3","4"]:
        n1, n2 = random.randint(10,50), random.randint(10,50)
    else:
        n1, n2 = random.randint(10,100), random.randint(5,100)

    if diff=="Easy":
        op = random.choice(["+","-"])
    elif diff=="Medium":
        op = random.choice(["+","-","*"])
    else:
        op = random.choice(["+","-","*","/"])
        if op=="/":
            n2 = random.randint(1,20)
            n1 = n2 * random.randint(1,10)

    question = f"{n1} {op} {n2} = ?"
    answer = round(eval(f"{n1}{op}{n2}"),2)
    return question, answer, None

def generate_word_problem(grade):
    # realistic story problems by grade
    if grade in ["1","2"]:
        n1,n2=random.randint(1,10), random.randint(1,10)
        q=f"Tom has {n1} apples and buys {n2} more. How many apples now?"
        a=n1+n2
    elif grade in ["3","4"]:
        n1,n2=random.randint(10,50), random.randint(5,30)
        q=f"A bus has {n1} seats. {n2} students get on. How many seats are empty?"
        a=n1-n2
    elif grade in ["5","6"]:
        n1,n2=random.randint(20,100), random.randint(5,20)
        q=f"A store sold {n2} items from {n1}. How many left?"
        a=n1-n2
    else:
        n1,n2=random.randint(50,200), random.randint(20,50)
        q=f"A book costs ${n1}. You buy {n2} books. Total cost?"
        a=n1*n2
    return q,a,None

def generate_algebra_question():
    x=random.randint(1,20)
    a=random.randint(1,10)
    b=random.randint(0,10)
    question=f"Solve: {a}x + {b} = {a*x + b}"
    return question,x,None

def generate_geometry_question(grade):
    shape=random.choice(["Square","Rectangle","Triangle","Circle","Cube","Sphere","Pyramid"])
    if shape=="Square":
        side=random.randint(2,10) if grade in ["1","2"] else random.randint(5,20)
        return f"Area of square with side {side}", side*side, ("square",side)
    elif shape=="Rectangle":
        w,h=(random.randint(2,10), random.randint(2,10)) if grade in ["1","2"] else (random.randint(5,20), random.randint(5,20))
        return f"Area of rectangle width {w}, height {h}", w*h, ("rectangle",w,h)
    elif shape=="Triangle":
        b,h=(random.randint(2,10), random.randint(2,10)) if grade in ["1","2"] else (random.randint(5,20), random.randint(5,20))
        return f"Area of triangle base {b}, height {h}", round(0.5*b*h,2), ("triangle",b,h)
    elif shape=="Circle":
        r=random.randint(1,5) if grade in ["1","2"] else random.randint(3,10)
        return f"Area of circle radius {r}", round(math.pi*r*r,2), ("circle",r)
    elif shape=="Cube":
        s=random.randint(2,6) if grade in ["1","2"] else random.randint(4,10)
        return f"Volume of cube side {s}", s**3, ("cube",s)
    elif shape=="Sphere":
        r=random.randint(1,3) if grade in ["1","2"] else random.randint(3,7)
        return f"Volume of sphere radius {r}", round(4/3*math.pi*r**3,2), ("sphere",r)
    else: # Pyramid
        b,h=random.randint(2,5), random.randint(3,6)
        return f"Volume of pyramid base {b}, height {h}", round(1/3*b*b*h,2), ("pyramid",b,h)

def generate_graph_question():
    x1,y1=random.randint(1,10),random.randint(1,10)
    x2,y2=random.randint(1,10),random.randint(1,10)
    return f"Distance between ({x1},{y1}) and ({x2},{y2})?", round(math.sqrt((x2-x1)**2+(y2-y1)**2),2), ("graph",(x1,y1),(x2,y2))

def generate_transformation_question():
    x,y=random.randint(1,10),random.randint(1,10)
    dx,dy=random.randint(1,5),random.randint(1,5)
    return f"Point ({x},{y}) translated by ({dx},{dy}). New coordinates?", (x+dx,y+dy), None

def generate_question(diff,grade):
    if grade in ["1","2","3"]:
        types=["arithmetic","word"]
    elif grade in ["4","5"]:
        types=["arithmetic","word","geometry","algebra"]
    else:
        types=["arithmetic","word","geometry","algebra","graph","transform"]
    q_type=random.choice(types)
    if q_type=="arithmetic": return generate_arithmetic_question(diff,grade)
    if q_type=="word": return generate_word_problem(grade)
    if q_type=="geometry": return generate_geometry_question(grade)
    if q_type=="algebra": return generate_algebra_question()
    if q_type=="graph": return generate_graph_question()
    if q_type=="transform": return generate_transformation_question()

# ---------- Canvas Drawer ----------
def draw_canvas(shape_info):
    canvas.delete("all")
    if not shape_info:
        return
    w,h=int(canvas["width"]),int(canvas["height"])
    cx,cy=w//2,h//2
    if shape_info[0]=="square":
        s=shape_info[1]*20
        canvas.create_rectangle(cx-s//2,cy-s//2,cx+s//2,cy+s//2,fill="#4a47a3")
    elif shape_info[0]=="rectangle":
        rw,rh=shape_info[1]*20,shape_info[2]*20
        canvas.create_rectangle(cx-rw//2,cy-rh//2,cx+rw//2,cy+rh//2,fill="#4a47a3")
    elif shape_info[0]=="triangle":
        b,h=shape_info[1]*20,shape_info[2]*20
        canvas.create_polygon(cx-b//2,cy+h//2,cx+b//2,cy+h//2,cx,cy-h//2,fill="#4a47a3")
    elif shape_info[0]=="circle":
        r=shape_info[1]*20
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="#4a47a3")
    elif shape_info[0]=="cube":
        s=shape_info[1]*20
        canvas.create_rectangle(cx-s//2,cy-s//2,cx+s//2,cy+s//2,fill="#4a47a3")
        canvas.create_line(cx-s//2,cy-s//2,cx-s//2+15,cy-s//2-15,width=2)
        canvas.create_line(cx+s//2,cy-s//2,cx+s//2+15,cy-s//2-15,width=2)
        canvas.create_line(cx+s//2,cy+s//2,cx+s//2+15,cy+s//2-15,width=2)
        canvas.create_line(cx-s//2+15,cy-s//2-15,cx+s//2+15,cy-s//2-15,width=2)
    elif shape_info[0]=="sphere":
        r=shape_info[1]*20
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="#4a47a3")
    elif shape_info[0]=="pyramid":
        b,h=shape_info[1]*20,shape_info[2]*20
        canvas.create_polygon(cx-b//2,cy+h//2,cx+b//2,cy+h//2,cx,cy-h//2,fill="#4a47a3")
    elif shape_info[0]=="graph":
        scale=20
        x1,y1=shape_info[1]
        x2,y2=shape_info[2]
        canvas.create_line(cx,0,cx,h)
        canvas.create_line(0,cy,w,cy)
        canvas.create_oval(cx+x1*scale-4,cy-y1*scale-4,cx+x1*scale+4,cy-y1*scale+4,fill="red")
        canvas.create_oval(cx+x2*scale-4,cy-y2*scale-4,cx+x2*scale+4,cy-y2*scale+4,fill="blue")
        canvas.create_line(cx+x1*scale,cy-y1*scale,cx+x2*scale,cy-y2*scale,width=2)

# ---------- Exam Flow ----------
def start_exam():
    global difficulty, grade_level, total_questions, question_count, score, questions_list, student_name
    difficulty=difficulty_var.get()
    grade_level=grade_var.get()
    student_name=name_entry.get().strip()
    if not student_name:
        messagebox.showwarning("Input Error","Enter your name to start")
        return
    total_questions=random.randint(8,20)
    question_count=0
    score=0
    questions_list=[]
    instruction_window.destroy()
    quiz_window()

def quiz_window():
    global question_label, answer_entry, submit_button, next_button, result_label, canvas
    quiz_win=tk.Toplevel(window)
    quiz_win.title("✦ CDY Math Tester - Quiz ✦")
    quiz_win.geometry("1000x750")
    quiz_win.configure(bg="#f2f2f8")

    tk.Label(quiz_win,text=f"Student: {student_name}",font=("Arial",14,"bold"),bg="#f2f2f8").pack(pady=5)

    canvas=tk.Canvas(quiz_win,width=400,height=300,bg="white",bd=2,relief="ridge")
    canvas.pack(pady=10)

    question_label=tk.Label(quiz_win,text="",font=("Arial",16,"bold"),bg="#f2f2f8")
    question_label.pack(pady=5)

    answer_entry=tk.Entry(quiz_win,font=("Arial",14))
    answer_entry.pack(pady=5)

    submit_button=tk.Button(quiz_win,text="Submit",command=lambda:submit_answer(quiz_win))
    submit_button.pack(pady=10)

    result_label=tk.Label(quiz_win,text="",bg="#f2f2f8")
    result_label.pack(pady=5)

    next_button=tk.Button(quiz_win,text="Next",state="disabled",command=lambda:next_question(quiz_win))
    next_button.pack(pady=10)

    generate_next_question()

def generate_next_question():
    global current_answer, question_count, canvas_item
    if question_count>=total_questions:
        review_window()
        return
    q_text,current_answer,canvas_item=generate_question(difficulty,grade_level)
    questions_list.append({"Question":q_text,"Answer":current_answer,"UserAnswer":None})
    question_label.config(text=f"Q{question_count+1}: {q_text}")
    answer_entry.config(state="normal")
    answer_entry.delete(0,tk.END)
    result_label.config(text="")
    submit_button.config(state="normal")
    next_button.config(state="disabled")
    if canvas_item: canvas.pack(pady=10)
    else: canvas.pack_forget()
    draw_canvas(canvas_item)

def submit_answer(win):
    global score, question_count
    user_input=answer_entry.get().strip()
    if not user_input:
        messagebox.showwarning("Invalid Input","Enter an answer")
        return
    try:
        if isinstance(current_answer, tuple):
            parts=user_input.replace("(","").replace(")","").split(",")
            user_answer=(int(parts[0]),int(parts[1]))
        else:
            user_answer=round(float(user_input),2)
    except:
        messagebox.showwarning("Invalid Format","Enter correct format")
        return
    questions_list[question_count]["UserAnswer"]=user_answer
    if user_answer==current_answer:
        result_label.config(text="✅ Correct!",fg="green")
        score+=1
    else:
        result_label.config(text=f"❌ Wrong! Correct: {current_answer}",fg="red")
    answer_entry.config(state="disabled")
    submit_button.config(state="disabled")
    next_button.config(state="normal")
    question_count+=1

def next_question(win):
    generate_next_question()

def review_window():
    review_win=tk.Toplevel(window)
    review_win.title("✦ Review Answers ✦")
    review_win.geometry("1000x600")
    tk.Label(review_win,text=f"Review your answers, then submit for grading",font=("Arial",14,"bold")).pack(pady=10)
    listbox=tk.Listbox(review_win,width=140)
    listbox.pack(fill="both",expand=True)
    for idx,q in enumerate(questions_list,1):
        ans=q["UserAnswer"] if q["UserAnswer"] is not None else ""
        listbox.insert(tk.END,f"Q{idx}: {q['Question']} | Your: {ans} | Correct: {q['Answer']}")
    tk.Button(review_win,text="Submit for Grading",command=lambda:show_results(review_win)).pack(pady=10)

def show_results(win):
    win.destroy()
    result_win=tk.Toplevel(window)
    result_win.title("✦ Results ✦")
    result_win.geometry("1000x600")
    tk.Label(result_win,text=f"Score: {score}/{total_questions}",font=("Arial",16,"bold")).pack(pady=15)
    listbox=tk.Listbox(result_win,width=140)
    listbox.pack(fill="both",expand=True)
    for idx,q in enumerate(questions_list,1):
        listbox.insert(tk.END,f"Q{idx}: {q['Question']} | Your: {q['UserAnswer']} | Correct: {q['Answer']}")

# ---------- Instruction Window ----------
instruction_window=tk.Toplevel(window)
instruction_window.title("✦ Instructions & Info ✦")
instruction_window.geometry("700x600")
instruction_window.configure(bg="#f2f2f8")

tk.Label(instruction_window,text="✦ CDY Math Tester ✦",font=("Arial",20,"bold"),bg="#f2f2f8",fg="#4a47a3").pack(pady=15)
tk.Label(instruction_window,text="Enter your name, select grade and difficulty to begin",font=("Arial",14),bg="#f2f2f8").pack(pady=5)

tk.Label(instruction_window,text="Name:",font=("Arial",12),bg="#f2f2f8").pack(pady=5)
name_entry=tk.Entry(instruction_window,font=("Arial",14))
name_entry.pack(pady=5)

grade_var=tk.StringVar(value="1")
tk.Label(instruction_window,text="Select Grade:",font=("Arial",12),bg="#f2f2f8").pack(pady=5)
for i in range(1,9):
    tk.Radiobutton(instruction_window,text=f"Grade {i}",variable=grade_var,value=str(i),bg="#f2f2f8").pack()

difficulty_var=tk.StringVar(value="Easy")
tk.Label(instruction_window,text="Select Difficulty:",font=("Arial",12),bg="#f2f2f8").pack(pady=5)
for d in ["Easy","Medium","Hard"]:
    tk.Radiobutton(instruction_window,text=d,variable=difficulty_var,value=d,bg="#f2f2f8").pack()

tk.Button(instruction_window,text="Start Exam",font=("Arial",14,"bold"),bg="#4a47a3",fg="white",command=start_exam).pack(pady=20)

window.mainloop()
