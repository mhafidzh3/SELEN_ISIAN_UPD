from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException as NSEE

import time

username = "yosua@live.undip.ac.id"
password = "insinyurj4y4"

driver = webdriver.Chrome()
action = ActionChains(driver)

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
Null = "no value"
def Check():
    time.sleep(1)
    print("\n===Checkpoint===\n")

#PENGISIAN I1
def FormI1(n_Alamat_I1,n_Lembaga_I1,n_Phone_I1):
    driver.find_element(By.LINK_TEXT, "I.1").click()
    driver.implicitly_wait(5)

    print("================================================\nFormI1")
    #add alamat
    ID_Count_Alamat_I1 = 0
    print("Alamat I1\n")
    try:
        while ID_Count_Alamat_I1 < 100:
            Row_Alamat_ID_I1 = f'//*[@class=" ala-item"][@data-id="{str(ID_Count_Alamat_I1)}"]'    
            Check_Row_Alamat_I1 = driver.find_element(By.XPATH, Row_Alamat_ID_I1)
            
            if Check_Row_Alamat_I1.is_enabled:
                print("Row " + str(ID_Count_Alamat_I1) + " ada") 
            else:
                break
            ID_Count_Alamat_I1 += 1
    except NSEE:
        print ("Row " + str(ID_Count_Alamat_I1) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_Alamat_I1))
    print("Row Ditambah = " + str(n_Alamat_I1) + "\n")

    Counter_Alamat_I1 = 1

    while Counter_Alamat_I1 <= n_Alamat_I1:
        #add row
        Alamat_Row_I1 = str(ID_Count_Alamat_I1)

        TambahI1alamat = driver.find_element(By.XPATH, '//button[@onclick="add111(\'ala\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI1alamat)
        action.move_to_element(TambahI1alamat).perform()
        TambahI1alamat.send_keys(Keys.ENTER)

        ID_AddressType_I1 = "addr_type" + Alamat_Row_I1
        Select_AddressType_I1 = Select(driver.find_element(By.ID, ID_AddressType_I1))
        AddressType_I1 = "3"
        Select_AddressType_I1.select_by_value(AddressType_I1)

        AddressDesc_I1 = "Alamat"
        ID_AddressDesc_I1 = "addr_desc" + Alamat_Row_I1
        driver.find_element(By.ID, ID_AddressDesc_I1).send_keys(AddressDesc_I1)

        AddressLoc_I1 = "Kota"
        ID_AddressLoc_I1 = "addr_loc" + Alamat_Row_I1
        driver.find_element(By.ID, ID_AddressLoc_I1).send_keys(AddressLoc_I1)

        AddressZip_I1 = "0000"
        ID_AddressZip_I1 = "addr_zip" + Alamat_Row_I1
        driver.find_element(By.ID, ID_AddressZip_I1).send_keys(AddressZip_I1)

        Check()

        #End/retry point of loop
        print("Counter Row = " + str(Counter_Alamat_I1))
        Counter_Alamat_I1 += 1
        ID_Count_Alamat_I1 += 1
        print("Row " + Alamat_Row_I1 + " telah diisi")

        Check()

    #add lembaga
    ID_Count_Lembaga_I1 = 1
    print("Lembaga I1\n")
    try:
        while ID_Count_Lembaga_I1 < 100:
            Row_Lembaga_ID_I1 = f'//*[@class=" wor-item"][@data-id="{str(ID_Count_Lembaga_I1)}"]'    
            Check_Row_Lembaga_I1 = driver.find_element(By.XPATH, Row_Lembaga_ID_I1)
            
            if Check_Row_Lembaga_I1.is_enabled:
                print("Row " + str(ID_Count_Lembaga_I1) + " ada") 
            else:
                break
            ID_Count_Lembaga_I1 += 1
    except NSEE:
        print ("Row " + str(ID_Count_Lembaga_I1) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_Lembaga_I1))
    print("Row Ditambah = " + str(n_Lembaga_I1) + "\n")

    Counter_Lembaga_I1 = 1

    while Counter_Lembaga_I1 <= n_Lembaga_I1:
        #add row
        Lembaga_Row_I1 = str(ID_Count_Lembaga_I1)

        TambahI1lembaga = driver.find_element(By.XPATH, '//button[@onclick="add112(\'wor\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI1lembaga)
        action.move_to_element(TambahI1lembaga).perform()
        TambahI1lembaga.send_keys(Keys.ENTER)

        ExpName_I1 = "Lembaga"
        ID_ExpName_I1 = "exp_name" + Lembaga_Row_I1
        driver.find_element(By.ID, ID_ExpName_I1).send_keys(ExpName_I1)

        ExpDesc_I1 = "Jabatan"
        ID_ExpDesc_I1 = "exp_desc" + Lembaga_Row_I1
        driver.find_element(By.ID, ID_ExpDesc_I1).send_keys(ExpDesc_I1)

        ExpLoc_I1 = "Kota"
        ID_ExpLoc_I1 = "exp_loc" + Lembaga_Row_I1
        driver.find_element(By.ID, ID_ExpLoc_I1).send_keys(ExpLoc_I1)

        ExpZip_I1 = "0001"
        ID_ExpZip_I1 = "exp_zip" + Lembaga_Row_I1
        driver.find_element(By.ID, ID_ExpZip_I1).send_keys(ExpZip_I1)

        Check()

        #End/retry point of loop
        print("Counter Row = " + str(Counter_Lembaga_I1))
        Counter_Lembaga_I1 += 1
        ID_Count_Lembaga_I1 += 1
        print("Row " + Lembaga_Row_I1 + " telah diisi")

        Check()

    #add phone number
    ID_Count_Phone_I1 = 0
    print("Phone I1\n")
    try:
        while ID_Count_Phone_I1 < 100:
            Row_Phone_ID_I1 = f'//*[@class=" pho-item"][@data-id="{str(ID_Count_Phone_I1)}"]'    
            Check_Row_Phone_I1 = driver.find_element(By.XPATH, Row_Phone_ID_I1)
            
            if Check_Row_Phone_I1.is_enabled:
                print("Row " + str(ID_Count_Phone_I1) + " ada") 
            else:
                break
            ID_Count_Phone_I1 += 1
    except NSEE:
        print ("Row " + str(ID_Count_Phone_I1) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_Phone_I1))
    print("Row Ditambah = " + str(n_Phone_I1) + "\n")

    Counter_Phone_I1 = 1

    while Counter_Phone_I1 <= n_Phone_I1:
        #add row
        Phone_Row_I1 = str(ID_Count_Phone_I1)

        TambahI1Phone = driver.find_element(By.XPATH, '//button[@onclick="add113(\'pho\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI1Phone)
        action.move_to_element(TambahI1Phone).perform()
        TambahI1Phone.send_keys(Keys.ENTER)

        ID_PhoneType_I1 = "phone_type" + Phone_Row_I1
        Select_PhoneType_I1 = Select(driver.find_element(By.ID, ID_PhoneType_I1))
        PhoneType_I1 = "mobile_phone"
        Select_PhoneType_I1.select_by_value(PhoneType_I1)

        PhoneValue_I1 = "+622112411575"
        ID_PhoneValue_I1 = "phone_value" + Phone_Row_I1
        driver.find_element(By.ID, ID_PhoneValue_I1).send_keys(PhoneValue_I1)

        Check()

        #End/retry point of loop
        print("Counter Row = " + str(Counter_Phone_I1))
        Counter_Phone_I1 += 1
        ID_Count_Phone_I1 += 1
        print("Row " + Phone_Row_I1 + " telah diisi")

        Check()
    print("\n") 

#PENGISIAN I2
def FormI2(n_I2):
    driver.find_element(By.LINK_TEXT, "I.2").click()
    driver.implicitly_wait(5)

    ID_Count_I2 = 1  
    print("================================================\nFormI2")
    
    try:
        while ID_Count_I2 < 100:
            Row_ID_I2 = f'//*[@class=" edu-item"][@data-id="{str(ID_Count_I2)}"]'    
            Check_Row_I2 = driver.find_element(By.XPATH, Row_ID_I2)
            
            if Check_Row_I2.is_enabled:
                print("Row " + str(ID_Count_I2) + " ada") 
            else:
                break
            ID_Count_I2 += 1
    except NSEE:
        print ("Row " + str(ID_Count_I2) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_I2))
    print("Row Ditambah = " + str(n_I2) + "\n")

    Counter_I2 = 1

    while Counter_I2 <= n_I2:
        #add row
        TambahI2 = driver.find_element(By.XPATH, '//button[@onclick="add12(\'edu\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI2)
        action.move_to_element(TambahI2).perform()
        TambahI2.send_keys(Keys.ENTER)

        Row_I2 = str(ID_Count_I2)

        Universitas_I2 = "Universitas Diponegoro"
        ID_Universitas_I2 = "12_school" + Row_I2
        driver.find_element(By.ID, ID_Universitas_I2).send_keys(Universitas_I2)

        ID_Tingkat_I2 = "12_degree" + Row_I2
        Select_Tingkat_I2 = Select(driver.find_element(By.ID, ID_Tingkat_I2))
        Tingkat_I2 = "S3"
        Select_Tingkat_I2.select_by_value(Tingkat_I2)

        Fakultas_I2 = "Teknik"
        ID_Fakultas_I2 = "12_fakultas" + Row_I2
        driver.find_element(By.ID, ID_Fakultas_I2).send_keys(Fakultas_I2)

        Jurusan_I2 = "Teknik Elektro"
        ID_Jurusan_I2 = "12_fieldofstudy" + Row_I2
        driver.find_element(By.ID, ID_Jurusan_I2).send_keys(Jurusan_I2)

        Kota_I2 = "Semarang"
        ID_Kota_I2 = "12_kota" + Row_I2
        driver.find_element(By.ID, ID_Kota_I2).send_keys(Kota_I2)

        Provinsi_I2 = "Jawa Tengah"
        ID_Provinsi_I2 = "12_provinsi" + Row_I2
        driver.find_element(By.ID, ID_Provinsi_I2).send_keys(Provinsi_I2)

        Negara_I2 = "Indonesia"
        ID_Negara_I2 = "12_negara" + Row_I2
        driver.find_element(By.ID, ID_Negara_I2).send_keys(Negara_I2)

        TahunLulus_I2 = "2018"
        ID_TahunLulus_I2 = "12_tahunlulus" + Row_I2
        driver.find_element(By.ID, ID_TahunLulus_I2).send_keys(TahunLulus_I2)

        Gelar_I2 = "Dr."
        ID_Gelar_I2 = "12_title" + Row_I2
        driver.find_element(By.ID, ID_Gelar_I2).send_keys(Gelar_I2)

        ID_JudulTA_I2 = "12_activities" + Row_I2
        JudulTA_I2 = "TA S3"
        Scroll_JudulTA_I2 = driver.find_element(By.ID, ID_JudulTA_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_JudulTA_I2)
        action.move_to_element(Scroll_JudulTA_I2).perform()
        Scroll_JudulTA_I2.send_keys(JudulTA_I2)

        ID_UraianTA_I2 = "12_description" + Row_I2
        UraianTA_I2 = "Uraian TA"
        Scroll_UraianTA_I2 = driver.find_element(By.ID, ID_UraianTA_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_UraianTA_I2)
        action.move_to_element(Scroll_UraianTA_I2).perform()
        Scroll_UraianTA_I2.send_keys(UraianTA_I2)

        ID_Nilai_I2 = "12_score" + Row_I2
        Nilai_I2 = "4.00"
        Scroll_Nilai_I2 = driver.find_element(By.ID, ID_Nilai_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Nilai_I2)
        action.move_to_element(Scroll_Nilai_I2).perform()
        Scroll_Nilai_I2.send_keys(Nilai_I2)

        #End/retry point of loop
        print("Counter Row = " + str(Counter_I2))
        Counter_I2 += 1
        ID_Count_I2 += 1
        print("Row " + Row_I2 + " telah diisi")

        Check()
    print("\n")    

#PENGISIAN I3   
def FormI3(n_I3):
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
    
    print("Start from Row = " + str(ID_Count_I3))
    print("Row Ditambah = " + str(n_I3) + "\n")

    Counter_I3 = 1

    while Counter_I3 <= n_I3:
        #add row
        TambahI3 = driver.find_element(By.XPATH, '//button[@onclick="add13(\'org\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI3)
        action.move_to_element(TambahI3).perform()
        TambahI3.send_keys(Keys.ENTER)

        Row_I3 = str(ID_Count_I3)

        Organisasi_I3 = "Organisasi"
        ID_Organisasi_I3 = "13_nama_org"+ Row_I3
        driver.find_element(By.ID, ID_Organisasi_I3).send_keys(Organisasi_I3)

        ID_Jenis_I3 = "13_jenis" + Row_I3
        Select_Jenis_I3 = Select(driver.find_element(By.ID, ID_Jenis_I3))
        Jenis_I3 = "Organisasi PII"
        Select_Jenis_I3.select_by_value(Jenis_I3)

        Kota_I3 = "Kota"
        ID_Kota_I3 = "13_tempat" + Row_I3
        driver.find_element(By.ID, ID_Kota_I3).send_keys(Kota_I3)

        Provinsi_I3 = "Provinsi"
        ID_Provinsi_I3 = "13_provinsi" + Row_I3
        driver.find_element(By.ID, ID_Provinsi_I3).send_keys(Provinsi_I3)

        Negara_I3 = "Negara"
        ID_Negara_I3 = "13_negara" + Row_I3
        driver.find_element(By.ID, ID_Negara_I3).send_keys(Negara_I3)

        #Periode I3
        ID_BulanMulai_I3 = "13_startdate" + Row_I3
        ID_TahunMulai_I3 = "13_startyear" + Row_I3
        Select_BulanMulai_I3 = Select(driver.find_element(By.ID, ID_BulanMulai_I3))
        Select_BulanMulai_I3.select_by_value("1")
        TahunMulai_I3 = "2018"
        driver.find_element(By.ID, ID_TahunMulai_I3).send_keys(TahunMulai_I3)

        ID_BulanSelesai_I3 = "13_enddate" + Row_I3
        ID_TahunSelesai_I3 = "13_endyear" + Row_I3
        Select_BulanSelesai_I3 = Select(driver.find_element(By.ID, ID_BulanSelesai_I3))
        Select_BulanSelesai_I3.select_by_value("6")
        TahunSelesai_I3 = "2023"
        driver.find_element(By.ID, ID_TahunSelesai_I3).send_keys(TahunSelesai_I3)

        ID_Jabatan_I3 = "13_jabatan" + Row_I3
        Select_Jabatan_I3 = Select(driver.find_element(By.ID, ID_Jabatan_I3))
        Jabatan_I3 = "2"
        Select_Jabatan_I3.select_by_value(Jabatan_I3)

        ID_Tingkat_I3 = "13_tingkat" + Row_I3
        Select_Tingkat_I3 = Select(driver.find_element(By.ID, ID_Tingkat_I3))
        Tingkat_I3 = "1"
        Select_Tingkat_I3.select_by_value(Tingkat_I3)

        ID_Lingkup_I3 = "13_lingkup" + Row_I3
        Select_Lingkup_I3 = Select(driver.find_element(By.ID, ID_Lingkup_I3))
        Lingkup_I3 = "Asosiasi Profesi"
        Select_Lingkup_I3.select_by_value(Lingkup_I3)

        ID_Anggota_I3 = "13_work" + Row_I3
        #driver.find_element(By.ID, checkanggota).click()
        Angggota_I3 = driver.find_element(By.ID, ID_Anggota_I3)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();",Angggota_I3)
        action.move_to_element_with_offset(Angggota_I3, 0, -20).click().perform()
        
        ID_Uraian_I3 = "13_aktifitas" + Row_I3
        Uraian_I3 = "aktifitas"
        Scroll_Uraian_I3 = driver.find_element(By.ID, ID_Uraian_I3)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Uraian_I3)
        action.move_to_element(Scroll_Uraian_I3).perform()
        Scroll_Uraian_I3.send_keys(Uraian_I3)

        #Kompetisi I3 Expandable
        ID_Komp_I3 = "13_komp" + Row_I3
        Scroll_Komp_I3 = driver.find_element(By.ID, ID_Komp_I3)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Komp_I3)
        action.move_to_element(Scroll_Komp_I3).perform()

        Check()
        
        #Choose Kompetisi Label W.1.1.2.
        Komp_Panel_I3 = ["W", 1, 1, 2]
        Komp_Label_I3 = str(Komp_Panel_I3[0]) + "." + str(Komp_Panel_I3[1]) + "." + str(Komp_Panel_I3[2]) + "."
        Komp_Value_I3 = Komp_Label_I3 + str(Komp_Panel_I3[3]) + "."

        # Komp_Label_I3 = "W.1.1."
        # Komp_Value_I3 = Komp_Label_I3 + "2."

        Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//optgroup[contains(@label, "{Komp_Label_I3}")]/option[@value="{Komp_Value_I3}"]'
        Komp_Find_I3 = driver.find_element(By.XPATH, Komp_Call_I3)

        if Row_I3 == "1":
            driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I3)
            action.move_to_element(Komp_Find_I3).click().perform()
        else:
            driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I3)
            action.move_to_element_with_offset(Komp_Find_I3, 0,-20).click().perform()

        #Untuk Tambah kompetisi ulang segmen diatas

        #End/retry point of loop
        print("Counter Row = " + str(Counter_I3))
        Counter_I3 += 1
        ID_Count_I3 += 1
        print("Row " + Row_I3 + " telah diisi")

        Check()
    print("\n")

#PENGISIAN I4
def FormI4(n_I4):
    driver.find_element(By.LINK_TEXT, "I.4").click()
    driver.implicitly_wait(5)

    ID_Count_I4 = 1  
    print("================================================\nFormI4")

    try:
        while ID_Count_I4 < 100:
            Row_ID_I4 = f'//*[@class=" phg-item"][@data-id="{str(ID_Count_I4)}"]'    
            Check_Row_I4 = driver.find_element(By.XPATH, Row_ID_I4)
            
            if Check_Row_I4.is_enabled:
                print("Row " + str(ID_Count_I4) + " ada") 
            else:
                break
            ID_Count_I4 += 1
    except NSEE:
        print ("Row " + str(ID_Count_I4) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_I4))
    print("Row Ditambah = " + str(n_I4) + "\n")

    Counter_I4 = 1

    while Counter_I4 <= n_I4:
        #add row
        TambahI4 = driver.find_element(By.XPATH, '//button[@onclick="add14(\'phg\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI4)
        action.move_to_element(TambahI4).perform()
        TambahI4.send_keys(Keys.ENTER)

        Row_I4 = str(ID_Count_I4)

        Penghargaan_I4 = "Penghargaan miliar"
        ID_Penghargaan_I4 = "14_nama" + Row_I4
        driver.find_element(By.ID, ID_Penghargaan_I4).send_keys(Penghargaan_I4)
        
        Lembaga_I4 = "Lembaga PHG"
        ID_Lembaga_I4 = "14_lembaga" + Row_I4
        driver.find_element(By.ID, ID_Lembaga_I4).send_keys(Lembaga_I4)
        
        Kota_I4 = "Kota PHG"
        ID_Kota_I4 = "14_location" + Row_I4
        driver.find_element(By.ID, ID_Kota_I4).send_keys(Kota_I4)
        
        Provinsi_I4 = "Provinsi PHG"
        ID_Provinsi_I4 = "14_provinsi" + Row_I4
        driver.find_element(By.ID, ID_Provinsi_I4).send_keys(Provinsi_I4)

        Negara_I4 = "Korea selatan"
        ID_Negara_I4 = "14_negara" + Row_I4
        driver.find_element(By.ID, ID_Negara_I4).send_keys(Negara_I4)
        
        ID_BulanTerbit_I4 = "14_startdate" + Row_I4
        Select_BulanTerbit_I4 = Select(driver.find_element(By.ID, ID_BulanTerbit_I4))
        BulanTerbit_I4 = "12"
        Select_BulanTerbit_I4.select_by_value(BulanTerbit_I4)

        Tahun_I4 = "2020"
        ID_Tahun_I4 = "14_startyear" + Row_I4
        driver.find_element(By.ID, ID_Tahun_I4).send_keys(Tahun_I4)

        ID_Tingkat_I4 = "14_tingkat" + Row_I4
        Select_Tingkat_I4 = Select(driver.find_element(By.ID, ID_Tingkat_I4))
        Tingkat_I4 = "4"
        Select_Tingkat_I4.select_by_value(Tingkat_I4)

        
        ID_Lembaga_I4 = "14_tingkatlembaga" + Row_I4
        Select_Lembaga_I4 = Select(driver.find_element(By.ID, ID_Lembaga_I4))
        Lembaga_I4 = "4"
        Select_Lembaga_I4.select_by_value(Lembaga_I4)

        ID_Uraian_I4 = "14_uraian" + Row_I4
        Uraian_I4 = "Uraian Singkat Aktifitas"
        Scroll_Uraian_I4 = driver.find_element(By.ID, ID_Uraian_I4)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Uraian_I4)
        action.move_to_element(Scroll_Uraian_I4).perform()
        Scroll_Uraian_I4.send_keys(Uraian_I4)

        #Kompetisi I4 Expandable
        ID_Komp_I4 = "14_komp" + Row_I4
        Scroll_Komp_I4 = driver.find_element(By.ID, ID_Komp_I4)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Komp_I4)
        action.move_to_element(Scroll_Komp_I4).perform()

        Check()
        
        #Choose Kompetisi Label W.1.1.2.
        Komp_Panel_I4 = ["W", 1, 1, 2]
        Komp_Label_I4 = str(Komp_Panel_I4[0]) + "." + str(Komp_Panel_I4[1]) + "." + str(Komp_Panel_I4[2]) + "."
        Komp_Value_I4 = Komp_Label_I4 + str(Komp_Panel_I4[3]) + "."

        # Komp_Label_I4 = "W.1.1."
        # Komp_Value_I4 = Komp_Label_I3 + "2."

        Komp_Call_I4 = f'//*[@id="{ID_Komp_I4}"]//optgroup[contains(@label, "{Komp_Label_I4}")]/option[@value="{Komp_Value_I4}"]'
        Komp_Find_I4 = driver.find_element(By.XPATH, Komp_Call_I4)

        driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I4)
        action.move_to_element_with_offset(Komp_Find_I4, 0,-20).click().perform()

        #Untuk Tambah kompetisi ulang segmen diatas

        #End/retry point of loop
        print("Counter Row = " + str(Counter_I4))
        Counter_I4 += 1
        ID_Count_I4 += 1
        print("Row " + Row_I4 + " telah diisi")

        Check()
    print("\n")

#PENGISIAN I5
def FormI5(n_I5):
    driver.find_element(By.LINK_TEXT, "I.5").click()
    driver.implicitly_wait(5)

    ID_Count_I5 = 1  
    print("================================================\nFormI5")

    try:
        while ID_Count_I5 < 100:
            Row_ID_I5 = f'//*[@class=" pdd-item"][@data-id="{str(ID_Count_I5)}"]'    
            Check_Row_I5 = driver.find_element(By.XPATH, Row_ID_I5)
            
            if Check_Row_I5.is_enabled:
                print("Row " + str(ID_Count_I5) + " ada") 
            else:
                break
            ID_Count_I5 += 1
    except NSEE:
        print ("Row " + str(ID_Count_I5) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_I5))
    print("Row Ditambah = " + str(n_I5) + "\n")

    Counter_I5 = 1

    while Counter_I5 <= n_I5:
        #add row
        TambahI5 = driver.find_element(By.XPATH, '//button[@onclick="add15(\'pdd\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI5)
        action.move_to_element(TambahI5).perform()
        TambahI5.send_keys(Keys.ENTER)

        Row_I5 = str(ID_Count_I5)

        Pendidikan_I5 = "Pendidikan Teknik"
        ID_Pendidikan_I5 = "15_nama" + Row_I5
        driver.find_element(By.ID, ID_Pendidikan_I5).send_keys(Pendidikan_I5)
        
        Lembaga_I5 = "Lembaga PDD Teknik"
        ID_Lembaga_I5 = "15_lembaga" + Row_I5
        driver.find_element(By.ID, ID_Lembaga_I5).send_keys(Lembaga_I5)
        
        Kota_I5 = "Kota PDD Teknik"
        ID_Kota_I5 = "15_location" + Row_I5
        driver.find_element(By.ID, ID_Kota_I5).send_keys(Kota_I5)
        
        Provinsi_I5 = "Provinsi PDD Teknik"
        ID_Provinsi_I5 = "15_provinsi" + Row_I5
        driver.find_element(By.ID, ID_Provinsi_I5).send_keys(Provinsi_I5)

        Negara_I5 = "Korea selatan"
        ID_Negara_I5 = "15_negara" + Row_I5
        driver.find_element(By.ID, ID_Negara_I5).send_keys(Negara_I5)

        ID_BulanMulai_I5 = "15_startdate" + Row_I5
        ID_TahunMulai_I5 = "15_startyear" + Row_I5
        Select_BulanMulai_I5 = Select(driver.find_element(By.ID, ID_BulanMulai_I5))
        Select_BulanMulai_I5.select_by_value("1")
        TahunMulai_I5 = "2019"
        driver.find_element(By.ID, ID_TahunMulai_I5).send_keys(TahunMulai_I5)

        ID_BulanSelesai_I5 = "15_enddate" + Row_I5
        ID_TahunSelesai_I5 = "15_endyear" + Row_I5
        Select_BulanSelesai_I5 = Select(driver.find_element(By.ID, ID_BulanSelesai_I5))
        Select_BulanSelesai_I5.select_by_value("7")
        TahunSelesai_I5 = "2022"
        driver.find_element(By.ID, ID_TahunSelesai_I5).send_keys(TahunSelesai_I5)

        ID_Tingkat_I5 = "15_tingkat" + Row_I5
        Select_Tingkat_I5 = Select(driver.find_element(By.ID, ID_Tingkat_I5))
        Tingkat_I5 = "2"
        Select_Tingkat_I5.select_by_value(Tingkat_I5)

        ID_Jam_I5 = "15_jam" + Row_I5
        Select_Jam_I5 = Select(driver.find_element(By.ID, ID_Jam_I5))
        Jam_I5 = "2"
        Select_Jam_I5.select_by_value(Jam_I5)
        
        ID_Anggota_I5 = "15_work" + Row_I5
        Angggota_I5 = driver.find_element(By.ID, ID_Anggota_I5)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();",Angggota_I5)
        action.move_to_element_with_offset(Angggota_I5, 0, -20).click().perform()

        ID_Uraian_I5 = "15_uraian" + Row_I5
        Uraian_I5 = "Uraian Singkat Aktifitas"
        Scroll_Uraian_I5 = driver.find_element(By.ID, ID_Uraian_I5)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Uraian_I5)
        action.move_to_element(Scroll_Uraian_I5).perform()
        Scroll_Uraian_I5.send_keys(Uraian_I5)

        #Kompetisi I5 Expandable
        ID_Komp_I5 = "15_komp" + Row_I5
        Scroll_Komp_I5 = driver.find_element(By.ID, ID_Komp_I5)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Komp_I5)
        action.move_to_element(Scroll_Komp_I5).perform()

        Check()
        
        #Choose Kompetisi Label W.1.1.2.
        Komp_Panel_I5 = ["W", 2, 1, 2]
        Komp_Label_I5 = str(Komp_Panel_I5[0]) + "." + str(Komp_Panel_I5[1]) + "." + str(Komp_Panel_I5[2]) + "."
        Komp_Value_I5 = Komp_Label_I5 + str(Komp_Panel_I5[3]) + "."

        # Komp_Label_I5 = "W.1.1."
        # Komp_Value_I5 = Komp_Label_I3 + "2."

        Komp_Call_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_I5}")]/option[@value="{Komp_Value_I5}"]'
        Komp_Find_I5 = driver.find_element(By.XPATH, Komp_Call_I5)

        driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I5)
        action.move_to_element_with_offset(Komp_Find_I5, 0,-20).click().perform()

        #Untuk Tambah kompetisi ulang segmen diatas

        #End/retry point of loop
        print("Counter Row = " + str(Counter_I5))
        Counter_I5 += 1
        ID_Count_I5 += 1
        print("Row " + Row_I5 + " telah diisi")

        Check()
    print("\n")

#PENGISIAN I6
def FormI6(n_I6):
    driver.find_element(By.LINK_TEXT, "I.6").click()
    driver.implicitly_wait(5)

    ID_Count_I6 = 1  
    print("================================================\nFormI6")

    try:
        while ID_Count_I6 < 100:
            Row_ID_I6 = f'//*[@class=" ppm-item"][@data-id="{str(ID_Count_I6)}"]'    
            Check_Row_I6 = driver.find_element(By.XPATH, Row_ID_I6)
            
            if Check_Row_I6.is_enabled:
                print("Row " + str(ID_Count_I6) + " ada") 
            else:
                break
            ID_Count_I6 += 1
    except NSEE:
        print ("Row " + str(ID_Count_I6) + " tidak ada") 
    
    print("Start from Row = " + str(ID_Count_I6))
    print("Row Ditambah = " + str(n_I6) + "\n")

    Counter_I6 = 1

    while Counter_I6 <= n_I6:
        #add row
        TambahI6 = driver.find_element(By.XPATH, '//button[@onclick="add16(\'ppm\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI6)
        action.move_to_element(TambahI6).perform()
        TambahI6.send_keys(Keys.ENTER)

        Row_I6 = str(ID_Count_I6)

        Pelatihan_I6 = "Sertif Teknik"
        ID_Pelatihan_I6 = "16_nama" + Row_I6
        driver.find_element(By.ID, ID_Pelatihan_I6).send_keys(Pelatihan_I6)
        
        Lembaga_I6 = "Lembaga PPM Teknik"
        ID_Lembaga_I6 = "16_lembaga" + Row_I6
        driver.find_element(By.ID, ID_Lembaga_I6).send_keys(Lembaga_I6)
        
        Kota_I6 = "Kota PPM Teknik"
        ID_Kota_I6 = "16_location" + Row_I6
        driver.find_element(By.ID, ID_Kota_I6).send_keys(Kota_I6)
        
        Provinsi_I6 = "Provinsi PPM Teknik"
        ID_Provinsi_I6 = "16_provinsi" + Row_I6
        driver.find_element(By.ID, ID_Provinsi_I6).send_keys(Provinsi_I6)

        Negara_I6 = "Korea selatan"
        ID_Negara_I6 = "16_negara" + Row_I6
        driver.find_element(By.ID, ID_Negara_I6).send_keys(Negara_I6)

        ID_BulanMulai_I6 = "16_startdate" + Row_I6
        ID_TahunMulai_I6 = "16_startyear" + Row_I6
        Select_BulanMulai_I6 = Select(driver.find_element(By.ID, ID_BulanMulai_I6))
        Select_BulanMulai_I6.select_by_value("1")
        TahunMulai_I6 = "2019"
        driver.find_element(By.ID, ID_TahunMulai_I6).send_keys(TahunMulai_I6)

        ID_BulanSelesai_I6 = "16_enddate" + Row_I6
        ID_TahunSelesai_I6 = "16_endyear" + Row_I6
        Select_BulanSelesai_I6 = Select(driver.find_element(By.ID, ID_BulanSelesai_I6))
        Select_BulanSelesai_I6.select_by_value("7")
        TahunSelesai_I6 = "2022"
        driver.find_element(By.ID, ID_TahunSelesai_I6).send_keys(TahunSelesai_I6)

        ID_Tingkat_I6 = "16_tingkat" + Row_I6
        Select_Tingkat_I6 = Select(driver.find_element(By.ID, ID_Tingkat_I6))
        Tingkat_I6 = "2"
        Select_Tingkat_I6.select_by_value(Tingkat_I6)

        ID_Jam_I6 = "16_jam" + Row_I6
        Select_Jam_I6 = Select(driver.find_element(By.ID, ID_Jam_I6))
        Jam_I6 = "2"
        Select_Jam_I6.select_by_value(Jam_I6)
        
        ID_Anggota_I6 = "16_work" + Row_I6
        #driver.find_element(By.ID, checkanggota).click()
        Angggota_I6 = driver.find_element(By.ID, ID_Anggota_I6)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();",Angggota_I6)
        action.move_to_element_with_offset(Angggota_I6, 0, -20).click().perform()

        ID_Uraian_I6 = "16_uraian" + Row_I6
        Uraian_I6 = "Uraian Singkat Aktifitas"
        Scroll_Uraian_I6 = driver.find_element(By.ID, ID_Uraian_I6)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Uraian_I6)
        action.move_to_element(Scroll_Uraian_I6).perform()
        Scroll_Uraian_I6.send_keys(Uraian_I6)

        #Kompetisi I4 Expandable
        ID_Komp_I6 = "16_komp" + Row_I6
        Scroll_Komp_I6 = driver.find_element(By.ID, ID_Komp_I6)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Komp_I6)
        action.move_to_element(Scroll_Komp_I6).perform()

        Check()
        
        #Choose Kompetisi Label W.1.1.2.
        Komp_Panel_I6 = ["W", 1, 1, 2]
        Komp_Label_I6 = str(Komp_Panel_I6[0]) + "." + str(Komp_Panel_I6[1]) + "." + str(Komp_Panel_I6[2]) + "."
        Komp_Value_I6 = Komp_Label_I6 + str(Komp_Panel_I6[3]) + "."

        # Komp_Label_I6 = "W.1.1."
        # Komp_Value_I6 = Komp_Label_I3 + "2."

        Komp_Call_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_I6}")]/option[@value="{Komp_Value_I6}"]'
        Komp_Find_I6 = driver.find_element(By.XPATH, Komp_Call_I6)

        driver.execute_script("arguments[0].scrollIntoView();",Komp_Find_I6)
        action.move_to_element_with_offset(Komp_Find_I6, 0,-20).click().perform()

        #Untuk Tambah kompetisi ulang segmen diatas

        #End/retry point of loop
        print("Counter Row = " + str(Counter_I6))
        Counter_I6 += 1
        ID_Count_I6 += 1
        print("Row " + Row_I6 + " telah diisi")

        Check()
    print("\n")

FormI1(2,2,2)
FormI2(2)
FormI3(3)
FormI4(2)
FormI5(3)
FormI6(2)