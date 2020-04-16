import psycopg2, os

conn = psycopg2.connect(
	host="database-1.cjpoxlvxbftx.us-east-1.rds.amazonaws.com",
	port = 5432,
	database="postgres",
	user="team128user",
	password="Xvo3dVJCCX8nPhuOWJWz"
)

cur = conn.cursor()

# Below are a list of tables within the database.
# select * from stocks_fundamental;
# select * from stocks_indexesday;
# select * from stocks_indexesmin;
# select * from stocks_nasdaqday;
# select * from stocks_nasdaqmin;
# select * from stocks_nyseday;
# select * from stocks_nysemin;


cur.execute("""SELECT * from stocks_nysemin""")
query_results = cur.fetchall()
query_results = [row for row in query_results]

for row in query_results:
	print(row[0])


cur.close()
conn.close()