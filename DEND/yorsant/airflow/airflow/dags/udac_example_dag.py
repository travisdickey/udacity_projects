from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (
    StageToRedshiftOperator, 
    PrepareTablesOperator,
    LoadFactOperator,
    LoadDimensionOperator, 
    DataQualityOperator
)
from helpers import SqlQueries

# Dictionary with default arguments for DAGs
default_args = {
    'owner': 'udacity',
    'start_date': datetime.now(),
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'depends_on_past': True,
    'catchup': False
}

dag = DAG(  # Directed Acyclic Graph
    'udac_example_dag',
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval=timedelta(hours=1),
)

start_operator = DummyOperator(  # Dummy Operators do nothing, use them to mark start and end processes
    task_id='Begin_execution',  
    dag=dag
)

prepare_tables_on_redshift = PrepareTablesOperator(
    task_id='Prepare_tables',
    dag=dag,
    redshift_conn_id="redshift"  # Make sure a connection called redshift is saved in airflow db
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
#     provide_context=True,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table="staging_events",
    s3_bucket=Variable.get("s3_bucket"),  # Make sure a variable called s3_bucket is saved in airflow db
    s3_key="log_data",
    extra_sql="""
    ACCEPTINVCHARS AS '^'
    TIMEFORMAT 'epochmillisecs'
    """    
#     JSON 's3://udacity-dend/log_json_path.json'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
#     provide_context=True,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table="staging_songs",
    s3_bucket=Variable.get("s3_bucket"),  # Make sure a variable called s3_bucket is saved in airflow db
    s3_key="song_data",
    extra_sql="""
    JSON 'auto'
    """
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table='songplays',
    sql=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table='users',
    sql=SqlQueries.user_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table='songs',
    sql=SqlQueries.song_table_insert
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table='artists',
    sql=SqlQueries.artist_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",  # Make sure a connection called redshift is saved in airflow db
    table='time',
    sql=SqlQueries.time_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    tables=['songplays', 'songs', 'artists', 'users', 'time']  # This have to be a list of strings 
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> prepare_tables_on_redshift

prepare_tables_on_redshift >> stage_events_to_redshift
prepare_tables_on_redshift >> stage_songs_to_redshift

stage_events_to_redshift >> load_user_dimension_table
stage_events_to_redshift >> load_time_dimension_table

stage_songs_to_redshift >> load_song_dimension_table
stage_songs_to_redshift >> load_artist_dimension_table

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table  >> run_quality_checks 
load_user_dimension_table  >> run_quality_checks
load_song_dimension_table  >> run_quality_checks
load_artist_dimension_table  >> run_quality_checks
load_time_dimension_table  >> run_quality_checks

run_quality_checks >> end_operator