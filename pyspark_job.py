from pyspark.sql import functions as F


def clean_data(df):
    # Remove rows where amount <= 0
    df = df.filter(F.col("amount") > 0)

    # Remove rows where name is NULL
    df = df.filter(F.col("name").isNotNull())

    # Add amount_with_tax column
    df = df.withColumn(
        "amount_with_tax",
        F.col("amount") * 1.20
    )

    return df