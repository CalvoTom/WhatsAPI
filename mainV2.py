import sqlite3

DB_FILE = 'BDD.db'
SQL_FILE = 'BDD.sql'

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

def ajouter_amis(pseudo_utilisateur, pseudo_utilisateur_a_ajouter):
    '''
    Cette fonction permet d'ajouter un amis a un utilisateur précis.

    INPUT
        pseudo_utiur type STR
        pseudo_utilisateur_a_ajouter type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT Not register in UTILISATEUR'
            4 -> 'INPUT already register as friend'
            5 -> 'INPUT are the same'
    '''
    global DB_FILE

    data_util = list_util()['data']
    data_amis = voir_amis(pseudo_utilisateur)['data']

    #test status 1
    if type(pseudo_utilisateur) != str or type(pseudo_utilisateur_a_ajouter) != str:
        return {'status' : 1, 'data' : ['INPUT type not STR']}

    #test status 2
    elif len(pseudo_utilisateur) > 20 or len(pseudo_utilisateur) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}
    elif len(pseudo_utilisateur_a_ajouter) > 20 or len(pseudo_utilisateur_a_ajouter) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}

    #test status 3
    erreur3_1 = True
    erreur3_2 = True
    for i in range (len(data_util)):
        if pseudo_utilisateur == data_util[i]['pseudo_utilisateur']:
            erreur3_1 = False
        if pseudo_utilisateur_a_ajouter == data_util[i]['pseudo_utilisateur']:
            erreur3_2 = False
    if erreur3_1 == True or erreur3_2 == True:
        return {'status' : 3, 'data' : ['INPUT Not register in UTILISATEUR']}

    #test status 4
    for i in range (len(data_amis)):
        if pseudo_utilisateur_a_ajouter == data_amis[i]:
            return {'status' : 4, 'data' : ['INPUT already register as friend']}
    
    #test status 5
    if pseudo_utilisateur == pseudo_utilisateur_a_ajouter :
        return {'status' : 5, 'data' : ['INPUT are the same']}
        
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO AMITIE (util1, util2) VALUES ('{pseudo_utilisateur}','{pseudo_utilisateur_a_ajouter}')")
    conn.commit()
    # Fermeture de la connexion a la bdd
    conn.close()

    return {'status' : 0, 'data' : []}

def voir_amis(pseudo_utilisateur):
    '''
    Cette fonction permet d'afficher le pseudo des personnes qui sont les amis de "pseudo_utilisateur"

    INPUT
        pseudo_utilisateur type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> pseudo_utilisateur type STR, . . . 
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT Not Registered in UTILISATEUR'
    '''
    global DB_FILE
    if type(pseudo_utilisateur) != str:
        return {'status' : 1, 'data' : ['INPUT Type not STR']}

    elif len(pseudo_utilisateur) < 5 or len(pseudo_utilisateur) > 20:
        return {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}

    erreur3 = True
    data3 = list_util()['data']
    for i in range (len(data3)):
        if pseudo_utilisateur == data3[i]['pseudo_utilisateur']:
            erreur3 = False

    if erreur3 == True:
        return {'status' : 3, 'data': ['INPUT Not Registered in UTILISATEUR']}
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"SELECT util2 FROM AMITIE WHERE util1=\'{pseudo_utilisateur}\'")
    rows = cur.fetchall()
    conn.close()
    
    data = []
    for elm in rows:
        data.append(elm[0])

    return({'status' : 0, 'data' : data})

def supprimer_amis(pseudo_utilisateur, pseudo_utilisateur_a_supp):
    '''
    Cette fonction permet de supprimer un ami choisit.

    INPUT
        pseudo_utilisateur type STR
        pseudo_utilisateur_a_supp type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT Not in friendlist'
    '''

    #data_util = list_util()['data']
    data_amis = voir_amis(pseudo_utilisateur)['data']

    if type(pseudo_utilisateur) != str or type(pseudo_utilisateur_a_supp) != str:
        return ({'status' : 1, 'data' : ['INPUT type not STR']})

    elif len(pseudo_utilisateur) <5 or len(pseudo_utilisateur)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})
    elif len(pseudo_utilisateur_a_supp) <5 or len(pseudo_utilisateur_a_supp)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})

    #test status 3
    erreur4 = True
    for i in range (len(data_amis)):
        if  pseudo_utilisateur_a_supp == data_amis[i]:
            erreur4 = False
    if erreur4:    
        return {'status' : 3, 'data' : ['INPUT Not in friendlist']}
            

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM AMITIE WHERE  util1 ='{pseudo_utilisateur}' AND  util2 = '{pseudo_utilisateur_a_supp}'")
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return{'status' :0, 'data' : []}

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
    DB_FILE = 'BDDtest.db'
    execution_SQL("BDD.sql")
    execution_SQL("BDDtest2.sql")

    #teste de list_util() avec une bdd vide
    execution_SQL('BDD.sql')
    assert list_util() == {"status" : 0, "data" : []}
    #teste de list_util() avec une bdd non vide
    execution_SQL('BDDtest2.sql')
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'},{"id_utilisateur": 3, "pseudo_utilisateur": 'Nyn.luk'}]}
	
    #teste de ajouter_util()
    assert ajouter_util('Guilbert') == {"status" : 0, "data" : []}
    assert ajouter_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Le.Boulanger.Qui.Fait.Du.Pain ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Tom.clv') == {"status" : 3, "data" : ['INPUT already in database']}
    #teste de ajouter_util() (état de la bdd après les testes)
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'},{"id_utilisateur" : 3, "pseudo_utilisateur" : 'Nyn.luk'},{"id_utilisateur" : 4, "pseudo_utilisateur" : 'Guilbert'}]}

    #teste de info_util()
    assert info_util('Dorian.jsr') == {"status" : 0, "data": [{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'}]}
    assert info_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert info_util('Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util('util.inexistant') == {"status" : 3, "data": ['INPUT Not in database']}

    #Teste de voir_amis()
    execution_SQL("BDDtest3.sql")
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : ['Dorian.jsr']}
    assert voir_amis('Dorian.jsr') == {'status' : 0, 'data' : ["Tom.clv"]}
    assert voir_amis(5) == {'status' : 1, 'data' : ['INPUT Type not STR']}
    assert voir_amis("1234567891011121314151617181920") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    assert voir_amis("123") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    assert voir_amis("Josseline") == {'status' : 3, 'data' : ['INPUT Not Registered in UTILISATEUR']}

    #test de ajouter_amis()
    assert ajouter_amis('Tom.clv','Nyn.luk') == {"status" : 0, "data": []}
    assert ajouter_amis('Dorian.jsr',1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_amis(1880,'Dorian.jsr') == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_amis('Tom.clv','Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Le.Boulanger.Qui.Fait.Du.Pain','Tom.clv') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Nyn.luk',' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis(' ','Nyn.luk') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Tom.clv','Xx_Michelle_xX') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}
    assert ajouter_amis('Xx_Michelle_xX','Tom.clv') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}
    assert ajouter_amis('Tom.clv','Dorian.jsr') == {"status" : 4, "data": ['INPUT already register as friend']}
    assert ajouter_amis('Tom.clv','Tom.clv') == {"status" : 5, "data": ['INPUT are the same']}
    #Vérification de l'éxécution
    assert voir_amis('Tom.clv') == {"status" : 0, "data": ['Dorian.jsr', 'Nyn.luk']}

    #Teste de supprimer_amis()
    assert supprimer_amis('Tom.clv','Dorian.jsr') == {"status" : 0, "data": []}
    assert supprimer_amis('Dorian.jsr',1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert supprimer_amis(1880,'Dorian.jsr') == {"status" : 1, "data" : ['INPUT type not STR']}
    assert supprimer_amis('Tom.clv','Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis('Le.Boulanger.Qui.Fait.Du.Pain','Tom.clv') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis('Nyn.luk',' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis(' ','Nyn.luk') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis('Dorian.jsr','Nyn.luk') == {"status" : 3, "data" : ['INPUT Not in friendlist']}
    #Vérification de l'éxécution
    assert voir_amis('Tom.clv') == {"status" : 0, "data": ['Nyn.luk']}

    
    DB_FILE = 'BDD.db'

