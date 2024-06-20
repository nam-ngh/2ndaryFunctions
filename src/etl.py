import oracledb
import threading

def thread_query_oracle(
        user: str, password: str, dsn: str, queries: list,
        pool_min: int=8, pool_max: int=8, pool_incr=1,
):
    # list of result dfs:
    dfs = []
    # create connection pool:
    pool = oracledb.create_pool(
        user=user, password=password, dsn=dsn,
        min=pool_min, max=pool_max, increment=pool_incr, 
        getmode=oracledb.POOL_GETMODE_WAIT,
    )
    # query exec function:
    def execute_query(qry):
        con = pool.acquire()
        df = pd.read_sql(qry, con)
        dfs.append(df)
        con.close()
    # initiate threads:
    threads = []
    for q in queries:
        thread = threading.Thread(target=execute_query, args=(q,))
        thread.start()
        threads.append(thread)
    # run threads:
    for i, thread in enumerate(threads):
        thread.join()
        print(f'Completed thread {i + 1}!', end='\r')

    return dfs