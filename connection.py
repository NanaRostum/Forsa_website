from mysql import connector

conn= connector.connect(
    host= "127.0.0.1",
    user= "root",
    password = "password",
    database = "test_db",
    port = 3307 
)

