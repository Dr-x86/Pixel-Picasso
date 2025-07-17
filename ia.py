import requests
import os
import json
import base64

from dotenv import load_dotenv
load_dotenv()

API_KEY=os.getenv("GEMINIKEY")

def solicitar_imagen(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": f"{prompt}"}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    
        if response.status_code == 200:
            data = response.json()
            parts = data['candidates'][0]['content']['parts']
            base64_image = parts[1]['inlineData']['data']
        
            with open("images/imagenIA.png", "wb") as f:
                f.write(base64.b64decode(base64_image))
            
            print("[IMAGEN] - Imagen guardada correctamente")
            return "images/imagenIA.png"
                
    except Exception as e:
        print(f"[IMAGEN] - Error excepcion. {e}")
        return ""
    
def solicitar_texto(prompt):
    
    url= f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
            "contents":[
            {
                "parts":[
                {
                    "text":f"{prompt}"
                }
                ]
            }
            ]
        }   
    response=requests.post(url,headers=headers,json=data)
    if(response.ok):
        return response.json()['candidates'][0]['content']['parts'][0]['text'] # Regresar el texto que escupio la IA
    print(f"[TEXTO] - Error Codigo: {response.status_code} \n Detalles: {response.json()}")
    return ""