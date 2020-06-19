from django.shortcuts import render, redirect
from .models import Tasks
from .forms import TaskForm, CalculatorForm
from .molar_mass import *
from .stoichiometry import stoichiometry_solver
import random
from .practice_reactions import reactions, get_reaction
from django.contrib import messages


# Create your views here.
def home(request):
    task_completed = Tasks.objects.filter(complete=True)
    tasks = Tasks.objects.filter(complete=False)
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'tasks':tasks, 'form':form, 'task_completed': task_completed}
    return render(request, 'todo/home.html', context)


def updateTask(request, pk):
    tasks = Tasks.objects.get(id=pk)
    form = TaskForm(instance=tasks)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=tasks)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'tasks': tasks, 'form':form}
    return render(request, 'todo/update_tasks.html', context)


def deleteTask(request, pk):
    tasks = Tasks.objects.get(id=pk)
    if request.method == "POST":
        tasks.delete()
        return redirect('/')
    context = {'tasks':tasks}
    return render(request, 'todo/delete.html', context)


g_a = random.randint(1,100)
rx_num = random.randint(1,len(reactions))
def practice(request):
    global g_a
    global rx_num
    if request.user.is_authenticated:
        current_user = request.user.account
    else:
        current_user = None
    r = reactions[rx_num]['reaction']
    g_u = reactions[rx_num]['given_units']
    g_f = reactions[rx_num]['given_formula']
    s_u = reactions[rx_num]['solving_units']
    s_f = reactions[rx_num]['solving_formula']
    question = get_reaction(rx_num, g_a)
    answer = stoichiometry_solver(r, g_a, g_u, g_f, s_u, s_f)[0]
    if request.method == "POST" and "answer" in request.POST:
        if request.POST.get('reset'):
            rx_num = random.randint(1, len(reactions))
            question = get_reaction(rx_num, g_a)
            r = reactions[rx_num]['reaction']
            g_u = reactions[rx_num]['given_units']
            g_f = reactions[rx_num]['given_formula']
            s_u = reactions[rx_num]['solving_units']
            s_f = reactions[rx_num]['solving_formula']
            answer = stoichiometry_solver(r, g_a, g_u, g_f, s_u, s_f)[0]
        elif not request.POST.get('reset'):
            response = request.POST.get('answer')
            if response == str(answer):
                if current_user and current_user.is_student:
                    current_user.student.correct += 1
                g_a = round(random.uniform(0,100), 2)
                rx_num = random.randint(1,len(reactions))
                question = get_reaction(rx_num,g_a)
                r = reactions[rx_num]['reaction']
                g_u = reactions[rx_num]['given_units']
                g_f = reactions[rx_num]['given_formula']
                s_u = reactions[rx_num]['solving_units']
                s_f = reactions[rx_num]['solving_formula']
                answer = stoichiometry_solver(r, g_a, g_u, g_f, s_u, s_f)[0]
                messages.success(request, "Correct! Good job!", extra_tags='alert')
            else:
                question = get_reaction(rx_num,g_a)
                answer = stoichiometry_solver(r, g_a, g_u, g_f, s_u, s_f)[0]
                messages.error(request, "Incorrect. Try again.", extra_tags='alert')
            if current_user and current_user.is_student:
                current_user.student.attempt += 1
                current_user.student.save()
    context = {
        'number': g_a,
        'c_user': current_user,
        'answer': answer,
        'question': question,
    }
    return render(request, 'todo/practice.html', context)


def calculator(request):
    reaction = 0
    given_amount = 0
    given_units = 0
    given_formula = 0
    coeff_given = 0
    coeff_solving = 0
    molmass_given = 0
    molmass_solving = 0
    solving_formula = 0
    solving_units = 0
    results = 0
    excess_amount = 0
    excess_reactant = 0
    excess_units = 0
    coeff_excess = 0
    molmass_excess = 0
    excess = 0
    form = CalculatorForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            reaction = request.POST.get("reaction")
            given_amount = float(request.POST.get("given_amount"))
            given_units = request.POST.get("given_units")
            given_formula = request.POST.get("given_formula").strip()
            solving_units = request.POST.get("solving_units")
            solving_formula = request.POST.get("solving_formula").strip()
            limiting = request.POST.get("limiting")
            if limiting:
                given_amount2 = float(request.POST.get("given_amount2"))
                given_units2 = request.POST.get("given_units2")
                given_formula2 = request.POST.get("given_formula2").strip()
                result1 = stoichiometry_solver(reaction,given_amount, given_units, given_formula, solving_units, solving_formula)[0]
                result2 = stoichiometry_solver(reaction, given_amount2, given_units2, given_formula2, solving_units, solving_formula)[0]
                if result1 < result2:
                    results = result1
                    excess_reactant = given_formula2
                    excess_amount = given_amount2
                    coeff_excess = (stoichiometry_solver(reaction, given_amount, given_units, given_formula2, given_units2, given_formula2)[1])
                    molmass_excess = molar_mass(excess_reactant)
                    excess_units = given_units2
                    excess = round(given_amount2 - (stoichiometry_solver(reaction, given_amount, given_units, given_formula, excess_units, excess_reactant)[0]),2)
                    coeff_given = stoichiometry_solver(reaction, given_amount, given_units, given_formula, solving_units, solving_formula)[1]
                    coeff_solving = stoichiometry_solver(reaction, given_amount, given_units, given_formula, solving_units, solving_formula)[2]
                    molmass_given = molar_mass(given_formula)
                    molmass_solving = molar_mass(solving_formula)
                elif result2 < result1:
                    results = result2
                    excess_reactant = given_formula
                    excess_amount = given_amount
                    coeff_excess = (stoichiometry_solver(reaction, given_amount2, given_units2, given_formula2, given_units, given_formula)[1])
                    molmass_excess = molar_mass(excess_reactant)
                    excess_units = given_units
                    excess = round(given_amount - (stoichiometry_solver(reaction, given_amount2, given_units2, given_formula2, excess_units, excess_reactant)[0]), 2)
                    given_amount = given_amount2
                    given_units = given_units2
                    given_formula = given_formula2
                    coeff_given = stoichiometry_solver(reaction, given_amount, given_units, given_formula, solving_units, solving_formula)[1]
                    coeff_solving = stoichiometry_solver(reaction, given_amount, given_units, given_formula, solving_units, solving_formula)[2]
                    molmass_given = molar_mass(given_formula)
                    molmass_solving = molar_mass(solving_formula)
            else:
                results = stoichiometry_solver(reaction,given_amount, given_units, given_formula, solving_units, solving_formula)[0]
                coeff_given = stoichiometry_solver(reaction,given_amount, given_units, given_formula, solving_units, solving_formula)[1]
                coeff_solving = stoichiometry_solver(reaction,given_amount, given_units, given_formula, solving_units, solving_formula)[2]
                molmass_given = molar_mass(given_formula)
                molmass_solving = molar_mass(solving_formula)
    context = {
        'reaction': reaction,
        'given_amount': given_amount,
        'given_units': given_units,
        'given_formula': given_formula,
        'solving_formula': solving_formula,
        'solving_units': solving_units,
        'coeff_given': coeff_given,
        'coeff_solving': coeff_solving,
        'molmass_given': molmass_given,
        'molmass_solving': molmass_solving,
        'results': results,
        'form': form,
        'excess': excess,
        'excess_amount': excess_amount,
        'excess_reactant': excess_reactant,
        'excess_units': excess_units,
        'coeff_excess': coeff_excess,
        'molmass_excess': molmass_excess
    }
    return render(request, 'todo/calculator.html', context)