from django.views.generic import ListView
from django.shortcuts import render
from .models import Rapport

from django.http import HttpResponse
from django.shortcuts import render
from .forms import AddReportTypeForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class RapportListView(ListView):
	queryset = Rapport.objects.all()
	template_name = "home_page.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Rapport.objects.all().order_by('-date')

def add_report(request):
	queryset = Rapport.objects.all()
	if request.method=='POST':
		form = AddReportTypeForm(request.POST, request.FILES)
		if form.is_valid():
			reportNr = Rapport.objects.count()+10000
			while True:
				qs = Rapport.objects.filter(reportNr=reportNr)
				if qs.exists():
					print("Exist")
					reportNr+=1
				else:
					break

			avd = form.cleaned_data.get("avd")
			ritningNr = form.cleaned_data.get("ritningNr")
			enhetsNr = form.cleaned_data.get("enhetsNr")
			atgard = form.cleaned_data.get("atgard")
			namn = form.cleaned_data.get("namn")
			anstNr = form.cleaned_data.get("anstNr")
			date = form.cleaned_data.get("date")
			file = form.cleaned_data.get("file")
			report = Rapport(reportNr=reportNr, avd=avd, ritningNr=ritningNr, enhetsNr=enhetsNr,
			atgard=atgard, namn=namn, anstNr=anstNr, date=date, file=request.FILES['file'])
			report.save()
			context = {
				"form":form,
				"context":"Rapport Tillagd"
			}

	else:
		form = AddReportTypeForm()
		context = {
			"form":form,
			"context":"Lägg till Rapport"
		}

	return render(request, "add_report.html", context)