from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException as NSEE

import time
import pymongo
from pymongo import MongoClient

#Akun
username = "yosua@live.undip.ac.id"
password = "insinyurj4y4"

#Driver
driver = webdriver.Chrome()
action = ActionChains(driver)

#Database META
# client = pymongo.MongoClient("mongodb://192.168.195.241:27017/")
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Database Name
db = client["piiclone"]
# Collection Name
col = db["form_penilaian"]

#Experimental Database
# PID = "formM-WijTbj_AvcPpJZ0p7BVh1"
# Student_ID = "56473829"
# tiga = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_tiga':1})

# # print(tiga) 
# print(type(tiga))
# I_3 = tiga['form_i_tiga']
# print(type(I_3))

# print(len(I_3))

# I_31 = I_3[0]
# print(type(I_31["key"]))
# print(I_31["key"])

# print(type(I_31["klaimKompetensiWSatu"]))
# print(len(I_31["klaimKompetensiWSatu"]))
# print(I_31["klaimKompetensiWSatu"])

#Enter FAIP
driver.get("http://updmember.pii.or.id/index.php")
driver.maximize_window()
#input username
driver.find_element(By.ID, "email").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
#masuk login
driver.find_element(By.ID, "m_login_signin_submit").click()

driver.implicitly_wait(2)

driver.find_element(By.LINK_TEXT, "FAIP").click()
driver.find_element(By.LINK_TEXT, "Edit").click()

# driver.find_element(By.LINK_TEXT, "BUAT FAIP BARU").click()

# WebDriverWait(driver, 10).until(EC.alert_is_present())
# driver.switch_to.alert.accept()

time.sleep(2)
def Check():
    time.sleep(1)
    print("\n===Checkpoint===\n")

#PENGISIAN I3   
def FormI3():
    driver.find_element(By.LINK_TEXT, "I.3").click()
    driver.implicitly_wait(5)

    ID_Count_I3 = 1  
    print("================================================\nFormI3")

    try:
        while ID_Count_I3 < 100:
            Row_ID_I3 = f'//*[@class=" org-item"][@data-id="{str(ID_Count_I3)}"]'    
            Check_Row_I3 = driver.find_element(By.XPATH, Row_ID_I3)
            
            if Check_Row_I3.is_enabled:
                print("Row " + str(ID_Count_I3) + " ada") 
            else:
                break
            ID_Count_I3 += 1
    except NSEE:
        print ("Row " + str(ID_Count_I3) + " tidak ada") 
    
    Counter_I3 = 1
    DB_Count_I3 = 0

    #Database
    PID = "formM-WijTbj_AvcPpJZ0p7BVh1"
    Student_ID = "56473829"
    Dict_I_Tiga = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_tiga':1})
    print("Metadata Database")
    print(type(Dict_I_Tiga))
    List_I_3 = Dict_I_Tiga['form_i_tiga']
    print(type(List_I_3))
    n_I3 = len(List_I_3)
    print("Jumlah Document: " + str(n_I3) + "\n")

    print("Start from Row = " + str(ID_Count_I3))
    print("Row Ditambah = " + str(n_I3) + "\n")

    while Counter_I3 <= n_I3:
        #add row
        TambahI3 = driver.find_element(By.XPATH, '//button[@onclick="add13(\'org\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI3)
        action.move_to_element(TambahI3).perform()
        TambahI3.send_keys(Keys.ENTER)

        Row_I3 = str(ID_Count_I3)

        #Document
        Isi_I3 = List_I_3[DB_Count_I3]
        print("Counter Row = " + str(Counter_I3))
        print("Metadata Document")
        print(type(Isi_I3))
        print(type(Isi_I3["key"]))
        print("Key Document: " + Isi_I3["key"] + "\n")

        try:
            Organisasi_I3 = Isi_I3["namaOrganisasi"]
            ID_Organisasi_I3 = "13_nama_org" + Row_I3
            driver.find_element(By.ID, ID_Organisasi_I3).send_keys(Organisasi_I3)
            print("- Nama Organisasi: " + Organisasi_I3)
        except KeyError:
            print("- Nama Organisasi I3: KeyError")
        
        try:
            Jenis_I3 = Isi_I3["jenisOrganisasi"]
            ID_Jenis_I3 = "13_jenis" + Row_I3
            Select_Jenis_I3 = Select(driver.find_element(By.ID, ID_Jenis_I3))
            try:
                Select_Jenis_I3.select_by_value(Jenis_I3)
                print("- Jenis I3: " + Jenis_I3)
            except NSEE:
                ("- Jenis I3: NSEE")
        except KeyError:
            print("- Jenis I3: KeyError")

        try:
            Kota_I3 = Isi_I3["kotaAsal"]
            ID_Kota_I3 = "13_tempat" + Row_I3
            driver.find_element(By.ID, ID_Kota_I3).send_keys(Kota_I3)
            print("- Kota I3: " + Kota_I3)
        except KeyError:
            print("- Kota I3: KeyError")

        try:
            Provinsi_I3 = Isi_I3["provinsiAsal"]
            ID_Provinsi_I3 = "13_provinsi" + Row_I3
            driver.find_element(By.ID, ID_Provinsi_I3).send_keys(Provinsi_I3)
            print("- Provinsi I3: " + Provinsi_I3)
        except KeyError:
            print("- Provinsi I3: KeyError")

        try:
            Negara_I3 = Isi_I3["negaraAsal"]
            ID_Negara_I3 = "13_negara" + Row_I3
            driver.find_element(By.ID, ID_Negara_I3).send_keys(Negara_I3)
            print("- Negara I3: " + Negara_I3)
        except KeyError:
            print("- Negara I3: KeyError")
        
        try:
            BulanMulai_I3 = Isi_I3["bulanMulai"]
            ID_BulanMulai_I3 = "13_startdate" + Row_I3
            Select_BulanMulai_I3 = Select(driver.find_element(By.ID, ID_BulanMulai_I3))
            try:
                Select_BulanMulai_I3.select_by_visible_text(BulanMulai_I3)
                print("- Bulan Mulai I3: " + BulanMulai_I3)
            except NSEE:
                print("- Bulan Mulai I3: NSEE")
        except KeyError:
            print("- Bulan Mulai I3: KeyError")

        try:
            TahunMulai_I3 = Isi_I3["tahunMulai"]
            ID_TahunMulai_I3 = "13_startyear" + Row_I3
            driver.find_element(By.ID, ID_TahunMulai_I3).send_keys(TahunMulai_I3)
            print("- Tahun Mulai I3: " + TahunMulai_I3)
        except KeyError:
            print("- Tahun Mulai I3: KeyError")

        #Periode I3
        ID_Anggota_I3 = "13_work" + Row_I3
        Angggota_I3 = driver.find_element(By.ID, ID_Anggota_I3)
        if Isi_I3["masihAnggota"] == True:
            driver.execute_script("arguments[0].scrollIntoView();",Angggota_I3)
            action.move_to_element_with_offset(Angggota_I3, 0, -20).click().perform()
            print("- Masih Anggota I3: True")
        else:
            print("- Masih Anggota I3: False")
            try:
                TahunSelesai_I3 = Isi_I3["tahun"]
                ID_TahunSelesai_I3 = "13_endyear" + Row_I3
                driver.find_element(By.ID, ID_TahunSelesai_I3).send_keys(TahunSelesai_I3)
                print("- Tahun Selesai I3: " + TahunSelesai_I3)
            except KeyError:
                print("- Tahun Selesai I3: KeyError")

            try:
                BulanSelesai_I3 = Isi_I3["bulan"]
                ID_BulanSelesai_I3 = "13_enddate" + Row_I3
                Select_BulanSelesai_I3 = Select(driver.find_element(By.ID, ID_BulanSelesai_I3))
                try:
                    Select_BulanSelesai_I3.select_by_visible_text(BulanSelesai_I3)
                    print("- Bulan Selesai I3: " + BulanSelesai_I3)
                except NSEE:
                    print("- Bulan Selesai I3: NSEE")
            except KeyError:
                print("- Bulan Selesai I3: KeyError")
        
        try:
            Jabatan_I3 = Isi_I3["jabatanOrganisasi"]
            ID_Jabatan_I3 = "13_jabatan" + Row_I3
            Select_Jabatan_I3 = Select(driver.find_element(By.ID, ID_Jabatan_I3))
            try:
                Select_Jabatan_I3.select_by_visible_text(Jabatan_I3)
                print("- Jabatan I3: " + Jabatan_I3)
            except NSEE:
                print("- Jabatan I3: NSEE")
        except KeyError:
            print("- Jabatan I3: KeyError")

        try:
            Tingkat_I3 = Isi_I3["tingkatanOrganisasi"]
            ID_Tingkat_I3 = "13_tingkat" + Row_I3
            Select_Tingkat_I3 = Select(driver.find_element(By.ID, ID_Tingkat_I3))
            try:
                Select_Tingkat_I3.select_by_visible_text(Tingkat_I3)
                print("- Tingkat I3: " + Tingkat_I3)
            except NSEE:
                print("- Tingkat I3: NSEE")
        except KeyError:
            print("- Tingkat I3: KeyError")

        try:
            Lingkup_I3 = Isi_I3["kegiatanOrganisasi"]
            ID_Lingkup_I3 = "13_lingkup" + Row_I3
            Scroll_Lingkup_I3 = driver.find_element(By.ID, ID_Lingkup_I3)
            driver.execute_script("arguments[0].scrollIntoView();",Scroll_Lingkup_I3)
            action.move_to_element(Scroll_Lingkup_I3).perform()
            Select_Lingkup_I3 = Select(Scroll_Lingkup_I3)
            try:
                Select_Lingkup_I3.select_by_value(Lingkup_I3)
                print("- Lingkup I3: " + Lingkup_I3)
            except NSEE:
                print("- Lingkup I3: NSEE")
        except KeyError:
            print("- Lingkup I3: KeyError")
        
        try:
            Uraian_I3 = Isi_I3["uraianTugas"]
            ID_Uraian_I3 = "13_aktifitas" + Row_I3
            Scroll_Uraian_I3 = driver.find_element(By.ID, ID_Uraian_I3)
            driver.execute_script("arguments[0].scrollIntoView();",Scroll_Uraian_I3)
            action.move_to_element(Scroll_Uraian_I3).perform()
            Scroll_Uraian_I3.send_keys(Uraian_I3)
            print("- Uraian I3: " + Uraian_I3)
        except KeyError:
            print("- Uraian I3: KeyError")
        
        # Kompetisi I3 
        try:
            Komp_I3 = Isi_I3["klaimKompetensiWSatu"]
            ID_Komp_I3 = "13_komp" + Row_I3
            Scroll_Komp_I3 = driver.find_element(By.ID, ID_Komp_I3)
            driver.execute_script("arguments[0].scrollIntoView();",Scroll_Komp_I3)
            action.move_to_element(Scroll_Komp_I3).perform()
            print("- Komp I3: " + str(len(Komp_I3)))

            for Komp_Value_I3 in Komp_I3:
                # Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//option[@value="{Komp_Value_I3}"]'
                Komp_Label_I3 = Komp_Value_I3[slice(5)]
                Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//optgroup[contains(@label, "{Komp_Label_I3}")]/option[@value="{Komp_Value_I3}."]'
                Komp_Find_I3 = driver.find_element(By.XPATH, Komp_Call_I3)
                driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I3)
                action.move_to_element_with_offset(Komp_Find_I3, 0, -15).click().perform()
                print("-", Komp_Value_I3)   
        except KeyError:
            pass
        
        #End/retry point of loop
        Counter_I3 += 1
        DB_Count_I3 += 1
        ID_Count_I3 += 1
        print("\nRow " + Row_I3 + " telah diisi")

        Check()



FormI3()



