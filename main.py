import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import csv
import os

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game with Leaderboard")
        self.root.geometry("420x500")
        self.root.resizable(False, False)
        
        # Difficulty levels: (lower, upper, attempts)
        self.difficulty_levels = {
            "Easy": (1, 50, 10),
            "Medium": (1, 100, 7),
            "Hard": (1, 500, 5)
        }
        
        # Ensure leaderboard file exists
        self.leaderboard_file = "leaderboard.csv"
        if not os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Score", "Difficulty"])
        
        self.setup_start_screen()

    # ------------------------ UI SCREENS ------------------------

    def setup_start_screen(self):
        """Display difficulty selection and leaderboard buttons."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="🎮 Number Guessing Game", font=("Helvetica", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text="Select Difficulty:", font=("Helvetica", 14)).pack(pady=10)
        
        for level in self.difficulty_levels.keys():
            tk.Button(self.root, text=level, font=("Helvetica", 12), width=10,
                      command=lambda l=level: self.start_game(l)).pack(pady=5)
        
        tk.Button(self.root, text="🏆 View Leaderboard", font=("Helvetica", 12), width=20,
                  command=self.show_leaderboard).pack(pady=20)

    def setup_game_screen(self):
        """Main game UI for guessing."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Difficulty: {self.level}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Guess the number between {self.lower} and {self.upper}",
                 font=("Helvetica", 12)).pack(pady=10)
        
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=5)
        
        self.entry = tk.Entry(self.root, font=("Helvetica", 12), justify='center')
        self.entry.pack(pady=10)
        
        tk.Button(self.root, text="Check Guess", font=("Helvetica", 12, "bold"),
                  command=self.check_guess).pack(pady=5)
        
        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts_left}",
                                       font=("Helvetica", 12))
        self.attempts_label.pack(pady=5)
        
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

    # ------------------------ GAME LOGIC ------------------------

    def start_game(self, level):
        """Initialize game variables for chosen difficulty."""
        self.level = level
        self.lower, self.upper, self.attempts_left = self.difficulty_levels[level]
        self.secret_number = random.randint(self.lower, self.upper)
        self.score = 100
        self.guess_count = 0
        
        self.setup_game_screen()

    def check_guess(self):
        """Validate input, check guess, and update feedback."""
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return
        
        if guess < self.lower or guess > self.upper:
            messagebox.showwarning("Out of Range", f"Enter a number between {self.lower} and {self.upper}.")
            return
        
        self.guess_count += 1
        self.attempts_left -= 1
        
        if guess < self.secret_number:
            self.feedback_label.config(text="📉 Too Low! Try again.")
        elif guess > self.secret_number:
            self.feedback_label.config(text="📈 Too High! Try again.")
        else:
            messagebox.showinfo("🎉 Congratulations!",
                                f"You guessed it right in {self.guess_count} attempts!\nScore: {self.score}")
            self.save_score()
            self.play_again()
            return
        
        # Update score and display
        self.score -= int(100 / self.difficulty_levels[self.level][2])
        self.score_label.config(text=f"Score: {self.score}")
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        
        # If out of attempts
        if self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"😢 Out of attempts! The number was {self.secret_number}.")
            self.play_again()

    # ------------------------ LEADERBOARD ------------------------

    def save_score(self):
        """Prompt for player's name and save score to CSV."""
        name = simpledialog.askstring("Enter Name", "Enter your name for the leaderboard:")
        if not name:
            name = "Anonymous"
        
        with open(self.leaderboard_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, self.score, self.level])

    def show_leaderboard(self):
        """Display leaderboard window."""
        if not os.path.exists(self.leaderboard_file):
            messagebox.showinfo("No Data", "No leaderboard data available yet.")
            return
        
        leaderboard_win = tk.Toplevel(self.root)
        leaderboard_win.title("🏆 Leaderboard")
        leaderboard_win.geometry("400x300")
        leaderboard_win.resizable(False, False)
        
        tk.Label(leaderboard_win, text="Top Scores", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Treeview Table
        columns = ("Name", "Score", "Difficulty")
        tree = ttk.Treeview(leaderboard_win, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(pady=10)
        
        # Load leaderboard data
        with open(self.leaderboard_file, "r") as f:
            reader = csv.DictReader(f)
            data = sorted(reader, key=lambda x: int(x["Score"]), reverse=True)
        
        for row in data[:10]:  # Show top 10 scores
            tree.insert("", tk.END, values=(row["Name"], row["Score"], row["Difficulty"]))

    # ------------------------ REPLAY / EXIT ------------------------

    def play_again(self):
        """Ask to replay or return to start screen."""
        response = messagebox.askyesno("Play Again?", "Do you want to play again?")
        if response:
            self.setup_start_screen()
        else:
            self.root.quit()


# ------------------------ MAIN EXECUTION ------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
