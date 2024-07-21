from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("ProductCategory").getOrCreate()

products_data = [
    (1, "Product1"),
    (2, "Product2"),
    (3, "Product3"),
    (4, "Product4"),
    (5, "Product5")
]

categories_data = [
    (1, "Category1"),
    (2, "Category2"),
    (3, "Category3")
]

product_category_data = [
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 3)
]

products_df = spark.createDataFrame(products_data, ["product_id", "product_name"])
categories_df = spark.createDataFrame(categories_data, ["category_id", "category_name"])
product_category_df = spark.createDataFrame(product_category_data, ["product_id", "category_id"])

# Джоин продуктов с категориями
product_category_joined_df = products_df.join(product_category_df, "product_id", "left") \
                                        .join(categories_df, "category_id", "left")

# Пары «Имя продукта – Имя категории»
product_category_pairs_df = product_category_joined_df.select("product_name", "category_name") \
                                                      .filter(col("category_name").isNotNull())

# Продукты без категорий
products_without_category_df = products_df.join(product_category_df, "product_id", "left_anti")

# Вывод результатов
product_category_pairs_df.show()
products_without_category_df.show()

spark.stop()