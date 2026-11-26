# Databricks Data Engineer study notebooks

This repository contains Databricks Academy Data Engineering notebooks and
solutions, originally built in 2023 for Databricks Runtime (DBR) 11.3. This
copy targets DBR 13.3 LTS; its changes have only been checked statically and
have **not** been run or certified on a Databricks workspace. Course content
has not been updated against the current certification exam.

## Runtime and compute

DBR 13.3 LTS reached end of support on August 22, 2026. Databricks removes
end-of-support runtimes from the compute UI; until end of life they may still
be usable through the [cluster creation API](https://docs.databricks.com/api/workspace/clusters/create),
subject to workspace policies, cloud availability and permissions. See the
[end-of-support history](https://docs.databricks.com/aws/en/release-notes/runtime/eos)
and consider a [currently supported runtime](https://docs.databricks.com/aws/en/release-notes/runtime/)
for other work.

The shared course setup accepts these runtime keys:

- `13.3.x-scala2.12`
- `13.3.x-photon-scala2.12`
- `13.3.x-cpu-ml-scala2.12`

Availability and behavior of each variant are unverified. `Includes/Workspace-Setup`
defaults to the CPU ML key, and its widget can select another course runtime.
Set the `spark_version` field when creating compute via the API, using a valid
cluster configuration and any policy required by your workspace. SQL warehouses
and Delta Live Tables (DLT) pipelines use separately managed compute or pipeline
channels; selecting DBR 13.3 for a notebook does not pin their runtime.

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
   lesson. Restarting clears Python state. DBR 13.3 does not automatically
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
DBR 13.3.

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
- The learner notebook `DE 4.99 - Land New Data` contains a pre-existing
  optional cell with uncommented prose that is not valid Python. Its solution
  notebook does not have that syntax issue.

## Suggested workspace smoke test

When an appropriate workspace is available, first verify compute creation and
the pinned wheel, then run one learner and one solution setup and check dataset
access. Exercise representative PySpark, SQL and Delta labs, followed by
streaming, jobs, DLT, SQL warehouse and Unity Catalog lessons where their
prerequisites are available. Confirm results and cleanup in an isolated
workspace before relying on the course. None of these steps has been executed
as part of this migration.