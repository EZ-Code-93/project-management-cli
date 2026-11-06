import ollama

class AIClient:
    def __init__(self, model='llama3.2'):
        self.model = model

    def generate_project_summary(self, project_instance):
        """Takes a Project instance and generates a risk/status summary via Ollama."""
        task_list = [f"- {t.description} ({t.status})" for t in project_instance.tasks]
        tasks_string = "\n".join(task_list) if task_list else "No tasks added yet."
        
        prompt = (
            f"Project Title: {project_instance.title}\n"
            f"Tasks:\n{tasks_string}\n\n"
            f"Provide a brief, 2-sentence risk note and a suggested next step for this project."
        )
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response.get('response', 'No response text received.')
        except Exception as e:
            return f"Could not connect to Ollama: {str(e)}"
