import jinja2
import pdfkit
from datetime import datetime

def generate_report(name, age, gender, location, summary, technical):
    date = datetime.now().strftime("%Y-%m-%d")
    context = {'name': name, 'date': date, 'age': age, 'gender': gender, 'location': location, 'summary': summary, 'technical': technical}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'FINAL_TuberculosisAIPreScreener.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    output_pdf = 'FINAL_doctor_report.pdf'
    # pdfkit.from_string(output_text, output_pdf, configuration=config, options={"enable-local-file-access": ""})
    pdfkit.from_string(output_text, output_pdf, configuration=config, options={"enable-local-file-access": True, "page-size": "Letter"})

    return output_pdf


generate_report("Anoop Rehman", "67", "Male", "Dharavi", "SUMMARY Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec odio. Quisque volutpat mattis eros. Nullam malesuada erat ut turpis. Suspendisse urna nibh viverra non semper suscipit posuere a pede. Donec nec justo eget felis facilisis fermentum. Aliquam porttitor mauris sit amet orci. Aenean dignissim pellentesque felis.", "Technical Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec odio. Quisque volutpat mattis eros. Nullam malesuada erat ut turpis. Suspendisse urna nibh viverra non semper suscipit posuere a pede. Donec nec justo eget felis facilisis fermentum. Aliquam porttitor mauris sit amet orci. Aenean dignissim pellentesque felis.")