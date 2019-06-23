from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import os


class PrepareTablesOperator(BaseOperator):
    sql = """
    CREATE TABLE IF NOT EXISTS public.staging_events (
        artist varchar(256),
        auth varchar(256),
        firstname varchar(256),
        gender varchar(256),
        iteminsession int4,
        lastname varchar(256),
        length numeric(18,0),
        "level" varchar(256),
        location varchar(256),
        "method" varchar(256),
        page varchar(256),
        registration numeric(18,0),
        sessionid int4,
        song varchar(256),
        status int4,
        ts int8,
        useragent varchar(256),
        userid int4
    );

    CREATE TABLE IF NOT EXISTS public.staging_songs (
        num_songs int4,
        artist_id varchar(256),
        artist_name varchar(256),
        artist_latitude numeric(18,0),
        artist_longitude numeric(18,0),
        artist_location varchar(256),
        song_id varchar(256),
        title varchar(256),
        duration numeric(18,0),
        "year" int4
    );

    CREATE TABLE IF NOT EXISTS public.users (
        user_id int4 PRIMARY KEY SORTKEY,
        first_name varchar(256),
        last_name varchar(256),
        gender varchar(256),
        "level" varchar(256)
    )
    DISTSTYLE ALL;

    CREATE TABLE IF NOT EXISTS public.artists (
        artist_id varchar(256) PRIMARY KEY SORTKEY DISTKEY,
        name varchar(256),
        location varchar(256),
        lattitude numeric(18,0),
        longitude numeric(18,0)
    );

    CREATE TABLE IF NOT EXISTS public.songs (
        song_id varchar(256) PRIMARY KEY SORTKEY DISTKEY,
        title varchar(256),
        artist_id varchar(256) NOT NULL,
        "year" int4,
        duration numeric(18,0)
    );

    CREATE TABLE IF NOT EXISTS public.time (
        start_time int4 PRIMARY KEY SORTKEY, 
        hour int4, 
        day int4, 
        week int4, 
        month int4, 
        year int4, 
        weekday VARCHAR(10)
    )
    DISTSTYLE ALL;

    CREATE TABLE IF NOT EXISTS public.songplays (
        play_id varchar(32) PRIMARY KEY,
        start_time timestamp NOT NULL,
        user_id int4 NOT NULL,
        "level" varchar(256),
        song_id varchar(256) SORTKEY  DISTKEY,
        artist_id varchar(256),
        session_id int4,
        location varchar(256),
        user_agent varchar(256)
    );
    """
    
    @apply_defaults
    def __init__(
        self,          
        redshift_conn_id="",
        *args, 
        **kwargs
    ):

        super(PrepareTablesOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)        
        self.log.info("Making sure tables are created on Redshift.")
        redshift.run(self.sql)