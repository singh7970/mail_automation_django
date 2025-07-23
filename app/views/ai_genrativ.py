from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from django.conf import settings

# Configure once
genai.configure(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def ai_generate_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            if not prompt:
                return JsonResponse({"error": "No prompt provided"}, status=400)

            # ✅ Use correct model name (update based on your list)
            model = genai.GenerativeModel("gemini-1.5-pro-latest")

            response = model.generate_content(prompt)
            text = response.text if hasattr(response, "text") else str(response)

            return JsonResponse({"content": text})
        except Exception as e:
            return JsonResponse({"error": f"Failed to generate: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from openai import OpenAI
from django.conf import settings

# # ✅ Initialize OpenAI client
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# @csrf_exempt
# def ai_generate_view(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             prompt = data.get("prompt", "")

#             if not prompt:
#                 return JsonResponse({"error": "No prompt provided"}, status=400)

#             # ✅ You can add a system message if you want
#             messages = [
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ]

#             # ✅ Create chat completion
#             response = client.chat.completions.create(
#                 model="gpt-4o",  # Use "gpt-3.5-turbo" if gpt-4 is not available in your trial
#                 messages=messages
#             )

#             text = response.choices[0].message.content

#             return JsonResponse({"content": text})
#         except Exception as e:
#             return JsonResponse({"error": f"Failed to generate: {str(e)}"}, status=500)

#     return JsonResponse({"error": "Invalid request"}, status=400)




# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from app.chatterbot_setup import chatbot

# @csrf_exempt
# def ai_generate_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         prompt = data.get("prompt", "")

#         if not prompt:
#             return JsonResponse({"error": "No prompt provided"}, status=400)

#         # Get bot response
#         bot_response = chatbot.get_response(prompt)

#         return JsonResponse({"content": str(bot_response)})

#     return JsonResponse({"error": "Invalid request"}, status=400)
