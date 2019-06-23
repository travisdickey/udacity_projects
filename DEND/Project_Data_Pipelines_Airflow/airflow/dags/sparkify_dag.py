from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from airflow.operators.postgres_operator import PostgresOperator
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'dwhuser',
    'start_date': datetime(2019, 5, 24),
#     'end_date': datetime(2018, 11, 3)
    'email': ['twdickey43@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('sparkify_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup=False,
          max_active_runs=1
        )

start_operator = PostgresOperator(
    task_id='Begin_execution',
    dag=dag,
    postgres_conn_id='redshift',
    sql="create_tables.sql"
)


stage_events = StageToRedshiftOperator(
    task_id='stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend',
    s3_key='log_data',
    json='s3://udacity-dend/log_json_path.json',
    table='public.staging_events'
)

stage_songs = StageToRedshiftOperator(
    task_id='stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend',
    s3_key='song_data',
    json='auto',
    table='staging_songs'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_stmt=SqlQueries.songplay_table_insert
)

load_user_dim_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    sql_stmt=SqlQueries.user_table_insert
)

load_song_dim_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    sql_stmt=SqlQueries.song_table_insert
)

load_artist_dim_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    sql_stmt=SqlQueries.artist_table_insert
)

load_time_dim_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    sql_stmt=SqlQueries.time_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    tables=['users', 'songs', 'artists', 'time']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >>  stage_events >> load_songplays_table
start_operator >> stage_songs >> load_songplays_table
dim_tasks = [load_song_dim_table, load_user_dim_table, load_artist_dim_table, load_time_dim_table]
for task in dim_tasks:
    load_songplays_table >> task >> run_quality_checks
run_quality_checks >> end_operator
