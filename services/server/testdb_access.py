import psycopg2

conn = psycopg2.connect(host="database-1.cjpoxlvxbftx.us-east-1.rds.amazonaws.com", port = 5432,
	database="database-1",
	user="team128user",
	password="Xvo3dVJCCX8nPhuOWJWz")

cur = conn.cursor()


cur.execute("""SELECT 1""")
query_results = cur.fetchall()
print(query_results)


cur.close()
conn.close()