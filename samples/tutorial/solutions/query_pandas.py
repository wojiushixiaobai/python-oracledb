# -----------------------------------------------------------------------------
# query_pandas.py (Section 16.1)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Copyright (c) 2025, Oracle and/or its affiliates.
#
# This software is dual-licensed to you under the Universal Permissive License
# (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl and Apache License
# 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose
# either license.
#
# If you elect to accept the software under the Apache License, Version 2.0,
# the following applies:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import pandas
import pyarrow
import oracledb
import db_config

con = oracledb.connect(
    user=db_config.user, password=db_config.pw, dsn=db_config.dsn
)

# Get an OracleDataFrame
# Adjust arraysize to tune the query fetch performance
odf = con.fetch_df_all(
    statement="select sal from emp order by empno", arraysize=100
)

# Get a Pandas DataFrame from the data
df = pyarrow.Table.from_arrays(
    odf.column_arrays(), names=odf.column_names()
).to_pandas()

# Perform various Pandas operations on the DataFrame

print("\nSum:")
print(df.sum())

print("\nMedian:")
print(df.median())
