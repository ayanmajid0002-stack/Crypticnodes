import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'

# CSV file name - use full path to be safe
CSV_FILE = 'users.csv'

# Initialize CSV file with headers if it doesn't exist
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'password'])
            print("CSV file created!")

# Get user by email
def get_user(email):
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 3 and row[1].strip() == email.strip():
                    return {'name': row[0].strip(), 'email': row[1].strip(), 'password': row[2].strip()}
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Save new user
def save_user(name, email, password):
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name.strip(), email.strip(), password.strip()])
            print(f"User saved: {name}, {email}")
            return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False

# Initialize CSV on startup
init_csv()

# Display all users (for debugging - remove later)
def show_all_users():
    with open(CSV_FILE, 'r', encoding='utf-8') as file:
        print("All users in CSV:")
        print(file.read())

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/How')
def How():
    return render_template('How.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    
    print(f"Trying to sign in with: {email}")
    
    user = get_user(email)
    
    if user:
        print(f"User found: {user}")
        if user['password'] == password:
            session['user_email'] = email
            print("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            print("Wrong password")
            error = "Invalid email or password!"
            return render_template('intro.html', error=error)
    else:
        print("User not found")
        error = "Invalid email or password!"
        return render_template('intro.html', error=error)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    print(f"Registering: {name}, {email}")
    
    # Check if email already exists
    if get_user(email):
        print("Email already exists!")
        error = "Email already registered!"
        return render_template('intro.html', error=error)
    
    # Save new user to CSV
    if save_user(name, email, password):
        print("Registration successful!")
        # Automatically sign in after registration
        session['user_email'] = email
        return redirect(url_for('dashboard'))
    else:
        error = "Registration failed!"
        return render_template('intro.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('home'))
    
    email = session['user_email']
    user = get_user(email)
    
    if user:
        return render_template('Dashboard.html', email=email, name=user['name'])
    else:
        session.clear()
        return redirect(url_for('home'))

@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for('home'))

@app.route('/Encrypt', methods=['POST', 'GET'])
def encrypt():
    encrypted_output = None
    encrypt = request.form.get('encrypt')
    shift = request.form.get('shiftkey')
    result_text = ''
    if encrypt and shift:
        for x in encrypt:
            convert = (ord(x) + int(shift)) % 256
            result_text += chr(convert)
        encrypted_output = result_text
    else:
        encrypted_output = 'Fill both field'
    return render_template('Encrypt.html', encrypted_output=encrypted_output)

@app.route('/Decrypt', methods=['POST', 'GET'])
def decrypt():
    decrypted_output = None
    decrypt = request.form.get('decrypt')
    shift = request.form.get('shiftkey')
    result_text = ''
    if decrypt and shift:
        for x in decrypt:
            convert = (ord(x) - int(shift)) % 256
            result_text += chr(convert)
        decrypted_output = result_text
    else:
        decrypted_output = 'Fill both field'
    return render_template('Decrypt.html', decrypted_output=decrypted_output)

@app.route('/Text', methods = ['POST', 'GET'])
def text_to_emoji():
    emoji_output = None
    Text_map = {
    'A': '😀', 'B': '😁', 'C': '😂', 'D': '🤣', 'E': '😃', 'F': '😄', 'G': '😅',
    'H': '😆', 'I': '😉', 'J': '😊', 'K': '😋', 'L': '😎', 'M': '😍', 'N': '😘',
    'O': '😗', 'P': '😙', 'Q': '😚', 'R': '🙂', 'S': '🤗', 'T': '🤔', 'U': '😐',
    'V': '😑', 'W': '😶', 'X': '🙄', 'Y': '😏', 'Z': '😣',
    'a': '😥', 'b': '😮', 'c': '🤐', 'd': '😯', 'e': '😪', 'f': '😫', 'g': '😴',
    'h': '😌', 'i': '😛', 'j': '😜', 'k': '😝', 'l': '🤤', 'm': '😒', 'n': '😓',
    'o': '😔', 'p': '😕', 'q': '🙃', 'r': '🫠', 's': '😲', 't': '🙁', 'u': '😖',
    'v': '😞', 'w': '😟', 'x': '😤', 'y': '😢', 'z': '😭', 
    }
    text = request.form.get('text')
    if text:
        result_text = ''
        for x in text:
            if x in Text_map:
                result_text += Text_map[x]
            else:
                result_text += x
            emoji_output = result_text
    else:
            emoji_output = 'Please enter some text...'
    return render_template('text.html', emoji_output = emoji_output)
@app.route('/Emoji', methods = ['POST', 'GET'])
def Emoji_to_text():
    text_output = None
    emoji_map = {
    '😀': 'A', '😁': 'B', '😂': 'C', '🤣': 'D', '😃': 'E', '😄': 'F', '😅': 'G',
    '😆': 'H', '😉': 'I', '😊': 'J', '😋': 'K', '😎': 'L', '😍': 'M', '😘': 'N',
    '😗': 'O', '😙': 'P', '😚': 'Q', '🙂': 'R', '🤗': 'S', '🤔': 'T', '😐': 'U',
    '😑': 'V', '😶': 'W', '🙄': 'X', '😏': 'Y', '😣': 'Z',
    '😥': 'a', '😮': 'b', '🤐': 'c', '😯': 'd', '😪': 'e', '😫': 'f', '😴': 'g',
    '😌': 'h', '😛': 'i', '😜': 'j', '😝': 'k', '🤤': 'l', '😒': 'm', '😓': 'n',
    '😔': 'o', '😕': 'p', '🙃': 'q', '🫠': 'r', '😲': 's', '🙁': 't', '😖': 'u',
    '😞': 'v', '😟': 'w', '😤': 'x', '😢': 'y', '😭': 'z'
    }
    emoji = request.form.get('emoji_text')
    if emoji:
        result_text = ''
        for x in emoji:
            if x in emoji_map:
                result_text += emoji_map[x]
            else:
                result_text += x
        text_output = result_text
    else:
            text_output = 'Please enter some text...'
    return render_template('Emoji.html', text_output = text_output)
if __name__ == '__main__':
    app.run(debug=True)