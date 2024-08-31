from flask import Flask, render_template, request, redirect, url_for, session
import random as r
from time import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Sample texts for typing test
examples = [
    # Existing examples...
    "The quick brown fox jumps over the lazy dog, showcasing every letter of the alphabet in a single sentence, a classic exercise to warm up your typing fingers.",
    "In today's digital world, the ability to type quickly and accurately is an invaluable skill that can enhance communication, productivity, and efficiency across various tasks.",
    "Typing is not just about speed; it's also about precision and rhythm, which together create a fluid and effective method of inputting text in any environment.",
    "Learning to type proficiently can transform your daily work routine, allowing you to complete tasks faster and with fewer errors, thus increasing overall productivity.",
    "The history of typing dates back to the invention of the typewriter, a revolutionary device that paved the way for modern keyboards and word processing systems.",
    "Touch typing involves using all ten fingers without looking at the keyboard, a technique that can greatly improve both speed and accuracy in the long run.",
    "Typing is a skill that, like any other, requires regular practice and patience to master, but the rewards in terms of efficiency and capability are well worth the effort.",
    "Whether you're writing a report, coding a program, or chatting with friends online, typing skills are essential to navigating the modern digital landscape.",
    "The ergonomics of typing are also important; proper posture and hand positioning can prevent strain and injury, ensuring a healthier and more sustainable typing practice."
]

def errors(og, userinput):
    count = 0
    for i in range(min(len(og), len(userinput))):
        if og[i] != userinput[i]:
            count += 1
    count += abs(len(og) - len(userinput))
    correct = len(og) - count
    accuracy = (correct / len(og)) * 100
    return accuracy

def timetaken(start, end, userinput):
    duration = round((end - start), 3) / 60  # Minutes
    word_count = len(userinput.split())
    return word_count / duration if duration > 0 else 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test = request.form['test']
        start_time = float(request.form['start_time'])
        userinput = request.form['userinput']
        end_time = time()

        netspeed = timetaken(start_time, end_time, userinput)
        accuracy = errors(test, userinput)

        # Optionally, store high scores in session
        high_score = session.get('high_score', 0)
        if netspeed > high_score:
            session['high_score'] = netspeed

        return render_template('result.html', speed=round(netspeed, 3), accuracy=round(accuracy, 2), test=test, high_score=session.get('high_score', 0))
    
    test = r.choice(examples)
    start_time = time()
    return render_template('index.html', test=test, start_time=start_time)

if __name__ == '__main__':
    app.run(debug=True)
