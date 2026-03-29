
# CODSOFT

A collection of Java projects completed as part of the **CodSoft Java Programming Internship**. Each task demonstrates core Java concepts including OOP, file I/O, API integration, and user interaction via the console.

---

## 📁 Project Structure

```
CODSOFT/
├── Task 1/
│   └── GuessingGame.java
├── Task 2/
│   └── StudentGradeCalculator.java
├── Task 3/
│   ├── ATM.java
│   └── BankAccount.java
├── Task 4/
│   └── CurrencyConverter.java
└── Task 5/
    ├── Main.java
    ├── Student.java
    └── StudentManagementSystem.java
```

---

## ✅ Tasks Overview

### Task 1 — Number Guessing Game
**File:** `Task 1/GuessingGame.java`

A console-based guessing game where the player tries to guess a randomly generated number between 1 and 100.

**Features:**
- Random number generation using `java.util.Random`
- Maximum of **7 attempts** per round
- Hints after each wrong guess (too high / too low)
- **Score system** — fewer attempts = higher score
- Multi-round support with a play-again prompt
- Input validation with graceful error handling

---

### Task 2 — Student Grade Calculator
**File:** `Task 2/StudentGradeCalculator.java`

Calculates the total marks, average percentage, and letter grade for a student based on subject-wise input.

**Features:**
- Accepts marks for any number of subjects (out of 100)
- Validates input to ensure marks are within range (0–100)
- Computes average percentage and assigns a letter grade:

| Percentage | Grade |
|------------|-------|
| ≥ 90       | A+    |
| ≥ 80       | A     |
| ≥ 70       | B     |
| ≥ 60       | C     |
| ≥ 50       | D     |
| < 50       | F     |

---

### Task 3 — ATM Interface
**Files:** `Task 3/ATM.java`, `Task 3/BankAccount.java`

Simulates a basic ATM machine with a linked bank account.

**Features:**
- Separate `BankAccount` class managing balance logic
- `ATM` class handles the user interface and menu
- Operations supported:
  - Check Balance
  - Deposit
  - Withdraw (with insufficient funds check)
- Default starting balance: **$1000.00**
- Input validation and clear feedback messages

---

### Task 4 — Currency Converter
**File:** `Task 4/CurrencyConverter.java`

Converts a given amount from one currency to another using live exchange rates fetched from an external API.

**Features:**
- Integrates with [ExchangeRate-API](https://www.exchangerate-api.com/) for real-time rates
- Supports any standard currency code (e.g., USD, EUR, INR, GBP)
- Raw JSON parsing without external libraries
- HTTP connection via `java.net.HttpURLConnection`
- Error handling for invalid currencies and failed API calls

> **Note:** Requires a valid API key in `CurrencyConverter.java` at the `API_KEY` constant.

---

### Task 5 — Student Management System
**Files:** `Task 5/Main.java`, `Task 5/Student.java`, `Task 5/StudentManagementSystem.java`

A full-featured student records management system with persistent file storage.

**Features:**
- Add, remove, search, edit, and display student records
- Each student has: **Name**, **Roll Number**, **Grade**
- Duplicate roll number prevention
- Data persisted to `students.dat` using Java **Serialization** (`ObjectOutputStream` / `ObjectInputStream`)
- Data auto-loads on startup if a save file exists
- Robust input validation and error handling throughout

---

## 🛠️ How to Run

**Prerequisites:** Java JDK 8 or higher installed.

```bash
# Compile
javac Task\ 1/GuessingGame.java

# Run
java -cp Task\ 1 GuessingGame
```

Repeat the same steps for each task folder. For **Task 3**, compile both files together:

```bash
javac Task\ 3/ATM.java Task\ 3/BankAccount.java
java -cp Task\ 3 ATM
```

For **Task 5**, compile all three files:

```bash
javac Task\ 5/Main.java Task\ 5/Student.java Task\ 5/StudentManagementSystem.java
java -cp Task\ 5 Main
```

---

## 🧰 Technologies Used

- **Language:** Java (JDK 8+)
- **Libraries:** Standard Java (`java.util`, `java.io`, `java.net`)
- **External API:** ExchangeRate-API (Task 4)
- **Concepts:** OOP, File I/O, Serialization, HTTP Networking, Exception Handling

---

## 👨‍💻 Author

Developed as part of the **CodSoft Java Internship Program**.

Project work link :
<a href="https://drive.google.com/drive/folders/1gbYNH_W-9n_HWmp5x0QLl3RhXGRCzYDe?usp=drive_link" target="_blank"><b><span style="color:blue;">Check out my Works 👇</span></b></a>

---

