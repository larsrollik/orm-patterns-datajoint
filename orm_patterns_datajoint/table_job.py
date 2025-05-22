import datajoint as dj

from orm_patterns_datajoint import get_datajoint_schema, prepare_schema_name

# >> START BLOCK: schema generation pattern

schema = get_datajoint_schema(
    schema_name=prepare_schema_name(file=__file__), linking_module=__name__
)
# >> END BLOCK: schema generation pattern


# >> START BLOCK: table job pattern
class JobHandler:
    def __init__(self, **kwargs):
        pass

    def submit_job(self, **job_data):
        # submits job...
        job_id = 23424

        return job_id


@schema
class JobTable(dj.Imported, JobHandler):
    definition = """
    source_key         :   varchar(64)
    ---
    """

    def __init__(self, **job_params):
        super(dj.Manual).__init__()
        super(JobHandler).__init__(**job_params)

    def make(self, key):
        # process key data for job...
        job_data = {}

        # submit job...
        job_id = self.submit_job(**job_data)

        # insert job for documentation...
        key.update({"job_id": job_id})
        self.insert1(row=key)


@schema
class JobOutputs(dj.Imported):
    definition = """
    -> JobTable
    ---
    job_data            :   longblob
    """

    def make(self, key):
        # check if data is processed
        # if yes, then insert
        pass


# >> END BLOCK: table job pattern

if __name__ == "__main__":
    # create jobs
    job_params = {}
    st = JobTable(**job_params)
    st.populate()

    # wait for processing...

    # insert job output data
    so = JobOutputs()
    so.populate()
