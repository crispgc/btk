import pymysql


class UCSC:

    db = 'hg19'

    def __init__(self):

        user_data = {
            'hostname': 'genome-mysql.cse.ucsc.edu',
            'username': 'genome',
            'password': '',
            'database': self.db,
        }

        # Create the connection
        conn = pymysql.connect(host=user_data['hostname'],
                               user=user_data['username'],
                               passwd=user_data['password'],
                               db=user_data['database'])

        cur = conn.cursor()
        self.cur = cur

    # Simple routine to run a query on a database and print the results:
    def execute_query(self, query):
        if query == "" or query is None:
            raise Exception("Query is empty")

        self.cur.execute(query)

        data = self.cur.fetchall()

        return data
