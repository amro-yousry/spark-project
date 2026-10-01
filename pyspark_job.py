from pyspark.sql import functions as F


# Clean transaction data and calculate the amount including tax
def clean_data(df):
    df = df.filter(F.col("amount") > 0)

    df = df.filter(F.col("name").isNotNull())

    df = df.withColumn(
        "amount_with_tax",
        F.col("amount") * 1.20
    )

    return df
