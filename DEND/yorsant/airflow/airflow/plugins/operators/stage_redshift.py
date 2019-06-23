from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    copy_sql = """
        COPY {} 
        FROM {}
        CREDENTIALS 'aws_iam_role={}'
        REGION 'us-west-2'
        COMPUPDATE ON 
        STATUPDATE ON
        {}
    """
    # Make sure to create a variable on airflow called AWS_IAM_ROLE_ARN
    # with a Redshift role with S3 read access
    aws_iam_role=Variable.get("AWS_IAM_ROLE_ARN")   

    @apply_defaults
    def __init__(
        self,              
        redshift_conn_id="",
        table="",
        s3_bucket="",
        s3_key="",
        extra_sql="",
        *args, 
        **kwargs
    ):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.extra_sql = extra_sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Clearing data from destination Redshift table.")
        redshift.run("DELETE FROM {}".format(self.table))
        
        self.log.info("Copying data from S3 to staging table on Redshift.")
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            self.aws_iam_role,  
            self.extra_sql
        )
        redshift.run(formatted_sql)
        