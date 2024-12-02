from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException as NSEE

import time

#Akun // Diisi dengan akun yang akan digunakan
username = ""
password = ""

driver = webdriver.Chrome()
action = ActionChains(driver)

driver.get("http://updmember.pii.or.id/index.php")
driver.maximize_window()

#input username
driver.find_element(By.ID, "email").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
# #masuk login
driver.find_element(By.ID, "m_login_signin_submit").click()

driver.implicitly_wait(2)

driver.find_element(By.LINK_TEXT, "FAIP").click()

driver.find_element(By.LINK_TEXT, "Edit").click()

# driver.find_element(By.LINK_TEXT, "BUAT FAIP BARU").click()
# WebDriverWait(driver, 10).until(EC.alert_is_present())
# driver.switch_to.alert.accept()

time.sleep(2)
Null = "no value"

#PENGISIAN I1
def FormI1(n_Alamat_I1,n_Lembaga_I1,n_Phone_I1):
    driver.find_element(By.LINK_TEXT, "I.1").click()
    driver.implicitly_wait(5)

    print("================================================\n\nFormI1\n")
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

    Counter_Alamat_I1 = 1
    
    print("Start from Row: " + str(ID_Count_Alamat_I1))
    print("Row Ditambah: " + str(n_Alamat_I1) + "\n")

    while Counter_Alamat_I1 <= n_Alamat_I1:
        #add row
        Alamat_Row_I1 = str(ID_Count_Alamat_I1)

        print("Counter Row: " + str(Counter_Alamat_I1))

        TambahI1alamat = driver.find_element(By.XPATH, '//button[@onclick="add111(\'ala\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI1alamat)
        action.move_to_element(TambahI1alamat).perform()
        TambahI1alamat.send_keys(Keys.ENTER)

        AddressType_I1 = "3"
        ID_AddressType_I1 = "addr_type" + Alamat_Row_I1
        Select_AddressType_I1 = Select(driver.find_element(By.ID, ID_AddressType_I1))
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

        #End/retry point of loop
        Counter_Alamat_I1 += 1
        ID_Count_Alamat_I1 += 1
        print("Row " + Alamat_Row_I1 + " telah diisi")

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

    Counter_Lembaga_I1 = 1
    
    print("Start from Row: " + str(ID_Count_Lembaga_I1))
    print("Row Ditambah: " + str(n_Lembaga_I1) + "\n")

    while Counter_Lembaga_I1 <= n_Lembaga_I1:
        #add row
        Lembaga_Row_I1 = str(ID_Count_Lembaga_I1)

        print("Counter Row: " + str(Counter_Lembaga_I1))

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

        #End/retry point of loop
        Counter_Lembaga_I1 += 1
        ID_Count_Lembaga_I1 += 1
        print("Row " + Lembaga_Row_I1 + " telah diisi")

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

    Counter_Phone_I1 = 1
    
    print("Start from Row: " + str(ID_Count_Phone_I1))
    print("Row Ditambah: " + str(n_Phone_I1) + "\n")

    while Counter_Phone_I1 <= n_Phone_I1:
        #add row
        Phone_Row_I1 = str(ID_Count_Phone_I1)

        print("Counter Row: " + str(Counter_Alamat_I1))

        TambahI1Phone = driver.find_element(By.XPATH, '//button[@onclick="add113(\'pho\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI1Phone)
        action.move_to_element(TambahI1Phone).perform()
        TambahI1Phone.send_keys(Keys.ENTER)

        PhoneType_I1 = "mobile_phone"
        ID_PhoneType_I1 = "phone_type" + Phone_Row_I1
        Select_PhoneType_I1 = Select(driver.find_element(By.ID, ID_PhoneType_I1))
        Select_PhoneType_I1.select_by_value(PhoneType_I1)

        PhoneValue_I1 = "+622112411575"
        ID_PhoneValue_I1 = "phone_value" + Phone_Row_I1
        driver.find_element(By.ID, ID_PhoneValue_I1).send_keys(PhoneValue_I1)

        #End/retry point of loop
        Counter_Phone_I1 += 1
        ID_Count_Phone_I1 += 1
        print("Row " + Phone_Row_I1 + " telah diisi")
    print("\n") 

    driver.refresh()

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

    Counter_I2 = 1
    
    print("Start from Row: " + str(ID_Count_I2))
    print("Row Ditambah: " + str(n_I2) + "\n")

    while Counter_I2 <= n_I2:
        #add row
        TambahI2 = driver.find_element(By.XPATH, '//button[@onclick="add12(\'edu\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI2)
        action.move_to_element(TambahI2).perform()
        TambahI2.send_keys(Keys.ENTER)

        Row_I2 = str(ID_Count_I2)

        print("Counter Row: " + str(Counter_I2))

        Universitas_I2 = "Universitas Diponegoro"
        ID_Universitas_I2 = "12_school" + Row_I2
        driver.find_element(By.ID, ID_Universitas_I2).send_keys(Universitas_I2)

        Tingkat_I2 = "S3"
        ID_Tingkat_I2 = "12_degree" + Row_I2
        Select_Tingkat_I2 = Select(driver.find_element(By.ID, ID_Tingkat_I2))
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

        JudulTA_I2 = "TA S3"
        ID_JudulTA_I2 = "12_activities" + Row_I2
        Scroll_JudulTA_I2 = driver.find_element(By.ID, ID_JudulTA_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_JudulTA_I2)
        action.move_to_element(Scroll_JudulTA_I2).perform()
        Scroll_JudulTA_I2.send_keys(JudulTA_I2)

        UraianTA_I2 = "Uraian TA"
        ID_UraianTA_I2 = "12_description" + Row_I2
        Scroll_UraianTA_I2 = driver.find_element(By.ID, ID_UraianTA_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_UraianTA_I2)
        action.move_to_element(Scroll_UraianTA_I2).perform()
        Scroll_UraianTA_I2.send_keys(UraianTA_I2)

        Nilai_I2 = "4.00"
        ID_Nilai_I2 = "12_score" + Row_I2
        Scroll_Nilai_I2 = driver.find_element(By.ID, ID_Nilai_I2)
        driver.execute_script("arguments[0].scrollIntoView();",Scroll_Nilai_I2)
        action.move_to_element(Scroll_Nilai_I2).perform()
        Scroll_Nilai_I2.send_keys(Nilai_I2)

        #End/retry point of loop
        Counter_I2 += 1
        ID_Count_I2 += 1
        print("Row " + Row_I2 + " telah diisi")
    print("\n")    
    
    driver.refresh()

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

    Counter_I3 = 1
    
    print("Start from Row: " + str(ID_Count_I3))
    print("Row Ditambah: " + str(n_I3) + "\n")

    while Counter_I3 <= n_I3:
        #add row
        TambahI3 = driver.find_element(By.XPATH, '//button[@onclick="add13(\'org\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI3)
        action.move_to_element(TambahI3).perform()
        TambahI3.send_keys(Keys.ENTER)

        Row_I3 = str(ID_Count_I3)

        print("Counter Row: " + str(Counter_I3))

        Organisasi_I3 = "Organisasi"
        ID_Organisasi_I3 = "13_nama_org"+ Row_I3
        driver.find_element(By.ID, ID_Organisasi_I3).send_keys(Organisasi_I3)

        Jenis_I3 = "Organisasi PII"      
        ID_Jenis_I3 = "13_jenis" + Row_I3
        Select_Jenis_I3 = Select(driver.find_element(By.ID, ID_Jenis_I3))
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

        BulanMulai_I3 = "1"
        ID_BulanMulai_I3 = "13_startdate" + Row_I3
        Select_BulanMulai_I3 = Select(driver.find_element(By.ID, ID_BulanMulai_I3))
        Select_BulanMulai_I3.select_by_value(BulanMulai_I3)

        TahunMulai_I3 = "2018"
        ID_TahunMulai_I3 = "13_startyear" + Row_I3
        driver.find_element(By.ID, ID_TahunMulai_I3).send_keys(TahunMulai_I3)

        BulanSelesai_I3 = "6"
        ID_BulanSelesai_I3 = "13_enddate" + Row_I3
        Select_BulanSelesai_I3 = Select(driver.find_element(By.ID, ID_BulanSelesai_I3))
        Select_BulanSelesai_I3.select_by_value(BulanSelesai_I3)

        TahunSelesai_I3 = "2023"
        ID_TahunSelesai_I3 = "13_endyear" + Row_I3
        driver.find_element(By.ID, ID_TahunSelesai_I3).send_keys(TahunSelesai_I3)

        Jabatan_I3 = "2"
        ID_Jabatan_I3 = "13_jabatan" + Row_I3
        Select_Jabatan_I3 = Select(driver.find_element(By.ID, ID_Jabatan_I3))
        Select_Jabatan_I3.select_by_value(Jabatan_I3)

        Tingkat_I3 = "1"
        ID_Tingkat_I3 = "13_tingkat" + Row_I3
        Select_Tingkat_I3 = Select(driver.find_element(By.ID, ID_Tingkat_I3))
        Select_Tingkat_I3.select_by_value(Tingkat_I3)

        Lingkup_I3 = "Asosiasi Profesi"
        ID_Lingkup_I3 = "13_lingkup" + Row_I3
        Select_Lingkup_I3 = Select(driver.find_element(By.ID, ID_Lingkup_I3))
        Select_Lingkup_I3.select_by_value(Lingkup_I3)

        ID_Anggota_I3 = "13_work" + Row_I3
        Angggota_I3 = driver.find_element(By.ID, ID_Anggota_I3)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();", Angggota_I3)
        action.move_to_element_with_offset(Angggota_I3, 0, -20).click().perform()
        
        Uraian_I3 = "aktifitas"
        ID_Uraian_I3 = "13_aktifitas" + Row_I3
        Scroll_Uraian_I3 = driver.find_element(By.ID, ID_Uraian_I3)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_I3)
        action.move_to_element(Scroll_Uraian_I3).perform()
        Scroll_Uraian_I3.send_keys(Uraian_I3)

        # Kompetisi I3 
        Komp_I3 = ["W.1.1.1","W.1.1.2","W.1.1.3"]
        ID_Komp_I3 = "13_komp" + Row_I3
        Scroll_Komp_I3 = driver.find_element(By.ID, ID_Komp_I3)
        action.move_to_element(Scroll_Komp_I3).perform()
        
        print("- Komp W1 I3: " + str(len(Komp_I3)))
        for Komp_Value_I3 in Komp_I3:
            Komp_Label_I3 = Komp_Value_I3[slice(5)]
            Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//optgroup[contains(@label, "{Komp_Label_I3}")]/option[@value="{Komp_Value_I3}."]'
            Komp_Find_I3 = driver.find_element(By.XPATH, Komp_Call_I3)
            action.move_to_element_with_offset(Komp_Find_I3, 0, -15).click().perform()
            print("-", Komp_Value_I3)

        #End/retry point of loop
        Counter_I3 += 1
        ID_Count_I3 += 1
        print("Row " + Row_I3 + " telah diisi")
    print("\n")
 
    driver.refresh()


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

    Counter_I4 = 1
    
    print("Start from Row: " + str(ID_Count_I4))
    print("Row Ditambah: " + str(n_I4) + "\n")

    while Counter_I4 <= n_I4:
        #add row
        TambahI4 = driver.find_element(By.XPATH, '//button[@onclick="add14(\'phg\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI4)
        action.move_to_element(TambahI4).perform()
        TambahI4.send_keys(Keys.ENTER)

        Row_I4 = str(ID_Count_I4)

        print("Counter Row: " + str(Counter_I4))

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
        
        BulanTerbit_I4 = "12"
        ID_BulanTerbit_I4 = "14_startdate" + Row_I4
        Select_BulanTerbit_I4 = Select(driver.find_element(By.ID, ID_BulanTerbit_I4))
        Select_BulanTerbit_I4.select_by_value(BulanTerbit_I4)

        Tahun_I4 = "2020"
        ID_Tahun_I4 = "14_startyear" + Row_I4
        driver.find_element(By.ID, ID_Tahun_I4).send_keys(Tahun_I4)

        Tingkat_I4 = "4"
        ID_Tingkat_I4 = "14_tingkat" + Row_I4
        Select_Tingkat_I4 = Select(driver.find_element(By.ID, ID_Tingkat_I4))
        Select_Tingkat_I4.select_by_value(Tingkat_I4)

        Lembaga_I4 = "4"
        ID_Lembaga_I4 = "14_tingkatlembaga" + Row_I4
        Select_Lembaga_I4 = Select(driver.find_element(By.ID, ID_Lembaga_I4))
        Select_Lembaga_I4.select_by_value(Lembaga_I4)

        Uraian_I4 = "Uraian Singkat Aktifitas"
        ID_Uraian_I4 = "14_uraian" + Row_I4
        Scroll_Uraian_I4 = driver.find_element(By.ID, ID_Uraian_I4)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_I4)
        action.move_to_element(Scroll_Uraian_I4).perform()
        Scroll_Uraian_I4.send_keys(Uraian_I4)

        # Kompetisi I4 
        Komp_I4 = ["W.1.1.1","W.1.1.2","W.1.1.3"]
        ID_Komp_I4 = "14_komp" + Row_I4
        Scroll_Komp_I4 = driver.find_element(By.ID, ID_Komp_I4)
        action.move_to_element(Scroll_Komp_I4).perform()
        
        print("- Komp W1 I4: " + str(len(Komp_I4)))
        for Komp_Value_I4 in Komp_I4:
            Komp_Label_I4 = Komp_Value_I4[slice(5)]
            Komp_Call_I4 = f'//*[@id="{ID_Komp_I4}"]//optgroup[contains(@label, "{Komp_Label_I4}")]/option[@value="{Komp_Value_I4}."]'
            Komp_Find_I4 = driver.find_element(By.XPATH, Komp_Call_I4)
            action.move_to_element_with_offset(Komp_Find_I4, 0, -15).click().perform()
            print("-", Komp_Value_I4)

        #End/retry point of loop
        Counter_I4 += 1
        ID_Count_I4 += 1
        print("Row " + Row_I4 + " telah diisi")
    print("\n")

    driver.refresh()

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

    Counter_I5 = 1
    
    print("Start from Row: " + str(ID_Count_I5))
    print("Row Ditambah: " + str(n_I5) + "\n")

    while Counter_I5 <= n_I5:
        #add row
        TambahI5 = driver.find_element(By.XPATH, '//button[@onclick="add15(\'pdd\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI5)
        action.move_to_element(TambahI5).perform()
        TambahI5.send_keys(Keys.ENTER)

        Row_I5 = str(ID_Count_I5)

        print("Counter Row: " + str(Counter_I5))

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

        BulanMulai_I5 = "1"
        ID_BulanMulai_I5 = "15_startdate" + Row_I5
        Select_BulanMulai_I5 = Select(driver.find_element(By.ID, ID_BulanMulai_I5))
        Select_BulanMulai_I5.select_by_value(BulanMulai_I5)

        TahunMulai_I5 = "2019"
        ID_TahunMulai_I5 = "15_startyear" + Row_I5
        driver.find_element(By.ID, ID_TahunMulai_I5).send_keys(TahunMulai_I5)

        BulanSelesai_I5 = "7"
        ID_BulanSelesai_I5 = "15_enddate" + Row_I5
        Select_BulanSelesai_I5 = Select(driver.find_element(By.ID, ID_BulanSelesai_I5))
        Select_BulanSelesai_I5.select_by_value(BulanSelesai_I5)
        
        TahunSelesai_I5 = "2022"
        ID_TahunSelesai_I5 = "15_endyear" + Row_I5
        driver.find_element(By.ID, ID_TahunSelesai_I5).send_keys(TahunSelesai_I5)

        Tingkat_I5 = "2"
        ID_Tingkat_I5 = "15_tingkat" + Row_I5
        Select_Tingkat_I5 = Select(driver.find_element(By.ID, ID_Tingkat_I5))
        Select_Tingkat_I5.select_by_value(Tingkat_I5)

        Jam_I5 = "2"
        ID_Jam_I5 = "15_jam" + Row_I5
        Select_Jam_I5 = Select(driver.find_element(By.ID, ID_Jam_I5))
        Select_Jam_I5.select_by_value(Jam_I5)
        
        ID_Anggota_I5 = "15_work" + Row_I5
        Angggota_I5 = driver.find_element(By.ID, ID_Anggota_I5)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();", Angggota_I5)
        action.move_to_element_with_offset(Angggota_I5, 0, -20).click().perform()

        Uraian_I5 = "Uraian Singkat Aktifitas"
        ID_Uraian_I5 = "15_uraian" + Row_I5
        Scroll_Uraian_I5 = driver.find_element(By.ID, ID_Uraian_I5)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_I5)
        action.move_to_element(Scroll_Uraian_I5).perform()
        Scroll_Uraian_I5.send_keys(Uraian_I5)

        # Kompetisi I5 
        Komp_I5 = ["W.2.1.1","W.2.1.2","W.2.1.3"]
        ID_Komp_I5 = "15_komp" + Row_I5
        Scroll_Komp_I5 = driver.find_element(By.ID, ID_Komp_I5)
        action.move_to_element(Scroll_Komp_I5).perform()
        
        print("- Komp W1 I5: " + str(len(Komp_I5)))
        for Komp_Value_I5 in Komp_I5:
            Komp_Label_I5 = Komp_Value_I5[slice(5)]
            Komp_Call_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_I5}")]/option[@value="{Komp_Value_I5}."]'
            Komp_Find_I5 = driver.find_element(By.XPATH, Komp_Call_I5)
            action.move_to_element_with_offset(Komp_Find_I5, 0, -15).click().perform()
            print("-", Komp_Value_I5)

        #End/retry point of loop
        Counter_I5 += 1
        ID_Count_I5 += 1
        print("Row " + Row_I5 + " telah diisi")
    print("\n")

    driver.refresh()

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

    Counter_I6 = 1
    
    print("Start from Row: " + str(ID_Count_I6))
    print("Row Ditambah: " + str(n_I6) + "\n")

    while Counter_I6 <= n_I6:
        #add row
        TambahI6 = driver.find_element(By.XPATH, '//button[@onclick="add16(\'ppm\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahI6)
        action.move_to_element(TambahI6).perform()
        TambahI6.send_keys(Keys.ENTER)

        Row_I6 = str(ID_Count_I6)

        print("Counter Row: " + str(Counter_I6))

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

        BulanMulai_I6 = "1"
        ID_BulanMulai_I6 = "16_startdate" + Row_I6
        Select_BulanMulai_I6 = Select(driver.find_element(By.ID, ID_BulanMulai_I6))
        Select_BulanMulai_I6.select_by_value(BulanMulai_I6)

        TahunMulai_I6 = "2019"
        ID_TahunMulai_I6 = "16_startyear" + Row_I6
        driver.find_element(By.ID, ID_TahunMulai_I6).send_keys(TahunMulai_I6)

        BulanSelesai_I6 = "7"
        ID_BulanSelesai_I6 = "16_enddate" + Row_I6
        Select_BulanSelesai_I6 = Select(driver.find_element(By.ID, ID_BulanSelesai_I6))
        Select_BulanSelesai_I6.select_by_value(BulanSelesai_I6)

        TahunSelesai_I6 = "2022"
        ID_TahunSelesai_I6 = "16_endyear" + Row_I6
        driver.find_element(By.ID, ID_TahunSelesai_I6).send_keys(TahunSelesai_I6)

        Tingkat_I6 = "2"
        ID_Tingkat_I6 = "16_tingkat" + Row_I6
        Select_Tingkat_I6 = Select(driver.find_element(By.ID, ID_Tingkat_I6))
        Select_Tingkat_I6.select_by_value(Tingkat_I6)

        Jam_I6 = "2"
        ID_Jam_I6 = "16_jam" + Row_I6
        Select_Jam_I6 = Select(driver.find_element(By.ID, ID_Jam_I6))
        Select_Jam_I6.select_by_value(Jam_I6)
        
        ID_Anggota_I6 = "16_work" + Row_I6
        Angggota_I6 = driver.find_element(By.ID, ID_Anggota_I6)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();", Angggota_I6)
        action.move_to_element_with_offset(Angggota_I6, 0, -20).click().perform()

        Uraian_I6 = "Uraian Singkat Aktifitas"
        ID_Uraian_I6 = "16_uraian" + Row_I6
        Scroll_Uraian_I6 = driver.find_element(By.ID, ID_Uraian_I6)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_I6)
        action.move_to_element(Scroll_Uraian_I6).perform()
        Scroll_Uraian_I6.send_keys(Uraian_I6)

        # Kompetisi I6 
        Komp_I6 = ["W.1.1.1","W.1.1.2","W.1.1.3"]
        ID_Komp_I6 = "16_komp" + Row_I6
        Scroll_Komp_I6 = driver.find_element(By.ID, ID_Komp_I6)
        action.move_to_element(Scroll_Komp_I6).perform()
        
        print("- Komp W1 I6: " + str(len(Komp_I6)))
        for Komp_Value_I6 in Komp_I6:
            Komp_Label_I6 = Komp_Value_I6[slice(5)]
            Komp_Call_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_I6}")]/option[@value="{Komp_Value_I6}."]'
            Komp_Find_I6 = driver.find_element(By.XPATH, Komp_Call_I6)
            action.move_to_element_with_offset(Komp_Find_I6, 0, -15).click().perform()
            print("-", Komp_Value_I6)

        #End/retry point of loop
        Counter_I6 += 1
        ID_Count_I6 += 1
        print("Row " + Row_I6 + " telah diisi")
    print("\n")

    driver.refresh()

#PENGISIAN II1
def FormII1(n_II1):
    driver.find_element(By.LINK_TEXT, "II.1").click()
    driver.implicitly_wait(5)

    ID_Count_II1 = 1  
    print("================================================\nFormII1")
    
    try:
        while ID_Count_II1 < 100:
            Row_ID_II1 = f'//*[@class=" ref-item"][@data-id="{str(ID_Count_II1)}"]'    
            Check_Row_II1 = driver.find_element(By.XPATH, Row_ID_II1)
            if Check_Row_II1.is_enabled:
                print("Row " + str(ID_Count_II1) + " ada") 
            else:
                break
            ID_Count_II1 += 1
    except NSEE:
        print ("Row " + str(ID_Count_II1) + " tidak ada") 

    Counter_II1 = 1
    
    print("Start from Row: " + str(ID_Count_II1))
    print("Row Ditambah: " + str(n_II1) + "\n")

    while Counter_II1 <= n_II1:
        #add row
        TambahII1 = driver.find_element(By.XPATH, '//button[@onclick="add21(\'ref\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahII1)
        action.move_to_element(TambahII1).perform()
        TambahII1.send_keys(Keys.ENTER)

        Row_II1 = str(ID_Count_II1)

        print("Counter Row: " + str(Counter_II1))

        Nama_II1 = "Referensi Kode Etika"
        ID_Nama_II1 = "21_nama" + Row_II1
        driver.find_element(By.ID, ID_Nama_II1).send_keys(Nama_II1)

        Lembaga_II1 = "Lembaga Kode Etika"
        ID_Lembaga_II1 = "21_lembaga" + Row_II1
        driver.find_element(By.ID, ID_Lembaga_II1).send_keys(Lembaga_II1)

        Alamat_II1 = "Alamat Kode Etika"
        ID_Alamat_II1 = "21_alamat" + Row_II1
        driver.find_element(By.ID, ID_Alamat_II1).send_keys(Alamat_II1)

        Kota_II1 = "Semarang"
        ID_Kota_II1 = "21_kota" + Row_II1
        driver.find_element(By.ID, ID_Kota_II1).send_keys(Kota_II1)

        Provinsi_II1 = "Jawa Tengah"
        ID_Provinsi_II1 = "21_provinsi" + Row_II1
        driver.find_element(By.ID, ID_Provinsi_II1).send_keys(Provinsi_II1)

        Negara_II1 = "Indonesia"
        ID_Negara_II1 = "21_negara" + Row_II1
        driver.find_element(By.ID, ID_Negara_II1).send_keys(Negara_II1)

        NoTelp_II1 = "0000"
        ID_NoTelp_II1 = "21_notelp" + Row_II1
        driver.find_element(By.ID, ID_NoTelp_II1).send_keys(NoTelp_II1)

        Email_II1 = "Email@undip.ac.id"
        ID_Email_II1 = "21_email" + Row_II1
        driver.find_element(By.ID, ID_Email_II1).send_keys(Email_II1)

        Hubungan_II1 = "Atasan"
        ID_Hubungan_II1 = "21_hubungan" + Row_II1
        Select_Hubungan_II1 = Select(driver.find_element(By.ID, ID_Hubungan_II1))
        Select_Hubungan_II1.select_by_value(Hubungan_II1)

        #End/retry point of loop
        Counter_II1 += 1
        ID_Count_II1 += 1
        print("Row " + Row_II1 + " telah diisi")
    print("\n")

    driver.refresh()   

#PENGISIAN II2
def FormII2(n_II2):
    driver.find_element(By.LINK_TEXT, "II.2").click()
    driver.implicitly_wait(5)

    ID_Count_II2 = 1  
    print("================================================\nFormII2")
    
    try:
        while ID_Count_II2 < 100:
            Row_ID_II2 = f'//*[@class=" eti-item"][@data-id="{str(ID_Count_II2)}"]'    
            Check_Row_II2 = driver.find_element(By.XPATH, Row_ID_II2)
            if Check_Row_II2.is_enabled:
                print("Row " + str(ID_Count_II2) + " ada") 
            else:
                break
            ID_Count_II2 += 1
    except NSEE:
        print ("Row " + str(ID_Count_II2) + " tidak ada") 

    Counter_II2 = 1
    
    print("Start from Row: " + str(ID_Count_II2))
    print("Row Ditambah: " + str(n_II2) + "\n")

    while Counter_II2 <= n_II2:
        #add row
        TambahII2 = driver.find_element(By.XPATH, '//button[@onclick="add22(\'eti\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahII2)
        action.move_to_element(TambahII2).perform()
        TambahII2.send_keys(Keys.ENTER)

        Row_II2 = str(ID_Count_II2)

        print("Counter Row: " + str(Counter_II2))

        Uraian_II2 = "Uraian"
        ID_Uraian_II2 = "22_uraian" + Row_II2
        driver.find_element(By.ID, ID_Uraian_II2).send_keys(Uraian_II2)

        #End/retry point of loop
        Counter_II2 += 1
        ID_Count_II2 += 1
        print("Row " + Row_II2 + " telah diisi")
    print("\n")
    
    driver.refresh()     

#PENGISIAN III
def FormIII(n_III):
    driver.find_element(By.LINK_TEXT, "III").click()
    driver.implicitly_wait(5)

    ID_Count_III = 1  
    print("================================================\nFormIII")
    
    try:
        while ID_Count_III < 100:
            Row_ID_III = f'//*[@class=" kup-item"][@data-id="{str(ID_Count_III)}"]'    
            Check_Row_III = driver.find_element(By.XPATH, Row_ID_III)
            if Check_Row_III.is_enabled:
                print("Row " + str(ID_Count_III) + " ada") 
            else:
                break
            ID_Count_III += 1
    except NSEE:
        print ("Row " + str(ID_Count_III) + " tidak ada") 
 
    Counter_III = 1
   
    print("Start from Row: " + str(ID_Count_III))
    print("Row Ditambah: " + str(n_III) + "\n")

    while Counter_III <= n_III:
        #add row
        TambahIII = driver.find_element(By.XPATH, '//button[@onclick="add3(\'kup\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahIII)
        action.move_to_element(TambahIII).perform()
        TambahIII.send_keys(Keys.ENTER)

        Row_III = str(ID_Count_III)

        print("Counter Row: " + str(Counter_III))

        BulanMulai_III = "1"
        ID_BulanMulai_III = "3_startdate" + Row_III
        Select_BulanMulai_III = Select(driver.find_element(By.ID, ID_BulanMulai_III))
        Select_BulanMulai_III.select_by_value(BulanMulai_III)

        TahunMulai_III = "2019"
        ID_TahunMulai_III = "3_startyear" + Row_III
        driver.find_element(By.ID, ID_TahunMulai_III).send_keys(TahunMulai_III)

        BulanSelesai_III = "4"
        ID_BulanSelesai_III = "3_enddate" + Row_III
        Select_BulanSelesai_III = Select(driver.find_element(By.ID, ID_BulanSelesai_III))
        Select_BulanSelesai_III.select_by_value(BulanSelesai_III)

        TahunSelesai_III = "2022"
        ID_TahunSelesai_III = "3_endyear" + Row_III
        driver.find_element(By.ID, ID_TahunSelesai_III).send_keys(TahunSelesai_III)

        ID_Anggota_III = "3_work" + Row_III
        Angggota_III = driver.find_element(By.ID, ID_Anggota_III)
        #IF masih anggota and yes
        driver.execute_script("arguments[0].scrollIntoView();",Angggota_III)
        action.move_to_element_with_offset(Angggota_III, 0, -20).click().perform()

        Instansi_III = "Instansi"
        ID_Instansi_III = "3_instansi" + Row_III
        driver.find_element(By.ID, ID_Instansi_III).send_keys(Instansi_III)

        Jabatan_III = "Jabatan"
        ID_Jabatan_III = "3_title" + Row_III
        driver.find_element(By.ID, ID_Jabatan_III).send_keys(Jabatan_III)
        
        Proyek_III = "Proyek"
        ID_Proyek_III = "3_namaproyek" + Row_III
        driver.find_element(By.ID, ID_Proyek_III).send_keys(Proyek_III)

        Penugas_III = "Penugas"
        ID_Penugas_III = "3_pemberitugas" + Row_III
        driver.find_element(By.ID, ID_Penugas_III).send_keys(Penugas_III)

        Kota_III = "Semarang"
        ID_Kota_III = "3_location" + Row_III
        driver.find_element(By.ID, ID_Kota_III).send_keys(Kota_III)

        Provinsi_III = "Jawa Tengah"
        ID_Provinsi_III = "3_provinsi" + Row_III
        driver.find_element(By.ID, ID_Provinsi_III).send_keys(Provinsi_III)

        Negara_III = "Indonesia"
        ID_Negara_III = "3_negara" + Row_III
        driver.find_element(By.ID, ID_Negara_III).send_keys(Negara_III)

        Periode_III = "2"
        ID_Periode_III = "3_periode" + Row_III
        Select_Periode_III = Select(driver.find_element(By.ID, ID_Periode_III))
        Select_Periode_III.select_by_value(Periode_III)
        
        Posisi_III = "2"
        ID_Posisi_III = "3_posisi" + Row_III
        Select_Posisi_III = Select(driver.find_element(By.ID, ID_Posisi_III))
        Select_Posisi_III.select_by_value(Posisi_III)

        Nilai_III = "100"
        ID_Nilai_III = "3_nilaipry" + Row_III
        Scroll_Nilai_III = driver.find_element(By.ID, ID_Nilai_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Nilai_III)
        driver.find_element(By.ID, ID_Nilai_III).send_keys(Nilai_III)

        TanggungJawab_III = "TanggungJawab"
        ID_TanggungJawab_III = "3_nilaijasa" + Row_III
        Scroll_TanggungJawab_III = driver.find_element(By.ID, ID_TanggungJawab_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_TanggungJawab_III)
        driver.find_element(By.ID, ID_TanggungJawab_III).send_keys(TanggungJawab_III)

        SDM_III = "2"
        ID_SDM_III = "3_nilaisdm" + Row_III
        Scroll_SDM_III = driver.find_element(By.ID, ID_SDM_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_SDM_III)
        Select_SDM_III = Select(driver.find_element(By.ID, ID_SDM_III))
        Select_SDM_III.select_by_value(SDM_III)

        TingkatSulit_III = "2"
        ID_TingkatSulit_III = "3_nilaisulit" + Row_III
        Scroll_TingkatSulit_III = driver.find_element(By.ID, ID_TingkatSulit_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_TingkatSulit_III)
        Select_TingkatSulit_III = Select(driver.find_element(By.ID, ID_TingkatSulit_III))
        Select_TingkatSulit_III.select_by_value(TingkatSulit_III)

        NilaiProyek_III = "2"
        ID_NilaiProyek_III = "3_nilaiproyek" + Row_III
        Scroll_NilaiProyek_III = driver.find_element(By.ID, ID_NilaiProyek_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_NilaiProyek_III)
        Select_NilaiProyek_III = Select(driver.find_element(By.ID, ID_NilaiProyek_III))
        Select_NilaiProyek_III.select_by_value(NilaiProyek_III)

        Uraian_III = "Uraian"
        ID_Uraian_III = "3_uraian" + Row_III
        Scroll_Uraian_III = driver.find_element(By.ID, ID_Uraian_III)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_III)
        driver.find_element(By.ID, ID_Uraian_III).send_keys(Uraian_III)

        # Kompetisi III 
        Komp_III = ["W.2.1.1","W.2.1.2","W.2.1.3"]
        ID_Komp_III = "3_komp" + Row_III
        Scroll_Komp_III = driver.find_element(By.ID, ID_Komp_III)
        action.move_to_element(Scroll_Komp_III).perform()
        
        print("- Komp W1 III: " + str(len(Komp_III)))
        for Komp_Value_III in Komp_III:
            Komp_Label_III = Komp_Value_III[slice(5)]
            Komp_Call_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_III}")]/option[@value="{Komp_Value_III}."]'
            Komp_Find_III = driver.find_element(By.XPATH, Komp_Call_III)
            action.move_to_element_with_offset(Komp_Find_III, 0, -15).click().perform()
            print("-", Komp_Value_III)

        #End/retry point of loop
        Counter_III += 1
        ID_Count_III += 1
        print("Row " + Row_III + " telah diisi")
    print("\n")

    driver.refresh()    

#PENGISIAN IV
def FormIV(n_IV):
    driver.find_element(By.LINK_TEXT, "IV").click()
    driver.implicitly_wait(5)

    ID_Count_IV = 1  
    print("================================================\nFormIV")
    
    try:
        while ID_Count_IV < 100:
            Row_ID_IV = f'//*[@class=" man-item"][@data-id="{str(ID_Count_IV)}"]'    
            Check_Row_IV = driver.find_element(By.XPATH, Row_ID_IV)
            if Check_Row_IV.is_enabled:
                print("Row " + str(ID_Count_IV) + " ada") 
            else:
                break
            ID_Count_IV += 1
    except NSEE:
        print ("Row " + str(ID_Count_IV) + " tidak ada") 

    Counter_IV = 1
    
    print("Start from Row: " + str(ID_Count_IV))
    print("Row Ditambah: " + str(n_IV) + "\n")

    while Counter_IV <= n_IV:
        #add row
        TambahIV = driver.find_element(By.XPATH, '//button[@onclick="add4(\'man\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahIV)
        action.move_to_element(TambahIV).perform()
        TambahIV.send_keys(Keys.ENTER)

        Row_IV = str(ID_Count_IV)

        print("Counter Row: " + str(Counter_IV))

        Instansi_IV = "Instansi"
        ID_Instansi_IV = "4_instansi" + Row_IV
        driver.find_element(By.ID, ID_Instansi_IV).send_keys(Instansi_IV)
        
        NamaProyek_IV = "Proyek"
        ID_NamaProyek_IV = "4_namaproyek" + Row_IV
        driver.find_element(By.ID, ID_NamaProyek_IV).send_keys(NamaProyek_IV)

        Kota_IV = "Semarang"
        ID_Kota_IV = "4_location" + Row_IV
        driver.find_element(By.ID, ID_Kota_IV).send_keys(Kota_IV)

        Provinsi_IV = "Jawa Tengah"
        ID_Provinsi_IV = "4_provinsi" + Row_IV
        driver.find_element(By.ID, ID_Provinsi_IV).send_keys(Provinsi_IV)

        Negara_IV = "Indonesia"
        ID_Negara_IV = "4_negara" + Row_IV
        driver.find_element(By.ID, ID_Negara_IV).send_keys(Negara_IV)

        Periode_IV = "3"
        ID_Periode_IV = "4_periode" + Row_IV
        Select_Periode_IV = Select(driver.find_element(By.ID, ID_Periode_IV))
        Select_Periode_IV.select_by_value(Periode_IV)

        Posisi_IV = "2"
        ID_Posisi_IV = "4_posisi" + Row_IV
        Select_Posisi_IV = Select(driver.find_element(By.ID, ID_Posisi_IV))
        Select_Posisi_IV.select_by_value(Posisi_IV)

        JumlahSKS_IV = "1"
        ID_JumlahSKS_IV = "4_jumlahsks" + Row_IV
        Select_JumlahSKS_IV = Select(driver.find_element(By.ID, ID_JumlahSKS_IV))
        Select_JumlahSKS_IV.select_by_value(JumlahSKS_IV)

        Uraian_IV = "Uraian"
        ID_Uraian_IV = "4_uraian" + Row_IV
        Scroll_Uraian_IV = driver.find_element(By.ID, ID_Uraian_IV)
        driver.execute_script("arguments[0].scrollIntoView();", Scroll_Uraian_IV)
        driver.find_element(By.ID, ID_Uraian_IV).send_keys(Uraian_IV)

        # Kompetisi IV 
        Komp_IV = ["P.5.1.1","P.5.1.2","P.5.1.3"]
        ID_Komp_IV = "4_komp" + Row_IV
        Scroll_Komp_IV = driver.find_element(By.ID, ID_Komp_IV)
        action.move_to_element(Scroll_Komp_IV).perform()
        
        print("- Komp W1 IV: " + str(len(Komp_IV)))
        for Komp_Value_IV in Komp_IV:
            Komp_Label_IV = Komp_Value_IV[slice(5)]
            Komp_Call_IV = f'//*[@id="{ID_Komp_IV}"]//optgroup[contains(@label, "{Komp_Label_IV}")]/option[@value="{Komp_Value_IV}."]'
            Komp_Find_IV = driver.find_element(By.XPATH, Komp_Call_IV)
            action.move_to_element_with_offset(Komp_Find_IV, 0, -15).click().perform()
            print("-", Komp_Value_IV)

        #End/retry point of loop
        Counter_IV += 1
        ID_Count_IV += 1
        print("Row " + Row_IV + " telah diisi")
    print("\n")

    driver.refresh() 

#PENGISIAN V1
def FormV1(n_V1):
    driver.find_element(By.LINK_TEXT, "V.1").click()
    driver.implicitly_wait(5)

    ID_Count_V1 = 1  
    print("================================================\nFormV1")
    
    try:
        while ID_Count_V1 < 100:
            Row_ID_V1 = f'//*[@class=" pub-item"][@data-id="{str(ID_Count_V1)}"]'    
            Check_Row_V1 = driver.find_element(By.XPATH, Row_ID_V1)
            if Check_Row_V1.is_enabled:
                print("Row " + str(ID_Count_V1) + " ada") 
            else:
                break
            ID_Count_V1 += 1
    except NSEE:
        print ("Row " + str(ID_Count_V1) + " tidak ada") 

    Counter_V1 = 1
    
    print("Start from Row: " + str(ID_Count_V1))
    print("Row Ditambah: " + str(n_V1) + "\n")

    while Counter_V1 <= n_V1:
        #add row
        TambahV1 = driver.find_element(By.XPATH, '//button[@onclick="add51(\'pub\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahV1)
        action.move_to_element(TambahV1).perform()
        TambahV1.send_keys(Keys.ENTER)

        Row_V1 = str(ID_Count_V1)

        Judul_V1 = "Judul"
        ID_Judul_V1 = "51_nama" + Row_V1
        driver.find_element(By.ID, ID_Judul_V1).send_keys(Judul_V1)

        Media_V1 = "Media"
        ID_Media_V1 = "51_media" + Row_V1
        driver.find_element(By.ID, ID_Media_V1).send_keys(Media_V1)

        Kota_V1 = "Semarang"
        ID_Kota_V1 = "51_location" + Row_V1
        driver.find_element(By.ID, ID_Kota_V1).send_keys(Kota_V1)

        Provinsi_V1 = "Jawa Tengah"
        ID_Provinsi_V1 = "51_provinsi" + Row_V1
        driver.find_element(By.ID, ID_Provinsi_V1).send_keys(Provinsi_V1)

        Negara_V1 = "Indonesia"
        ID_Negara_V1 = "51_negara" + Row_V1
        driver.find_element(By.ID, ID_Negara_V1).send_keys(Negara_V1)

        BulanPublikasi_V1 = "1"
        ID_BulanPublikasi_V1 = "51_startdate" + Row_V1
        Select_BulanPublikasi_V1 = Select(driver.find_element(By.ID, ID_BulanPublikasi_V1))
        Select_BulanPublikasi_V1.select_by_value(BulanPublikasi_V1)

        TahunPublikasi_V1 = "2018"
        ID_TahunPublikasi_V1 = "51_startyear" + Row_V1
        driver.find_element(By.ID, ID_TahunPublikasi_V1).send_keys(TahunPublikasi_V1)

        TingkatMedia_V1 = "1"
        ID_TingkatMedia_V1 = "51_tingkatmedia" + Row_V1
        Select_TingkatMedia_V1 = Select(driver.find_element(By.ID, ID_TingkatMedia_V1))
        Select_TingkatMedia_V1.select_by_value(TingkatMedia_V1)

        Uraian_V1 = "Uraian"
        ID_Uraian_V1 = "51_uraian" + Row_V1
        driver.find_element(By.ID, ID_Uraian_V1).send_keys(Uraian_V1)

        Tingkat_V1 = "1"
        ID_Tingkat_V1 = "51_tingkat" + Row_V1
        Select_Tingkat_V1 = Select(driver.find_element(By.ID, ID_Tingkat_V1))
        Select_Tingkat_V1.select_by_value(Tingkat_V1)

        # Kompetisi V1 
        Komp_V1 = ["W.4.1.1","W.4.1.2","W.4.1.3"]
        ID_Komp_V1 = "51_komp" + Row_V1
        Scroll_Komp_V1 = driver.find_element(By.ID, ID_Komp_V1)
        action.move_to_element(Scroll_Komp_V1).perform()
        
        print("- Komp W1 V1: " + str(len(Komp_V1)))
        for Komp_Value_V1 in Komp_V1:
            Komp_Label_V1 = Komp_Value_V1[slice(5)]
            Komp_Call_V1 = f'//*[@id="{ID_Komp_V1}"]//optgroup[contains(@label, "{Komp_Label_V1}")]/option[@value="{Komp_Value_V1}."]'
            Komp_Find_V1 = driver.find_element(By.XPATH, Komp_Call_V1)
            action.move_to_element_with_offset(Komp_Find_V1, 0, -15).click().perform()
            print("-", Komp_Value_V1)

        #End/retry point of loop
        Counter_V1 += 1
        ID_Count_V1 += 1
        print("Row " + Row_V1 + " telah diisi")
    print("\n")

    driver.refresh() 

#PENGISIAN V2
def FormV2(n_V2):
    driver.find_element(By.LINK_TEXT, "V.2").click()
    driver.implicitly_wait(5)

    ID_Count_V2 = 1  
    print("================================================\nFormV2")
    
    try:
        while ID_Count_V2 < 100:
            Row_ID_V2 = f'//*[@class=" lok-item"][@data-id="{str(ID_Count_V2)}"]'    
            Check_Row_V2 = driver.find_element(By.XPATH, Row_ID_V2)
            if Check_Row_V2.is_enabled:
                print("Row " + str(ID_Count_V2) + " ada") 
            else:
                break
            ID_Count_V2 += 1
    except NSEE:
        print ("Row " + str(ID_Count_V2) + " tidak ada") 

    Counter_V2 = 1
    
    print("Start from Row: " + str(ID_Count_V2))
    print("Row Ditambah: " + str(n_V2) + "\n")

    while Counter_V2 <= n_V2:
        #add row
        TambahV2 = driver.find_element(By.XPATH, '//button[@onclick="add52(\'lok\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahV2)
        action.move_to_element(TambahV2).perform()
        TambahV2.send_keys(Keys.ENTER)

        Row_V2 = str(ID_Count_V2)

        print("Counter Row: " + str(Counter_V2))

        Judul_V2 = "Judul"
        ID_Judul_V2 = "52_judul" + Row_V2
        driver.find_element(By.ID, ID_Judul_V2).send_keys(Judul_V2)

        Seminar_V2 = "Seminar"
        ID_Seminar_V2 = "52_nama" + Row_V2
        driver.find_element(By.ID, ID_Seminar_V2).send_keys(Seminar_V2)
        
        Penyelenggara_V2 = "Penyelenggara"
        ID_Penyelenggara_V2 = "52_penyelenggara" + Row_V2
        driver.find_element(By.ID, ID_Penyelenggara_V2).send_keys(Penyelenggara_V2)

        Kota_V2 = "Semarang"
        ID_Kota_V2 = "52_location" + Row_V2
        driver.find_element(By.ID, ID_Kota_V2).send_keys(Kota_V2)

        Provinsi_V2 = "Jawa Tengah"
        ID_Provinsi_V2 = "52_provinsi" + Row_V2
        driver.find_element(By.ID, ID_Provinsi_V2).send_keys(Provinsi_V2)

        Negara_V2 = "Indonesia"
        ID_Negara_V2 = "52_negara" + Row_V2
        driver.find_element(By.ID, ID_Negara_V2).send_keys(Negara_V2)

        BulanSeminar_V2 = "1"
        ID_BulanSeminar_V2 = "52_startdate" + Row_V2
        Select_BulanSeminar_V2 = Select(driver.find_element(By.ID, ID_BulanSeminar_V2))
        Select_BulanSeminar_V2.select_by_value(BulanSeminar_V2)

        TahunSeminar_V2 = "2018"
        ID_TahunSeminar_V2 = "52_startyear" + Row_V2
        driver.find_element(By.ID, ID_TahunSeminar_V2).send_keys(TahunSeminar_V2)

        TingkatSeminar_V2 = "1"
        ID_TingkatSeminar_V2 = "52_tingkatseminar" + Row_V2
        Select_TingkatSeminar_V2 = Select(driver.find_element(By.ID, ID_TingkatSeminar_V2))
        Select_TingkatSeminar_V2.select_by_value(TingkatSeminar_V2)

        Uraian_V2 = "Uraian"
        ID_Uraian_V2 = "52_uraian" + Row_V2
        driver.find_element(By.ID, ID_Uraian_V2).send_keys(Uraian_V2)

        Tingkat_V2 = "1"
        ID_Tingkat_V2 = "52_tingkat" + Row_V2
        Select_Tingkat_V2 = Select(driver.find_element(By.ID, ID_Tingkat_V2))
        Select_Tingkat_V2.select_by_value(Tingkat_V2)

        # Kompetisi V2 
        Komp_V2 = ["W.4.1.1","W.4.1.2","W.4.1.3"]
        ID_Komp_V2 = "52_komp" + Row_V2
        Scroll_Komp_V2 = driver.find_element(By.ID, ID_Komp_V2)
        action.move_to_element(Scroll_Komp_V2).perform()
        
        print("- Komp W1 V2: " + str(len(Komp_V2)))
        for Komp_Value_V2 in Komp_V2:
            Komp_Label_V2 = Komp_Value_V2[slice(5)]
            Komp_Call_V2 = f'//*[@id="{ID_Komp_V2}"]//optgroup[contains(@label, "{Komp_Label_V2}")]/option[@value="{Komp_Value_V2}."]'
            Komp_Find_V2 = driver.find_element(By.XPATH, Komp_Call_V2)
            action.move_to_element_with_offset(Komp_Find_V2, 0, -15).click().perform()
            print("-", Komp_Value_V2)

        #End/retry point of loop
        Counter_V2 += 1
        ID_Count_V2 += 1
        print("Row " + Row_V2 + " telah diisi")
    print("\n")

    driver.refresh() 

#PENGISIAN V3
def FormV3(n_V3):
    driver.find_element(By.LINK_TEXT, "V.3").click()
    driver.implicitly_wait(5)

    ID_Count_V3 = 1  
    print("================================================\nFormV3")
    
    try:
        while ID_Count_V3 < 100:
            Row_ID_V3 = f'//*[@class=" sem-item"][@data-id="{str(ID_Count_V3)}"]'    
            Check_Row_V3 = driver.find_element(By.XPATH, Row_ID_V3)
            if Check_Row_V3.is_enabled:
                print("Row " + str(ID_Count_V3) + " ada") 
            else:
                break
            ID_Count_V3 += 1
    except NSEE:
        print ("Row " + str(ID_Count_V3) + " tidak ada") 

    Counter_V3 = 1
    
    print("Start from Row: " + str(ID_Count_V3))
    print("Row Ditambah: " + str(n_V3) + "\n")

    while Counter_V3 <= n_V3:
        #add row
        TambahV3 = driver.find_element(By.XPATH, '//button[@onclick="add53(\'sem\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahV3)
        action.move_to_element(TambahV3).perform()
        TambahV3.send_keys(Keys.ENTER)

        Row_V3 = str(ID_Count_V3)

        print("Counter Row: " + str(Counter_V3))

        NamaSeminar_V3 = "Nama Seminar"
        ID_NamaSeminar_V3 = "53_nama" + Row_V3
        driver.find_element(By.ID, ID_NamaSeminar_V3).send_keys(NamaSeminar_V3)
        
        Penyelenggara_V3 = "Penyelenggara"
        ID_Penyelenggara_V3 = "53_penyelenggara" + Row_V3
        driver.find_element(By.ID, ID_Penyelenggara_V3).send_keys(Penyelenggara_V3)

        Kota_V3 = "Semarang"
        ID_Kota_V3 = "53_location" + Row_V3
        driver.find_element(By.ID, ID_Kota_V3).send_keys(Kota_V3)

        Provinsi_V3 = "Jawa Tengah"
        ID_Provinsi_V3 = "53_provinsi" + Row_V3
        driver.find_element(By.ID, ID_Provinsi_V3).send_keys(Provinsi_V3)

        Negara_V3 = "Indonesia"
        ID_Negara_V3 = "53_negara" + Row_V3
        driver.find_element(By.ID, ID_Negara_V3).send_keys(Negara_V3)

        BulanSeminar_V3 = "1"
        ID_BulanSeminar_V3 = "53_startdate" + Row_V3
        Select_BulanSeminar_V3 = Select(driver.find_element(By.ID, ID_BulanSeminar_V3))
        Select_BulanSeminar_V3.select_by_value(BulanSeminar_V3)

        TahunSeminar_V3 = "2018"
        ID_TahunSeminar_V3 = "53_startyear" + Row_V3
        driver.find_element(By.ID, ID_TahunSeminar_V3).send_keys(TahunSeminar_V3)

        TingkatSeminar_V3 = "1"
        ID_TingkatSeminar_V3 = "53_tingkatseminar" + Row_V3
        Select_TingkatSeminar_V3 = Select(driver.find_element(By.ID, ID_TingkatSeminar_V3))
        Select_TingkatSeminar_V3.select_by_value(TingkatSeminar_V3)

        Uraian_V3 = "Uraian"
        ID_Uraian_V3 = "53_uraian" + Row_V3
        driver.find_element(By.ID, ID_Uraian_V3).send_keys(Uraian_V3)

        Tingkat_V3 = "1"
        ID_Tingkat_V3 = "53_tingkat" + Row_V3
        Select_Tingkat_V3 = Select(driver.find_element(By.ID, ID_Tingkat_V3))
        Select_Tingkat_V3.select_by_value(Tingkat_V3)

        # Kompetisi V3 
        Komp_V3 = ["W.2.1.1","W.2.1.2","W.2.1.3"]
        ID_Komp_V3 = "53_komp" + Row_V3
        Scroll_Komp_V3 = driver.find_element(By.ID, ID_Komp_V3)
        action.move_to_element(Scroll_Komp_V3).perform()
        
        print("- Komp W1 V3: " + str(len(Komp_V3)))
        for Komp_Value_V3 in Komp_V3:
            Komp_Label_V3 = Komp_Value_V3[slice(5)]
            Komp_Call_V3 = f'//*[@id="{ID_Komp_V3}"]//optgroup[contains(@label, "{Komp_Label_V3}")]/option[@value="{Komp_Value_V3}."]'
            Komp_Find_V3 = driver.find_element(By.XPATH, Komp_Call_V3)
            action.move_to_element_with_offset(Komp_Find_V3, 0, -15).click().perform()
            print("-", Komp_Value_V3)

        #End/retry point of loop
        Counter_V3 += 1
        ID_Count_V3 += 1
        print("Row " + Row_V3 + " telah diisi")
    print("\n")

    driver.refresh() 

#PENGISIAN V4
def FormV4(n_V4):
    driver.find_element(By.LINK_TEXT, "V.4").click()
    driver.implicitly_wait(5)

    ID_Count_V4 = 1  
    print("================================================\nFormV4")
    
    try:
        while ID_Count_V4 < 100:
            Row_ID_V4 = f'//*[@class=" ino-item"][@data-id="{str(ID_Count_V4)}"]'    
            Check_Row_V4 = driver.find_element(By.XPATH, Row_ID_V4)
            if Check_Row_V4.is_enabled:
                print("Row " + str(ID_Count_V4) + " ada") 
            else:
                break
            ID_Count_V4 += 1
    except NSEE:
        print ("Row " + str(ID_Count_V4) + " tidak ada") 

    Counter_V4 = 1
    
    print("Start from Row: " + str(ID_Count_V4))
    print("Row Ditambah: " + str(n_V4) + "\n")

    while Counter_V4 <= n_V4:
        #add row
        TambahV4 = driver.find_element(By.XPATH, '//button[@onclick="add54(\'ino\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahV4)
        action.move_to_element(TambahV4).perform()
        TambahV4.send_keys(Keys.ENTER)

        Row_V4 = str(ID_Count_V4)

        print("Counter Row: " + str(Counter_V4))

        Judul_V4 = "Judul"
        ID_Judul_V4 = "54_nama" + Row_V4
        driver.find_element(By.ID, ID_Judul_V4).send_keys(Judul_V4)

        Bulan_V4 = "1"
        ID_Bulan_V4 = "54_startdate" + Row_V4
        Select_Bulan_V4 = Select(driver.find_element(By.ID, ID_Bulan_V4))
        Select_Bulan_V4.select_by_value(Bulan_V4)

        Tahun_V4 = "2018"
        ID_Tahun_V4 = "54_startyear" + Row_V4
        driver.find_element(By.ID, ID_Tahun_V4).send_keys(Tahun_V4)

        MediaPublikasi_V4 = "MediaPublikasi"
        ID_MediaPublikasi_V4 = "54_media_publikasi" + Row_V4
        driver.find_element(By.ID, ID_MediaPublikasi_V4).send_keys(MediaPublikasi_V4)

        TingkatMedia_V4 = "1"
        ID_TingkatMedia_V4 = "54_tingkatseminar" + Row_V4
        Select_TingkatMedia_V4 = Select(driver.find_element(By.ID, ID_TingkatMedia_V4))
        Select_TingkatMedia_V4.select_by_value(TingkatMedia_V4)

        Uraian_V4 = "Uraian"
        ID_Uraian_V4 = "54_uraian" + Row_V4
        driver.find_element(By.ID, ID_Uraian_V4).send_keys(Uraian_V4)

        Tingkat_V4 = "1"
        ID_Tingkat_V4 = "54_tingkat" + Row_V4
        Select_Tingkat_V4 = Select(driver.find_element(By.ID, ID_Tingkat_V4))
        Select_Tingkat_V4.select_by_value(Tingkat_V4)

        # Kompetisi V4 
        Komp_V4 = ["P.6.1.1","P.6.1.2","P.6.1.3"]
        ID_Komp_V4 = "54_komp" + Row_V4
        Scroll_Komp_V4 = driver.find_element(By.ID, ID_Komp_V4)
        action.move_to_element(Scroll_Komp_V4).perform()
        
        print("- Komp W1 V4: " + str(len(Komp_V4)))
        for Komp_Value_V4 in Komp_V4:
            Komp_Label_V4 = Komp_Value_V4[slice(5)]
            Komp_Call_V4 = f'//*[@id="{ID_Komp_V4}"]//optgroup[contains(@label, "{Komp_Label_V4}")]/option[@value="{Komp_Value_V4}."]'
            Komp_Find_V4 = driver.find_element(By.XPATH, Komp_Call_V4)
            action.move_to_element_with_offset(Komp_Find_V4, 0, -15).click().perform()
            print("-", Komp_Value_V4)

        #End/retry point of loop
        Counter_V4 += 1
        ID_Count_V4 += 1
        print("Row " + Row_V4 + " telah diisi")
    print("\n")

    driver.refresh() 

#PENGISIAN VI
def FormVI(n_VI):
    driver.find_element(By.LINK_TEXT, "VI").click()
    driver.implicitly_wait(5)

    ID_Count_VI = 1  
    print("================================================\nFormVI")
    
    try:
        while ID_Count_VI < 100:
            Row_ID_VI = f'//*[@class=" bah-item"][@data-id="{str(ID_Count_VI)}"]'    
            Check_Row_VI = driver.find_element(By.XPATH, Row_ID_VI)
            if Check_Row_VI.is_enabled:
                print("Row " + str(ID_Count_VI) + " ada") 
            else:
                break
            ID_Count_VI += 1
    except NSEE:
        print ("Row " + str(ID_Count_VI) + " tidak ada") 

    Counter_VI = 1
    
    print("Start from Row: " + str(ID_Count_VI))
    print("Row Ditambah: " + str(n_VI) + "\n")

    while Counter_VI <= n_VI:
        #add row
        TambahVI = driver.find_element(By.XPATH, '//button[@onclick="add6(\'bah\')"]')
        driver.execute_script("arguments[0].scrollIntoView();",TambahVI)
        action.move_to_element(TambahVI).perform()
        TambahVI.send_keys(Keys.ENTER)

        Row_VI = str(ID_Count_VI)

        print("Counter Row: " + str(Counter_VI))

        Bahasa_VI = "Indonesia"
        ID_Bahasa_VI = "6_nama" + Row_VI
        driver.find_element(By.ID, ID_Bahasa_VI).send_keys(Bahasa_VI)

        JenisBahasa_VI = "2"
        ID_JenisBahasa_VI = "6_jenisbahasa" + Row_VI
        Select_JenisBahasa_VI = Select(driver.find_element(By.ID, ID_JenisBahasa_VI))
        Select_JenisBahasa_VI.select_by_value(JenisBahasa_VI)

        Verbal_VI = "2"
        ID_Verbal_VI = "6_verbal" + Row_VI
        Select_Verbal_VI = Select(driver.find_element(By.ID, ID_Verbal_VI))
        Select_Verbal_VI.select_by_value(Verbal_VI)

        JenisTulisan_VI = "Jurnal"
        ID_JenisTulisan_VI = "6_jenistulisan" + Row_VI
        Select_JenisTulisan_VI = Select(driver.find_element(By.ID, ID_JenisTulisan_VI))
        Select_JenisTulisan_VI.select_by_value(JenisTulisan_VI)

        # Kompetisi VI 
        Komp_VI = ["W.4.1.1","W.4.1.2","W.4.1.3"]
        ID_Komp_VI = "6_komp" + Row_VI
        Scroll_Komp_VI = driver.find_element(By.ID, ID_Komp_VI)
        action.move_to_element(Scroll_Komp_VI).perform()
        
        print("- Komp W1 VI: " + str(len(Komp_VI)))
        for Komp_Value_VI in Komp_VI:
            Komp_Label_VI = Komp_Value_VI[slice(5)]
            Komp_Call_VI = f'//*[@id="{ID_Komp_VI}"]//optgroup[contains(@label, "{Komp_Label_VI}")]/option[@value="{Komp_Value_VI}."]'
            Komp_Find_VI = driver.find_element(By.XPATH, Komp_Call_VI)
            action.move_to_element_with_offset(Komp_Find_VI, 0, -15).click().perform()
            print("-", Komp_Value_VI)

        #End/retry point of loop
        Counter_VI += 1
        ID_Count_VI += 1
        print("Row " + Row_VI + " telah diisi")
    print("\n")

    driver.refresh() 

def AllForm():
    FormI1(2,2,2)
    FormI2(2)
    FormI3(3)
    FormI4(2)
    FormI5(3)
    FormI6(2)
    FormII1(2)
    FormII2(2)
    FormIII(2)
    FormIV(2)
    FormV1(2)
    FormV2(2)
    FormV3(2)
    FormV4(2)
    FormVI(2)
    # FormVII()
    # FormL1(2)
    # FormR()

# AllForm()
FormVI(2)

    