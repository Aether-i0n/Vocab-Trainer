# 🧠 Vocab Trainer

Vocab Trainer is a customizable, console-based vocabulary revision tool built in Python. It allows you to practice foreign language vocabulary in both directions, save your progress between sessions, and review mistakes until mastery. 

Designed for **flexibility and structure**, it supports:
- Multiple vocabulary files across folders
- Random/reverse questioning
- Progress tracking
- Full terminal interface with colors and menus

---

## 📁 Project Structure

```
vocab-trainer/
├── main.py                  # Entry point: choose file,
│                            start quiz
│
├── trainer.py               # Quiz engine and logic
│
├── utils.py                 # Utility functions (file
│                            search, input, formatting)
│
├── vocab/                   # Your vocab sets (organized
│   ├── french/              freely in folders)
│   │   └── colors.json
│   └── japanese/
│       └── greetings.json
├── data/                    # Generated on use; saves
│   ├── french/              progress & history
│   │   │
│   │   ├── colors_progress.json
```

---

## 🗂️ Vocab File Format

Each file is a `.json` file structured like this:

```json
{
    "languages": ["en", "fr"],
    "vocab": [
    [["the media"], ["les médias"]],
    [["journalism"], ["le journalisme"]],
    [["Artificial Intelligence", "AI"], ["l'Intelligence Artificielle", "l'IA"]]
  ]
}
```

You can structure vocab folders freely (e.g., by topic, language, difficulty).

---

## 🚀 How to Use

### 1. ✅ Set up
Make sure you have Python 3.7+ installed. Clone or download the repo:

```bash
git clone https://github.com/yourname/vocab-trainer.git
cd vocab-trainer
```

Install dependencies (only uses standard libraries unless color libs added).

### 2. 🧠 Add your vocab

Create your vocab files inside the `vocab/` folder. You can organize them as:

```
vocab/
├── spanish/
│   └── food.json
├── japanese/
│   └── verbs/basic.json
```

Each file must match the JSON format shown above.

### 3. ▶️ Run the trainer

Launch the tool with:

```bash
python main.py
```

You’ll be presented with options like:

```
📦 3 vocab sets in progress:
 • french/colors
 • spanish/food
 • japanese/verbs/basic

1. Start quiz
2. Clear all saved progress
Choose an option:
```

Then, select the file you want to practice from the scanned list.

### 4. ❓ Training Modes

Select the **language** you want the trainer to give you or select **random** if you want the question to be random between the two languages.

Missed questions will be repeated until all are correct — exactly in the form they were originally asked.

---

## 💾 Progress

When you start practicing a file, it creates:

```
data/{folder}/{file}_progress.json   # Tracks wrong answers until success
```

You can quit anytime — progress will resume next time.

### ✅ Full success?
Once you get every word right, your progress file is deleted automatically (and its folder if empty).

---

## 🧹 Other Features

- **Color-coded terminal output** for clarity
- **Accurate repetition** of failed questions
- **Automatic cleanup** of empty progress folders
- **Option to clear all saved progress**

---

## 📌 To Do (optional ideas)

- [ ] GUI or TUI version (Tkinter, curses, or Rich)
- [ ] Statistics viewer for history logs
- [ ] Word hint or partial answer system
- [ ] Import/export vocab files (CSV/Anki)

---

## 📄 License

MIT License – free for personal and educational use.
