import datajoint as dj

from orm_patterns_datajoint import get_datajoint_schema
from orm_patterns_datajoint import prepare_schema_name

# >> START BLOCK: schema generation pattern

schema = get_datajoint_schema(
    schema_name=prepare_schema_name(file=__file__), linking_module=__name__
)
# >> END BLOCK: schema generation pattern


# >> START BLOCK: import checks pattern
@schema
class SourceTable(dj.Manual):
    definition = """
    source_key         :   varchar(64)
    ---
    """
    # import function not shown...


@schema
class ImportChecks(dj.Imported):
    definition = """
    -> source_key
    ---
    check_1             :   bool
    check_2             :   bool
    """
    # key_source is already implied by definition above, here just explicit
    key_source = SourceTable()

    def make(self, key):
        raise NotImplementedError(
            "Tests to check that data related to key_source "
            "can be imported in NextStep table"
        )


@schema
class NextStep(dj.Imported):
    definition = """
    -> source_key
    ---
    some_data           :   longblob
    """
    key_source = ImportChecks()

    def make(self, key):
        raise NotImplementedError("Actual data import goes here...")


# >> END BLOCK: import checks pattern
