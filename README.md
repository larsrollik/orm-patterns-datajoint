[contribution guidelines]: https://github.com/larsrollik/orm-patterns-datajoint/blob/main/CONTRIBUTING.md
[issues]: https://github.com/larsrollik/orm-patterns-datajoint/issues
[BSD 3-Clause License]: https://github.com/larsrollik/orm-patterns-datajoint/blob/main/LICENSE
[Github]: https://github.com/larsrollik/orm-patterns-datajoint/settings/secrets/actions/new
[release]: https://github.com/larsrollik/orm-patterns-datajoint/releases/new

[//]: # (Badges)
[//]: # ([![PyPI]&#40;https://img.shields.io/pypi/v/orm-patterns-datajoint.svg&#41;]&#40;https://pypi.org/project/orm-patterns-datajoint&#41;)
[//]: # ([![Wheel]&#40;https://img.shields.io/pypi/wheel/orm-patterns-datajoint.svg&#41;]&#40;https://pypi.org/project/orm-patterns-datajoint&#41;)
[//]: # (![CI]&#40;https://github.com/larsrollik/orm-patterns-datajoint/workflows/tests/badge.svg&#41;)

[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/larsrollik/orm-patterns-datajoint/blob/main/CONTRIBUTING.md)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fgithub.com/larsrollik/orm-patterns-datajoint)](https://github.com/larsrollik/orm-patterns-datajoint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# orm-patterns-datajoint
Patterns for Object Relational Mapping (ORM) in Python (here via DataJoint)

## Patterns

### Standardized schema initialization

By using this pattern, you ensure that all schemas are consistently named and organized.
No further naming / loading of schemata required.

In package `__init__.py`:
```python
def get_datajoint_schema(
    schema_prefix=None,
    schema_name=None,
    linking_module=None,
):
    # ...
    return schema
```

Then in **each** module that will contain table classes:
```python
from orm_patterns_datajoint import get_datajoint_schema
from orm_patterns_datajoint import prepare_schema_name

schema = get_datajoint_schema(
    schema_name=prepare_schema_name(file=__file__),
    linking_module=__name__
)

# ... table classes ...
```


### Import checks

This table pattern uses an additional table `ImportChecks` that reference the base table `SourceTable` and carries out checks prior to imports into `NextStep`.
The downstream `NextStep` table references the same base table, but draws it's actual key tuples to process from the `ImportChecks` table.
This results in a sidestep via `ImportChecks`, so that all checks are documented to avoid frequent re-checks of datasets that were already checked or even imported.
Additionally, this clears up the code logic of the `NextStep` table.

- `SourceTable`: base for keys in this example, but can be anywhere in relational chain
```python
@schema
class SourceTable(dj.Manual):
    definition = """
    source_key         :   varchar(64)
    ---
    """

```

- `ImportChecks`: builds on `SourceTable` and performs checks, inserts result
```python
@schema
class ImportChecks(dj.Imported):
    definition = """
    -> source_key
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

```

- `NextStep`: also builds on `SourceTable`, but takes it's actually key tuples from `ImportChecks`. These keys will be exactly the same as from `SourceTable`, only filtered for successful checks (`importable` bool)
```python
@schema
class NextStep(dj.Imported):
    definition = """
    -> source_key
    ---
    some_data           :   longblob
    """
    key_source = ImportChecks() & {"importable": True}

    def make(self, key):
        pass  # logic for data import goes here...
```


### Job tables

The next snippet illustrates how to define job-related tables using DataJoint.
The pattern includes a job submission handler `JobHandler` and two tables: one for job metadata, `JobTable`, and one for job outputs, `JobOutputs`.
One example application is the submission of jobs to `Slurm` clusters or other infrastructure to carry out the computation/processing


- `JobHandler`: Provides a helper method submit_job to submit a job and return a job identifier.
```python
class JobHandler:
    def __init__(self, **kwargs):
        pass

    def submit_job(self, **job_data):
        # submits job...
        job_id = 23424
        return job_id

```

- `JobTable`: inherits both an ORM table type (e.g. `dj.Imported`) and the `JobHandler`
- This class processes the data and uses the job handler to submit/manage jobs
```python
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

```

- Then the downstream `JobOutput` table can check for completed jobs and import their outputs/results


## Contributing
Contributions are very welcome!
Please see the [contribution guidelines] or check out the [issues]


## License
This software is released under the **[BSD 3-Clause License]**
