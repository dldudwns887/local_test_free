#####################################
# 이 파일은 테스트를 위한 dag파일임.
# 테스트 목적은 다음과 같음
# 1. operator를 정의하여 s3 목록을 가져오고 자 함. 
# 2. 모든 작업은 airflow에서 진행할 예정이므로 airflow를 기준으로 코드를 작성할 것.
# 3. s3 목록을 가져오고 간단하게 크롤링할 수 있는 코드도 짜보면 좋을 듯 함.
#
#
#######################################


from airflow import DAG
from datetime import datetime
from test_operator import S3ListOperator,CrawlingOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    's3_list_dag_v1',
    default_args=default_args,
    description='DAG for listing files in S3 using a custom operator_v6',
    schedule_interval='@daily', 
    catchup=False,
) as dag:

    # S3 버킷의 마지막 파일 목록을 가져오는 작업
    list_s3_files = S3ListOperator(
        task_id='list_s3_files',
        aws_conn_id='aws_default',
        bucket_name='otto-glue',
        s3_root='integrated-data/products/',
    )

    #체크하는 dag 실행하고, 없으면 처음부터 실행

    test_crawling_files = CrawlingOperator(
        task_id = 'crawling_test',
        aws_conn_id='aws_default',
        bucket_name='otto-glue',
        reviews_s3_root = 'integrated-data/reviews/',
        products_s3_root='integrated-data/products/',
        
    )
    
    list_s3_files >> test_crawling_files
