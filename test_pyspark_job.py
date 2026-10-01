import pytest
from pyspark.sql import SparkSession

from pyspark_job import clean_data


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("PySparkTests")
        .getOrCreate()
    )

    yield spark

    spark.stop()


def test_clean_data(spark):
    data = [
        ("Ahmed", 100.0),
        ("Sara", -20.0),
        ("Ali", 0.0),
        (None, 50.0),
        ("Mona", 200.0),
    ]

    df = spark.createDataFrame(
        data,
        ["name", "amount"]
    )

    result = clean_data(df)

    rows = result.collect()

    # Only Ahmed and Mona should remain
    assert len(rows) == 2

    names = [row["name"] for row in rows]

    # Valid records are kept
    assert "Ahmed" in names
    assert "Mona" in names

    # Invalid records are removed
    assert "Sara" not in names
    assert "Ali" not in names
    assert None not in names

    # Check amount_with_tax
    result_dict = {
        row["name"]: row["amount_with_tax"]
        for row in rows
    }

    assert result_dict["Ahmed"] == pytest.approx(120.0)
    assert result_dict["Mona"] == pytest.approx(240.0)