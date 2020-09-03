f = open('login_credentials.csv')
tf = f.readlines()
header = tf[0]
num_stud = (len(tf) - 1) // 3
of1 = open('login_credentials1.csv', mode='w')
of2 = open('login_credentials2.csv', mode='w')
of3 = open('login_credentials3.csv', mode='w')

tf1 = tf[:num_stud]
tf2 = tf[num_stud:2*num_stud]
tf2.insert(0, header)
tf3 = tf[2*num_stud:]
tf3.insert(0, header)

of1.writelines(tf1)
of2.writelines(tf2)
of3.writelines(tf3)

f.close()
of1.close()
of2.close()
of3.close()