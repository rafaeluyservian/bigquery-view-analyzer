import re
import pytest

from bigquery_view_analyzer.analyzer import (
    STANDARD_SQL_TABLE_PATTERN,
    LEGACY_SQL_TABLE_PATTERN,
)


valid_standard_table_references = [
    "`project.dataset.table`",
    "`project`.dataset.table",
    "`project.dataset`.table",
    "`project`.`dataset`.`table`",
]

invalid_standard_table_references = [
    "project.`dataset`.table",
    "project.`dataset.table`",
    "project.dataset.`table`",
    "project.dataset.table",
]

legacy_table_references = ["[project:dataset.table]", "[dataset.table]"]
join_prefix = ["", "INNER", "LEFT", "RIGHT", "CROSS", "FULL OUTER"]


@pytest.mark.parametrize("table_a", valid_standard_table_references)
@pytest.mark.parametrize("table_b", valid_standard_table_references)
@pytest.mark.parametrize("join_prefix", join_prefix)
def test_valid_standard_table_reference_in_view(table_a, table_b, join_prefix):
    sql_ddl = """
    SELECT
        table_a.id
        ,table_a.field_a
        ,table_b.field_b
        ,table_b.field_a AS different_field_a
    FROM
        {table_a} AS table_a
    {join_prefix} JOIN
        {table_b} AS table_b
    """.format(
        table_a=table_a, table_b=table_b, join_prefix=join_prefix
    )
    match = re.findall(
        STANDARD_SQL_TABLE_PATTERN, sql_ddl, re.IGNORECASE | re.MULTILINE
    )
    assert match is not None
    assert len(match) == 2  # find both table a and b


@pytest.mark.parametrize("table_a", invalid_standard_table_references)
@pytest.mark.parametrize("table_b", invalid_standard_table_references)
@pytest.mark.parametrize("join_prefix", join_prefix)
def test_invalid_standard_table_reference_in_view(table_a, table_b, join_prefix):
    sql_ddl = """
    SELECT
        table_a.id
        ,table_a.field_a
        ,table_b.field_b
        ,table_b.field_a AS different_field_a
    FROM
        {table_a} AS table_a
    {join_prefix} JOIN
        {table_b} AS table_b
    """.format(
        table_a=table_a, table_b=table_b, join_prefix=join_prefix
    )
    match = re.findall(
        STANDARD_SQL_TABLE_PATTERN, sql_ddl, re.IGNORECASE | re.MULTILINE
    )
    assert match == []


@pytest.mark.parametrize("table_a", legacy_table_references)
@pytest.mark.parametrize("table_b", legacy_table_references)
@pytest.mark.parametrize("join_prefix", join_prefix)
def test_legacy_table_reference_in_view(table_a, table_b, join_prefix):
    sql_ddl = """
    SELECT
        table_a.id
        ,table_a.field_a
        ,table_b.field_b
        ,table_b.field_a AS different_field_a
    FROM
        {table_a} AS table_a
    {join_prefix} JOIN
        {table_b} AS table_b
    """.format(
        table_a=table_a, table_b=table_b, join_prefix=join_prefix
    )
    match = re.findall(LEGACY_SQL_TABLE_PATTERN, sql_ddl, re.IGNORECASE | re.MULTILINE)
    assert match is not None
    assert len(match) == 2  # find both table a and b
