def getURI():
    POSTGRES = {
        'user': 'iexjbzgokmyxlg',
        'pw': '276eb739dac0baa74caab92ea6864cd208624960df664675423e1a809831217e',
        'db': 'appdb',
        'host': 'localhost',
        'port': '5432',
    }
    # return 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    return "postgresql://postgres:password@127.0.0.1:5432/appdb";

if __name__ == '__main__':
    getURI()
