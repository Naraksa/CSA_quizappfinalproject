import sqlite3
from tkinter import *
from tkinter import messagebox

def create_db():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            attempts INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

class QuizAppLogin:
    def __init__(self, root):
        self.root = root
        self.current_user_id = None
        self.username_entry = None
        self.password_entry = None
        self.quiz_app = None 

    def show_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Login")
        self.root.config(bg="#1e2a47")  

        Label(self.root, text="Login", font=("Helvetica", 26, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=30)

        Label(self.root, text="Username", font=("Helvetica", 14), fg="#ffffff", bg="#1e2a47").pack(pady=10)
        self.username_entry = Entry(self.root, font=("Helvetica", 14), bd=2, relief="solid", width=25)
        self.username_entry.pack(pady=10)

        Label(self.root, text="Password", font=("Helvetica", 14), fg="#ffffff", bg="#1e2a47").pack(pady=10)
        self.password_entry = Entry(self.root, show="*", font=("Helvetica", 14), bd=2, relief="solid", width=25)
        self.password_entry.pack(pady=10)

        Button(self.root, text="Login", command=self.login_user, font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=20)
        Button(self.root, text="Register", command=self.show_register_window, font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=10)

    def show_register_window(self):
        register_window = Toplevel(self.root)
        register_window.title("Register")
        register_window.config(bg="#1e2a47") 

        Label(register_window, text="Register", font=("Helvetica", 26, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=30)

        Label(register_window, text="Username", font=("Helvetica", 14), fg="#ffffff", bg="#1e2a47").pack(pady=10)
        self.username_entry = Entry(register_window, font=("Helvetica", 14), bd=2, relief="solid", width=25)
        self.username_entry.pack(pady=10)

        Label(register_window, text="Password", font=("Helvetica", 14), fg="#ffffff", bg="#1e2a47").pack(pady=10)
        self.password_entry = Entry(register_window, show="*", font=("Helvetica", 14), bd=2, relief="solid", width=25)
        self.password_entry.pack(pady=10)

        Button(register_window, text="Register", command=self.register_user, font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=20)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists!")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        conn.close()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.current_user_id = user[0]
            conn.close()

            for widget in self.root.winfo_children():
                widget.destroy()

            self.quiz_app = QuizApp(self.root, self.current_user_id)
            self.quiz_app.show_category_page()
        else:
            messagebox.showerror("Error", "Invalid login credentials!")
        conn.close()

class QuizApp:
    def __init__(self, root, current_user_id):
        self.root = root
        self.current_user_id = current_user_id
        self.current_question = 0
        self.user_score = 0
        self.category_frame = None

    question_data = {
        "Grammar": {
            "Paper 1": [
                ("What is the past tense of go?", ["went", "gone", "goed", "going"]),
                ("Which sentence is correct?", ["She go to school", "She goes to school", "She gone to school", "She going to school"]),
                ("We saw____children in the park.", ["any", "some","much","a"]),
                ("I_____tennis every Sunday morning", ["playing", "play","am playing","am play"]),
                ("Do not make so much noise. Dara_____to study for his final exam.", ["try", "tries","tired","is trying"])
            ],
            "Paper 2": [
                ("Which is correct?", ["I can do it", "I can doing it", "I can did it", "I can to do it"]),
                ("Which is the proper form?", ["He is playing", "He play", "He played", "He playeded"]),
                ("I don't understand______your job. So suddenly, why did you do that?", ["your quitting", "you have to quit","to quit","you quit"]),
                ("Tykea_____his teeth before breakfast every morning.", ["will clean", "is cleaning","clean","cleans"]),
                ("The car_______start this morning, so I was late for work.", ["couldn't", "wouldn't","shouldn't","doesn't"])
            ],
            "Paper 3": [
                ("If it does not stop raining, the roads_____", ["have beeen flooded", "would be have flooded", "would be flooded", "will be flooded"]),
                ("I feel tired because I_______for hours.", ["was working", "am working", "have been working", "has worked"]),
                ("Let's go out for dancing,______.", ["are we", "do not we","will we","shall we"]),
                ("Do you know the man________sits next to you?", ["whom", "whose","who","which"]),
                ("My brother and I_______hard to suppout our family ever since we were children.", ["have worked", "work","were working","worked"])
            ],
            "Paper 4": [
                ("Our town has two cinemas, but it_______have a theater.", ["don't", "doesn't", "haven't", "hasn't"]),
                ("Our weather is cloud in the winter. We don't have______.", ["many sunshine", "many sunshines", "much sunshine", "much sunshines"]),
                ("Knowingg serveral_________helpful if you work for an international corporation.", ["languages are", "language is","languages is","language are"]),
                ("Computers can be used in stores to check inventory and tell the store which products are selling well and which are______.", ["less popular", "less popularly","leastly popular","as popular as"]),
                ("In small companies, the same human resource workers may interview and hire as well as________employees.", ["training", "train","to train","they train"])
            ],
            "Paper 5": [
                ("Samnang works in the post office,________?", ["is he", "isn't he", "works he", "doesn't he"]),
                ("My father_______in that firm from 1975 to 1989. Now he's retired.", ["has worked", "worked", "is working", "had worked"]),
                ("Which sentence is the correct one?", ["I am a cold", "I've catched a cold","I have cold","I have caught a cold"]),
                ("I_________on the bench in the park when they ran past me.", ["was sitting", "have sat","sat","was sat"]),
                ("Thida________to the cinema if you went with her.", ["will go", "would go","goes","went"])
            ],
        },
        "Vocabulary": {
            "Paper 1": [
                ("Choose the correct word: 'I feel _____ today.'", ["happy", "happiness", "happily", "happier"]),
                ("Which word is a synonym of quick?", ["fast", "slow", "delayed", "late"]),
                ("At______time thereis always plenty of work to do on a farm.", ["production", "profit", "plant", "harvest"]),
                ("It is against the_______not to wear seat bests in a plan.", ["rule", "regulation", "law", "order"]),
                ("Everything in the sale has been_______to half price.", ["reduced", "decreased", "bargained", "lowered"])
            ],
            "Paper 2":[
                ("We had a perfect view from the plane because the skies were_______", ["empty", "cloudy", "open", "clear"]),
                ("The path was very_____because of the wet weather.", ["stony", "muddy", "sandy", "dusty"]),
                ("It's always a good idea to______clothes before you buy them.", ["put", "hang","take","try"]),
                ("I hate doing the______, especially cleaning the windows.", ["homework", "employment","jobs","housework"]),
                ("Most people in the town______the idea of green and clean city.", ["agree", "approve","support","believe"])
            ],
            "Paper 3": [
                ("She never really________her parents for not having allowed her to go to university.", ["forgave", "forgot", "pardoned", "excused"]),
                ("My parents often does_____with people from Korea.", ["affairs", "finances", "economy", "business"]),
                ("Is it possible to______now for next term's evening class?", ["participate", "join in","enroll","enter"]),
                ("______the national election is conducted this year, the Grade 9 national examination won't be delayed.", ["Unless", "If","If not","Even if"]),
                ("My work's got worse and worse. Unless I_____I'll fail mmy exams in the end of the year.", ["improve", "get well","increase","get back"])
            ],
            "Paper 4": [
                ("What is the opposite of difficult?", ["easy", "hard", "complicated", "complex"]),
                ("Which of the following means to speak in a low voice?", ["whisper", "shout", "yell", "speak"]),
                ("I_______ to inform you that your grandmother died ten minutes ago.", ["apologise", "sorry", "pity", "regret"]),
                ("We were unable to reach an agreement because of the_____between the two groups.", ["contact", "concern", "connection", "conflict"]),
                ("I saw a nasty_______between two cars this morning.", ["damage", "danger", "accident", "happening"])
            ],
            "Paper 5": [
                ("We see each other at regular_______, usually about once a month.", ["breaks", "times", "schedules", "intervals"]),
                ("The building of New Dam will______thousands of people who live in this area.", ["replace", "misplace", "displace", "place"]),
                ("The commander ordered his army to________fire.", ["stop", "put off", "discontinue", "cease"]),
                ("He was an entertaining travelling________.", ["friend", "companion", "partner", "male"]),
                ("The weather was great, it was really_______.", ["strong sun", "sunshine", "sun", "sunny"])
            ],
        }
    }

    answer_data = {
        "Grammar": {
            "Paper 1": ["went", "She goes to school", "some", "play", "is trying"],
            "Paper 2": ["I can do it", "He is playing", "your quitting", "cleans", "wouldn't"],
            "Paper 3": ["will be flooded", "have been working", "shall we", "who", "have worked"],
            "Paper 4": ["doesn't", "much sunshine", "language is", "less popular", "train"],
            "Paper 5": ["doesn't he", "worked", "I have caught a cold", "was sitting", "would go"]
        },
        "Vocabulary": {
            "Paper 1": ["happy", "fast", "harvest", "law", "reduced"],
            "Paper 2": ["clear", "muddy", "try", "housework", "support"],
            "Paper 3": ["forgave", "business", "enroll", "unless", "improve"],
            "Paper 4": ["easy", "whisper", "regret", "conflict", "accident"],
            "Paper 5": ["intervals", "displace", "cease", "companion", "sunny"]

        }
    }

    def show_category_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.category_frame = Frame(self.root, bg="#1e2a47")
        self.category_frame.pack(fill=BOTH, expand=True)

        Label(self.category_frame, text="Choose Category", font=("Helvetica", 26, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=50)

        Button(self.category_frame, text="Vocabulary", command=lambda: self.show_paper_selection("Vocabulary"), font=("Helvetica", 18, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=20)
        Button(self.category_frame, text="Grammar", command=lambda: self.show_paper_selection("Grammar"), font=("Helvetica", 18, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=20)

    def show_paper_selection(self, category):
        for widget in self.category_frame.winfo_children():
            widget.destroy()

        Label(self.category_frame, text=f"Choose Paper for {category}", font=("Helvetica", 26, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=50)

        for paper in self.question_data[category]:
            Button(self.category_frame, text=paper, command=lambda p=paper, c=category: self.start_quiz(p, c), font=("Helvetica", 18, "bold"), bg="#557a95", fg="white", relief="raised", width=20).pack(pady=20)


    def start_quiz(self, paper, category):
        self.current_question = 0
        self.user_score = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        quiz_window = Frame(self.root, bg="#1e2a47")
        quiz_window.pack(fill=BOTH, expand=True)

        self.load_question(quiz_window, category, paper)

    def load_question(self, quiz_window, category, paper):
        if self.current_question < len(self.question_data[category][paper]):
            question_text, options = self.question_data[category][paper][self.current_question]

            for widget in quiz_window.winfo_children():
                widget.destroy()

            Label(quiz_window, text=f"Question: {question_text}", font=("Helvetica", 18, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=10)

            user_answer = StringVar()

            for option in options:
                Radiobutton(quiz_window, text=option, variable=user_answer, value=option, font=("Helvetica", 14), bg="#1e2a47", fg="white", activebackground="#557a95", activeforeground="white").pack(anchor=W, padx=100, pady=5)

            Button(quiz_window, text="Submit", command=lambda: self.check_answer(quiz_window, category, paper, user_answer.get()), font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised").pack(pady=20)

        else:
            self.show_result(quiz_window, category)


    def check_answer(self, quiz_window, category, paper, answer):
        correct_answer = self.answer_data[category][paper][self.current_question]
        if answer == correct_answer:
            self.user_score += 1
        self.current_question += 1
        self.load_question(quiz_window, category, paper)

    def show_result(self, quiz_window, category):
        for widget in quiz_window.winfo_children():
            widget.destroy()

        percentage_score = (self.user_score / len(self.question_data[category])) * 100

        if percentage_score >= 80:
            feedback = "Great job! You really know your stuff!"
        elif percentage_score >= 50:
            feedback = "Good effort! Keep practicing to improve!"
        else:
            feedback = "Keep trying! Don't give up, you'll get better with practice!"

        Label(quiz_window, text=f"You scored {self.user_score}/{len(self.question_data[category])} ({percentage_score:.2f}%)", font=("Helvetica", 26, "bold"), fg="#f7f7f7", bg="#1e2a47").pack(pady=50)
        Label(quiz_window, text=feedback, font=("Helvetica", 18), fg="#f7f7f7", bg="#1e2a47").pack(pady=20)

        Button(quiz_window, text="Back to Categories", command=self.show_category_page, font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised").pack(pady=20)
        
        Button(quiz_window, text="Exit", command=self.exit_app, font=("Helvetica", 16, "bold"), bg="#557a95", fg="white", relief="raised").pack(pady=20)

    def exit_app(self):
        self.root.quit()

root = Tk()
root.title("Slay BacE")
root.geometry("850x520")
root.config(bg="#1e2a47")

create_db()
login_app = QuizAppLogin(root)
login_app.show_login_window()
root.mainloop()
