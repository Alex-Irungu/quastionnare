from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import QuestionForm, ChoiceForm, ChoiceFormSet
from .models import Question, Choice
from random import shuffle
from django.contrib import messages
from django.http import HttpResponse


def showAlerts(request):
    return HttpResponse("hello here")

def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question = Question.objects.create(question_text=question_text)

        for key, value in request.POST.items():
            if key.startswith('choice_text_'):
                choice_number = key.split('_')[-1]
                choice_text = value
                is_correct = request.POST.get(f'is_correct_{choice_number}', False)
                is_correct = is_correct == 'on'

                Choice.objects.create(question=question, choice_text=choice_text, is_correct=is_correct)

        return redirect('add/')
    else:
        return render(request, 'addquestion.html')

def view_questions(request):
    percentage_correct = request.session.pop('percentage_correct', None) 
    questions = list(Question.objects.all())  
    shuffle(questions)  
    return render(request, 'viewquestions.html', {'questions': questions, 'percentage_correct': percentage_correct})

def submit_answers(request):
    if request.method == 'POST':
        total_questions = Question.objects.count()
        correct_answers = 0

        for question in Question.objects.all():
            if question.choice_set.count() == 1:
                answer_text = request.POST.get('choice_' + str(question.id))
                if answer_text:
                    correct_choice_text = question.choice_set.first().choice_text
                    if answer_text.strip().lower() == correct_choice_text.strip().lower():
                        correct_answers += 1
                    messages.success(request, f'Your answer for question "{question.question_text}" is correct.')
                else:
                    messages.error(request, f'Please provide an answer for question "{question.question_text}".')
            else:
                choice_id = request.POST.get('choice_' + str(question.id))
                if choice_id:
                    selected_choice = Choice.objects.get(pk=choice_id)
                    if selected_choice.is_correct:
                        correct_answers += 1
                    messages.success(request, f'You selected "{selected_choice.choice_text}" for question "{question.question_text}".')
                else:
                    messages.error(request, f'Please select an answer for question "{question.question_text}".')

        percentage_correct = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0

        print(percentage_correct)

        request.session['percentage_correct'] = percentage_correct

        return render(request, 'results.html', {'percentage_correct': percentage_correct})
    else:
        return redirect('viewquestion')
