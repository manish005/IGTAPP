from flask import Flask, render_template, request, redirect, url_for
from groq import Groq
import re
from markupsafe import Markup
from api.index  import beautify_response, client, model_llama318B

app = Flask(__name__)

# Store chat messages in a list (in-memory storage)
conversation = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['message']
        if user_message:
            # Append the user message to the conversation list
            conversation.append({"role": "user", "content": user_message})

            # Send the entire conversation to the model
            chat_completion = client.chat.completions.create(
                messages=conversation,
                model=model_llama318B
            )

            # Get the model's response
            model_response = chat_completion.choices[0].message.content

            # Beautify and format the model response
            if isinstance(model_response, list):
                for item in model_response:
                    formatted_item = beautify_response(item)
                    conversation.append({"role": "assistant", "content": formatted_item})
            else:
                formatted_response = beautify_response(model_response)
                conversation.append({"role": "assistant", "content": formatted_response})

        # Redirect to the chat page to display the updated conversation
        return redirect(url_for('chat'))

    return render_template('index.html', messages=conversation)

if __name__ == '__main__':
    app.run(debug=True)
