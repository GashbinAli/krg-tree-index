from db_handler import execute_query

sql = """
UPDATE tree_data
SET    image_path = REPLACE(image_path, '\\', '/')
WHERE  image_path LIKE '%\\%';
"""
execute_query(sql)
print("✅ Backslashes fixed.")
