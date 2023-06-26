from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = []
        letters = request.form.getlist('letter')
        amounts = request.form.getlist('amount')

        # Validate input: Ensure the number of letters and amounts match
        if len(letters) != len(amounts):
            return 'Error: Number of letters and amounts do not match.'

        # Convert amounts to integers
        try:
            amounts = list(map(int, amounts))
        except ValueError:
            return 'Error: Amounts should be integers.'

        # Create data list of tuples
        data = list(zip(letters, amounts))

        labels = []
        total_amount = sum(amounts)

        for letter, amount in data:
            labels.append(f'{letter} {amount}')

        # Check if there are any amounts
        if not amounts:
            return 'Error: No amounts provided.'

        # Calculate the percentage of each amount
        percentages = [amount / total_amount * 100 for amount in amounts]

        # Generate the pie chart
        fig, ax = plt.subplots()
        _, text_labels, _ = ax.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=90)

        # Add labels outside the pie slices
        for text_label in text_labels:
            text_label.set_horizontalalignment('center')

        plt.axis('equal')

        # Convert the pie chart to a base64-encoded string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        plt.close()

        return render_template('index.html', pie_chart=image_base64)
    else:
        return render_template('index.html', pie_chart=None)
    



   
   



if __name__ == '__main__':
    app.run(debug=True)

