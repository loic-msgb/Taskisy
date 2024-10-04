from openai import OpenAI
import json
from llmModels import responseModel

# --- Constants ---
client = OpenAI()
#Modèle de l'API
MODEL="gpt-4o-mini" 
#system message
systemMessage = "You are a helpful productivity assistant, you will be provided with a long term objective that the user wants to achieve, and your role will be to reformulate the objective as a project name, and output a list of actionnable, daily and precise tasks to achive this project."
#--------

# message de l'utilisateur
userMessage = "My long term objective is to learn how to play the guitar."



# --- Fonction pour obtenir les tâches par l'API---

def generate_task_API(userMessage):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": systemMessage},
            {"role": "user", "content": userMessage}
        ],
        response_format= responseModel,
    )
    # Convert tasks list to a list of dictionaries
    tasks_list = [{"title": task.title, "done": task.done} for task in completion.choices[0].message.parsed.task]

    result = {
        "project": completion.choices[0].message.parsed.project,
        "tasks": tasks_list
    }
    return result


#--- Convertir le résultat en JSON ---
def convert_to_json(result):
    return json.dumps(result, indent=4)

#--- Appel de la fonction pour obtenir les tâches ---
result = generate_task_API(userMessage)

#--- Convertir le résultat en JSON ---
json_result = convert_to_json(result)

#--- Enregistrer le résultat dans un fichier JSON ---
with open("result.json", "w") as f:
    f.write(json_result)