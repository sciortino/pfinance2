from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import pandas as pd
from datetime import date

from .forms import IntakeForm, ReportForm
from .calcs import pmt, nper

from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import components


def index(request):

  if request.method == 'POST':
    form = IntakeForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data

      schedule = pd.DataFrame(nper(
        data['amt'], 
        data['pmt'],
        data['r'], 
        addl_principal=0, 
        annual_payments=12, 
        start_date=date.today()))

      d_head = schedule.head(1).iloc[0].to_dict()
      d_tail = schedule.tail(1).iloc[0].to_dict()

      initial_dict = {
        'amt': data['amt'],
        'pmt': data['pmt'],
        'r': data['r'],
        'per': d_tail['Period']
        } 

      rpt_form = ReportForm(initial=initial_dict)

      # Render Bokeh
      p = figure(x_axis_type="datetime")
      p.line(schedule['Month'], schedule['End_Balance'], color='navy')
      p.toolbar_location = None
      script, div = components(p, CDN)

      context_dict = {
        "the_script": script, 
        "the_div": div,
        "d_head": d_head,
        "d_tail": d_tail,
        "form": rpt_form
      }

      return render(request, "report.html", context_dict)

  else:

    form = IntakeForm()
    context_dict = {"form": form}
    return render(request, "index.html", context_dict)
   
def report(request):

  if request.method == 'POST':
    form = ReportForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data

      calc_type = data['calc_type']
      if calc_type == 'per':
        schedule = pd.DataFrame(nper(
          principal = data['amt'], 
          pmt = data['pmt'],
          interest_rate = data['r'], 
          addl_principal=0, 
          annual_payments=12, 
          start_date=date.today()))
      elif calc_type == 'pmt':
        schedule = pd.DataFrame(pmt(
          principal = data['amt'], 
          interest_rate = data['r'], 
          years = data['per']/12,
          addl_principal=0, 
          annual_payments=12, 
          start_date=date.today()))
      else:
        schedule = pd.DataFrame(pmt(
          principal = data['amt'], 
          interest_rate = data['r'], 
          years = data['per']/12,
          addl_principal=0, 
          annual_payments=12, 
          start_date=date.today()))

      d_head = schedule.head(1).iloc[0].to_dict()
      d_tail = schedule.tail(1).iloc[0].to_dict()

      print(schedule.head(10))
      print(schedule.tail(10))

      # Used to populate form

      initial_dict = {
        'amt': d_head['Begin_Balance'],
        'pmt': d_head['Payment'],
        'r': data['r'],
        'per': d_tail['Period'] - 1
        } 

      rpt_form = ReportForm(initial=initial_dict)

      # Render Bokeh
      p = figure(x_axis_type="datetime")
      p.line(schedule['Month'], schedule['End_Balance'], color='navy')
      p.toolbar_location = None
      script, div = components(p, CDN)

      context_dict = {
        "the_script": script, 
        "the_div": div,
        "d_head": d_head,
        "d_tail": d_tail,
        "form": rpt_form
      }

      return render(request, "report.html", context_dict)

    else:

      return HttpResponse("Damn Daniel")

  else:

    form = ReportForm()
    context_dict = {"form": form}
    return render(request, "report.html", context_dict)