import sqlite3

DB_FILE = 'BDDv1.db'
SQL_FILE = 'BDDv1.sql'

def list_util():
    '''
    Cette fonction permet d'afficher tous les utilisateurs de WhatsAPI.

    OUTPUT

        Type Dict {
            status : 
            data : []
            }

        status -> data : 
            0 -> [{id_utilisateur : (type INT), pseudo_utilisateur : (type STR)}, . . . ]
            1 -> 'INPUT Type incorrect'
            2 -> 'INPUT Lenght incorrect'
            3 -> 'INPUT Not Correspond'
    '''
    global DB_FILE, SQL_FILE

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute("SELECT * FROM UTILISATEUR")
    rows = cur.fetchall()
    conn.close()
    
    status = 0
    data = []
    for elm in rows :
        data.append({"id_utilisateur" : elm[0], "pseudo_utilisateur" : elm[1] })
    return { 'status' : status, 'data' : data }


def ajouter_util(pseudo_utilisateur):
    '''
    Cette fonction permet d'ajouter un nouvel utilisateur à la base de donnée.

    INPUT
        pseudo_utilisateur type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status -> data : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT already in database'
    '''
    global DB_FILE, SQL_FILE

    data = list_util()['data']
    #test status 1
    if type(pseudo_utilisateur) != str:
        return {'status' : 1, 'data' : ['INPUT type not STR']}
    #test status 2
    elif len(pseudo_utilisateur) > 20 or len(pseudo_utilisateur) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}
    #test status 3
    for i in range (len(data)):
        if pseudo_utilisateur == data[i]['pseudo_utilisateur']:
            return {'status' : 3, 'data' : ['INPUT already in database']}
        
        
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO UTILISATEUR (pseudo_utilisateur) VALUES ('{pseudo_utilisateur}')")
    conn.commit()
    # Fermeture de la connexion a la bdd
    conn.close()

    return {'status' : 0, 'data' : []}

def info_util(pseudo_utilisateur):
    '''
    Cette fonction permet d'afficher les informations relatives à un utilisateur.

        INPUT
            pseudo_utilisateur type STR

        OUTPUT
    
            Type Dict {
                status : 
                data : []
                }
            
            status : 
                0 -> {id_utilisateur : INT, pseudo_utilisateur : STR,...}
                1 -> 'Type not STR'
                2 -> 'INPUT Lenght not between 5, 20'
                3 -> 'INPUT Not in database'
    '''
    global DB_FILE, SQL_FILE
    #test status 1
    if type(pseudo_utilisateur) != str:
        return ({'status' : 1, 'data' : ['INPUT type not STR']})
    #test status 2
    elif len(pseudo_utilisateur) <5 or len(pseudo_utilisateur)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})
    #test status 3
    erreur3 = True
    data3 = list_util()['data']
    for i in range (len(data3)):
        if pseudo_utilisateur == data3[i]['pseudo_utilisateur']:
            erreur3 = False
            
    if erreur3 == True:
        return {"status" : 3, "data": ['INPUT Not in database']}
    
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute("SELECT * FROM UTILISATEUR")
    rows = cur.fetchall()
    conn.close()

    for elm in rows:
        if elm[1] == pseudo_utilisateur:
            data = [{'id_utilisateur' : elm[0],'pseudo_utilisateur': elm[1]}]
            return({'status' : 0, 'data' : data})
        
def execution_SQL(SQL_FILE):
    global DB_FILE 

    with open(SQL_FILE, 'r') as f :
        createSql = f.read()
    # Placement des requêtes dans un tableau
    sqlQueries = createSql.split(";")

    try:
        # Ouverture de la connexion avec la bdd
        conn = sqlite3.connect(DB_FILE)
        #On active les foreign key
        conn.execute("PRAGMA foreign_keys = 1")
    except sqlite3.Error as e:
        print(e)


    # Execution de toutes les requêtes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)
    # commit des modifications
    conn.commit()
    # fermeture de la connexion
    conn.close()

if __name__ == "__main__":
    DB_FILE = 'BDDv1test.db'

    #teste de list_util() avec une bdd vide
    execution_SQL('BDDv1test1.sql')
    assert list_util() == {"status" : 0, "data" : []}
    #teste de list_util() avec une bdd non vide
    execution_SQL('BDDv1test2.sql')
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'}]}
	
	
    #teste de ajouter_util()
    assert ajouter_util('Nyn.luk') == {"status" : 0, "data" : []}
    assert ajouter_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Le.Boulanger.Qui.Fait.Du.Pain ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Tom.clv') == {"status" : 3, "data" : ['INPUT already in database']}
    #teste de ajouter_util() (état de la bdd après les testes)
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'},{"id_utilisateur" : 3, "pseudo_utilisateur" : 'Nyn.luk'}]}

    #teste de info_util()
    assert info_util('Dorian.jsr') == {"status" : 0, "data": [{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'}]}
    assert info_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert info_util('Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util('util.inexistant') == {"status" : 3, "data": ['INPUT Not in database']}
    
    DB_FILE = 'BDDv1.db'