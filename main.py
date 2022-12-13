import time
import mysql.connector
import random
from prettytable import PrettyTable
import time

db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="game"
    )

if db.is_connected():
    print('database berhasil disambungkan')

global cursor
global user_signedin
cursor= db.cursor()

def user_register():
    # input all field
    email = input("email : ")
    username = input("username : ")
    password = input("password : ")

    id = random.randint(2,100000000)

    sql = "INSERT INTO user (id_user, email, username, password, exp, lencana, emas, jamu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, email, username, password, 1, 0, 10000, 10000)
    cursor.execute(sql, val)

    db.commit()

    print("{} data ditambahkan".format(cursor.rowcount))

    user_login()

def user_login():
    print("Login")
    username = input("username : ")
    password = input("password : ")

    sql = "SELECT * FROM user WHERE username=%s AND password=%s"
    val = (username, password)
    cursor.execute(sql, val)

    results = cursor.fetchall()

    if(results):
        print('berhasil login')
        user_signedin = results[0][0]
        home(user_signedin)
    else:
        print('username atau password salah')

def home(user_signedin):
    while (True):
        print('Silahkan pilih menu-menu di bawah ini :')
        print("1. Info profil")
        print("2. tambah bangunan")
        print("3. upgrade bangunan")
        print("4. latih prajurit")
        print("5. upgrade prajurit")
        print("6. lakukan serangan")
        print("7. logout")

        try:
            inputan = int(input('masukkan pilihan anda : '))

            if (inputan == 1):
                lihat_profil(user_signedin)
            elif (inputan == 2):
                construction(user_signedin)
            elif (inputan == 3):
                upgradebangunan(user_signedin)
            elif (inputan == 4):
                trainning(user_signedin)
            elif (inputan == 5):
                upgrade(user_signedin)
            elif (inputan == 6):
                attack(user_signedin)
            elif (inputan == 7):
                break

        except Exception as e:
            print("masukan anda salah", e)

def lihat_profil(user_signedin):
    cursor.execute(f"SELECT * FROM user WHERE id_user ={user_signedin}")
    user= cursor.fetchall()
    print(user)

    print("---------Profile----------")
    print("Id User           | ", user[0][0])
    print("Username          | ", user[0][3])
    print("Experience        | ", user[0][4])
    print("Jumlah Lencana    | ", user[0][5])
    print("Jumlah Emas       | ", user[0][6])
    print("Jumlah Jamu       | ", user[0][7])
    print("")

    # bangunan
    cursor.execute(f"SELECT level, nama_bangunan, deskripsi FROM detail_balai_desa INNER JOIN balai_desa USING (id_balai_desa) INNER JOIN bangunan USING (id_bangunan) WHERE id_user={user_signedin}")
    balai_desa = cursor.fetchall()

    cursor.execute(f"SELECT level, kerusakan, target, jangkauan, harga, nama_bangunan, HP_bangunan FROM detail_pertahanan INNER JOIN pertahanan USING (id_pertahanan) INNER JOIN bangunan USING (id_bangunan) WHERE id_user ={user_signedin}")
    pertahanan = cursor.fetchall()

    cursor.execute(
        f"SELECT level, harga, nama_bangunan, HP_bangunan FROM detail_padepokan INNER JOIN padepokan USING (id_padepokan) INNER JOIN bangunan USING (id_bangunan) WHERE id_user ={user_signedin}")
    padepokan = cursor.fetchall()

    cursor.execute(
        f"SELECT level, laju_produksi, kapasitas_terpenuhi, kapasitas_total, harga, nama_bangunan, HP_bangunan FROM detail_pengumpul INNER JOIN pengumpul USING (id_pengumpul) INNER JOIN bangunan USING (id_bangunan) WHERE id_user ={user_signedin}")
    pengumpul = cursor.fetchall()

    cursor.execute(
        f"SELECT level,persentase,  kapasitas_total, harga, nama_bangunan, HP_bangunan FROM detail_penampung INNER JOIN penampung USING (id_penampung) INNER JOIN bangunan USING (id_bangunan) WHERE id_user ={user_signedin}")
    penampung = cursor.fetchall()

    print("----------bangunan----------")
    table_balai_desa = PrettyTable(["level", "nama bangunan", "deskripsi"])
    for i in range(len(balai_desa)):
        table_balai_desa.add_row([balai_desa[0][0], balai_desa[0][1], balai_desa[0][2]])
    print(table_balai_desa)

    print("")
    print("pertahanan")
    table_pertahanan = PrettyTable(["level","kerusakan", "target","jangkauan", "harga", "nama bangunan", "HP_bangunan"])
    for i in range(len(pertahanan)):
        table_pertahanan.add_row([ pertahanan[i][j] for j in range(7)])
    print(table_pertahanan)

    print("")
    print("padepokan")
    table_padepokan = PrettyTable(
        ["level", "harga", "nama bangunan", "HP_bangunan"])
    for i in range(len(padepokan)):
        table_padepokan.add_row([padepokan[i][j] for j in range(4)])
    print(table_padepokan)

    print("")
    print("pengumpul")
    table_pengumpul = PrettyTable(
        ["level","laju produksi", "kapasitas terpenuhi", "kapasitas total", "harga", "nama bangunan", "hp bangunan"])
    for i in range(len(pengumpul)):
        table_pengumpul.add_row([pengumpul[i][j] for j in range(7)])
    print(table_pengumpul)

    print("")
    print("penampung")
    table_penampung = PrettyTable(
        ["level","persentase", "kapasitas total", "harga", "nama bangunan", "HP bangunan"])
    for i in range(len(penampung)):
        table_penampung.add_row([penampung[i][j] for j in range(6)])
    print(table_penampung)


    # prajurit
    cursor.execute(f"SELECT jumlah_pasukan, level, kerusakan, hp_prajurit,Nama_prajurit, prajurit.kapasitas, target, harga FROM kamp_pasukan INNER JOIN detail_pasukan USING (id_pasukan) INNER JOIN detail_prajurit ON detail_pasukan.id_detail_pasukan = detail_prajurit.id_prajurit INNER JOIN prajurit USING (id_prajurit) WHERE id_user={user_signedin}")
    semua_pasukan = cursor.fetchall()
    print(semua_pasukan)
    print("Pasukan yang dimiliki")
    table_pasukan = PrettyTable(
        ["jumlah pasukan","level", "kerusakan", "hp prajurit", "Nama Prajurit", "kapasitas", "target","harga"])
    for i in range(len(semua_pasukan)):
        table_pasukan.add_row([semua_pasukan[i][j] for j in range(8)])
    print(table_pasukan)



def attack(user_signedin):
    stop = False
    while not(stop):
        print('user menyerang')
        messages = [
            "lari terbirit-birit", "sudah meninggoy", "kabur","menembak pertahanan lawan", "menyerang dari sebelah kiri","sedang makan sate di warung pak Slamet","mengeroyok menara pemanah","melempar sabun"
        ]

        messages2 = [
            "disambar petir","ditelan bumi","rusak terporak poranda","kesenggol dikit tumbang","hancur lebur","lecet dikit","tumbang"
        ]
        # get all user
        cursor.execute(f"SELECT * FROM user WHERE NOT id_user={user_signedin}")

        users = cursor.fetchall()

        # cari user secara random
        idx = random.randint(0, len(users)-1)
        print('idx',idx)
        print('selected user',users[idx])
        selected_user = users[idx]

        # user memilih musuh
        cursor.execute(
            f"SELECT level, kerusakan, target, jangkauan, harga, nama_bangunan, HP_bangunan FROM detail_pertahanan INNER JOIN pertahanan USING (id_pertahanan) INNER JOIN bangunan USING (id_bangunan) WHERE id_user ={selected_user[0]}")
        pertahanan = cursor.fetchall()

        power_of_defense = sum([defense[1] for defense in pertahanan]) if len(pertahanan) > 0 else 0
        hp_of_defense = sum([defense[6] for defense in pertahanan]) if len(pertahanan) > 0 else 0
        print('kekuatan pertahanan :',power_of_defense)
        print('hp pertahanan :',hp_of_defense)
        print("")
        print("Apakah ingin menyerang?")
        print("1. ya")
        print("2. lewatkan")
        decision = int(input('masukkan pilihan : '))

        if(decision == 1):
            print('anda menyerang')
            cursor.execute(
                f"SELECT jumlah_pasukan, level, kerusakan, hp_prajurit,Nama_prajurit, prajurit.kapasitas, target, harga FROM kamp_pasukan INNER JOIN detail_pasukan USING (id_pasukan) INNER JOIN detail_prajurit ON detail_pasukan.id_detail_pasukan = detail_prajurit.id_prajurit INNER JOIN prajurit USING (id_prajurit) WHERE id_user={user_signedin}")
            pasukan_penyerang = cursor.fetchall()

            attackers_power = sum([int(tentara[2])*int(tentara[0]) for tentara in pasukan_penyerang]) if len(pasukan_penyerang) > 0 else 0
            attackers_hp = sum([int(tentara[3]) for tentara in pasukan_penyerang]) if len(pasukan_penyerang) > 0 else 0

            print("")
            print("kekuatan penyerang",attackers_power)
            print("hp penyerang",hp_of_defense)

            war = 1
            while war <= 12:
                idx_luar_defense = random.randint(0,len(pertahanan)-1)
                idx_luar_attack = random.randint(0, len(pasukan_penyerang)-1)
                message = messages[random.randint(0,len(messages)-1)]
                message2 = messages2[random.randint(0,len(messages2)-1)]
                if(war % 2 == 0):
                    print(pertahanan[idx_luar_defense][5],message2)
                else:
                    print(pasukan_penyerang[idx_luar_attack][4], message)
                time.sleep(3)
                war+=1

            r1 = attackers_power - hp_of_defense
            r2 = power_of_defense - attackers_hp

            print('penyerangan ke pertahanan',r1)
            print('pertahanan ke penyerang',r2)

            if(r1 > r2):
                print('Pertahanan telah takluk')

            if(r2 >= r1):
                print('Penyerang gagal menaklukkan desa, desa berhasil dipertahankan')

            stop=True
        else:
            pass
        # lakukan serangan


            #


def trainning(id_user):
    print("========Daftar Prajurit=========")
    cursor.execute("SELECT * FROM prajurit")
    data = cursor.fetchall()
    cursor.execute(f"SELECT id_pasukan,kapasitas FROM kamp_pasukan WHERE id_user ={id_user}")
    data_id_kapasitas = cursor.fetchall()
    id_pasukan = data_id_kapasitas[0][0]

    cursor.execute(f"SELECT id_detail_pasukan, jumlah_pasukan FROM detail_pasukan WHERE id_pasukan={id_pasukan}")
    listpasukan = cursor.fetchall()

    kapasistasterpenuhi = 0
    for i in range(len(listpasukan)):
        cursor.execute(f"SELECT kapasitas FROM prajurit WHERE id_prajurit={listpasukan[i][0]}")
        kapasitasperpasukan = cursor.fetchall()
        kapasistasterpenuhi += (int(listpasukan[i][1]) * int(kapasitasperpasukan[0][0]))
    print(f"kapasitas terpenuhi : {kapasistasterpenuhi}")

    kapasitas = int(data_id_kapasitas[0][1]) - kapasistasterpenuhi
    cursor.execute(f"SELECT * FROM detail_prajurit where id_pasukan={id_pasukan}")
    data2 = cursor.fetchall()
    print(f"Kapasitas Kamp tersedia = {kapasitas}")

    myTable = PrettyTable(["Nama Prajurit", "kapasitas", "target", "level","kerusakan","HP","Harga"])

    for i in range(len(data)):
        myTable.add_row([data[i][1], data[i][3], data[i][4], data2[i][1],data2[i][2],data2[i][3],data[i][5]])
        # print(data[i][0], " | Nama Prajurit : ", data[i][1], " | kapasitas : ", data[i][3], " | target : ", data[i][4],
        #       " | level : ", data2[i][1], " | kerusakan : ", data2[i][2], " | HP : ", data2[i][3], " | Harga : ",
        #       data[i][5])
    print(myTable)
    print("\n")

    jalan = True
    while jalan and kapasitas != 0:
        print("pilih pasukan anda")
        no = input("masukkan id pasukan : ")
        if no in "23456789":
            jumlah = int(input("masukkan jumlah pasukan : "))
            cursor.execute(f"SELECT kapasitas,harga FROM prajurit WHERE id_prajurit ={no}")
            kapasitas2 = cursor.fetchall()
            hargatotal = int(kapasitas2[0][1]) * jumlah
            kapasitas_pasukan = jumlah * int(kapasitas2[0][0])
            if kapasitas_pasukan <= kapasitas:
                cursor.execute(
                    f"SELECT id_detail_pasukan, jumlah_pasukan FROM detail_pasukan WHERE id_detail_pasukan ={no} && id_pasukan={id_pasukan}")
                cektable = cursor.fetchall()
                cursor.execute(f"SELECT jamu FROM user WHERE id_user={id_user}")
                jamudimiliki = cursor.fetchall()
                sisajamu = int(jamudimiliki[0][0]) - hargatotal
                if sisajamu <= 0:
                    print("Sisa jamu tidak mencukupi")
                else:
                    if len(cektable) == 0:
                        cursor.execute(
                            f"INSERT INTO detail_pasukan (id_detail_pasukan, jumlah_pasukan, id_pasukan) VALUES ('{no}', '{jumlah}', '{id_pasukan}');")
                        db.commit()
                    else:
                        jumlahlama = cektable[0][1]
                        jumlahbaru = int(jumlahlama) + jumlah
                        cursor.execute(
                            f"UPDATE detail_pasukan SET jumlah_pasukan='{jumlahbaru}' WHERE id_detail_pasukan ={no} && id_pasukan={id_pasukan}")
                        db.commit()
                        cursor.execute(f"UPDATE user SET jamu={sisajamu} WHERE id_user={id_user}")
                        db.commit()
                kapasitas -= kapasitas_pasukan
            else:
                print("kapasitas tidak cukup")
            print(f"kapasitas tersedia : {kapasitas}")
        else:
            print("Pilihan tidak tersedia")
        if kapasitas == 0:
            print("kapasitas penuh")
            break
        stop = input("lagi atau tidak? (y/t)")
        if stop == "t":
            break
    cursor.execute(f"SELECT id_detail_pasukan, jumlah_pasukan FROM detail_pasukan WHERE id_pasukan={id_pasukan}")
    listpasukan = cursor.fetchall()
    print("list pasukan : ", listpasukan)
    return listpasukan


# trainning(1)

def upgrade(id_user):
    print("========Daftar Prajurit=========")
    cursor.execute("SELECT * FROM prajurit")
    data = cursor.fetchall()
    cursor.execute(f"SELECT id_pasukan FROM kamp_pasukan WHERE id_user ={id_user}")
    data_id = cursor.fetchall()
    id_pasukan = data_id[0][0]
    cursor.execute(f"SELECT * FROM detail_prajurit WHERE id_pasukan={id_pasukan}")
    data2 = cursor.fetchall()
    myTable = PrettyTable(["Nama Prajurit", "kapasitas", "target", "level", "kerusakan", "HP", "Harga"])
    for i in range(len(data)):
        myTable.add_row([data[i][1], data[i][3], data[i][4], data2[i][1], data2[i][2], data2[i][3], data[i][5]])
        # print(data[i][0], " | Nama : ", data[i][1], " | kapasitas : ", data[i][3], " | target : ", data[i][4],
        #       " | level : ", data2[i][1], " | kerusakan : ", data2[i][2], " | HP : ", data2[i][3], " | Harga : ",
        #       data[i][5])
    print(myTable)
    print("\n")
    print("pilih prajurit yang akan diupgrade")

    no = input("masukkan id prajurit : ")
    if no in "23456789":
        cursor.execute(f"SELECT * FROM prajurit WHERE id_prajurit={no}")
        data3 = cursor.fetchall()
        cursor.execute(f"SELECT * FROM detail_prajurit WHERE id_pasukan={id_pasukan} && id_prajurit={no}")
        data4 = cursor.fetchall()
        harga = int(data3[0][5]) * int(data4[0][1]) * 10
        pilihan = input(f"apakah anda yakin akan meningkatkan {data3[0][1]} dengan harga {harga} (y/t)")
        cursor.execute(f"SELECT jamu FROM user WHERE id_user ={id_user}")
        data_jamu = cursor.fetchall()
        jamu = int(data_jamu[0][0])
        print(f"Sisa Jamu : {jamu}")
        if pilihan == "y":
            level = int(data4[0][1]) + 1
            kerusakan = int(data4[0][2]) + 5
            hp = int(data4[0][3]) + 5
            cursor.execute(
                f"UPDATE detail_prajurit SET level={level}, kerusakan={kerusakan}, hp_prajurit={hp} WHERE id_prajurit={no} && id_pasukan={id_pasukan}")
            db.commit()
            sisajamu = int(jamu[0][0]) - harga
            cursor.execute(f"UPDATE user SET jamu={sisajamu} WHERE id_user={id_user}")
            db.commit()
            print("berhasil meningkatkan")
        else:
            print("anda membatalkan operasi")
    else:
        print("pilihan tidak tersedia")


# upgrade(1)


def collect(id_user):
    cursor.execute(f"SELECT id_pengumpul FROM detail_pengumpul WHERE id_user={id_user}")
    data_id_pengumpul = cursor.fetchall()
    for i in range(1, int(len(data_id_pengumpul)) + 1):
        if data_id_pengumpul[0][0] == '1':
            cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
            emas_yang_dimiliki = cursor.fetchall()
            cursor.execute(
                f"SELECT kapasitas_total FROM detail_penampung WHERE id_user={id_user} && id_detail_penampung={i}")
            kapasitas_emas = cursor.fetchall()
            cursor.execute(
                f"SELECT kapasitas_terpenuhi FROM detail_pengumpul WHERE id_user={id_user} && id_detail_pengumpul={i}")
            emas_terkumpul = cursor.fetchall()
            if int(kapasitas_emas[0][0]) >= int(emas_terkumpul[0][0]) + int(emas_yang_dimiliki[0][0]):
                emas_baru = int(emas_yang_dimiliki[0][0]) + int(emas_terkumpul[0][0])
                cursor.execute(f"UPDATE user SET emas={emas_baru} WHERE id_user={id_user}")
                db.commit()
        elif data_id_pengumpul[0][0] == '2':
            cursor.execute(f"SELECT jamu FROM user WHERE id_user={id_user}")
            jamu_yang_dimiliki = cursor.fetchall()
            cursor.execute(
                f"SELECT kapasitas_total FROM detail_penampung WHERE id_user={id_user} && id_detail_penampung={i}")
            kapasitas_jamu = cursor.fetchall()
            cursor.execute(
                f"SELECT kapasitas_terpenuhi FROM detail_pengumpul WHERE id_user={id_user} && id_detail_pengumpul={i}")
            jamu_terkumpul = cursor.fetchall()
            if int(kapasitas_jamu[0][0]) >= int(jamu_terkumpul[0][0]) + int(jamu_yang_dimiliki[0][0]):
                jamu_baru = int(jamu_yang_dimiliki[0][0]) + int(jamu_terkumpul[0][0])
                cursor.execute(f"UPDATE user SET jamu={jamu_baru} WHERE id_user={id_user}")
                db.commit()


# collect(1)


def construction(id_user):
    cursor.execute(f"SELECT id_bangunan,nama_bangunan FROM bangunan")
    bangunan = cursor.fetchall()
    print("============Daftar Bangunan=========")
    for i in range(1, len(bangunan)):
        print(f"id : {bangunan[i][0]} | Nama : {bangunan[i][1]}")
    pilihan = input("masukkan id bangunan yang akan dibangun : ")
    if pilihan in "23456789" or pilihan == "10" or pilihan == "11":
        cursor.execute(f"SELECT tipe FROM bangunan where id_bangunan={pilihan}")
        tipe = cursor.fetchall()
        tipe = tipe[0][0]
        if tipe == "padepokan":
            cursor.execute(f"SELECT id_detail_padepokan FROM detail_padepokan WHERE id_user={id_user}")
            n_padepokan = cursor.fetchall()
            if len(n_padepokan) < 1:
                cursor.execute(
                    f"INSERT INTO detail_padepokan (persentase,level,id_user,id_padepokan) VALUES (100,1,{id_user},1)")
                db.commit()
            else:
                print("Anda seudah membuat padepokan")
        elif tipe == "pertahanan":
            cursor.execute(f"SELECT id_pertahanan FROM detail_pertahanan WHERE id_user={id_user}")
            pertahanan_yang_ada = cursor.fetchall()
            pertahanan_dimiliki = []
            for i in range(len(pertahanan_yang_ada)):
                pertahanan_dimiliki.append(f"{pertahanan_yang_ada[i][0]}")
            if pilihan in pertahanan_dimiliki:
                print("Anda sudah memiliki bangunan ini")
            else:
                if pilihan == "3":
                    cursor.execute(
                        f"INSERT INTO detail_pertahanan (persentase,level,kerusakan,id_user,id_pertahanan) VALUES (100,1,10,{id_user},1)")
                    db.commit()
                elif pilihan == "4":
                    cursor.execute(
                        f"INSERT INTO detail_pertahanan (persentase,level,kerusakan,id_user,id_pertahanan) VALUES (100,1,15,{id_user},2)")
                    db.commit()
                elif pilihan == "9":
                    cursor.execute(
                        f"INSERT INTO detail_pertahanan (persentase,level,kerusakan,id_user,id_pertahanan) VALUES (100,1,30,{id_user},3)")
                    db.commit()
                elif pilihan == "10":
                    cursor.execute(
                        f"INSERT INTO detail_pertahanan (persentase,level,kerusakan,id_user,id_pertahanan) VALUES (100,1,35,{id_user},4)")
                    db.commit()
                elif pilihan == "11":
                    cursor.execute(
                        f"INSERT INTO detail_pertahanan (persentase,level,kerusakan,id_user,id_pertahanan) VALUES (100,1,35,{id_user},5)")
                    db.commit()
                print("Bangunan berhasil ditambahkan")
        elif tipe == "pengumpul":
            cursor.execute(f"SELECT id_pengumpul FROM detail_pengumpul WHERE id_user={id_user}")
            pengumpul_yang_ada = cursor.fetchall()
            pengumpul_dimiliki = []
            for i in range(len(pengumpul_yang_ada)):
                pengumpul_dimiliki.append(f"{pengumpul_yang_ada[i][0]}")
            if pilihan in pengumpul_dimiliki:
                print("Anda sudah memiliki bangunan ini")
            else:
                if pilihan == "7":
                    cursor.execute(
                        f"INSERT INTO detail_pengumpul (persentase,level,laju_produksi,kapasitas_terpenuhi,kapasitas_total,id_user,id_pengumpul) VALUES (100,1,5,0,5000,{id_user},1)")
                    db.commit()
                elif pilihan == "8":
                    cursor.execute(
                        f"INSERT INTO detail_pengumpul (persentase,level,laju_produksi,kapasitas_terpenuhi,kapasitas_total,id_user,id_pengumpul) VALUES (100,1,5,0,5000,{id_user},2)")
                    db.commit()
                print("Bangunan berhasil ditambahkan")
        elif tipe == "penampung":
            cursor.execute(f"SELECT id_penampung FROM detail_penampung WHERE id_user={id_user}")
            penampung_yang_ada = cursor.fetchall()
            penampung_dimiliki = []
            for i in range(len(penampung_yang_ada)):
                penampung_dimiliki.append(f"{penampung_yang_ada[i][0]}")
            if pilihan in penampung_dimiliki:
                print("Anda sudah memiliki bangunan ini")
            else:
                if pilihan == "5":
                    cursor.execute(
                        f"INSERT INTO detail_penampung (persentase,level,kapasitas_total,id_user,id_penampung) VALUES (100,1,10000,{id_user},1)")
                    db.commit()
                elif pilihan == "6":

                    cursor.execute(
                        f"INSERT INTO detail_penampung (persentase,level,kapasitas_total,id_user,id_penampung) VALUES (100,1,10000,{id_user},2)")
                    db.commit()
                print("Bangunan berhasil ditambahkan")
    else:
        print("pilihan tidak tersedia")


# construction(1)

def upgradebangunan(id_user):
    cursor.execute(f"SELECT id_bangunan,nama_bangunan FROM bangunan")
    bangunan = cursor.fetchall()
    print("============Daftar Bangunan=========")
    for i in range(0, len(bangunan)):
        print(f"id : {bangunan[i][0]} | Nama : {bangunan[i][1]}")
    pilihan = input("masukkan id bangunan yang akan diupgrade : ")
    if pilihan in "23456789" or pilihan == "10" or pilihan == "11":
        cursor.execute(f"SELECT tipe FROM bangunan where id_bangunan={pilihan}")
        tipe = cursor.fetchall()
        tipe = tipe[0][0]
        if tipe == "padepokan":
            cursor.execute(f"SELECT harga FROM padepokan")
            harga = cursor.fetchall()
            harga = int(harga[0][0])

            cursor.execute(f"SELECT level FROM detail_padepokan WHERE id_user={id_user}")
            level_padepokan_lama = cursor.fetchall()
            level_padepokan_lama = int(level_padepokan_lama[0][0])

            harga_baru = (harga * 0.7) * level_padepokan_lama
            level_padepokan_baru = level_padepokan_lama + 1
            pilihan = input(
                f"apakah anda yakin akan mengupgrade padepokan ke level {level_padepokan_baru} dengan harga {harga_baru}? (yes/no) :")
            if pilihan == "yes":
                cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                emas_yang_tersedia = cursor.fetchall()
                emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                if emas_yang_tersedia >= harga_baru:
                    emas_sekarang = emas_yang_tersedia - harga_baru
                    cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                    db.commit()
                    cursor.execute(f"UPDATE detail_padepokan SET level={level_padepokan_baru} WHERE id_user={id_user}")
                    db.commit()
                    print("Padepokan berhasil diupdate")
                else:
                    print("emas tidak cukup")
            else:
                print("anda membatalkan upgrade")
        elif tipe == "pertahanan":
            cursor.execute(
                f"SELECT id_detail_pertahanan, level, harga, id_user, id_bangunan FROM detail_pertahanan INNER JOIN pertahanan USING(id_pertahanan) INNER JOIN bangunan USING(id_bangunan) GROUP BY id_pertahanan HAVING id_bangunan = {pilihan} && id_user={id_user};")
            data_pertahanan = cursor.fetchall()
            harga = data_pertahanan[0][2]
            id_detail_pertahanan = data_pertahanan[0][0]
            level_pertahanan_lama = data_pertahanan[0][1]
            harga_baru = (harga * 0.7) * level_pertahanan_lama
            level_pertahanan_baru = level_pertahanan_lama + 1
            pilihan = input(
                f"apakah anda yakin akan mengupgrade pertahanan ke level {level_pertahanan_baru} dengan harga {harga_baru}? (yes/no) :")
            if pilihan == "yes":
                cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                emas_yang_tersedia = cursor.fetchall()
                emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                if emas_yang_tersedia >= harga_baru:
                    emas_sekarang = emas_yang_tersedia - harga_baru
                    cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                    db.commit()
                    cursor.execute(
                        f"UPDATE detail_pertahanan SET level={level_pertahanan_baru} WHERE id_user={id_user} && id_detail_pertahanan={id_detail_pertahanan}")
                    db.commit()
                    print("Pertahanan berhasil diupdate")
                else:
                    print("emas tidak cukup")
            else:
                print("anda membatalkan pilihan")
        elif tipe == "penampung":
            if pilihan == "5":
                cursor.execute(f"SELECT harga from penampung WHERE id_penampung=1")
                harga = cursor.fetchall()
                harga = int(harga[0][0])

                cursor.execute(
                    f"SELECT level,kapasitas_total FROM detail_penampung WHERE id_user={id_user} && id_penampung=1")
                data_penampung = cursor.fetchall()
                level_penampung_lama = int(data_penampung[0][0])
                harga_baru = (harga * 0.7) * level_penampung_lama
                level_penampung_baru = level_penampung_lama + 1
                kapasitas_lama = int(data_penampung[0][1])
                kapasitas_baru = kapasitas_lama + 5000
                pilihan = input(
                    f"apakah anda yakin akan mengupgrade penampung ke level {level_penampung_baru} dengan harga {harga_baru}? (yes/no) :")
                if pilihan == "yes":
                    cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                    emas_yang_tersedia = cursor.fetchall()
                    emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                    if emas_yang_tersedia >= harga_baru:
                        emas_sekarang = emas_yang_tersedia - harga_baru
                        cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                        db.commit()
                        cursor.execute(
                            f"UPDATE detail_penampung SET level={level_penampung_baru},kapasitas_total={kapasitas_baru} WHERE id_user={id_user} && id_penampung=1")
                        db.commit()
                        print("penampung berhasil diupdate")
                    else:
                        print("emas tidak cukup")
                else:
                    print("anda membatalkan operasi")
            elif pilihan == "6":
                cursor.execute(f"SELECT harga from penampung WHERE id_penampung=2")
                harga = cursor.fetchall()
                harga = int(harga[0][0])

                cursor.execute(
                    f"SELECT level,kapasitas_total FROM detail_penampung WHERE id_user={id_user} && id_penampung=2")
                data_penampung = cursor.fetchall()
                level_penampung_lama = int(data_penampung[0][0])
                harga_baru = (harga * 0.7) * level_penampung_lama
                level_penampung_baru = level_penampung_lama + 1
                kapasitas_lama = int(data_penampung[0][1])
                kapasitas_baru = kapasitas_lama + 5000
                pilihan = input(
                    f"apakah anda yakin akan mengupgrade penampung ke level {level_penampung_baru} dengan harga {harga_baru}? (yes/no) :")
                if pilihan == "yes":
                    cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                    emas_yang_tersedia = cursor.fetchall()
                    emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                    if emas_yang_tersedia >= harga_baru:
                        emas_sekarang = emas_yang_tersedia - harga_baru
                        cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                        db.commit()
                        cursor.execute(
                            f"UPDATE detail_penampung SET level={level_penampung_baru},kapasitas_total={kapasitas_baru} WHERE id_user={id_user} && id_penampung=2")
                        db.commit()
                        print("penampung berhasil diupdate")
                    else:
                        print("emas tidak cukup")
                else:
                    print("anda membatalkan operasi")
        elif tipe == "pengumpul":
            if pilihan == "7":
                cursor.execute(f"SELECT harga from pengumpul WHERE id_pengumpul=1")
                harga = cursor.fetchall()
                harga = int(harga[0][0])

                cursor.execute(
                    f"SELECT level, laju_produksi FROM detail_pengumpul WHERE id_user={id_user} && id_pengumpul=1")
                data_pengumpul = cursor.fetchall()
                level_pengumpul_lama = int(data_pengumpul[0][0])
                harga_baru = (harga * 0.7) * level_pengumpul_lama
                level_pengumpul_baru = level_pengumpul_lama + 1
                produksi_lama = int(data_pengumpul[0][1])
                produksi_baru = produksi_lama + 5
                pilihan = input(
                    f"apakah anda yakin akan mengupgrade pengumpul ke level {level_pengumpul_baru} dengan harga {harga_baru}? (yes/no) :")
                if pilihan == "yes":
                    cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                    emas_yang_tersedia = cursor.fetchall()
                    emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                    if emas_yang_tersedia >= harga_baru:
                        emas_sekarang = emas_yang_tersedia - harga_baru
                        cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                        db.commit()
                        cursor.execute(
                            f"UPDATE detail_pengumpul SET level={level_pengumpul_baru},laju_produksi={produksi_baru} WHERE id_user={id_user} && id_pengumpul=1")
                        db.commit()
                        print("Anda berhasil mengupgrade")
                    else:
                        print("emas tidak cukup")
                else:
                    print("anda membatalkan operasi")
            elif pilihan == "8":
                cursor.execute(f"SELECT harga from pengumpul WHERE id_pengumpul=2")
                harga = cursor.fetchall()
                harga = int(harga[0][0])

                cursor.execute(
                    f"SELECT level, laju_produksi FROM detail_pengumpul WHERE id_user={id_user} && id_pengumpul=2")
                data_pengumpul = cursor.fetchall()
                level_pengumpul_lama = int(data_pengumpul[0][0])
                level_pengumpul_baru = level_pengumpul_lama + 1
                harga_baru = (harga * 0.7) * level_pengumpul_lama
                produksi_lama = int(data_pengumpul[0][1])
                produksi_baru = produksi_lama + 5
                pilihan = input(
                    f"apakah anda yakin akan mengupgrade pengumpul ke level {level_pengumpul_baru} dengan harga {harga_baru}? (yes/no) :")
                if pilihan == "yes":
                    cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                    emas_yang_tersedia = cursor.fetchall()
                    emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                    if emas_yang_tersedia >= harga_baru:
                        emas_sekarang = emas_yang_tersedia - harga_baru
                        cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                        db.commit()
                        cursor.execute(
                            f"UPDATE detail_pengumpul SET level={level_pengumpul_baru},laju_produksi={produksi_baru} WHERE id_user={id_user} && id_pengumpul=2")
                        db.commit()
                        print("Anda berhasil mengupgrade")
                    else:
                        print("emas tidak cukup")
                else:
                    print("anda membatalkan operasi")
        elif tipe == "balai desa":
            cursor.execute(f"SELECT harga from pengumpul WHERE id_pengumpul=2")
            harga = cursor.fetchall()
            harga = int(harga[0][0])

            cursor.execute(f"SELECT level FROM detail_balai_desa WHERE id_user={id_user}")
            level_bd_lama = cursor.fetchall()
            level_bd_lama = int(level_bd_lama[0][0])
            level_bd_baru = level_bd_lama + 1
            harga_baru = (harga * 0.7) * level_bd_lama
            pilihan = input(
                f"apakah anda yakin akan mengupgrade balai desa ke level {level_pengumpul_baru} dengan harga {harga_baru}? (yes/no) :")
            if pilihan == "yes":
                cursor.execute(f"SELECT emas FROM user WHERE id_user={id_user}")
                emas_yang_tersedia = cursor.fetchall()
                emas_yang_tersedia = int(emas_yang_tersedia[0][0])
                if emas_yang_tersedia >= harga_baru:
                    emas_sekarang = emas_yang_tersedia - harga_baru
                    cursor.execute(f"UPDATE user SET emas={emas_sekarang} WHERE id_user={id_user}")
                    db.commit()
                    cursor.execute(f"UPDATE detail_balai_desa SET level={level_bd_baru} WHERE id_user={id_user}")
                    db.commit()
                    print("balai desa berhasil diupdate")
                else:
                    print("emas tidak cukup")
            else:
                print("anda membatalkan operasi")
    else:
        print("pilihan tidak tersedia")


# upgradebangunan(1)

def repair(id_user):
    cursor.execute(f"UPDATE detail_balai_desa SET persentase =100 WHERE id_user={id_user}")
    db.commit()
    cursor.execute(f"UPDATE detail_pengumpul SET persentase =100 WHERE id_user={id_user}")
    db.commit()
    cursor.execute(f"UPDATE detail_penampung SET persentase =100 WHERE id_user={id_user}")
    db.commit()
    cursor.execute(f"UPDATE detail_pertahanan SET persentase =100 WHERE id_user={id_user}")
    db.commit()
    cursor.execute(f"UPDATE detail_padepokan SET persentase =100 WHERE id_user={id_user}")
    db.commit()
    print("Semua bangunan berhasil diperbaiki")

def run_game():

    print('Pilih keinginan')
    print('1. register')
    print('2. login')

    pilihan = int(input('masukkan pilihan anda : '))

    if(pilihan == 1):
        user_register()
    elif pilihan == 2:
        user_login()

if __name__ == "__main__":
    run_game()