import os
from pathlib import Path
from datetime import datetime
import functions_framework
from google.cloud import bigquery
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from common.report_utils import get_report_query, upload_pdfs

PROJECT_ID = os.getenv("PROJECT_ID")
UPLOAD_BUCKET = os.getenv("UPLOAD_BUCKET")


# @functions_framework.cloud_event
def generate_pdfs(cloud_event):

    # Instansiate BQ Client
    bqclient = bigquery.Client(PROJECT_ID)
    query = get_report_query()

    ctr = 1
    stylesheets = [
        f"{os.path.dirname(__file__)}/config/table.css",
    ]
    data = bqclient.query(query).to_dataframe().to_dict('records')

    # Print the PDF
    env = Environment(
        loader=FileSystemLoader(
            searchpath=f"{os.getcwd()}/config"
        )
    )
    template = env.get_template("report_format.html")

    config = template.render(
        abs_path=os.getcwd(),
        data=data
    )

    htmldoc = HTML(string=config, base_url=__file__)
    
    file_name = "top_google_trends.pdf"
    file_path = "/tmp/reports"
    
    Path(file_path).mkdir(mode=0o755, parents=True, exist_ok=True)
    
    htmldoc.write_pdf(
        f"{file_path}/{file_name}",
        stylesheets=stylesheets,
    )
    
    upload_pdfs(
        bucket_name=UPLOAD_BUCKET,
        source_file_name=f"{file_path}/{file_name}"
    )
    
    return "OK"

if __name__ == "__main__":
    generate_pdfs(None)
