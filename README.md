# Databricks Data Engineer study notebooks

This repository contains Databricks Academy Data Engineering notebooks and
solutions, originally built in 2023 for Databricks Runtime (DBR) 11.3. This
copy targets DBR 15.4 LTS; its changes have only been checked statically and
have **not** been run or certified on a Databricks workspace. Course content
has not been updated against the current certification exam.

## Runtime and compute

DBR 15.4 LTS is supported until August 19, 2027. See the
[supported runtime versions](https://docs.databricks.com/aws/en/release-notes/runtime/)
for the current lifecycle.

The shared course setup accepts these runtime keys:

- `15.4.x-scala2.12`
- `15.4.x-cpu-ml-scala2.12`

Availability and behavior of each variant are unverified. `Includes/Workspace-Setup`
defaults to the CPU ML key, and its widget can select another course runtime.
Check the keys available in your workspace and any applicable compute policy.
Photon is an independently configured runtime engine; its behavior with the
course's runtime check has not been verified. SQL warehouses and Delta Live
Tables (DLT) pipelines use separately managed compute or pipeline channels;
selecting DBR 15.4 for a notebook does not pin their runtime.

## Getting started

1. Import the `data-enginer associate cert` directory into a Databricks workspace,
   preserving its directory structure. Attach a notebook to compatible classic
   compute and start with the module introductions. Solutions are in the
   `Solutions` directory.
2. The shared setup installs the pinned
   [dbacademy v3.0.42 wheel](https://github.com/databricks-academy/dbacademy/releases/tag/v3.0.42)
   from GitHub and installs course datasets. Network access to GitHub and the
   Academy dataset sources is required. Dataset availability is unverified.
3. If another `dbacademy` version was already imported, start a fresh notebook
   session and install the pinned wheel before running a lesson's setup:

   ```python
   %pip install https://github.com/databricks-academy/dbacademy/releases/download/v3.0.42/dbacademy-3.0.42-py3-none-any.whl
   ```

   Run `dbutils.library.restartPython()` in the next cell before running the
   lesson. Restarting clears Python state. DBR 15.4 does not automatically
   restart Python after `%pip`; see the
   [library documentation](https://docs.databricks.com/aws/en/libraries/notebooks-python-libraries).
   Do not restart after running the lesson setup, since it creates Python state
   used by later cells.
4. `Includes/Workspace-Setup` is intended for administrators and can create
   instance pools, compute policies and a SQL warehouse, launch jobs, and grant
   privileges to broad groups. Review it and obtain appropriate approval before
   running it; it can incur costs and alter shared workspace resources. Some
   lessons reset or replace their course data and resources.

The pinned Academy library is retained because the newer v5.0.11 changes APIs
used by these notebooks. Neither library version has been validated here on
DBR 15.4.

## Workspace requirements and limitations

- The Academy helper defaults to DBFS mount paths for shared datasets and
  per-user files. Some lessons use `/dbfs/` FUSE paths, local files or JDBC.
  These operations depend on compute access mode, workspace configuration and
  permissions; they may not work in a Unity Catalog-enabled workspace or on
  standard access mode without changes.
- Unity Catalog lessons additionally require a UC-enabled workspace, a metastore
  and suitable catalog, schema and object privileges. Other lessons do not
  necessarily require UC. Do not grant broad privileges solely to bypass an
  error; coordinate with your workspace administrator.
- Jobs, DLT pipelines and SQL lessons require their respective workspace
  features, service permissions, available compute and, in places, Academy
  cluster policies. Old UI instructions may differ from the current interface.
  This course states that it cannot be delivered on Community Edition.
- DBR 13.3 changes Delta `UPDATE`/`MERGE` implicit casts and Parquet timestamp
  inference. Data-dependent exercises may need attention; see the
  [13.3 release notes](https://docs.databricks.com/aws/en/release-notes/runtime/13.3lts).
- DBR 15.4 changes view schema binding and JDBC timestamp calendar defaults;
  review affected exercises against the
  [15.4 release notes](https://docs.databricks.com/aws/en/release-notes/runtime/15.4lts).
- The learner notebook `DE 4.99 - Land New Data` contains a pre-existing
  optional cell with uncommented prose that is not valid Python. Its solution
  notebook does not have that syntax issue.

## Read-only workspace checks

On an existing 15.4 cluster, run these cells in a fresh Python notebook. They do
not invoke course setup, install packages, create tables or modify datasets:

```python
import importlib.util
import sys
from importlib.metadata import version

print("Python:", sys.version)
print("Spark:", spark.version)
print("Runtime key:", spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion", "unavailable"))
print("Academy installed:", importlib.util.find_spec("dbacademy") is not None)
if importlib.util.find_spec("dbacademy") is not None:
    print("Academy version:", version("dbacademy"))
    from dbacademy import dbgems
    from dbacademy.dbhelper import DBAcademyHelper, Paths, CourseConfig, LessonConfig
    print("Academy imports succeeded")
```

```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("string")
def first_letter(value: pd.Series) -> pd.Series:
    return value.str[0]

rows = spark.createDataFrame([("abc",), ("xyz",)], ["value"])
assert [row[0] for row in rows.select(first_letter("value")).collect()] == ["a", "x"]
assert spark.sql("SELECT element_at(array(1, 2), 1)").first()[0] == 1
print("Read-only Spark and Pandas UDF checks passed")
```

Share results and any errors after removing sensitive workspace information.
These probes do not validate installing the wheel, course setup, datasets,
learner or solution labs, Unity Catalog, jobs, DLT, SQL warehouses or write
operations. Those workflows remain unverified and can create or change
resources; review them with an administrator before running them.