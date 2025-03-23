from openai import OpenAI
import requests

class TextGenerator:
    def __init__(self, api_key, model_name, select_api):
        self.api_key = api_key
        self.model_name = model_name
        self.select_api = select_api

    def text_render(self, prompt, log, END, message):
        log.insert(END, f"[DEBUG]  {message}\n")
        print(f"[DEBUG]  {message}\n")
        content = ''
        i = 1
        while i < 4:
            if self.select_api == "DeepSeek":
                client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
                try:
                    response = client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are content writing assistant"},
                            {"role": "user", "content": prompt},
                        ],
                        stream=False
                    )
                    content = response.choices[0].message.content
                    break
                except Exception as e:
                    log.insert(END, f"[DEBUG]  API-ERROR from Deepseek, trying ({i}) time\n")
                    print(f"[DEBUG]  API-ERROR from Deepseek, trying ({i}) time\n")
                    print("[DEBUG]  Error details:", str(e))
                    content = 'API-ERROR'
            elif self.select_api == "Gemni":
                try:
                    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": prompt}]}]}

                    response = requests.post(API_URL, json=data, headers=headers)
                    result = response.json()  # Convert response to JSON

                    # ✅ Handle errors in response
                    if response.status_code != 200:
                        log.insert(END, f"[DEBUG]  API-ERROR from Gemini ({i}) time\n")
                        print(f"[DEBUG]  API-ERROR from Gemini, trying ({i}) time\n")
                        print("[DEBUG]  Error Response:", result)
                        content = 'API-ERROR'
                    elif "candidates" not in result:
                        log.insert(END, f"[DEBUG]  API-ERROR: No candidates found, trying ({i}) time\n")
                        print(f"[DEBUG]  API-ERROR: No candidates found, trying ({i}) time\n")
                        print("[DEBUG]  Error Response:", result)
                        content = 'API-ERROR'
                    else:
                        content = result["candidates"][0]["content"]["parts"][0]["text"].replace("*", '')
                        break
                except Exception as e:
                    log.insert(END, f"[DEBUG]  API-ERROR from Gemini, trying ({i}) time\n")
                    print(f"[DEBUG]  API-ERROR from Gemini, trying ({i}) time\n")
                    print("[DEBUG]  Exception details:", str(e))
                    content = 'API-ERROR'
            else:
                client = OpenAI(api_key=self.api_key)
                try:
                    response = client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are content writing assistant"},
                            {"role": "user", "content": prompt},
                        ],
                        stream=False
                    )
                    content = response.choices[0].message.content
                    break
                except Exception as e:
                    log.insert(END, f"[DEBUG]  API-ERROR from OpenAI, trying ({i}) time\n")
                    print(f"[DEBUG]  API-ERROR from OpenAI, trying ({i}) time\n")
                    print("[DEBUG]  Error details:", str(e))
                    content = 'API-ERROR'
            i += 1
        return content