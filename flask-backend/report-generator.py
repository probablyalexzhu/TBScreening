import jinja2
import pdfkit
from datetime import datetime

name = "Frank Ocean"
date_completed = "2021/09/01"
general = "General blah blah blah"
symptoms = "Symptoms blah blah blah"
exposure = "Exposure blah blah blah"
ai_comments = "AI Comments blah blah blah"
risk_level_summary = "Risk Level Summary blah blah blah"

today_date = datetime.today().strftime("%d %b, %Y")
month = datetime.today().strftime("%B")

context = {'name': name, 'date_completed': date_completed, 'general': general, 'symptoms': symptoms, 'exposure': exposure, 'ai_comments': ai_comments, 'risk_level_summary': risk_level_summary}

template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

html_template = 'doctor_report.html'
# html_template = 'NOIMAGES_doctor_report.html'
template = template_env.get_template(html_template)
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
output_pdf = 'doctor_report.pdf'
output_pdf = 'NOIMAGES_doctor_report.pdf'
pdfkit.from_string(output_text, output_pdf, configuration=config)