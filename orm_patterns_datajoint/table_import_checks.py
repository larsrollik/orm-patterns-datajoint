import datajoint as dj

from orm_patterns_datajoint import get_datajoint_schema

# >> START BLOCK: schema generation pattern

schema = get_datajoint_schema(file=__file__, linking_module=__name__)
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
    -> SourceTable
    ---
    check_1             :   bool
    check_2             :   bool
    importable          :   bool
    """
    # key_source is already implied by definition above, here just explicit
    key_source = SourceTable()

    def make(self, key):
        # Tests to check that data related to key_source
        # can be imported in NextStep table
        pass


@schema
class NextStep(dj.Imported):
    definition = """
    -> SourceTable
    ---
    some_data           :   longblob
    """
    key_source = ImportChecks() & {"importable": True}

    def make(self, key):
        pass  # logic for data import goes here


# >> END BLOCK: import checks pattern
