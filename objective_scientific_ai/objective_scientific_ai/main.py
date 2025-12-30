from nicegui import ui
from evidence import fetch_all_evidence
from llm_core import answer_with_constraints

# Container for chat messages
chat_history = ui.column()

# Input box for questions
input_box = ui.input(placeholder="Enter a scientific question...")

# Function to send message and fetch AI response
def send_message():
    question = input_box.value.strip()
    if not question:
        return
    
    chat_history.add(ui.label(f"You: {question}"))
    input_box.value = ""  # Clear input
    
    try:
        with ui.spinner("Gathering evidence..."):
            evidence = fetch_all_evidence(question)

        with ui.spinner("Analyzing evidence..."):
            answer = answer_with_constraints(question, evidence)

        chat_history.add(ui.markdown(f"**AI:** {answer}"))

    except Exception:
        chat_history.add(ui.label("Sorry — I don’t have enough information to give you a solid conclusion."))

# Send button
ui.button("Ask", on_click=send_message)

# Run the NiceGUI server
ui.run(title="Objective Scientific AI")


