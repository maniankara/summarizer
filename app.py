from translate import AzureOpenAITranslate
from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Chat route to handle user inputs
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_reply = "Sorry, something went wrong."

    # check
    if 'file' not in request.files:
        bot_reply = 'No file part'
    
    file = request.files['file']
    file_contents = file.read().decode('utf-8')

    # Perform the translation
    tr = AzureOpenAITranslate()
    bot_reply = tr.translate(file_contents)

    return render_template('index.html', user_message=user_message, bot_reply=bot_reply)

if __name__ == '__main__':
    app.run(debug=True)


# def main():
#     tr = AzureOpenAITranslate("")
#     output = tr.translate()
#     print("output: ", output)

# if __name__ == '__main__':
#     main()