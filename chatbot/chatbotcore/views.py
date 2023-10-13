import openai

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .forms import AudioUploadForm
from django.views.decorators.csrf import csrf_exempt

openai.api_key = settings.OPEN_AI_API_KEY

def ask_open_ai_question(message):
    responce = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = responce.choices[0].text.strip()
    return answer


def transcribe_audio(audio):
    transcript = openai.Audio.transcribe("whisper-1", audio)
    return transcript


@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        audio_file = request.FILES.get("audio_file")
        response = ""
        if (message):
            response += ask_open_ai_question(message)

        if audio_file:
            transcript = transcribe_audio(audio_file)
            response = f"\nTranscript: {transcript.text}"

        return JsonResponse({"response": response})

    form = AudioUploadForm()
    return render(request, "chatbot.html", {"form": form})
