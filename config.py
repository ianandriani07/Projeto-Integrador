import urllib.parse

class Config(object):
    SECRET_KEY = 'Extradigital'
    
    # Formate corretamente a string de conexão com ODBC
    odbc_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:projetopi.database.windows.net,1433;"
        "Database=DB_FORMULARIOS;"
        "Uid=projetopi;"
        "Pwd=Forw@rd123;"  # Substitua 'Teste' pela sua senha real
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    # Codifique a string ODBC
    params = urllib.parse.quote_plus(odbc_str)
    
    # Construa a URI completa
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
