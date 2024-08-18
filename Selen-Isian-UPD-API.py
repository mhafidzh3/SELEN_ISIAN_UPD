from fastapi import FastAPI
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

app = FastAPI()

@app.get("/")
def test():
    #Akun
    username = "yosua@live.undip.ac.id"
    password = "insinyurj4y4"

    #Driver
    driver = webdriver.Chrome()
    action = ActionChains(driver)

    #Database META
    # client = pymongo.MongoClient("mongodb://192.168.195.241:27017/")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    #Database Name
    db = client["piiclone"]
    #Collection Name
    col = db["form_penilaian"]

    #Database Key
    PID = "formM-gONh9yHYwFgjZt5fb9dKQ"
    Student_ID = "21060124190767"

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

    #PENGISIAN I1
    def FormI1():
        driver.find_element(By.LINK_TEXT, "I.1").click()
        driver.implicitly_wait(5)

        #Database
        Dict_I1 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_satu':1})
        Object_I1 = Dict_I1['form_i_satu']

        #add alamat
        ID_Count_Alamat_I1 = 0

        try:
            while ID_Count_Alamat_I1 < 100:
                Row_Alamat_ID_I1 = f'//*[@class=" ala-item"][@data-id="{str(ID_Count_Alamat_I1)}"]'    
                Check_Row_Alamat_I1 = driver.find_element(By.XPATH, Row_Alamat_ID_I1)
                
                if Check_Row_Alamat_I1.is_enabled:
                    pass
                else:
                    break
                ID_Count_Alamat_I1 += 1
        except NSEE:
            pass
        
        Counter_Alamat_I1 = 1
        DB_CountAlamat_I1 = 0

        #Database Alamat
        Alamat_I1 = Object_I1['alamat']
        n_Alamat_I1 = len(Alamat_I1)

        while Counter_Alamat_I1 <= n_Alamat_I1:
            #add row
            Alamat_Row_I1 = str(ID_Count_Alamat_I1)

            TambahI1alamat = driver.find_element(By.XPATH, '//button[@onclick="add111(\'ala\')"]')
            action.move_to_element(TambahI1alamat).perform()
            TambahI1alamat.send_keys(Keys.ENTER)

            #Document I1 Alamat
            Isi_Alamat_I1 = Alamat_I1[DB_CountAlamat_I1]

            try:
                AddressType_I1 = Isi_Alamat_I1["tipe"]
                ID_AddressType_I1 = "addr_type" + Alamat_Row_I1
                try:
                    Select_AddressType_I1 = Select(driver.find_element(By.ID, ID_AddressType_I1))
                    Select_AddressType_I1.select_by_visible_text(AddressType_I1)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                AddressDesc_I1 = Isi_Alamat_I1["alamat"]
                ID_AddressDesc_I1 = "addr_desc" + Alamat_Row_I1
                driver.find_element(By.ID, ID_AddressDesc_I1).send_keys(AddressDesc_I1)
            except KeyError:
                pass

            try:
                AddressLoc_I1 = Isi_Alamat_I1["kota"]
                ID_AddressLoc_I1 = "addr_loc" + Alamat_Row_I1
                driver.find_element(By.ID, ID_AddressLoc_I1).send_keys(AddressLoc_I1)
            except KeyError:
                pass

            try:
                AddressZip_I1 = Isi_Alamat_I1["kodePos"]
                ID_AddressZip_I1 = "addr_zip" + Alamat_Row_I1
                driver.find_element(By.ID, ID_AddressZip_I1).send_keys(AddressZip_I1)
            except KeyError:
                pass

            #End/retry point of loop
            Counter_Alamat_I1 += 1
            DB_CountAlamat_I1 += 1
            ID_Count_Alamat_I1 += 1

            Check()

        #add lembaga
        ID_Count_Lembaga_I1 = 1

        try:
            while ID_Count_Lembaga_I1 < 100:
                Row_Lembaga_ID_I1 = f'//*[@class=" wor-item"][@data-id="{str(ID_Count_Lembaga_I1)}"]'    
                Check_Row_Lembaga_I1 = driver.find_element(By.XPATH, Row_Lembaga_ID_I1)
                
                if Check_Row_Lembaga_I1.is_enabled:
                    pass
                else:
                    break
                ID_Count_Lembaga_I1 += 1
        except NSEE:
            pass
        
        Counter_Lembaga_I1 = 1
        DB_CountLembaga_I1 = 0

        #Database Lembaga
        Lembaga_I1 = Object_I1['lembaga']
        n_Lembaga_I1 = len(Lembaga_I1)

        while Counter_Lembaga_I1 <= n_Lembaga_I1:
            #add row
            Lembaga_Row_I1 = str(ID_Count_Lembaga_I1)

            TambahI1lembaga = driver.find_element(By.XPATH, '//button[@onclick="add112(\'wor\')"]')
            action.move_to_element(TambahI1lembaga).perform()
            TambahI1lembaga.send_keys(Keys.ENTER)

            #Document I1 Lembaga
            Isi_Lembaga_I1 = Lembaga_I1[DB_CountLembaga_I1]

            try:
                ExpName_I1 = Isi_Lembaga_I1["nama"]
                ID_ExpName_I1 = "exp_name" + Lembaga_Row_I1
                driver.find_element(By.ID, ID_ExpName_I1).send_keys(ExpName_I1)
            except KeyError:
                pass

            try:
                ExpDesc_I1 = Isi_Lembaga_I1["jabatan"]
                ID_ExpDesc_I1 = "exp_desc" + Lembaga_Row_I1
                driver.find_element(By.ID, ID_ExpDesc_I1).send_keys(ExpDesc_I1)
            except KeyError:
                pass

            try:
                ExpLoc_I1 = Isi_Lembaga_I1["kota"]
                ID_ExpLoc_I1 = "exp_loc" + Lembaga_Row_I1
                driver.find_element(By.ID, ID_ExpLoc_I1).send_keys(ExpLoc_I1)
            except KeyError:
                pass

            try:
                ExpZip_I1 = Isi_Lembaga_I1["kodePos"]
                ID_ExpZip_I1 = "exp_zip" + Lembaga_Row_I1
                driver.find_element(By.ID, ID_ExpZip_I1).send_keys(ExpZip_I1)
            except KeyError:
                pass

            #End/retry point of loop
            Counter_Lembaga_I1 += 1
            DB_CountLembaga_I1 += 1
            ID_Count_Lembaga_I1 += 1

            Check()

        #add phone number
        ID_Count_Phone_I1 = 0

        try:
            while ID_Count_Phone_I1 < 100:
                Row_Phone_ID_I1 = f'//*[@class=" pho-item"][@data-id="{str(ID_Count_Phone_I1)}"]'    
                Check_Row_Phone_I1 = driver.find_element(By.XPATH, Row_Phone_ID_I1)
                
                if Check_Row_Phone_I1.is_enabled:
                    pass
                else:
                    break
                ID_Count_Phone_I1 += 1
        except NSEE:
            pass

        Counter_Phone_I1 = 1
        DB_CountPhone_I1 = 0

        #Database Phone
        Phone_I1 = Object_I1['komunikasi']
        n_Phone_I1 = len(Phone_I1)

        while Counter_Phone_I1 <= n_Phone_I1:
            #add row
            Phone_Row_I1 = str(ID_Count_Phone_I1)

            TambahI1Phone = driver.find_element(By.XPATH, '//button[@onclick="add113(\'pho\')"]')
            action.move_to_element(TambahI1Phone).perform()
            TambahI1Phone.send_keys(Keys.ENTER)

            #Document I1 Phone
            Isi_Phone_I1 = Phone_I1[DB_CountPhone_I1]

            try:
                PhoneType_I1 = Isi_Phone_I1["tipe"]
                ID_PhoneType_I1 = "phone_type" + Phone_Row_I1
                try:
                    Select_PhoneType_I1 = Select(driver.find_element(By.ID, ID_PhoneType_I1))
                    Select_PhoneType_I1.select_by_visible_text(PhoneType_I1)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                PhoneValue_I1 = Isi_Phone_I1["nomor"]
                ID_PhoneValue_I1 = "phone_value" + Phone_Row_I1
                driver.find_element(By.ID, ID_PhoneValue_I1).send_keys(PhoneValue_I1)
            except KeyError:
                pass

            Check()

            #End/retry point of loop
            Counter_Phone_I1 += 1
            DB_CountPhone_I1 += 1
            ID_Count_Phone_I1 += 1

            Check()

    #PENGISIAN I2
    def FormI2():
        driver.find_element(By.LINK_TEXT, "I.2").click()
        driver.implicitly_wait(5)

        ID_Count_I2 = 1  
        
        try:
            while ID_Count_I2 < 100:
                Row_ID_I2 = f'//*[@class=" edu-item"][@data-id="{str(ID_Count_I2)}"]'    
                Check_Row_I2 = driver.find_element(By.XPATH, Row_ID_I2)
                
                if Check_Row_I2.is_enabled:
                    pass
                else:
                    break
                ID_Count_I2 += 1
        except NSEE:
            pass
        
        Counter_I2 = 1
        DB_Count_I2 = 0

        #Database I2
        Dict_I2 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_dua':1})
        List_I2 = Dict_I2['form_i_dua']
        n_I2 = len(List_I2)

        while Counter_I2 <= n_I2:
            #add row
            TambahI2 = driver.find_element(By.XPATH, '//button[@onclick="add12(\'edu\')"]')
            action.move_to_element(TambahI2).perform()
            TambahI2.send_keys(Keys.ENTER)

            Row_I2 = str(ID_Count_I2)

            #Document I2
            Isi_I2 = List_I2[DB_Count_I2]

            try:
                Universitas_I2 = Isi_I2["namaPerguruan"]
                ID_Universitas_I2 = "12_school" + Row_I2
                driver.find_element(By.ID, ID_Universitas_I2).send_keys(Universitas_I2)
            except KeyError:
                pass
            
            try:
                Tingkat_I2 = Isi_I2["tingkatPendidikan"]
                ID_Tingkat_I2 = "12_degree" + Row_I2
                try:
                    Select_Tingkat_I2 = Select(driver.find_element(By.ID, ID_Tingkat_I2))
                    Select_Tingkat_I2.select_by_visible_text(Tingkat_I2)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Fakultas_I2 = Isi_I2["fakultas"]
                ID_Fakultas_I2 = "12_fakultas" + Row_I2
                driver.find_element(By.ID, ID_Fakultas_I2).send_keys(Fakultas_I2)
            except KeyError:
                pass

            try:
                Jurusan_I2 = Isi_I2["jurusan"]
                ID_Jurusan_I2 = "12_fieldofstudy" + Row_I2
                driver.find_element(By.ID, ID_Jurusan_I2).send_keys(Jurusan_I2)
            except KeyError:
                pass

            try:
                Kota_I2 = Isi_I2["kotaPerguruan"]
                ID_Kota_I2 = "12_kota" + Row_I2
                driver.find_element(By.ID, ID_Kota_I2).send_keys(Kota_I2)   
            except KeyError:
                pass 

            try:
                Provinsi_I2 = Isi_I2["provinsi"]
                ID_Provinsi_I2 = "12_provinsi" + Row_I2
                driver.find_element(By.ID, ID_Provinsi_I2).send_keys(Provinsi_I2)
            except KeyError:
                pass

            try:
                Negara_I2 = Isi_I2["negara"]
                ID_Negara_I2 = "12_negara" + Row_I2
                driver.find_element(By.ID, ID_Negara_I2).send_keys(Negara_I2)
            except KeyError:
                pass

            try:
                TahunLulus_I2 = Isi_I2["tahunLulus"]
                ID_TahunLulus_I2 = "12_tahunlulus" + Row_I2
                driver.find_element(By.ID, ID_TahunLulus_I2).send_keys(TahunLulus_I2)
            except KeyError:
                pass

            try:
                Gelar_I2 = Isi_I2["gelar"]
                ID_Gelar_I2 = "12_title" + Row_I2
                driver.find_element(By.ID, ID_Gelar_I2).send_keys(Gelar_I2)
            except KeyError:
                pass

            try:
                JudulTA_I2 = Isi_I2["judulTa"]
                ID_JudulTA_I2 = "12_activities" + Row_I2
                Scroll_JudulTA_I2 = driver.find_element(By.ID, ID_JudulTA_I2)
                action.move_to_element(Scroll_JudulTA_I2).perform()
                Scroll_JudulTA_I2.send_keys(JudulTA_I2)
            except KeyError:
                pass

            try:
                UraianTA_I2 = Isi_I2["uraianSingkat"]
                ID_UraianTA_I2 = "12_description" + Row_I2
                Scroll_UraianTA_I2 = driver.find_element(By.ID, ID_UraianTA_I2)
                action.move_to_element(Scroll_UraianTA_I2).perform()
                Scroll_UraianTA_I2.send_keys(UraianTA_I2)
            except KeyError:
                pass

            try:
                Nilai_I2 = Isi_I2["nilaiAkademikRata"]
                ID_Nilai_I2 = "12_score" + Row_I2
                Scroll_Nilai_I2 = driver.find_element(By.ID, ID_Nilai_I2)
                action.move_to_element(Scroll_Nilai_I2).perform()
                Scroll_Nilai_I2.send_keys(Nilai_I2)
            except KeyError:
                pass
            
            #End/retry point of loop
            Counter_I2 += 1
            DB_Count_I2 += 1
            ID_Count_I2 += 1

            Check()

    #PENGISIAN I3   
    def FormI3():
        driver.find_element(By.LINK_TEXT, "I.3").click()
        driver.implicitly_wait(5)

        ID_Count_I3 = 1  

        try:
            while ID_Count_I3 < 100:
                Row_ID_I3 = f'//*[@class=" org-item"][@data-id="{str(ID_Count_I3)}"]'    
                Check_Row_I3 = driver.find_element(By.XPATH, Row_ID_I3)
                
                if Check_Row_I3.is_enabled:
                    pass
                else:
                    break
                ID_Count_I3 += 1
        except NSEE:
            pass
        
        Counter_I3 = 1
        DB_Count_I3 = 0

        #Database
        Dict_I3 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_tiga':1})
        List_I3 = Dict_I3['form_i_tiga']
        n_I3 = len(List_I3)

        while Counter_I3 <= n_I3:
            #add row
            TambahI3 = driver.find_element(By.XPATH, '//button[@onclick="add13(\'org\')"]')
            action.move_to_element(TambahI3).perform()
            TambahI3.send_keys(Keys.ENTER)

            Row_I3 = str(ID_Count_I3)

            #Document I3
            Isi_I3 = List_I3[DB_Count_I3]

            try:
                Organisasi_I3 = Isi_I3["namaOrganisasi"]
                ID_Organisasi_I3 = "13_nama_org" + Row_I3
                driver.find_element(By.ID, ID_Organisasi_I3).send_keys(Organisasi_I3)
            except KeyError:
                pass
            
            try:
                Jenis_I3 = Isi_I3["jenisOrganisasi"]
                ID_Jenis_I3 = "13_jenis" + Row_I3
                Select_Jenis_I3 = Select(driver.find_element(By.ID, ID_Jenis_I3))
                try:
                    Select_Jenis_I3.select_by_visible_text(Jenis_I3)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Kota_I3 = Isi_I3["kotaAsal"]
                ID_Kota_I3 = "13_tempat" + Row_I3
                driver.find_element(By.ID, ID_Kota_I3).send_keys(Kota_I3)
            except KeyError:
                pass

            try:
                Provinsi_I3 = Isi_I3["provinsiAsal"]
                ID_Provinsi_I3 = "13_provinsi" + Row_I3
                driver.find_element(By.ID, ID_Provinsi_I3).send_keys(Provinsi_I3)
            except KeyError:
                pass

            try:
                Negara_I3 = Isi_I3["negaraAsal"]
                ID_Negara_I3 = "13_negara" + Row_I3
                driver.find_element(By.ID, ID_Negara_I3).send_keys(Negara_I3)
            except KeyError:
                pass
            
            try:
                BulanMulai_I3 = Isi_I3["bulanMulai"]
                ID_BulanMulai_I3 = "13_startdate" + Row_I3
                Select_BulanMulai_I3 = Select(driver.find_element(By.ID, ID_BulanMulai_I3))
                try:
                    Select_BulanMulai_I3.select_by_visible_text(BulanMulai_I3)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                TahunMulai_I3 = Isi_I3["tahunMulai"]
                ID_TahunMulai_I3 = "13_startyear" + Row_I3
                driver.find_element(By.ID, ID_TahunMulai_I3).send_keys(TahunMulai_I3)
            except KeyError:
                pass

            #Periode I3
            ID_Anggota_I3 = "13_work" + Row_I3
            Angggota_I3 = driver.find_element(By.ID, ID_Anggota_I3)
            if Isi_I3["masihAnggota"] == True:
                action.move_to_element_with_offset(Angggota_I3, 0, -20).click().perform()
            else:
                try:
                    TahunSelesai_I3 = Isi_I3["tahun"]
                    ID_TahunSelesai_I3 = "13_endyear" + Row_I3
                    driver.find_element(By.ID, ID_TahunSelesai_I3).send_keys(TahunSelesai_I3)
                except KeyError:
                    pass

                try:
                    BulanSelesai_I3 = Isi_I3["bulan"]
                    ID_BulanSelesai_I3 = "13_enddate" + Row_I3
                    Select_BulanSelesai_I3 = Select(driver.find_element(By.ID, ID_BulanSelesai_I3))
                    try:
                        Select_BulanSelesai_I3.select_by_visible_text(BulanSelesai_I3)
                    except NSEE:
                        pass
                except KeyError:
                    pass
            
            try:
                Jabatan_I3 = Isi_I3["jabatanOrganisasi"]
                ID_Jabatan_I3 = "13_jabatan" + Row_I3
                Select_Jabatan_I3 = Select(driver.find_element(By.ID, ID_Jabatan_I3))
                try:
                    Select_Jabatan_I3.select_by_visible_text(Jabatan_I3)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Tingkat_I3 = Isi_I3["tingkatanOrganisasi"]
                ID_Tingkat_I3 = "13_tingkat" + Row_I3
                Select_Tingkat_I3 = Select(driver.find_element(By.ID, ID_Tingkat_I3))
                try:
                    Select_Tingkat_I3.select_by_visible_text(Tingkat_I3)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Lingkup_I3 = Isi_I3["kegiatanOrganisasi"]
                ID_Lingkup_I3 = "13_lingkup" + Row_I3
                Scroll_Lingkup_I3 = driver.find_element(By.ID, ID_Lingkup_I3)
                action.move_to_element(Scroll_Lingkup_I3).perform()
                Select_Lingkup_I3 = Select(Scroll_Lingkup_I3)
                try:
                    Select_Lingkup_I3.select_by_visible_text(Lingkup_I3)
                except NSEE:
                    pass
            except KeyError:
                pass
            
            try:
                Uraian_I3 = Isi_I3["uraianTugas"]
                ID_Uraian_I3 = "13_aktifitas" + Row_I3
                Scroll_Uraian_I3 = driver.find_element(By.ID, ID_Uraian_I3)
                action.move_to_element(Scroll_Uraian_I3).perform()
                Scroll_Uraian_I3.send_keys(Uraian_I3)
            except KeyError:
                pass

            # Kompetisi I3 
            ID_Komp_I3 = "13_komp" + Row_I3
            Scroll_Komp_I3 = driver.find_element(By.ID, ID_Komp_I3)
            action.move_to_element(Scroll_Komp_I3).perform()
            try:
                Komp_I3 = Isi_I3["klaimKompetensiWSatu"]
                for Komp_Value_I3 in Komp_I3:
                    Komp_Label_I3 = Komp_Value_I3[slice(5)]
                    Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//optgroup[contains(@label, "{Komp_Label_I3}")]/option[@value="{Komp_Value_I3}."]'
                    Komp_Find_I3 = driver.find_element(By.XPATH, Komp_Call_I3)
                    action.move_to_element_with_offset(Komp_Find_I3, 0, -15).click().perform()
            except KeyError:
                pass

            #End/retry point of loop
            Counter_I3 += 1
            DB_Count_I3 += 1
            ID_Count_I3 += 1

            Check()

    #PENGISIAN I4
    def FormI4():
        driver.find_element(By.LINK_TEXT, "I.4").click()
        driver.implicitly_wait(5)

        ID_Count_I4 = 1  

        try:
            while ID_Count_I4 < 100:
                Row_ID_I4 = f'//*[@class=" phg-item"][@data-id="{str(ID_Count_I4)}"]'    
                Check_Row_I4 = driver.find_element(By.XPATH, Row_ID_I4)
                
                if Check_Row_I4.is_enabled:
                    pass
                else:
                    break
                ID_Count_I4 += 1
        except NSEE:
            pass

        Counter_I4 = 1
        DB_Count_I4 = 0

        #Database
        Dict_I4 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_empat':1})
        List_I4 = Dict_I4['form_i_empat']
        n_I4 = len(List_I4)

        while Counter_I4 <= n_I4:
            #add row
            TambahI4 = driver.find_element(By.XPATH, '//button[@onclick="add14(\'phg\')"]')
            action.move_to_element(TambahI4).perform()
            TambahI4.send_keys(Keys.ENTER)
            Row_I4 = str(ID_Count_I4)

            #Document I4
            Isi_I4 = List_I4[DB_Count_I4]

            try:
                Penghargaan_I4 = Isi_I4["namaTandaPenghargaan"]
                ID_Penghargaan_I4 = "14_nama" + Row_I4
                driver.find_element(By.ID, ID_Penghargaan_I4).send_keys(Penghargaan_I4)
            except KeyError:
                Row_I4 = str(ID_Count_I4)

            try:
                Lembaga_I4 = Isi_I4["namaTandaPenghargaan"]
                ID_Lembaga_I4 = "14_lembaga" + Row_I4
                driver.find_element(By.ID, ID_Lembaga_I4).send_keys(Lembaga_I4)
            except KeyError:
                Row_I4 = str(ID_Count_I4)

            try:
                Kota_I4 = Isi_I4["kotaAsal"]
                ID_Kota_I4 = "14_location" + Row_I4
                driver.find_element(By.ID, ID_Kota_I4).send_keys(Kota_I4)
            except KeyError:
                Row_I4 = str(ID_Count_I4)

            try:
                Provinsi_I4 = Isi_I4["provinsiAsal"]
                ID_Provinsi_I4 = "14_provinsi" + Row_I4
                driver.find_element(By.ID, ID_Provinsi_I4).send_keys(Provinsi_I4)
            except KeyError:
                pass
                
            try:
                Negara_I4 = Isi_I4["negaraAsal"]
                ID_Negara_I4 = "14_negara" + Row_I4
                driver.find_element(By.ID, ID_Negara_I4).send_keys(Negara_I4)
            except KeyError:
                pass

            try:
                BulanTerbit_I4 = Isi_I4["bulanTerbit"]
                ID_BulanTerbit_I4 = "14_startdate" + Row_I4
                Select_BulanTerbit_I4 = Select(driver.find_element(By.ID, ID_BulanTerbit_I4))
                try:
                    Select_BulanTerbit_I4.select_by_visible_text(BulanTerbit_I4)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Tahun_I4 = Isi_I4["tahunTerbit"]
                ID_Tahun_I4 = "14_startyear" + Row_I4
                driver.find_element(By.ID, ID_Tahun_I4).send_keys(Tahun_I4)
            except KeyError:
                pass

            try:
                Tingkat_I4 = Isi_I4["tingkatPenghargaan"]
                ID_Tingkat_I4 = "14_tingkat" + Row_I4
                Select_Tingkat_I4 = Select(driver.find_element(By.ID, ID_Tingkat_I4))
                try:
                    Select_Tingkat_I4.select_by_visible_text(Tingkat_I4)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Lembaga_I4 = Isi_I4["jenisLembagaPenghargaan"]
                ID_Lembaga_I4 = "14_tingkatlembaga" + Row_I4
                Select_Lembaga_I4 = Select(driver.find_element(By.ID, ID_Lembaga_I4))
                try:
                    Select_Lembaga_I4.select_by_visible_text(Lembaga_I4)
                except NSEE:
                    pass
            except KeyError:
                pass
            
            try:
                Uraian_I4 = Isi_I4["uraianSingkatAktifitas"]
                ID_Uraian_I4 = "14_uraian" + Row_I4
                Scroll_Uraian_I4 = driver.find_element(By.ID, ID_Uraian_I4)
                action.move_to_element(Scroll_Uraian_I4).perform()
                Scroll_Uraian_I4.send_keys(Uraian_I4)
            except KeyError:
                pass

            # Kompetisi I4 
            ID_Komp_I4 = "14_komp" + Row_I4
            Scroll_Komp_I4 = driver.find_element(By.ID, ID_Komp_I4)
            action.move_to_element(Scroll_Komp_I4).perform()

            try:
                Komp_I4 = Isi_I4["klaimKompetensiWSatu"]
                for Komp_Value_I4 in Komp_I4:
                    Komp_Label_I4 = Komp_Value_I4[slice(5)]
                    Komp_Call_I4 = f'//*[@id="{ID_Komp_I4}"]//optgroup[contains(@label, "{Komp_Label_I4}")]/option[@value="{Komp_Value_I4}."]'
                    Komp_Find_I4 = driver.find_element(By.XPATH, Komp_Call_I4)
                    if Row_I4 == "1":
                        action.move_to_element_with_offset(Komp_Find_I4, 0, -30).click().perform()
                    else:
                        action.move_to_element_with_offset(Komp_Find_I4, 0, -20).click().perform() 
            except KeyError:
                pass
                
            #End/retry point of loop
            Counter_I4 += 1
            DB_Count_I4 += 1
            ID_Count_I4 += 1

            Check()

    #PENGISIAN I5
    def FormI5():
        driver.find_element(By.LINK_TEXT, "I.5").click()
        driver.implicitly_wait(5)

        ID_Count_I5 = 1  

        try:
            while ID_Count_I5 < 100:
                Row_ID_I5 = f'//*[@class=" pdd-item"][@data-id="{str(ID_Count_I5)}"]'    
                Check_Row_I5 = driver.find_element(By.XPATH, Row_ID_I5)
                
                if Check_Row_I5.is_enabled:
                    pass
                else:
                    break
                ID_Count_I5 += 1
        except NSEE:
            pass
        
        Counter_I5 = 1
        DB_Count_I5 = 0

        #Database
        Dict_I5 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_lima':1})
        List_I5 = Dict_I5['form_i_lima']
        n_I5 = len(List_I5)

        while Counter_I5 <= n_I5:
            #add row
            TambahI5 = driver.find_element(By.XPATH, '//button[@onclick="add15(\'pdd\')"]')
            action.move_to_element(TambahI5).perform()
            TambahI5.send_keys(Keys.ENTER)
            Row_I5 = str(ID_Count_I5)

            #Document I5
            Isi_I5 = List_I5[DB_Count_I5]

            try:
                Pendidikan_I5 = Isi_I5["namaPendidikanTeknik"]
                ID_Pendidikan_I5 = "15_nama" + Row_I5
                driver.find_element(By.ID, ID_Pendidikan_I5).send_keys(Pendidikan_I5)
            except KeyError:
                pass

            try:
                Lembaga_I5 = Isi_I5["penyelenggara"]
                ID_Lembaga_I5 = "15_lembaga" + Row_I5
                driver.find_element(By.ID, ID_Lembaga_I5).send_keys(Lembaga_I5)
            except KeyError:
                pass

            try:
                Kota_I5 = Isi_I5["kotaAsal"]
                ID_Kota_I5 = "15_location" + Row_I5
                driver.find_element(By.ID, ID_Kota_I5).send_keys(Kota_I5)
            except KeyError:
                pass

            try:
                Provinsi_I5 = Isi_I5["provinsiAsal"]
                ID_Provinsi_I5 = "15_provinsi" + Row_I5
                driver.find_element(By.ID, ID_Provinsi_I5).send_keys(Provinsi_I5)
            except KeyError:
                pass

            try:
                Negara_I5 = Isi_I5["negaraAsal"]
                ID_Negara_I5 = "15_negara" + Row_I5
                driver.find_element(By.ID, ID_Negara_I5).send_keys(Negara_I5)
            except KeyError:
                pass

            try:
                BulanMulai_I5 = Isi_I5["bulanMulai"]
                ID_BulanMulai_I5 = "15_startdate" + Row_I5
                Select_BulanMulai_I5 = Select(driver.find_element(By.ID, ID_BulanMulai_I5))
                try:
                    Select_BulanMulai_I5.select_by_visible_text(BulanMulai_I5)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                TahunMulai_I5 = Isi_I5["tahunMulai"]
                ID_TahunMulai_I5 = "15_startyear" + Row_I5
                driver.find_element(By.ID, ID_TahunMulai_I5).send_keys(TahunMulai_I5)
            except KeyError:
                pass

            #Periode I5
            ID_Anggota_I5 = "15_work" + Row_I5
            Angggota_I5 = driver.find_element(By.ID, ID_Anggota_I5)
            if Isi_I5["masihAnggota"] == True:
                action.move_to_element_with_offset(Angggota_I5, 0, -20).click().perform()
            else:
                try:
                    TahunSelesai_I5 = Isi_I5["tahun"]
                    ID_TahunSelesai_I5 = "15_endyear" + Row_I5
                    driver.find_element(By.ID, ID_TahunSelesai_I5).send_keys(TahunSelesai_I5)
                except KeyError:
                    pass

                try:
                    BulanSelesai_I5 = Isi_I5["bulan"]
                    ID_BulanSelesai_I5 = "15_enddate" + Row_I5
                    Select_BulanSelesai_I5 = Select(driver.find_element(By.ID, ID_BulanSelesai_I5))
                    try:
                        Select_BulanSelesai_I5.select_by_visible_text(BulanSelesai_I5)
                    except NSEE:
                        pass
                except KeyError:
                    pass

            try:
                Tingkat_I5 = Isi_I5["tingkatanMateriPelatihan"]
                ID_Tingkat_I5 = "15_tingkat" + Row_I5
                try:
                    Select_Tingkat_I5 = Select(driver.find_element(By.ID, ID_Tingkat_I5))
                    Select_Tingkat_I5.select_by_visible_text(Tingkat_I5)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Jam_I5 = Isi_I5["jamPendidikanTeknik"]
                ID_Jam_I5 = "15_jam" + Row_I5
                try:
                    Select_Jam_I5 = Select(driver.find_element(By.ID, ID_Jam_I5))
                    Select_Jam_I5.select_by_visible_text(Jam_I5)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Uraian_I5 = Isi_I5["uraianSingkatAktifitas"]
                ID_Uraian_I5 = "15_uraian" + Row_I5
                Scroll_Uraian_I5 = driver.find_element(By.ID, ID_Uraian_I5)
                action.move_to_element(Scroll_Uraian_I5).perform()
                Scroll_Uraian_I5.send_keys(Uraian_I5)
            except KeyError:
                pass

        # Kompetisi I5 
            ID_Komp_I5 = "15_komp" + Row_I5
            Scroll_Komp_I5 = driver.find_element(By.ID, ID_Komp_I5)
            action.move_to_element(Scroll_Komp_I5).perform()

            try:
                Komp_W2_I5 = Isi_I5["klaimKompetensiWdua"]
                for Komp_Value_W2_I5 in Komp_W2_I5:
                    Komp_Label_W2_I5 = Komp_Value_W2_I5[slice(5)]
                    Komp_Call_W2_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_W2_I5}")]/option[@value="{Komp_Value_W2_I5}."]'
                    Komp_Find_W2_I5 = driver.find_element(By.XPATH, Komp_Call_W2_I5)
                    if Row_I5 == "1":
                        action.move_to_element_with_offset(Komp_Find_W2_I5, 0, -30).click().perform()
                    else:
                        action.move_to_element_with_offset(Komp_Find_W2_I5, 0, -20).click().perform()
            except KeyError:
                pass

            try:
                Komp_W4_I5 = Isi_I5["klaimKompetensiWempat"]
                for Komp_Value_W4_I5 in Komp_W4_I5:
                    Komp_Label_W4_I5 = Komp_Value_W4_I5[slice(5)]
                    Komp_Call_W4_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_W4_I5}")]/option[@value="{Komp_Value_W4_I5}."]'
                    Komp_Find_W4_I5 = driver.find_element(By.XPATH, Komp_Call_W4_I5)
                    if Row_I5 == "1":
                        action.move_to_element_with_offset(Komp_Find_W4_I5, 0, -30).click().perform()
                    else:
                        action.move_to_element_with_offset(Komp_Find_W4_I5, 0, -20).click().perform()
            except KeyError:
                pass

            try:
                Komp_P10_I5 = Isi_I5["klaimKompetensiPsepuluh"]
                for Komp_Value_P10_I5 in Komp_P10_I5:
                    Komp_Label_P10_I5 = Komp_Value_P10_I5[slice(5)]
                    Komp_Call_P10_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_P10_I5}")]/option[@value="{Komp_Value_P10_I5}."]'
                    Komp_Find_P10_I5 = driver.find_element(By.XPATH, Komp_Call_P10_I5)
                    if Row_I5 == "1":
                        action.move_to_element_with_offset(Komp_Find_P10_I5, 0, -30).click().perform()
                    else:
                        action.move_to_element_with_offset(Komp_Find_P10_I5, 0, -20).click().perform() 
            except KeyError:
                pass

            #End/retry point of loop
            Counter_I5 += 1
            DB_Count_I5 += 1
            ID_Count_I5 += 1

            Check()

    #PENGISIAN I6
    def FormI6():
        driver.find_element(By.LINK_TEXT, "I.6").click()
        driver.implicitly_wait(5)

        ID_Count_I6 = 1  

        try:
            while ID_Count_I6 < 100:
                Row_ID_I6 = f'//*[@class=" ppm-item"][@data-id="{str(ID_Count_I6)}"]'    
                Check_Row_I6 = driver.find_element(By.XPATH, Row_ID_I6)
                
                if Check_Row_I6.is_enabled:
                    pass
                else:
                    break
                ID_Count_I6 += 1
        except NSEE:
            pass
        
        Counter_I6 = 1
        DB_Count_I6 = 0

        #Database
        Dict_I6 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_enam':1})
        List_I6 = Dict_I6['form_i_enam']
        n_I6 = len(List_I6)

        while Counter_I6 <= n_I6:
            #add row
            TambahI6 = driver.find_element(By.XPATH, '//button[@onclick="add16(\'ppm\')"]')
            action.move_to_element(TambahI6).perform()
            TambahI6.send_keys(Keys.ENTER)
            Row_I6 = str(ID_Count_I6)

            #Document I6
            Isi_I6 = List_I6[DB_Count_I6]

            try:
                Pelatihan_I6 = Isi_I6["namaPendidikanPelatihan"]
                ID_Pelatihan_I6 = "16_nama" + Row_I6
                driver.find_element(By.ID, ID_Pelatihan_I6).send_keys(Pelatihan_I6)
            except KeyError:
                pass

            try:
                Lembaga_I6 = Isi_I6["penyelenggara"]
                ID_Lembaga_I6 = "16_lembaga" + Row_I6
                driver.find_element(By.ID, ID_Lembaga_I6).send_keys(Lembaga_I6)
            except KeyError:
                pass

            try:
                Kota_I6 = Isi_I6["kotaAsal"]
                ID_Kota_I6 = "16_location" + Row_I6
                driver.find_element(By.ID, ID_Kota_I6).send_keys(Kota_I6)
            except KeyError:
                pass

            try:
                Provinsi_I6 = Isi_I6["provinsiAsal"]
                ID_Provinsi_I6 = "16_provinsi" + Row_I6
                driver.find_element(By.ID, ID_Provinsi_I6).send_keys(Provinsi_I6)
            except KeyError:
                pass

            try:
                Negara_I6 = Isi_I6["negaraAsal"]
                ID_Negara_I6 = "16_negara" + Row_I6
                driver.find_element(By.ID, ID_Negara_I6).send_keys(Negara_I6)
            except KeyError:
                pass

            try:
                BulanMulai_I6 = Isi_I6["bulanMulai"]
                ID_BulanMulai_I6 = "16_startdate" + Row_I6
                Select_BulanMulai_I6 = Select(driver.find_element(By.ID, ID_BulanMulai_I6))
                try:
                    Select_BulanMulai_I6.select_by_visible_text(BulanMulai_I6)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                TahunMulai_I6 = Isi_I6["tahunMulai"]
                ID_TahunMulai_I6 = "16_startyear" + Row_I6
                driver.find_element(By.ID, ID_TahunMulai_I6).send_keys(TahunMulai_I6)
            except KeyError:
                pass

            #Periode I6
            ID_Anggota_I6 = "16_work" + Row_I6
            Angggota_I6 = driver.find_element(By.ID, ID_Anggota_I6)
            if Isi_I6["masihAnggota"] == True:
                action.move_to_element_with_offset(Angggota_I6, 0, -20).click().perform()
            else:
                try:
                    TahunSelesai_I6 = Isi_I6["tahun"]
                    ID_TahunSelesai_I6 = "16_endyear" + Row_I6
                    driver.find_element(By.ID, ID_TahunSelesai_I6).send_keys(TahunSelesai_I6)
                except KeyError:
                    pass

                try:
                    BulanSelesai_I6 = Isi_I6["bulan"]
                    ID_BulanSelesai_I6 = "16_enddate" + Row_I6
                    Select_BulanSelesai_I6 = Select(driver.find_element(By.ID, ID_BulanSelesai_I6))
                    try:
                        Select_BulanSelesai_I6.select_by_visible_text(BulanSelesai_I6)
                    except NSEE:
                        pass
                except KeyError:
                    pass

            try:
                Tingkat_I6 = Isi_I6["tingkatanMateriPendidikanManajemen"]
                ID_Tingkat_I6 = "16_tingkat" + Row_I6
                try:
                    Select_Tingkat_I6 = Select(driver.find_element(By.ID, ID_Tingkat_I6))
                    Select_Tingkat_I6.select_by_visible_text(Tingkat_I6)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Jam_I6 = Isi_I6["jamPendidikanTeknikManajemen"]
                ID_Jam_I6 = "16_jam" + Row_I6
                try:
                    Select_Jam_I6 = Select(driver.find_element(By.ID, ID_Jam_I6))
                    Select_Jam_I6.select_by_visible_text(Jam_I6)
                except NSEE:
                    pass
            except KeyError:
                pass

            try:
                Uraian_I6 = Isi_I6["uraianSingkatAktifitas"]
                ID_Uraian_I6 = "16_uraian" + Row_I6
                Scroll_Uraian_I6 = driver.find_element(By.ID, ID_Uraian_I6)
                action.move_to_element(Scroll_Uraian_I6).perform()
                Scroll_Uraian_I6.send_keys(Uraian_I6)
            except KeyError:
                pass

        # Kompetisi I6 
            ID_Komp_I6 = "16_komp" + Row_I6
            Scroll_Komp_I6 = driver.find_element(By.ID, ID_Komp_I6)
            action.move_to_element(Scroll_Komp_I6).perform()

            try:
                Komp_W1_I6 = Isi_I6["klaimKompetensiWSatu"]
                for Komp_Value_W1_I6 in Komp_W1_I6:
                    Komp_Label_W1_I6 = Komp_Value_W1_I6[slice(5)]
                    Komp_Call_W1_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_W1_I6}")]/option[@value="{Komp_Value_W1_I6}."]'
                    Komp_Find_W1_I6 = driver.find_element(By.XPATH, Komp_Call_W1_I6)
                    action.move_to_element_with_offset(Komp_Find_W1_I6, 0, -15).click().perform()
            except KeyError:
                pass        

            try:
                Komp_W4_I6 = Isi_I6["klaimKompetensiWempat"]
                for Komp_Value_W4_I6 in Komp_W4_I6:
                    Komp_Label_W4_I6 = Komp_Value_W4_I6[slice(5)]
                    Komp_Call_W4_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_W4_I6}")]/option[@value="{Komp_Value_W4_I6}."]'
                    Komp_Find_W4_I6 = driver.find_element(By.XPATH, Komp_Call_W4_I6)
                    action.move_to_element_with_offset(Komp_Find_W4_I6, 0, -15).click().perform() 
            except KeyError:
                pass

            try:
                Komp_P10_I6 = Isi_I6["klaimKompetensiPsepuluh"]
                for Komp_Value_P10_I6 in Komp_P10_I6:
                    Komp_Label_P10_I6 = Komp_Value_P10_I6[slice(5)]
                    Komp_Call_P10_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_P10_I6}")]/option[@value="{Komp_Value_P10_I6}."]'
                    Komp_Find_P10_I6 = driver.find_element(By.XPATH, Komp_Call_P10_I6)
                    action.move_to_element_with_offset(Komp_Find_P10_I6, 0, -15).click().perform() 
            except KeyError:
                pass

            #End/retry point of loop
            Counter_I6 += 1
            DB_Count_I6 += 1
            ID_Count_I6 += 1

            Check()

    def Allform():
        FormI1()
        FormI2()
        FormI3()
        FormI4()
        FormI5()
        FormI6()

    Allform()

    return {"Hello": "World"}