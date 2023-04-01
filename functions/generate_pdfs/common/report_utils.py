import os
from google.cloud import storage


def get_report_query():
    return """
    SELECT  rank,term,max(week) week, max(refresh_date) refresh_date
    FROM `bigquery-public-data.google_trends.top_terms` 
    WHERE refresh_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) 
    AND week > DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY)
    AND rank <=10
    GROUP BY rank,term
    ORDER by rank
    LIMIT 10 
    """


def upload_pdfs(bucket_name, source_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(
        os.path.basename(source_file_name)
    )
    blob.upload_from_filename(source_file_name, content_type="application/pdf")
