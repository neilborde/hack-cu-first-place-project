def getURI():
    POSTGRES = {
        'user': 'postgres',
        'pw': 'password',
        'db': 'appdb',
        'host': 'localhost',
        'port': '5432',
    }
    # return 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    return "postgresql://postgres:password@127.0.0.1:5432/appdb";

if __name__ == '__main__':
    getURI()
