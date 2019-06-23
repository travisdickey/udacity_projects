from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import os

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    tables = []

    @apply_defaults
    def __init__(
        self,            
        redshift_conn_id="",
        tables="",
        *args, 
        **kwargs
    ):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.tables=tables

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Checking quality of the data on Redshift tables.")
        for table in self.tables:
            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} table returned no results.")
            if records[0][0] < 1:
                raise ValueError(f"Data quality check failed. {table} table contained 0 rows.")

            self.log.info("Data quality check on table {table} passed with {records[0][0]} records.")