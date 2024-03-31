import jinja2
import pdfkit
from datetime import datetime

client_name = "Frank Ocean 2"
date_completed = "2021/09/01"
general = "General blah blah blah"
symptoms = "Symptoms blah blah blah"
exposure = "Exposure blah blah blah"
ai_comments = "AI Comments blah blah blah"
risk_level_summary = "Risk Level Summary blah blah blah"


item1 = "TV"
item2 = "Couch"
item3 = "Washing Machine"

subtotal1 = 499
subtotal2 = 399
subtotal3 = 129
total = subtotal1 + subtotal2 + subtotal3

today_date = datetime.today().strftime("%d %b, %Y")
month = datetime.today().strftime("%B")

# context = {'client_name': client_name, 'today_date': today_date, 'date_completed': date_completed, 'total': f'${total:.2f}', 'month': month,
#            'item1': item1, 'subtotal1': f'${subtotal1:.2f}',
#            'item2': item2, 'subtotal2': f'${subtotal2:.2f}',
#            'item3': item3, 'subtotal3': f'${subtotal3:.2f}'
#            }

context = {'client_name': client_name, 'date_completed': date_completed, 'general': general, 'symptoms': symptoms, 'exposure': exposure, 'ai_comments': ai_comments, 'risk_level_summary': risk_level_summary}

template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

# html_template = 'invoice.html'
html_template = 'doctor_report.html'
template = template_env.get_template(html_template)
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
output_pdf = 'doctor_report.pdf'
# pdfkit.from_string(output_text, output_pdf, configuration=config, css='invoice.css')
pdfkit.from_string(output_text, output_pdf, configuration=config)