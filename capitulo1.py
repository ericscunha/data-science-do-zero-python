from __future__ import division
from collections import Counter, defaultdict


# Dicionário de usuários
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" },
]

# Lista de pares de amizade
friendships = [(0,1), (0,2), (1,2), (1,3), (2,3), (3,4),
               (4,5), (5,6), (5,7), (6,8), (7,8), (8,9)]

# Interesses
interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "progamming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]


# cria um campo friends para item da lista
for user in users:
    user["friends"] = []

for i, j in friendships:
    # isso funciona porque users[i] é o usuário cuja id é i
    users[i]["friends"].append(users[j]) # adiciona i como um amigo de j
    users[j]["friends"].append(users[i]) # adiciona j como um amigo de i

def number_of_friends(user):
    """quantos amigos o usuário tem?"""
    return len(user["friends"])     # tamanho da lista de friends_ids

total_connections = sum(number_of_friends(user) for user in users) # 24
num_users = len(users)                                             # tamanho da lista de usuários
avg_connections = total_connections / num_users                    # 2.4

# cria uma lista (user_id, number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

sorted(num_friends_by_id, key=lambda pair_friends: pair_friends[1], reverse=True)

# Amigos de amigos
def friends_of_friend_ids_bad(user):
    # "foaf" é abreviação de "friend of a friend"
    return [foaf["id"]
            for friend in user["friends"]   # para cada amigo de usuário
            for foaf in friend["friends"]]  # pega cada _their_friends

print(friends_of_friend_ids_bad(users[0]))

# Retorna True se não for o mesmo ID
def not_the_same(user, other_user):
    """dois usuários não são os mesmos se possuem ids diferentes"""
    return user["id"] != other_user["id"]

# Retorna True se não forem amigos
def not_friends(user, other_user):
    """other_user não é um amigo se não está em user["friends"];
    isso é, se é not_the_same com todos as pessoas em user["friends"]"""
    return all(not_the_same(friend, other_user)
               for friend in user["friends"])

# Amigos de amigos: apresenta a quantidade de amigos em comuns de um não amigo
def friends_of_friend_ids(user):
    return Counter(foaf["id"]
                   for friend in user["friends"]   # para cada um dos meus amigos
                   for foaf in friend["friends"]   # que contam *their* amigos
                   if not_the_same(user, foaf)     # que não sejam eu
                   and not_friends(user, foaf))    # e que nã sejam meus amigos

print(friends_of_friend_ids(users[0]))
print(friends_of_friend_ids(users[3]))   # Counter({0: 2, 5: 1})

# retorna usuários que possuem o interesse informado
def data_scientists_who_like(target_interest):
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]

print("Usuários que se interessam por 'machine learning': {}".format(data_scientists_who_like("machine learning")))

# as chaves são interesses, os valores são listas de user_ids com interests
user_ids_by_interest = defaultdict(list)

# Organiza usuários por interesse
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

print("Usuários por interesse 'Big Data': {}".format(user_ids_by_interest["Big Data"]))

# as chaves são user_ids, os valores são as listas de interesses para aquele user_id
interests_by_user_id = defaultdict(list)

# Organiza os interesses de cada usuário
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

print("Interesses do usuário 0: {}".format(interests_by_user_id[0]))

# Usuários com interesses comuns (quantidade)
# Itera sobre os usuários
# Para cada interesse, itera sobre os outros usuários com aquele interesse
# Mantém a contage de quantas vezes vemos cada outro usuário
def most_commom_intrests_with(user):
    return Counter(interested_user_id
                   for interest in interests_by_user_id[user["id"]]
                   for interested_user_id in user_ids_by_interest[interest]
                   if interested_user_id != user["id"])

print("Qtd. de interesses comuns por usuário em relação ao usuário 0: {}".format(most_commom_intrests_with(users[0])))
