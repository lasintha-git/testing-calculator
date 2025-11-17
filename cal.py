from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .calculator {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 20px;
            font-size: 28px;
        }
        
        .display {
            background: #f5f5f5;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: right;
            font-size: 32px;
            font-weight: bold;
            color: #333;
            min-height: 70px;
            word-wrap: break-word;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        
        button {
            padding: 20px;
            font-size: 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .number, .operator {
            background: #f0f0f0;
            color: #333;
        }
        
        .clear {
            background: #ff6b6b;
            color: white;
            grid-column: span 2;
        }
        
        .equals {
            background: #667eea;
            color: white;
            grid-column: span 2;
        }
        
        .error {
            color: #ff6b6b;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <div class="display" id="display">0</div>
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="operator" onclick="appendToDisplay('/')">/</button>
            <button class="operator" onclick="appendToDisplay('*')">×</button>
            
            <button class="number" onclick="appendToDisplay('7')">7</button>
            <button class="number" onclick="appendToDisplay('8')">8</button>
            <button class="number" onclick="appendToDisplay('9')">9</button>
            <button class="operator" onclick="appendToDisplay('-')">−</button>
            
            <button class="number" onclick="appendToDisplay('4')">4</button>
            <button class="number" onclick="appendToDisplay('5')">5</button>
            <button class="number" onclick="appendToDisplay('6')">6</button>
            <button class="operator" onclick="appendToDisplay('+')">+</button>
            
            <button class="number" onclick="appendToDisplay('1')">1</button>
            <button class="number" onclick="appendToDisplay('2')">2</button>
            <button class="number" onclick="appendToDisplay('3')">3</button>
            <button class="operator" onclick="appendToDisplay('.')">.</button>
            
            <button class="number" onclick="appendToDisplay('0')">0</button>
            <button class="equals" onclick="calculate()">=</button>
        </div>
    </div>
    
    <script>
        let currentDisplay = '0';
        
        function appendToDisplay(value) {
            if (currentDisplay === '0' || currentDisplay === 'Error') {
                currentDisplay = value;
            } else {
                currentDisplay += value;
            }
            document.getElementById('display').textContent = currentDisplay;
        }
        
        function clearDisplay() {
            currentDisplay = '0';
            document.getElementById('display').textContent = currentDisplay;
            document.getElementById('display').classList.remove('error');
        }
        
        async function calculate() {
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ expression: currentDisplay })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    currentDisplay = 'Error';
                    document.getElementById('display').classList.add('error');
                } else {
                    currentDisplay = data.result.toString();
                    document.getElementById('display').classList.remove('error');
                }
                
                document.getElementById('display').textContent = currentDisplay;
            } catch (error) {
                currentDisplay = 'Error';
                document.getElementById('display').textContent = currentDisplay;
                document.getElementById('display').classList.add('error');
            }
        }
        
        // Keyboard support
        document.addEventListener('keydown', function(event) {
            if (event.key >= '0' && event.key <= '9') {
                appendToDisplay(event.key);
            } else if (event.key === '.') {
                appendToDisplay('.');
            } else if (['+', '-', '*', '/'].includes(event.key)) {
                appendToDisplay(event.key);
            } else if (event.key === 'Enter') {
                calculate();
            } else if (event.key === 'Escape') {
                clearDisplay();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Replace × and − symbols if present
        expression = expression.replace('×', '*')
        expression = expression.replace('−', '-')
        
        result = eval(expression)  # simple calculator
        return jsonify({'result': result})
    except:
        return jsonify({'error': 'Invalid Expression'}), 400


if __name__ == '_main_':
    # Final line was missing — now fixed
    app.run(debug=True, host='0.0.0.0', port=5000)