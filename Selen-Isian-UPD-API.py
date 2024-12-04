from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException as NSEE
from pydantic import BaseModel
from pymongo import MongoClient
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv()
import time
import pymongo

#pip install selenium == 4.19
#pip install fastapi
#pip install uvicorn
#pip install pydantic
#pip install pymongo
#pip install cryptography

# baca body JSON
class terimaJSON(BaseModel):
    process_id: str
    url: str
    student_id: str

app = FastAPI()

@app.post("/trigger-selenium")
def trigger_selenium(req: terimaJSON):
    #open driver and log in
    try:
        #Driver
        driver = webdriver.Chrome()
        action = ActionChains(driver)

        #Database META
        
        # client = pymongo.MongoClient("mongodb://localhost:27017/") # localhost Uji coba sendiri

        client = pymongo.MongoClient("mongodb://192.168.195.83:27017/")
        
        # client = pymongo.MongoClient("mongodb://192.168.195.241:27017/") # client naufal

        # client = pymongo.MongoClient("mongodb://192.168.195.245:27017/") # client anto

        #Database Name
        db = client["piiclone"]
        #Collection Name
        col = db["form_penilaian"]
        col_user = db["users_selenium"]

        #Return Log Error Dictionary
        Log_Error = {}

        #Variabel return
        Elemen = 0
        ErrorKey = 0
        NSEEn = 0
        Labelkomp = 0
    
        #Database Key
        # PID = "formM-gONh9yHYwFgjZt5fb9dKQ"
        # Student_ID = "21060124190767" 
        PID = req.process_id
        Student_ID = req.student_id

        def decrypt_password(encrypted_data, iv, key):
            # Convert the 64-character hex key back to 32 bytes
            key_bytes = binascii.unhexlify(key)

            # Convert the 32-character hex IV back to 16 bytes
            iv_bytes = binascii.unhexlify(iv)

            # Convert hexadecimal encrypted data back to bytes
            encrypted_data_bytes = binascii.unhexlify(encrypted_data)

            # Create the cipher object for AES-256-CBC
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt the data
            decrypted_data_padded = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

            # Remove padding
            padder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            decrypted_data = padder.update(decrypted_data_padded) + padder.finalize()

            # The decrypted data is in bytes, decode it to a UTF-8 string
            return decrypted_data.decode('utf-8')

        #Username Req
        ID_Student = col_user.find_one({'user_info':Student_ID},{'_id': 0})
        username = ID_Student["alt_user_info"]
        encrypted_data = ID_Student["alt_password"]
        iv = ID_Student["alt_iv"]
        key = os.getenv("ENC_PSS")
        
        decrypted_password = decrypt_password(encrypted_data, iv, key)

        #Enter FAIP
        driver.get(req.url)
        driver.maximize_window()

        #input username & password
        driver.find_element(By.ID, "email").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(decrypted_password)

        #masuk login
        driver.find_element(By.ID, "m_login_signin_submit").click()

        driver.implicitly_wait(2)

        driver.find_element(By.LINK_TEXT, "FAIP").click()

        driver.find_element(By.LINK_TEXT, "Edit").click()

        # driver.find_element(By.LINK_TEXT, "BUAT FAIP BARU").click()

        # WebDriverWait(driver, 10).until(EC.alert_is_present())
        # driver.switch_to.alert.accept()

        #Form Isian

        #PENGISIAN I1
        def FormI1():
            driver.find_element(By.LINK_TEXT, "I.1").click()
            driver.implicitly_wait(5)

            print("================================================\nFormI1")

            #Database
            Dict_I1 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_satu':1})
            Object_I1 = Dict_I1["form_i_satu"]

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            #add alamat
            ID_Count_Alamat_I1 = 0
            print("\nAlamat I1\n")

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
                print ("Row " + str(ID_Count_Alamat_I1) + " tidak ada\n") 
            
            Counter_Alamat_I1 = 1
            DB_CountAlamat_I1 = 0

            #Database Alamat
            Alamat_I1 = Object_I1["alamat"]
            n_Alamat_I1 = len(Alamat_I1)

            print("Jumlah Document: " + str(n_Alamat_I1) + "\n")

            print("Start from Row: " + str(ID_Count_Alamat_I1))
            print("Row Ditambah: " + str(n_Alamat_I1) + "\n")

            while Counter_Alamat_I1 <= n_Alamat_I1:
                #add row
                Alamat_Row_I1 = str(ID_Count_Alamat_I1)

                TambahI1alamat = driver.find_element(By.XPATH, '//button[@onclick="add111(\'ala\')"]')
                action.move_to_element(TambahI1alamat).perform()
                TambahI1alamat.send_keys(Keys.ENTER)

                #Document I1 Alamat
                Isi_Alamat_I1 = Alamat_I1[DB_CountAlamat_I1]
                print("Counter Row: " + str(Counter_Alamat_I1))
                print("Key Document: " + Isi_Alamat_I1["key"] + "\n")

                try:
                    AddressType_I1 = Isi_Alamat_I1["tipe"]
                    ID_AddressType_I1 = "addr_type" + Alamat_Row_I1
                    try:
                        Select_AddressType_I1 = Select(driver.find_element(By.ID, ID_AddressType_I1))
                        Select_AddressType_I1.select_by_visible_text(AddressType_I1)
                        print("- AddressType I1: " + AddressType_I1)
                        Elemen += 1
                    except NSEE:
                        print("- AddressType I1: NSEE")
                        Log_Error.update({"AddressType I1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- AddressType I1: KeyError")
                    Log_Error.update({"AddressType I1":"KeyError"})
                    ErrorKey += 1

                try:
                    AddressDesc_I1 = Isi_Alamat_I1["alamat"]
                    ID_AddressDesc_I1 = "addr_desc" + Alamat_Row_I1
                    driver.find_element(By.ID, ID_AddressDesc_I1).send_keys(AddressDesc_I1)
                    print("- AddressDesc I1: " + AddressDesc_I1)
                    Elemen += 1
                except KeyError:
                    print("- AddressDesc I1: KeyError")
                    Log_Error.update({"AddressDesc I1":"KeyError"})
                    ErrorKey += 1

                try:
                    AddressLoc_I1 = Isi_Alamat_I1["kota"]
                    ID_AddressLoc_I1 = "addr_loc" + Alamat_Row_I1
                    driver.find_element(By.ID, ID_AddressLoc_I1).send_keys(AddressLoc_I1)
                    print("- AddressLoc I1: " + AddressLoc_I1)
                    Elemen += 1
                except KeyError:
                    print("- AddressLoc I1: KeyError")
                    Log_Error.update({"AddressLoc I1":"KeyError"})
                    ErrorKey += 1

                try:
                    AddressZip_I1 = Isi_Alamat_I1["kodePos"]
                    ID_AddressZip_I1 = "addr_zip" + Alamat_Row_I1
                    driver.find_element(By.ID, ID_AddressZip_I1).send_keys(AddressZip_I1)
                    print("- AddressZip I1: " + AddressZip_I1)
                    Elemen += 1
                except KeyError:
                    print("- AddressZip I1: KeyError")
                    Log_Error.update({"AddressZip I1":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_Alamat_I1 += 1
                DB_CountAlamat_I1 += 1
                ID_Count_Alamat_I1 += 1
                print("\nRow " + Alamat_Row_I1 + " telah diisi\n")

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
                print ("Row " + str(ID_Count_Lembaga_I1) + " tidak ada\n") 
            
            Counter_Lembaga_I1 = 1
            DB_CountLembaga_I1 = 0

            #Database Lembaga
            Lembaga_I1 = Object_I1["lembaga"]
            n_Lembaga_I1 = len(Lembaga_I1)

            print("Jumlah Document: " + str(n_Lembaga_I1) + "\n")

            print("Start from Row: " + str(ID_Count_Lembaga_I1))
            print("Row Ditambah: " + str(n_Lembaga_I1) + "\n")

            while Counter_Lembaga_I1 <= n_Lembaga_I1:
                #add row
                Lembaga_Row_I1 = str(ID_Count_Lembaga_I1)

                TambahI1lembaga = driver.find_element(By.XPATH, '//button[@onclick="add112(\'wor\')"]')
                action.move_to_element(TambahI1lembaga).perform()
                TambahI1lembaga.send_keys(Keys.ENTER)

                #Document I1 Lembaga
                Isi_Lembaga_I1 = Lembaga_I1[DB_CountLembaga_I1]
                print("Counter Row: " + str(Counter_Lembaga_I1))
                print("Key Document: " + Isi_Lembaga_I1["key"] + "\n")

                try:
                    ExpName_I1 = Isi_Lembaga_I1["nama"]
                    ID_ExpName_I1 = "exp_name" + Lembaga_Row_I1
                    driver.find_element(By.ID, ID_ExpName_I1).send_keys(ExpName_I1)
                    print("- ExpName I1: " + ExpName_I1)
                    Elemen += 1
                except KeyError:
                    print("- ExpName I1: KeyError")
                    Log_Error.update({"ExpName I1":"KeyError"})
                    ErrorKey += 1

                try:
                    ExpDesc_I1 = Isi_Lembaga_I1["jabatan"]
                    ID_ExpDesc_I1 = "exp_desc" + Lembaga_Row_I1
                    driver.find_element(By.ID, ID_ExpDesc_I1).send_keys(ExpDesc_I1)
                    print("- ExpDesc I1: " + ExpDesc_I1)
                    Elemen += 1
                except KeyError:
                    print("- ExpDesc I1: KeyError")
                    Log_Error.update({"ExpDesc I1":"KeyError"})
                    ErrorKey += 1

                try:
                    ExpLoc_I1 = Isi_Lembaga_I1["kota"]
                    ID_ExpLoc_I1 = "exp_loc" + Lembaga_Row_I1
                    driver.find_element(By.ID, ID_ExpLoc_I1).send_keys(ExpLoc_I1)
                    print("- ExpLoc I1: " + ExpLoc_I1)
                    Elemen += 1
                except KeyError:
                    print("- ExpLoc I1: KeyError")
                    Log_Error.update({"ExpLoc I1":"KeyError"})
                    ErrorKey += 1

                try:
                    ExpZip_I1 = Isi_Lembaga_I1["kodePos"]
                    ID_ExpZip_I1 = "exp_zip" + Lembaga_Row_I1
                    driver.find_element(By.ID, ID_ExpZip_I1).send_keys(ExpZip_I1)
                    print("- ExpZip I1: " + ExpZip_I1)
                    Elemen += 1
                except KeyError:
                    print("- ExpZip I1: KeyError")
                    Log_Error.update({"ExpZip I1":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_Lembaga_I1 += 1
                DB_CountLembaga_I1 += 1
                ID_Count_Lembaga_I1 += 1
                print("\nRow " + Lembaga_Row_I1 + " telah diisi\n")

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
                print ("Row " + str(ID_Count_Phone_I1) + " tidak ada\n") 

            Counter_Phone_I1 = 1
            DB_CountPhone_I1 = 0

            #Database Phone
            Phone_I1 = Object_I1["komunikasi"]
            n_Phone_I1 = len(Phone_I1)

            print("Jumlah Document: " + str(n_Phone_I1) + "\n")
            
            print("Start from Row: " + str(ID_Count_Phone_I1))
            print("Row Ditambah: " + str(n_Phone_I1) + "\n")

            while Counter_Phone_I1 <= n_Phone_I1:
                #add row
                Phone_Row_I1 = str(ID_Count_Phone_I1)

                TambahI1Phone = driver.find_element(By.XPATH, '//button[@onclick="add113(\'pho\')"]')
                action.move_to_element(TambahI1Phone).perform()
                TambahI1Phone.send_keys(Keys.ENTER)

                #Document I1 Phone
                Isi_Phone_I1 = Phone_I1[DB_CountPhone_I1]
                print("Counter Row: " + str(Counter_Phone_I1))
                print("Key Document: " + Isi_Phone_I1["key"] + "\n")

                try:
                    PhoneType_I1 = Isi_Phone_I1["tipe"]
                    ID_PhoneType_I1 = "phone_type" + Phone_Row_I1
                    try:
                        Select_PhoneType_I1 = Select(driver.find_element(By.ID, ID_PhoneType_I1))
                        Select_PhoneType_I1.select_by_visible_text(PhoneType_I1)
                        print("- PhoneType I1: " + PhoneType_I1)
                        Elemen += 1
                    except NSEE:
                        print("- PhoneType I1: NSEE")
                        Log_Error.update({"PhoneType I1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- PhoneType I1: KeyError")
                    Log_Error.update({"PhoneType I1":"KeyError"})
                    ErrorKey += 1

                try:
                    PhoneValue_I1 = Isi_Phone_I1["nomor"]
                    ID_PhoneValue_I1 = "phone_value" + Phone_Row_I1
                    driver.find_element(By.ID, ID_PhoneValue_I1).send_keys(PhoneValue_I1)
                    print("- PhoneValue I1: " + PhoneValue_I1)
                    Elemen += 1
                except KeyError:
                    print("- PhoneValue I1: KeyError")
                    Log_Error.update({"PhoneValue I1":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_Phone_I1 += 1
                DB_CountPhone_I1 += 1
                ID_Count_Phone_I1 += 1
                print("\nRow " + Phone_Row_I1 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN I2
        def FormI2():
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
                print ("Row " + str(ID_Count_I2) + " tidak ada\n") 
            
            Counter_I2 = 1
            DB_Count_I2 = 0

            #Database
            Dict_I2 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_dua':1})
            List_I2 = Dict_I2["form_i_dua"]
            n_I2 = len(List_I2)

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_I2) + "\n")

            print("Start from Row: " + str(ID_Count_I2))
            print("Row Ditambah: " + str(n_I2) + "\n")

            while Counter_I2 <= n_I2:
                #add row
                TambahI2 = driver.find_element(By.XPATH, '//button[@onclick="add12(\'edu\')"]')
                action.move_to_element(TambahI2).perform()
                TambahI2.send_keys(Keys.ENTER)

                Row_I2 = str(ID_Count_I2)

                #Document I2
                Isi_I2 = List_I2[DB_Count_I2]
                print("Counter Row: " + str(Counter_I2))
                print("Key Document: " + Isi_I2["key"] + "\n")

                try:
                    Universitas_I2 = Isi_I2["namaPerguruan"]
                    ID_Universitas_I2 = "12_school" + Row_I2
                    driver.find_element(By.ID, ID_Universitas_I2).send_keys(Universitas_I2)
                    print("- Universitas I2: " + Universitas_I2)
                    Elemen += 1
                except KeyError:
                    print("- Universitas I2: KeyError")
                    Log_Error.update({"Universitas I2":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Tingkat_I2 = Isi_I2["tingkatPendidikan"]
                    ID_Tingkat_I2 = "12_degree" + Row_I2
                    try:
                        Select_Tingkat_I2 = Select(driver.find_element(By.ID, ID_Tingkat_I2))
                        Select_Tingkat_I2.select_by_visible_text(Tingkat_I2)
                        print("- Tingkat I2: " + Tingkat_I2)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat I2: NSEE")
                        Log_Error.update({"Tingkat I2":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat I2: KeyError")
                    Log_Error.update({"Tingkat I2":"KeyError"})
                    ErrorKey += 1

                try:
                    Fakultas_I2 = Isi_I2["fakultas"]
                    ID_Fakultas_I2 = "12_fakultas" + Row_I2
                    driver.find_element(By.ID, ID_Fakultas_I2).send_keys(Fakultas_I2)
                    print("- Fakultas I2: " + Fakultas_I2)
                    Elemen += 1
                except KeyError:
                    print("- Fakultas I2: KeyError")
                    Log_Error.update({"Fakultas I2":"KeyError"})
                    ErrorKey += 1

                try:
                    Jurusan_I2 = Isi_I2["jurusan"]
                    ID_Jurusan_I2 = "12_fieldofstudy" + Row_I2
                    driver.find_element(By.ID, ID_Jurusan_I2).send_keys(Jurusan_I2)
                    print("- Jurusan I2: " + Jurusan_I2)
                    Elemen += 1
                except KeyError:
                    print("- Jurusan I2: KeyError")
                    Log_Error.update({"":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_I2 = Isi_I2["kotaPerguruan"]
                    ID_Kota_I2 = "12_kota" + Row_I2
                    driver.find_element(By.ID, ID_Kota_I2).send_keys(Kota_I2)   
                    print("- Kota I2: " + Kota_I2)
                    Elemen += 1
                except KeyError:
                    print("- Kota I2: KeyError")
                    Log_Error.update({"Kota I2":"KeyError"}) 
                    ErrorKey += 1

                try:
                    Provinsi_I2 = Isi_I2["provinsi"]
                    ID_Provinsi_I2 = "12_provinsi" + Row_I2
                    driver.find_element(By.ID, ID_Provinsi_I2).send_keys(Provinsi_I2)
                    print("- Provinsi I2: " + Provinsi_I2)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi I2: KeyError")
                    Log_Error.update({"Provinsi I2":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_I2 = Isi_I2["negara"]
                    ID_Negara_I2 = "12_negara" + Row_I2
                    driver.find_element(By.ID, ID_Negara_I2).send_keys(Negara_I2)
                    print("- Negara: " + Negara_I2)
                    Elemen += 1
                except KeyError:
                    print("- Negara I2: KeyError")
                    Log_Error.update({"Negara I2":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunLulus_I2 = Isi_I2["tahunLulus"]
                    ID_TahunLulus_I2 = "12_tahunlulus" + Row_I2
                    driver.find_element(By.ID, ID_TahunLulus_I2).send_keys(TahunLulus_I2)
                    print("- Tahun Lulus I2: " + TahunLulus_I2)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Lulus I2: KeyError")
                    Log_Error.update({"Tahun Lulus I2:":"KeyError"})
                    ErrorKey += 1

                try:
                    Gelar_I2 = Isi_I2["gelar"]
                    ID_Gelar_I2 = "12_title" + Row_I2
                    driver.find_element(By.ID, ID_Gelar_I2).send_keys(Gelar_I2)
                    print("- Gelar I2: " + Gelar_I2)
                    Elemen += 1
                except KeyError:
                    print("- Gelar I2: KeyError")
                    Log_Error.update({"Gelar I2":"KeyError"})
                    ErrorKey += 1

                try:
                    JudulTA_I2 = Isi_I2["judulTa"]
                    ID_JudulTA_I2 = "12_activities" + Row_I2
                    Scroll_JudulTA_I2 = driver.find_element(By.ID, ID_JudulTA_I2)
                    action.move_to_element(Scroll_JudulTA_I2).perform()
                    Scroll_JudulTA_I2.send_keys(JudulTA_I2)
                    print("- Judul TA I2: " + JudulTA_I2)
                    Elemen += 1
                except KeyError:
                    print("- Judul TA I2: KeyError")
                    Log_Error.update({"Judul TA":"KeyError"})
                    ErrorKey += 1

                try:
                    UraianTA_I2 = Isi_I2["uraianSingkat"]
                    ID_UraianTA_I2 = "12_description" + Row_I2
                    Scroll_UraianTA_I2 = driver.find_element(By.ID, ID_UraianTA_I2)
                    action.move_to_element(Scroll_UraianTA_I2).perform()
                    Scroll_UraianTA_I2.send_keys(UraianTA_I2)
                    print("- Uraian TA I2: " + UraianTA_I2)
                    Elemen += 1
                except KeyError:
                    print("- Uraian TA I2: KeyError")
                    Log_Error.update({"Uraian TA I2":"KeyError"})
                    ErrorKey += 1

                try:
                    Nilai_I2 = Isi_I2["nilaiAkademikRata"]
                    ID_Nilai_I2 = "12_score" + Row_I2
                    Scroll_Nilai_I2 = driver.find_element(By.ID, ID_Nilai_I2)
                    action.move_to_element(Scroll_Nilai_I2).perform()
                    Scroll_Nilai_I2.send_keys(Nilai_I2)
                    print("- Nilai I2: " + Nilai_I2)
                    Elemen += 1
                except KeyError:
                    print("- Nilai I2: KeyError")
                    Log_Error.update({"Nilai I2":"KeyError"})
                    ErrorKey += 1
                
                #End/retry point of loop
                Counter_I2 += 1
                DB_Count_I2 += 1
                ID_Count_I2 += 1
                print("\nRow " + Row_I2 + " telah diisi\n")

            driver.refresh() 

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
                print ("Row " + str(ID_Count_I3) + " tidak ada\n") 
            
            Counter_I3 = 1
            DB_Count_I3 = 0

            #Database
            Dict_I3 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_tiga':1})
            List_I3 = Dict_I3["form_i_tiga"]
            n_I3 = len(List_I3)

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_I3) + "\n")

            print("Start from Row: " + str(ID_Count_I3))
            print("Row Ditambah: " + str(n_I3) + "\n")

            while Counter_I3 <= n_I3:
                #add row
                TambahI3 = driver.find_element(By.XPATH, '//button[@onclick="add13(\'org\')"]')
                action.move_to_element(TambahI3).perform()
                TambahI3.send_keys(Keys.ENTER)

                Row_I3 = str(ID_Count_I3)

                #Document I3
                Isi_I3 = List_I3[DB_Count_I3]
                print("Counter Row: " + str(Counter_I3))
                print("Key Document: " + Isi_I3["key"] + "\n")

                try:
                    Organisasi_I3 = Isi_I3["namaOrganisasi"]
                    ID_Organisasi_I3 = "13_nama_org" + Row_I3
                    driver.find_element(By.ID, ID_Organisasi_I3).send_keys(Organisasi_I3)
                    print("- Nama Organisasi: " + Organisasi_I3)
                    Elemen += 1
                except KeyError:
                    print("- Nama Organisasi I3: KeyError")
                    Log_Error.update({"Nama Organisasi I3":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Jenis_I3 = Isi_I3["jenisOrganisasi"]
                    ID_Jenis_I3 = "13_jenis" + Row_I3
                    Select_Jenis_I3 = Select(driver.find_element(By.ID, ID_Jenis_I3))
                    try:
                        Select_Jenis_I3.select_by_visible_text(Jenis_I3)
                        print("- Jenis I3: " + Jenis_I3)
                        Elemen += 1
                    except NSEE:
                        print("- Jenis I3: NSEE")
                        Log_Error.update({"Jenis I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jenis I3: KeyError")
                    Log_Error.update({"Jenis I3":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_I3 = Isi_I3["kotaAsal"]
                    ID_Kota_I3 = "13_tempat" + Row_I3
                    driver.find_element(By.ID, ID_Kota_I3).send_keys(Kota_I3)
                    print("- Kota I3: " + Kota_I3)
                    Elemen += 1
                except KeyError:
                    print("- Kota I3: KeyError")
                    Log_Error.update({"Kota I3":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_I3 = Isi_I3["provinsiAsal"]
                    ID_Provinsi_I3 = "13_provinsi" + Row_I3
                    driver.find_element(By.ID, ID_Provinsi_I3).send_keys(Provinsi_I3)
                    print("- Provinsi I3: " + Provinsi_I3)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi I3: KeyError")
                    Log_Error.update({"Provinsi I3":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_I3 = Isi_I3["negaraAsal"]
                    ID_Negara_I3 = "13_negara" + Row_I3
                    driver.find_element(By.ID, ID_Negara_I3).send_keys(Negara_I3)
                    print("- Negara I3: " + Negara_I3)
                    Elemen += 1
                except KeyError:
                    print("- Negara I3: KeyError")
                    Log_Error.update({"Negara I3":"KeyError"})
                    ErrorKey += 1
                
                try:
                    BulanMulai_I3 = Isi_I3["bulanMulai"]
                    ID_BulanMulai_I3 = "13_startdate" + Row_I3
                    Select_BulanMulai_I3 = Select(driver.find_element(By.ID, ID_BulanMulai_I3))
                    try:
                        Select_BulanMulai_I3.select_by_visible_text(BulanMulai_I3)
                        print("- Bulan Mulai I3: " + BulanMulai_I3)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Mulai I3: NSEE")
                        Log_Error.update({"Bulan Mulai I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Mulai I3: KeyError")
                    Log_Error.update({"Bulan Mulai I3":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunMulai_I3 = Isi_I3["tahunMulai"]
                    ID_TahunMulai_I3 = "13_startyear" + Row_I3
                    driver.find_element(By.ID, ID_TahunMulai_I3).send_keys(TahunMulai_I3)
                    print("- Tahun Mulai I3: " + TahunMulai_I3)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Mulai I3: KeyError")
                    Log_Error.update({"Tahun Mulai I3":"KeyError"})
                    ErrorKey += 1

                try:
                    ID_Anggota_I3 = "13_work" + Row_I3
                    Angggota_I3 = driver.find_element(By.ID, ID_Anggota_I3)
                    if Isi_I3["masihAnggota"] == True:
                        action.move_to_element_with_offset(Angggota_I3, 0, 0).click().perform()
                        print("- Masih Anggota I3: True")
                        Elemen += 1
                    else:
                        print("- Masih Anggota I3: False")
                        Elemen += 1
                        try:
                            BulanSelesai_I3 = Isi_I3["bulan"]
                            ID_BulanSelesai_I3 = "13_enddate" + Row_I3
                            Select_BulanSelesai_I3 = Select(driver.find_element(By.ID, ID_BulanSelesai_I3))
                            try:
                                Select_BulanSelesai_I3.select_by_visible_text(BulanSelesai_I3)
                                print("- Bulan Selesai I3: " + BulanSelesai_I3)
                                Elemen += 1
                            except NSEE:
                                print("- Bulan Selesai I3: NSEE")
                                Log_Error.update({"Bulan Selesai I3":"NSEE"})
                                NSEEn += 1
                        except KeyError:
                            print("- Bulan Selesai I3: KeyError")
                            Log_Error.update({"Bulan Selesai I3":"KeyError"})
                            ErrorKey += 1
                        
                        try:
                            TahunSelesai_I3 = Isi_I3["tahun"]
                            ID_TahunSelesai_I3 = "13_endyear" + Row_I3
                            driver.find_element(By.ID, ID_TahunSelesai_I3).send_keys(TahunSelesai_I3)
                            print("- Tahun Selesai I3: " + TahunSelesai_I3)
                            Elemen += 1
                        except KeyError:
                            print("- Tahun Selesai I3: KeyError")
                            Log_Error.update({"Tahun Selesai I3":"KeyError"})
                            ErrorKey += 1
                except KeyError:
                    print("- Masih Anggota I3: KeyError")
                    Log_Error.updata({"Masih Anggota I3":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Jabatan_I3 = Isi_I3["jabatanOrganisasi"]
                    ID_Jabatan_I3 = "13_jabatan" + Row_I3
                    Select_Jabatan_I3 = Select(driver.find_element(By.ID, ID_Jabatan_I3))
                    try:
                        Select_Jabatan_I3.select_by_visible_text(Jabatan_I3)
                        print("- Jabatan I3: " + Jabatan_I3)
                        Elemen += 1
                    except NSEE:
                        print("- Jabatan I3: NSEE")
                        Log_Error.update({"Jabatan I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jabatan I3: KeyError")
                    Log_Error.update({"Jabatan I3":"KeyError"})
                    ErrorKey += 1

                try:
                    Tingkat_I3 = Isi_I3["tingkatanOrganisasi"]
                    ID_Tingkat_I3 = "13_tingkat" + Row_I3
                    Scroll_Tingkat_I3 = driver.find_element(By.ID, ID_Tingkat_I3)
                    action.move_to_element(Scroll_Tingkat_I3).perform()
                    Select_Tingkat_I3 = Select(Scroll_Tingkat_I3)
                    try:
                        Select_Tingkat_I3.select_by_visible_text(Tingkat_I3)
                        print("- Tingkat I3: " + Tingkat_I3)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat I3: NSEE")
                        Log_Error.update({"Tingkat I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat I3: KeyError")
                    Log_Error.update({"Tingkat I3":"KeyError"})
                    ErrorKey += 1

                try:
                    Lingkup_I3 = Isi_I3["kegiatanOrganisasi"]
                    ID_Lingkup_I3 = "13_lingkup" + Row_I3
                    Scroll_Lingkup_I3 = driver.find_element(By.ID, ID_Lingkup_I3)
                    action.move_to_element(Scroll_Lingkup_I3).perform()
                    Select_Lingkup_I3 = Select(Scroll_Lingkup_I3)
                    try:
                        Select_Lingkup_I3.select_by_visible_text(Lingkup_I3)
                        print("- Lingkup I3: " + Lingkup_I3)
                        Elemen += 1
                    except NSEE:
                        print("- Lingkup I3: NSEE")
                        Log_Error.update({"Lingkup I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Lingkup I3: KeyError")
                    Log_Error.update({"Lingkup I3":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Uraian_I3 = Isi_I3["uraianTugas"]
                    ID_Uraian_I3 = "13_aktifitas" + Row_I3
                    Scroll_Uraian_I3 = driver.find_element(By.ID, ID_Uraian_I3)
                    action.move_to_element(Scroll_Uraian_I3).perform()
                    Scroll_Uraian_I3.send_keys(Uraian_I3)
                    print("- Uraian I3: " + Uraian_I3)
                    Elemen += 1
                except KeyError:
                    print("- Uraian I3: KeyError")
                    Log_Error.update({"Uraian I3":"KeyError"})
                    ErrorKey += 1
                
                #Kompetisi I3 
                ID_Komp_I3 = "13_komp" + Row_I3
                Scroll_Komp_I3 = driver.find_element(By.ID, ID_Komp_I3)
                action.move_to_element(Scroll_Komp_I3).perform()

                try:
                    Komp_I3 = Isi_I3["klaimKompetensiWsatu"]
                    print("- Komp W1 I3: " + str(len(Komp_I3)))
                    try:
                        for Komp_Value_I3 in Komp_I3:
                            Komp_Label_I3 = Komp_Value_I3[slice(5)]
                            Komp_Call_I3 = f'//*[@id="{ID_Komp_I3}"]//optgroup[contains(@label, "{Komp_Label_I3}")]/option[@value="{Komp_Value_I3}."]'
                            Komp_Find_I3 = driver.find_element(By.XPATH, Komp_Call_I3)
                            action.move_to_element_with_offset(Komp_Find_I3, 0, -15).click().perform()
                            print("-", Komp_Value_I3)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W1 I3: NSEE")
                        Log_Error.update({"Komp W1 I3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W1 I3: KeyError")
                    Log_Error.update({"Komp W1 I3":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_I3 += 1
                DB_Count_I3 += 1
                ID_Count_I3 += 1
                print("\nRow " + Row_I3 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN I4
        def FormI4():
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
                print ("Row " + str(ID_Count_I4) + " tidak ada\n") 

            Counter_I4 = 1
            DB_Count_I4 = 0

            #Database
            Dict_I4 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_empat':1})
            List_I4 = Dict_I4["form_i_empat"]
            n_I4 = len(List_I4)

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_I4) + "\n")
            
            print("Start from Row: " + str(ID_Count_I4))
            print("Row Ditambah: " + str(n_I4) + "\n")

            while Counter_I4 <= n_I4:
                #add row
                TambahI4 = driver.find_element(By.XPATH, '//button[@onclick="add14(\'phg\')"]')
                action.move_to_element(TambahI4).perform()
                TambahI4.send_keys(Keys.ENTER)

                #Document I4
                Isi_I4 = List_I4[DB_Count_I4]
                print("Counter Row: " + str(Counter_I4))
                print("Key Document: " + Isi_I4["key"] + "\n")

                Row_I4 = str(ID_Count_I4)

                try:
                    Penghargaan_I4 = Isi_I4["namaTandaPenghargaan"]
                    ID_Penghargaan_I4 = "14_nama" + Row_I4
                    driver.find_element(By.ID, ID_Penghargaan_I4).send_keys(Penghargaan_I4)
                    print("- Penghargaan I4: " + Penghargaan_I4)
                    Elemen += 1
                except KeyError:
                    print("- Penghargaan I4: KeyError")
                    Log_Error.update({"Penghargaan I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Lembaga_I4 = Isi_I4["namaTandaPenghargaan"]
                    ID_Lembaga_I4 = "14_lembaga" + Row_I4
                    driver.find_element(By.ID, ID_Lembaga_I4).send_keys(Lembaga_I4)
                    print("- Lembaga I4: " + Lembaga_I4)
                    Elemen += 1
                except KeyError:
                    print("- Lembaga I4: KeyError")
                    Log_Error.update({"Lembaga I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_I4 = Isi_I4["kotaAsal"]
                    ID_Kota_I4 = "14_location" + Row_I4
                    driver.find_element(By.ID, ID_Kota_I4).send_keys(Kota_I4)
                    print("- Kota I4: " + Kota_I4)
                    Elemen += 1
                except KeyError:
                    print("- Kota I4: KeyError")
                    Log_Error.update({"Kota I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_I4 = Isi_I4["provinsiAsal"]
                    ID_Provinsi_I4 = "14_provinsi" + Row_I4
                    driver.find_element(By.ID, ID_Provinsi_I4).send_keys(Provinsi_I4)
                    print("- Provinsi I4: " + Provinsi_I4)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi I4: KeyError")
                    Log_Error.update({"Provinsi I4":"KeyError"})
                    ErrorKey += 1
                    
                try:
                    Negara_I4 = Isi_I4["negaraAsal"]
                    ID_Negara_I4 = "14_negara" + Row_I4
                    driver.find_element(By.ID, ID_Negara_I4).send_keys(Negara_I4)
                    print("- Negara I4: " + Negara_I4)
                    Elemen += 1
                except KeyError:
                    print("- Negara I4: KeyError")
                    Log_Error.update({"Negara I4":"KeyError"})
                    ErrorKey += 1

                try:
                    BulanTerbit_I4 = Isi_I4["bulanTerbit"]
                    ID_BulanTerbit_I4 = "14_startdate" + Row_I4
                    Select_BulanTerbit_I4 = Select(driver.find_element(By.ID, ID_BulanTerbit_I4))
                    try:
                        Select_BulanTerbit_I4.select_by_visible_text(BulanTerbit_I4)
                        print("- Bulan Terbit I4: " + BulanTerbit_I4)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Terbit I4: NSEE")
                        Log_Error.update({"Bulan Terbit I4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Terbit I4: KeyError")
                    Log_Error.update({"Bulan Terbit I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Tahun_I4 = Isi_I4["tahunTerbit"]
                    ID_Tahun_I4 = "14_startyear" + Row_I4
                    driver.find_element(By.ID, ID_Tahun_I4).send_keys(Tahun_I4)
                    print("- Tahun I4: " + Tahun_I4)
                    Elemen += 1
                except KeyError:
                    print("- Tahun I4: KeyError")
                    Log_Error.update({"Tahun I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Tingkat_I4 = Isi_I4["tingkatPenghargaan"]
                    ID_Tingkat_I4 = "14_tingkat" + Row_I4
                    Select_Tingkat_I4 = Select(driver.find_element(By.ID, ID_Tingkat_I4))
                    try:
                        Select_Tingkat_I4.select_by_visible_text(Tingkat_I4)
                        print("- Tingkat I4: " + Tingkat_I4)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat I4: NSEE")
                        Log_Error.update({"Tingkat I4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat I4: KeyError")
                    Log_Error.update({"Tingkat I4":"KeyError"})
                    ErrorKey += 1

                try:
                    Lembaga_I4 = Isi_I4["jenisLembagaPenghargaan"]
                    ID_Lembaga_I4 = "14_tingkatlembaga" + Row_I4
                    Select_Lembaga_I4 = Select(driver.find_element(By.ID, ID_Lembaga_I4))
                    try:
                        Select_Lembaga_I4.select_by_visible_text(Lembaga_I4)
                        print("- Lembaga I4: " + Lembaga_I4)
                        Elemen += 1
                    except NSEE:
                        print("- Lembaga I4: NSEE")
                        Log_Error.update({"Lembaga I4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Lembaga I4: KeyError")
                    Log_Error.update({"Lembaga I4":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Uraian_I4 = Isi_I4["uraianSingkatAktifitas"]
                    ID_Uraian_I4 = "14_uraian" + Row_I4
                    Scroll_Uraian_I4 = driver.find_element(By.ID, ID_Uraian_I4)
                    action.move_to_element(Scroll_Uraian_I4).perform()
                    Scroll_Uraian_I4.send_keys(Uraian_I4)
                    print("- Uraian I4: " + Uraian_I4)
                    Elemen += 1
                except KeyError:
                    print("- Uraian I4: KeyError")
                    Log_Error.update({"Uraian I4":"KeyError"})
                    ErrorKey += 1

                #Kompetisi I4 
                ID_Komp_I4 = "14_komp" + Row_I4
                Scroll_Komp_I4 = driver.find_element(By.ID, ID_Komp_I4)
                action.move_to_element(Scroll_Komp_I4).perform()

                try:
                    Komp_I4 = Isi_I4["klaimKompetensiWsatu"]
                    print("- Komp W1 I4: " + str(len(Komp_I4)))
                    try:
                        for Komp_Value_I4 in Komp_I4:
                            Komp_Label_I4 = Komp_Value_I4[slice(5)]
                            Komp_Call_I4 = f'//*[@id="{ID_Komp_I4}"]//optgroup[contains(@label, "{Komp_Label_I4}")]/option[@value="{Komp_Value_I4}."]'
                            Komp_Find_I4 = driver.find_element(By.XPATH, Komp_Call_I4)
                            action.move_to_element_with_offset(Komp_Find_I4, 0, -15).click().perform()
                            print("-", Komp_Value_I4)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W1 I4: NSEE") 
                        Log_Error.update({"Komp W1 I4":"NSEE"})  
                        NSEEn += 1
                except KeyError:
                    print("- Komp W1 I4: KeyError")
                    Log_Error.update({"Komp W1 I4":"KeyError"})
                    ErrorKey += 1
                    
                #End/retry point of loop
                Counter_I4 += 1
                DB_Count_I4 += 1
                ID_Count_I4 += 1
                print("Row " + Row_I4 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN I5
        def FormI5():
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
                print ("Row " + str(ID_Count_I5) + " tidak ada\n") 
            
            Counter_I5 = 1
            DB_Count_I5 = 0

            #Database
            Dict_I5 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_lima':1})
            List_I5 = Dict_I5["form_i_lima"]
            n_I5 = len(List_I5)

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_I5) + "\n")

            print("Start from Row: " + str(ID_Count_I5))
            print("Row Ditambah: " + str(n_I5) + "\n")

            while Counter_I5 <= n_I5:
                #add row
                TambahI5 = driver.find_element(By.XPATH, '//button[@onclick="add15(\'pdd\')"]')
                action.move_to_element(TambahI5).perform()
                TambahI5.send_keys(Keys.ENTER)

                #Document I5
                Isi_I5 = List_I5[DB_Count_I5]
                print("Counter Row: " + str(Counter_I5))
                print("Key Document: " + Isi_I5["key"] + "\n")

                Row_I5 = str(ID_Count_I5)

                try:
                    Pendidikan_I5 = Isi_I5["namaPendidikanTeknik"]
                    ID_Pendidikan_I5 = "15_nama" + Row_I5
                    driver.find_element(By.ID, ID_Pendidikan_I5).send_keys(Pendidikan_I5)
                    print("- Pendidikan I5: " + Pendidikan_I5)
                    Elemen += 1
                except KeyError:
                    print("- Pendidikan I5: KeyError")
                    Log_Error.update({"Pendidikan I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Lembaga_I5 = Isi_I5["penyelenggara"]
                    ID_Lembaga_I5 = "15_lembaga" + Row_I5
                    driver.find_element(By.ID, ID_Lembaga_I5).send_keys(Lembaga_I5)
                    print("- Lembaga I5: " + Lembaga_I5)
                    Elemen += 1
                except KeyError:
                    print("- Lembaga I5: KeyError")
                    Log_Error.update({"Lembaga I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_I5 = Isi_I5["kotaAsal"]
                    ID_Kota_I5 = "15_location" + Row_I5
                    driver.find_element(By.ID, ID_Kota_I5).send_keys(Kota_I5)
                    print("- Kota I5: " + Kota_I5)
                    Elemen += 1
                except KeyError:
                    print("- Kota I5: KeyError")
                    Log_Error.update({"Kota I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_I5 = Isi_I5["provinsiAsal"]
                    ID_Provinsi_I5 = "15_provinsi" + Row_I5
                    driver.find_element(By.ID, ID_Provinsi_I5).send_keys(Provinsi_I5)
                    print("- Provinsi I5: " + Provinsi_I5)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi I5: KeyError")
                    Log_Error.update({"Provinsi I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_I5 = Isi_I5["negaraAsal"]
                    ID_Negara_I5 = "15_negara" + Row_I5
                    driver.find_element(By.ID, ID_Negara_I5).send_keys(Negara_I5)
                    print("- Negara I5: " + Negara_I5)
                    Elemen += 1
                except KeyError:
                    print("- Negara I5: KeyError")
                    Log_Error.update({"Negara I5":"KeyError"})
                    ErrorKey += 1

                try:
                    BulanMulai_I5 = Isi_I5["bulanMulai"]
                    ID_BulanMulai_I5 = "15_startdate" + Row_I5
                    Select_BulanMulai_I5 = Select(driver.find_element(By.ID, ID_BulanMulai_I5))
                    try:
                        Select_BulanMulai_I5.select_by_visible_text(BulanMulai_I5)
                        print("- Bulan Mulai I5: " + BulanMulai_I5)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Mulai I5: NSEE")
                        Log_Error.update({"Bulan Mulai I5":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Mulai I5: KeyError")
                    Log_Error.update({"Bulan Mulai I5":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunMulai_I5 = Isi_I5["tahunMulai"]
                    ID_TahunMulai_I5 = "15_startyear" + Row_I5
                    driver.find_element(By.ID, ID_TahunMulai_I5).send_keys(TahunMulai_I5)
                    print("- Tahun Mulai I5: " + TahunMulai_I5)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Mulai I5: KeyError")
                    Log_Error.update({"Tahun Mulai I5":"KeyError"})
                    ErrorKey += 1
                
                try:
                    ID_Anggota_I5 = "15_work" + Row_I5
                    Angggota_I5 = driver.find_element(By.ID, ID_Anggota_I5)
                    if Isi_I5["masihAnggota"] == True:
                        action.move_to_element_with_offset(Angggota_I5, 0, -20).click().perform()
                        print("- Masih Anggota I5: True")
                        Elemen += 1
                    else:
                        print("- Masih Anggota I5: False")
                        Elemen += 1
                        try:
                            BulanSelesai_I5 = Isi_I5["bulan"]
                            ID_BulanSelesai_I5 = "15_enddate" + Row_I5
                            Select_BulanSelesai_I5 = Select(driver.find_element(By.ID, ID_BulanSelesai_I5))
                            try:
                                Select_BulanSelesai_I5.select_by_visible_text(BulanSelesai_I5)
                                print("- Bulan Selesai I5: " + BulanSelesai_I5)
                                Elemen += 1
                            except NSEE:
                                print("- Bulan Selesai I5: NSEE")
                                Log_Error.update({"Bulan Selesai I5":"NSEE"})
                                NSEEn += 1
                        except KeyError:
                            print("- Bulan Selesai I5: KeyError")
                            Log_Error.update({"Bulan Selesai I5":"KeyError"})
                            ErrorKey += 1

                        try:
                            TahunSelesai_I5 = Isi_I5["tahun"]
                            ID_TahunSelesai_I5 = "15_endyear" + Row_I5
                            driver.find_element(By.ID, ID_TahunSelesai_I5).send_keys(TahunSelesai_I5)
                            print("- Tahun Selesai I5: " + TahunSelesai_I5)
                            Elemen += 1
                        except KeyError:
                            print("- Tahun Selesai I5: KeyError")
                            Log_Error.update({"Tahun Selesai I5":"KeyError"})
                            ErrorKey += 1
                except KeyError:
                    print("- Masih Anggota I5: KeyError")
                    Log_Error.update({"Masih Anggota I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Tingkat_I5 = Isi_I5["tingkatanMateriPelatihan"]
                    ID_Tingkat_I5 = "15_tingkat" + Row_I5
                    Select_Tingkat_I5 = Select(driver.find_element(By.ID, ID_Tingkat_I5))
                    try:
                        Select_Tingkat_I5.select_by_visible_text(Tingkat_I5)
                        print("- Tingkat I5: " + Tingkat_I5)
                        Elemen += 1
                    except NSEE:
                            print("- Tingkat I5: NSEE")
                            Log_Error.update({"Tingkat I5":"NSEE"})
                            NSEEn += 1
                except KeyError:
                    print("- Tingkat I5: KeyError")
                    Log_Error.update({"Tingkat I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Jam_I5 = Isi_I5["jamPendidikanTeknik"]
                    ID_Jam_I5 = "15_jam" + Row_I5
                    try:
                        Select_Jam_I5 = Select(driver.find_element(By.ID, ID_Jam_I5))
                        Select_Jam_I5.select_by_visible_text(Jam_I5)
                        print("- Jam I5: " + Jam_I5)
                        Elemen += 1
                    except NSEE:
                            print("- Jam I5: NSEE")
                            Log_Error.update({"Jam I5":"NSEE"})
                            NSEEn += 1
                except KeyError:
                    print("- Jam I5: KeyError")
                    Log_Error.update({"Jam I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_I5 = Isi_I5["uraianSingkatAktifitas"]
                    ID_Uraian_I5 = "15_uraian" + Row_I5
                    Scroll_Uraian_I5 = driver.find_element(By.ID, ID_Uraian_I5)
                    action.move_to_element(Scroll_Uraian_I5).perform()
                    Scroll_Uraian_I5.send_keys(Uraian_I5)
                    print("- Uraian I5: " + Uraian_I5)
                    Elemen += 1
                except KeyError:
                    print("- Uraian I5: KeyError")
                    Log_Error.update({"Uraian I5":"KeyError"})
                    ErrorKey += 1

                #Kompetisi I5 
                ID_Komp_I5 = "15_komp" + Row_I5
                Scroll_Komp_I5 = driver.find_element(By.ID, ID_Komp_I5)
                action.move_to_element(Scroll_Komp_I5).perform()

                try:
                    Komp_W2_I5 = Isi_I5["klaimKompetensiWdua"]
                    print("- Komp W2 I5: " + str(len(Komp_W2_I5)))
                    try:
                        for Komp_Value_W2_I5 in Komp_W2_I5:
                            Komp_Label_W2_I5 = Komp_Value_W2_I5[slice(5)]
                            Komp_Call_W2_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_W2_I5}")]/option[@value="{Komp_Value_W2_I5}."]'
                            Komp_Find_W2_I5 = driver.find_element(By.XPATH, Komp_Call_W2_I5)
                            action.move_to_element_with_offset(Komp_Find_W2_I5, 0, -15).click().perform()
                            print("-", Komp_Value_W2_I5)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W2 I5: NSEE")
                        Log_Error.update({"Komp W2 I5":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W2 I5: KeyError")
                    Log_Error.update({"Komp W2 I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_W4_I5 = Isi_I5["klaimKompetensiWempat"]
                    print("- Komp W4 I5: " + str(len(Komp_W4_I5)))
                    try:
                        for Komp_Value_W4_I5 in Komp_W4_I5:
                            Komp_Label_W4_I5 = Komp_Value_W4_I5[slice(5)]
                            Komp_Call_W4_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_W4_I5}")]/option[@value="{Komp_Value_W4_I5}."]'
                            Komp_Find_W4_I5 = driver.find_element(By.XPATH, Komp_Call_W4_I5)
                            action.move_to_element_with_offset(Komp_Find_W4_I5, 0, -15).click().perform()
                            print("-", Komp_Value_W4_I5)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 I5: NSEE")
                        Log_Error.update({"Komp W4 I5":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 I5: KeyError")
                    Log_Error.update({"Komp W4 I5":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P10_I5 = Isi_I5["klaimKompetensiPsepuluh"]
                    print("- Komp P10 I5: " + str(len(Komp_P10_I5))) 
                    try:
                        for Komp_Value_P10_I5 in Komp_P10_I5:
                            Komp_Label_P10_I5 = Komp_Value_P10_I5[slice(5)]
                            Komp_Call_P10_I5 = f'//*[@id="{ID_Komp_I5}"]//optgroup[contains(@label, "{Komp_Label_P10_I5}")]/option[@value="{Komp_Value_P10_I5}."]'
                            Komp_Find_P10_I5 = driver.find_element(By.XPATH, Komp_Call_P10_I5)
                            action.move_to_element_with_offset(Komp_Find_P10_I5, 0, -15).click().perform()
                            print("-", Komp_Value_P10_I5) 
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P10 I5: NSEE") 
                        Log_Error.update({"Komp P10 I5":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P10 I5: KeyError")
                    Log_Error.update({"Komp P10 I5":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_I5 += 1
                DB_Count_I5 += 1
                ID_Count_I5 += 1
                print("Row " + Row_I5 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN I6
        def FormI6():
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
                print ("Row " + str(ID_Count_I6) + " tidak ada\n") 
            
            Counter_I6 = 1
            DB_Count_I6 = 0

            #Database
            Dict_I6 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_i_enam':1})
            List_I6 = Dict_I6["form_i_enam"]
            n_I6 = len(List_I6)

            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_I6) + "\n")

            print("Start from Row: " + str(ID_Count_I6))
            print("Row Ditambah: " + str(n_I6) + "\n")

            while Counter_I6 <= n_I6:
                #add row
                TambahI6 = driver.find_element(By.XPATH, '//button[@onclick="add16(\'ppm\')"]')
                action.move_to_element(TambahI6).perform()
                TambahI6.send_keys(Keys.ENTER)

                #Document I6
                Isi_I6 = List_I6[DB_Count_I6]
                print("Counter Row: " + str(Counter_I6))
                print("Key Document: " + Isi_I6["key"] + "\n")

                Row_I6 = str(ID_Count_I6)

                try:
                    Pelatihan_I6 = Isi_I6["namaPendidikanPelatihan"]
                    ID_Pelatihan_I6 = "16_nama" + Row_I6
                    driver.find_element(By.ID, ID_Pelatihan_I6).send_keys(Pelatihan_I6)
                    print("- Pelatihan I6: " + Pelatihan_I6)
                    Elemen += 1
                except KeyError:
                    print("- Pelatihan I6: KeyError")
                    Log_Error.update({"Pelatihan I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Lembaga_I6 = Isi_I6["penyelenggara"]
                    ID_Lembaga_I6 = "16_lembaga" + Row_I6
                    driver.find_element(By.ID, ID_Lembaga_I6).send_keys(Lembaga_I6)
                    print("- Lembaga I6: " +Lembaga_I6)
                    Elemen += 1
                except KeyError:
                    print("- Lembaga I6: KeyError")
                    Log_Error.update({"Lembaga I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_I6 = Isi_I6["kotaAsal"]
                    ID_Kota_I6 = "16_location" + Row_I6
                    driver.find_element(By.ID, ID_Kota_I6).send_keys(Kota_I6)
                    print("- Kota I6: " + Kota_I6)
                    Elemen += 1
                except KeyError:
                    print("- Kota I6: KeyError")
                    Log_Error.update({"Kota I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_I6 = Isi_I6["provinsiAsal"]
                    ID_Provinsi_I6 = "16_provinsi" + Row_I6
                    driver.find_element(By.ID, ID_Provinsi_I6).send_keys(Provinsi_I6)
                    print("- Provinsi I6: " + Provinsi_I6)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi I6: KeyError")
                    Log_Error.update({"Provinsi I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_I6 = Isi_I6["negaraAsal"]
                    ID_Negara_I6 = "16_negara" + Row_I6
                    driver.find_element(By.ID, ID_Negara_I6).send_keys(Negara_I6)
                    print("- Negara I6: " + Negara_I6)
                    Elemen += 1
                except KeyError:
                    print("- Negara I6: KeyError")
                    Log_Error.update({"Negara I6":"KeyError"})
                    ErrorKey += 1

                try:
                    BulanMulai_I6 = Isi_I6["bulanMulai"]
                    ID_BulanMulai_I6 = "16_startdate" + Row_I6
                    Select_BulanMulai_I6 = Select(driver.find_element(By.ID, ID_BulanMulai_I6))
                    try:
                        Select_BulanMulai_I6.select_by_visible_text(BulanMulai_I6)
                        print("- Bulan Mulai I6: " + BulanMulai_I6)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Mulai I6: NSEE")
                        Log_Error.update({"Bulan Mulai I6":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Mulai I6: KeyError")
                    Log_Error.update({"Bulan Mulai I6":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunMulai_I6 = Isi_I6["tahunMulai"]
                    ID_TahunMulai_I6 = "16_startyear" + Row_I6
                    driver.find_element(By.ID, ID_TahunMulai_I6).send_keys(TahunMulai_I6)
                    print("- Tahun Mulai I6: " + TahunMulai_I6)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Mulai I6: KeyError")
                    Log_Error.update({"Tahun Mulai I6":"KeyError"})
                    ErrorKey += 1

                try:
                    ID_Anggota_I6 = "16_work" + Row_I6
                    Angggota_I6 = driver.find_element(By.ID, ID_Anggota_I6)
                    if Isi_I6["masihAnggota"] == True:
                        action.move_to_element_with_offset(Angggota_I6, 0, -20).click().perform()
                        print("- Masih Anggota I6: True")
                        Elemen += 1
                    else:
                        print("- Masih Anggota I6: False")
                        Elemen += 1
                        try:
                            BulanSelesai_I6 = Isi_I6["bulan"]
                            ID_BulanSelesai_I6 = "16_enddate" + Row_I6
                            Select_BulanSelesai_I6 = Select(driver.find_element(By.ID, ID_BulanSelesai_I6))
                            try:
                                Select_BulanSelesai_I6.select_by_visible_text(BulanSelesai_I6)
                                print("- Bulan Selesai I6: " + BulanSelesai_I6)
                                Elemen += 1
                            except NSEE:
                                print("- Bulan Selesai I6: NSEE")
                                Log_Error.update({"Bulan Selesai I6":"NSEE"})
                                NSEEn += 1
                        except KeyError:
                            print("- Bulan Selesai I6: KeyError")
                            Log_Error.update({"Bulan Selesai I6":"KeyError"})
                            ErrorKey += 1

                        try:
                            TahunSelesai_I6 = Isi_I6["tahun"]
                            ID_TahunSelesai_I6 = "16_endyear" + Row_I6
                            driver.find_element(By.ID, ID_TahunSelesai_I6).send_keys(TahunSelesai_I6)
                            print("- Tahun Selesai I6: " + TahunSelesai_I6)
                            Elemen += 1
                        except KeyError:
                            print("- Tahun Selesai I6: KeyError")
                            Log_Error.update({"Tahun Selesai I6":"KeyError"})
                            ErrorKey += 1
                except KeyError:
                    print("- Masih Anggota I6: KeyError")
                    Log_Error.update({"Masih Anggota I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Tingkat_I6 = Isi_I6["tingkatanMateriPendidikanManajemen"]
                    ID_Tingkat_I6 = "16_tingkat" + Row_I6
                    try:
                        Select_Tingkat_I6 = Select(driver.find_element(By.ID, ID_Tingkat_I6))
                        Select_Tingkat_I6.select_by_visible_text(Tingkat_I6)
                        print("- Tingkat I6: " + Tingkat_I6)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat I6: NSEE")
                        Log_Error.update({"Tingkat I6":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat I6: KeyError")
                    Log_Error.update({"Tingkat I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Jam_I6 = Isi_I6["jamPendidikanTeknikManajemen"]
                    ID_Jam_I6 = "16_jam" + Row_I6
                    try:
                        Select_Jam_I6 = Select(driver.find_element(By.ID, ID_Jam_I6))
                        Select_Jam_I6.select_by_visible_text(Jam_I6)
                        print("- Jam I6: " + Jam_I6)
                        Elemen += 1
                    except NSEE:
                        print("- Jam I6: NSEE")
                        Log_Error.update({"Jam I6":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jam I6: KeyError")
                    Log_Error.update({"Jam I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_I6 = Isi_I6["uraianSingkatAktifitas"]
                    ID_Uraian_I6 = "16_uraian" + Row_I6
                    Scroll_Uraian_I6 = driver.find_element(By.ID, ID_Uraian_I6)
                    action.move_to_element(Scroll_Uraian_I6).perform()
                    Scroll_Uraian_I6.send_keys(Uraian_I6)
                    print("- Uraian I6: " + Uraian_I6)
                    Elemen += 1
                except KeyError:
                    print("- Uraian I6: KeyError")
                    Log_Error.update({"Uraian I6":"KeyError"})
                    ErrorKey += 1

                #Kompetisi I6 
                ID_Komp_I6 = "16_komp" + Row_I6
                Scroll_Komp_I6 = driver.find_element(By.ID, ID_Komp_I6)
                action.move_to_element(Scroll_Komp_I6).perform()

                try:
                    Komp_W1_I6 = Isi_I6["klaimKompetensiWsatu"]
                    print("- Komp W1 I6: " + str(len(Komp_W1_I6)))
                    try:
                        for Komp_Value_W1_I6 in Komp_W1_I6:
                            Komp_Label_W1_I6 = Komp_Value_W1_I6[slice(5)]
                            Komp_Call_W1_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_W1_I6}")]/option[@value="{Komp_Value_W1_I6}."]'
                            Komp_Find_W1_I6 = driver.find_element(By.XPATH, Komp_Call_W1_I6)
                            action.move_to_element_with_offset(Komp_Find_W1_I6, 0, -15).click().perform()
                            print("-", Komp_Value_W1_I6)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W1 I6: NSEE")
                        Log_Error.update({"Komp W1 I6":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W1 I6: KeyError") 
                    Log_Error.update({"Komp W1 I6":"KeyError"})  
                    ErrorKey += 1        

                try:
                    Komp_W4_I6 = Isi_I6["klaimKompetensiWempat"]
                    print("- Komp W4 I6: " + str(len(Komp_W4_I6)))
                    try:
                        for Komp_Value_W4_I6 in Komp_W4_I6:
                            Komp_Label_W4_I6 = Komp_Value_W4_I6[slice(5)]
                            Komp_Call_W4_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_W4_I6}")]/option[@value="{Komp_Value_W4_I6}."]'
                            Komp_Find_W4_I6 = driver.find_element(By.XPATH, Komp_Call_W4_I6)
                            action.move_to_element_with_offset(Komp_Find_W4_I6, 0, -15).click().perform()
                            print("-", Komp_Value_W4_I6) 
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 I6: NSEE")
                        Log_Error.update({"Komp W4 I6":"NSEE"}) 
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 I6: KeyError") 
                    Log_Error.update({"Komp W4 I6":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P10_I6 = Isi_I6["klaimKompetensiPsepuluh"]
                    print("- Komp P10 I6: " + str(len(Komp_P10_I6)))
                    try:
                        for Komp_Value_P10_I6 in Komp_P10_I6:
                            Komp_Label_P10_I6 = Komp_Value_P10_I6[slice(5)]
                            Komp_Call_P10_I6 = f'//*[@id="{ID_Komp_I6}"]//optgroup[contains(@label, "{Komp_Label_P10_I6}")]/option[@value="{Komp_Value_P10_I6}."]'
                            Komp_Find_P10_I6 = driver.find_element(By.XPATH, Komp_Call_P10_I6)
                            action.move_to_element_with_offset(Komp_Find_P10_I6, 0, -15).click().perform()
                            print("-", Komp_Value_P10_I6)  
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P10 I6: NSEE")
                        Log_Error.update({"Komp P10 I6":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P10 I6: KeyError") 
                    Log_Error.update({"Komp P10 I6":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_I6 += 1
                DB_Count_I6 += 1
                ID_Count_I6 += 1
                print("Row " + Row_I6 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN II1
        def FormII1():
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
            DB_Count_II1 = 0

            #Database
            Dict_II1 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_ii_satu':1})
            List_II1 = Dict_II1["form_ii_satu"]
            n_II1 = len(List_II1)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_II1) + "\n")

            print("Start from Row: " + str(ID_Count_II1))
            print("Row Ditambah: " + str(n_II1) + "\n")

            while Counter_II1 <= n_II1:
                #add row
                TambahII1 = driver.find_element(By.XPATH, '//button[@onclick="add21(\'ref\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahII1)
                action.move_to_element(TambahII1).perform()
                TambahII1.send_keys(Keys.ENTER)

                Row_II1 = str(ID_Count_II1)

                #Document II1
                Isi_II1 = List_II1[DB_Count_II1]
                print("Counter Row: " + str(Counter_II1))
                print("Key Document: " + Isi_II1["key"] + "\n")

                try:
                    Nama_II1 = Isi_II1["namaKualifikasiEtik"]          
                    ID_Nama_II1 = "21_nama" + Row_II1
                    driver.find_element(By.ID, ID_Nama_II1).send_keys(Nama_II1)
                    print("- Nama II1: " + Nama_II1)
                    Elemen += 1
                except KeyError:
                    print("- Nama II1: KeyError")
                    Log_Error.update({"Nama II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Lembaga_II1 = Isi_II1["lembaga"] 
                    ID_Lembaga_II1 = "21_lembaga" + Row_II1
                    driver.find_element(By.ID, ID_Lembaga_II1).send_keys(Lembaga_II1)
                    print("- Lembaga II1: " + Lembaga_II1)
                    Elemen += 1
                except KeyError:
                    print("- Lembaga II1: KeyError")
                    Log_Error.update({"Lembaga II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Alamat_II1 = Isi_II1["alamat"] 
                    ID_Alamat_II1 = "21_alamat" + Row_II1
                    driver.find_element(By.ID, ID_Alamat_II1).send_keys(Alamat_II1)
                    print("- Alamat II1: " + Alamat_II1)
                    Elemen += 1
                except KeyError:
                    print("- Alamat II1: KeyError")
                    Log_Error.update({"Alamat II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_II1 = Isi_II1["kota"] 
                    ID_Kota_II1 = "21_kota" + Row_II1
                    driver.find_element(By.ID, ID_Kota_II1).send_keys(Kota_II1)
                    print("- Kota II1: " + Kota_II1)
                    Elemen += 1
                except KeyError:
                    print("- Kota II1: KeyError")
                    Log_Error.update({"Kota II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_II1 = Isi_II1["provinsi"] 
                    ID_Provinsi_II1 = "21_provinsi" + Row_II1
                    driver.find_element(By.ID, ID_Provinsi_II1).send_keys(Provinsi_II1)
                    print("- Provinsi II1: " + Provinsi_II1)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi II1: KeyError")
                    Log_Error.update({"Provinsi II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_II1 = Isi_II1["negara"]     
                    ID_Negara_II1 = "21_negara" + Row_II1
                    driver.find_element(By.ID, ID_Negara_II1).send_keys(Negara_II1)
                    print("- Negara II1: " + Negara_II1)
                    Elemen += 1
                except KeyError:
                    print("- Negara II1: KeyError")
                    Log_Error.update({"Negara II1":"KeyError"})
                    ErrorKey += 1
                
                try:
                    NoTelp_II1 = Isi_II1["noTelp"] 
                    ID_NoTelp_II1 = "21_notelp" + Row_II1
                    driver.find_element(By.ID, ID_NoTelp_II1).send_keys(NoTelp_II1)
                    print("- NoTelp II1: " + NoTelp_II1)
                    Elemen += 1
                except KeyError:
                    print("- NoTelp II1: KeyError")
                    Log_Error.update({"NoTelp II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Email_II1 = Isi_II1["email"] 
                    ID_Email_II1 = "21_email" + Row_II1
                    Scroll_Email_II1 = driver.find_element(By.ID, ID_Email_II1)
                    action.move_to_element(Scroll_Email_II1).perform()
                    Scroll_Email_II1.send_keys(Email_II1)                    
                    print("- Email II1: " + Email_II1)
                    Elemen += 1
                except KeyError:
                    print("- Email II1: KeyError")
                    Log_Error.update({"Email II1":"KeyError"})
                    ErrorKey += 1

                try:
                    Hubungan_II1 = Isi_II1["hubungan"] 
                    ID_Hubungan_II1 = "21_hubungan" + Row_II1
                    Scroll_Hubungan_II1 = driver.find_element(By.ID, ID_Hubungan_II1)
                    action.move_to_element(Scroll_Hubungan_II1).perform() 
                    Select_Hubungan_II1 = Select(Scroll_Hubungan_II1)
                    try:
                        Select_Hubungan_II1.select_by_visible_text(Hubungan_II1)
                        print("- Hubungan II1: " + Hubungan_II1)
                        Elemen += 1
                    except NSEE:
                        print("- Hubungan II1: NSEE")
                        Log_Error.update({"Hubungan II1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Hubungan II1: KeyError")
                    Log_Error.update({"Hubungan II1":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_II1 += 1
                ID_Count_II1 += 1
                print("Row " + Row_II1 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN II2
        def FormII2():
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
            DB_Count_II2 = 0

            #Database
            Dict_II2 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_ii_dua':1})
            List_II2 = Dict_II2["form_ii_dua"]
            n_II2 = len(List_II2)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_II2) + "\n")

            print("Start from Row: " + str(ID_Count_II2))
            print("Row Ditambah: " + str(n_II2) + "\n")

            while Counter_II2 <= n_II2:
                #add row
                TambahII2 = driver.find_element(By.XPATH, '//button[@onclick="add22(\'eti\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahII2)
                action.move_to_element(TambahII2).perform()
                TambahII2.send_keys(Keys.ENTER)

                Row_II2 = str(ID_Count_II2)

                #Document II2
                Isi_II2 = List_II2[DB_Count_II2]
                print("Counter Row: " + str(Counter_II2))
                print("Key Document: " + Isi_II2["key"] + "\n")

                try:
                    Uraian_II2 = Isi_II2["pendapatEtik"]  
                    ID_Uraian_II2 = "22_uraian" + Row_II2
                    driver.find_element(By.ID, ID_Uraian_II2).send_keys(Uraian_II2)
                    print("- Uraian II2: " + Uraian_II2)
                    Elemen += 1
                except KeyError:
                    print("- Uraian II2: KeyError")
                    Log_Error.update({"Uraian II2":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_II2 += 1
                ID_Count_II2 += 1
                print("Row " + Row_II2 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN III
        def FormIII():
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
            DB_Count_III = 0

            #Database
            Dict_III = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_iii':1})
            List_III = Dict_III["form_iii"]
            n_III = len(List_III)
        
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_III) + "\n")

            print("Start from Row: " + str(ID_Count_III))
            print("Row Ditambah: " + str(n_III) + "\n")

            while Counter_III <= n_III:
                #add row
                TambahIII = driver.find_element(By.XPATH, '//button[@onclick="add3(\'kup\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahIII)
                action.move_to_element(TambahIII).perform()
                TambahIII.send_keys(Keys.ENTER)

                Row_III = str(ID_Count_III)

                #Document III
                Isi_III = List_III[DB_Count_III]
                print("Counter Row: " + str(Counter_III))
                print("Key Document: " + Isi_III["key"] + "\n")

                try:
                    BulanMulai_III = Isi_III["bulanMulai"]  
                    ID_BulanMulai_III = "3_startdate" + Row_III
                    Select_BulanMulai_III = Select(driver.find_element(By.ID, ID_BulanMulai_III))
                    try:
                        Select_BulanMulai_III.select_by_visible_text(BulanMulai_III)
                        print("- Bulan Mulai III: " + BulanMulai_III)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Mulai III: NSEE")
                        Log_Error.update({"Bulan Mulai III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Mulai III: KeyError")
                    Log_Error.update({"Bulan Mulai III":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunMulai_III = Isi_III["tahunMulai"]  
                    ID_TahunMulai_III = "3_startyear" + Row_III
                    driver.find_element(By.ID, ID_TahunMulai_III).send_keys(TahunMulai_III)
                    print("- Tahun Mulai III: " + TahunMulai_III)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Mulai III: KeyError")
                    Log_Error.update({"Tahu nMulai III":"KeyError"})
                    ErrorKey += 1

                try:
                    ID_Anggota_III = "3_work" + Row_III
                    Angggota_III = driver.find_element(By.ID, ID_Anggota_III)
                    if Isi_III["masihdiInstansi"] == True:
                        action.move_to_element_with_offset(Angggota_III, 0, -20).click().perform()
                        print("- Masih Anggota III: True")
                        Elemen += 1
                    else:
                        print("- Masih Anggota III: False")
                        Elemen += 1
                        try:
                            BulanSelesai_III = Isi_III["bulanBerakhir"]  
                            ID_BulanSelesai_III = "3_enddate" + Row_III
                            Select_BulanSelesai_III = Select(driver.find_element(By.ID, ID_BulanSelesai_III))
                            try:
                                Select_BulanSelesai_III.select_by_visible_text(BulanSelesai_III)
                                print("- BulanSelesai III: " + BulanSelesai_III)
                                Elemen += 1
                            except NSEE:
                                print("- BulanSelesai III: NSEE")
                                Log_Error.update({"Bulan Selesai III":"NSEE"})
                                NSEEn += 1
                        except KeyError:
                            print("- BulanSelesai III: KeyError") 
                            Log_Error.update({"Bulan Selesai III":"KeyError"})  
                            ErrorKey += 1 

                        try:
                            TahunSelesai_III = Isi_III["tahunBerakhir"]  
                            ID_TahunSelesai_III = "3_endyear" + Row_III
                            driver.find_element(By.ID, ID_TahunSelesai_III).send_keys(TahunSelesai_III)
                            print("- Tahun Selesai III: " + TahunSelesai_III)
                            Elemen += 1
                        except KeyError:
                            print("- Tahun Selesai III: KeyError")
                            Log_Error.update({"Tahun Selesai III":"KeyError"})
                            ErrorKey += 1
                except KeyError:
                    print("- Masih Anggota III: KeyError")
                    Log_Error.update({"Masih Anggota III":"KeyError"})
                    ErrorKey += 1

                try:
                    Instansi_III = Isi_III["namaInstansi"]  
                    ID_Instansi_III = "3_instansi" + Row_III
                    driver.find_element(By.ID, ID_Instansi_III).send_keys(Instansi_III)
                    print("- Instansi III: " + Instansi_III)
                    Elemen += 1
                except KeyError:
                    print("- Instansi III: KeyError")
                    Log_Error.update({"Instansi III":"KeyError"})
                    ErrorKey += 1

                try:
                    Jabatan_III = Isi_III["jabatandiInstansi"]  
                    ID_Jabatan_III = "3_title" + Row_III
                    driver.find_element(By.ID, ID_Jabatan_III).send_keys(Jabatan_III)
                    print("- Jabatan III: " + Jabatan_III)
                    Elemen += 1
                except KeyError:
                    print("- Jabatan III: KeyError")
                    Log_Error.update({"Jabatan III":"KeyError"})
                    ErrorKey += 1

                try:        
                    Proyek_III = Isi_III["namaProyek"]  
                    ID_Proyek_III = "3_namaproyek" + Row_III
                    driver.find_element(By.ID, ID_Proyek_III).send_keys(Proyek_III)
                    print("- Proyek III: " + Proyek_III)
                    Elemen += 1
                except KeyError:
                    print("- Proyek III: KeyError")
                    Log_Error.update({"Proyek III":"KeyError"})
                    ErrorKey += 1

                try:
                    Penugas_III = Isi_III["pemberiTugas"]  
                    ID_Penugas_III = "3_pemberitugas" + Row_III
                    driver.find_element(By.ID, ID_Penugas_III).send_keys(Penugas_III)
                    print("- Penugas III: " + Penugas_III)
                    Elemen += 1
                except KeyError:
                    print("- Penugas III: KeyError")
                    Log_Error.update({"Penugas III":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_III = Isi_III["kotaProyek"]  
                    ID_Kota_III = "3_location" + Row_III
                    driver.find_element(By.ID, ID_Kota_III).send_keys(Kota_III)
                    print("- Kota III: " + Kota_III)
                    Elemen += 1
                except KeyError:
                    print("- Kota III: KeyError")
                    Log_Error.update({"Kota III":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_III = Isi_III["provinsiProyek"]  
                    ID_Provinsi_III = "3_provinsi" + Row_III
                    driver.find_element(By.ID, ID_Provinsi_III).send_keys(Provinsi_III)
                    print("- Provinsi III: " +  Provinsi_III)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi III: KeyError")
                    Log_Error.update({"Provinsi III":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_III = Isi_III["negaraProyek"]  
                    ID_Negara_III = "3_negara" + Row_III
                    driver.find_element(By.ID, ID_Negara_III).send_keys(Negara_III)
                    print("- Negara III : " + Negara_III)
                    Elemen += 1
                except KeyError:
                    print("- Negara III: KeyError")
                    Log_Error.update({"Negara III":"KeyError"})
                    ErrorKey += 1

                try:
                    Periode_III = Isi_III["durasi"]  
                    ID_Periode_III = "3_periode" + Row_III
                    Select_Periode_III = Select(driver.find_element(By.ID, ID_Periode_III))
                    try:
                        Select_Periode_III.select_by_visible_text(Periode_III)
                        print("- Periode III: " + Periode_III)
                        Elemen += 1
                    except NSEE:
                        print("- Periode III: NSEE")
                        Log_Error.update({"Periode III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Periode III: KeyError")
                    Log_Error.update({"Periode III":"KeyError"})
                    ErrorKey += 1

                try:        
                    Posisi_III = Isi_III["jabatan"]  
                    ID_Posisi_III = "3_posisi" + Row_III
                    Scroll_Posisi_III = driver.find_element(By.ID, ID_Posisi_III)
                    action.move_to_element(Scroll_Posisi_III).perform() 
                    Select_Posisi_III = Select(Scroll_Posisi_III)
                    try:
                        Select_Posisi_III.select_by_visible_text(Posisi_III)
                        print("- Posisi III: " + Posisi_III)
                        Elemen += 1
                    except NSEE:
                        print("- Posisi III: NSEE")
                        Log_Error.update({"Posisi III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Posisi III: KeyError")
                    Log_Error.update({"Posisi III":"KeyError"})
                    ErrorKey += 1

                try:
                    Nilai_III = Isi_III["nilaiProyek"]  
                    ID_Nilai_III = "3_nilaipry" + Row_III
                    Scroll_Nilai_III = driver.find_element(By.ID, ID_Nilai_III)
                    action.move_to_element(Scroll_Nilai_III).perform()
                    Scroll_Nilai_III.send_keys(Nilai_III)
                    print("- Nilai III: " + Nilai_III)
                    Elemen += 1
                except KeyError:
                    print("- Nilai III: KeyError")
                    Log_Error.update({"Nilai III":"KeyError"})
                    ErrorKey += 1

                try:
                    TanggungJawab_III = Isi_III["nilaiTanggungJawab"]  
                    ID_TanggungJawab_III = "3_nilaijasa" + Row_III
                    Scroll_TanggungJawab_III = driver.find_element(By.ID, ID_TanggungJawab_III)
                    action.move_to_element(Scroll_TanggungJawab_III).perform()
                    Scroll_TanggungJawab_III.send_keys(TanggungJawab_III)
                    print("- Tanggung Jawab III: " + TanggungJawab_III)
                    Elemen += 1
                except KeyError:
                    print("- Tanggung Jawab III: KeyError")
                    Log_Error.update({"Tanggung Jawab III":"KeyError"})
                    ErrorKey += 1
                
                try:
                    SDM_III = Isi_III["sdmyangTerlibat"]  
                    ID_SDM_III = "3_nilaisdm" + Row_III
                    Scroll_SDM_III = driver.find_element(By.ID, ID_SDM_III)
                    action.move_to_element(Scroll_SDM_III).perform()
                    Select_SDM_III = Select(Scroll_SDM_III)
                    try:
                        Select_SDM_III.select_by_visible_text(SDM_III)
                        print("- SDM III: " + SDM_III)
                        Elemen += 1
                    except NSEE:
                        print("- SDM III: NSEE")
                        Log_Error.update({"SDM III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- SDM III: KeyError")
                    Log_Error.update({"SDM III":"KeyError"})
                    ErrorKey += 1

                try:
                    TingkatSulit_III = Isi_III["tingkatKesulitan"]  
                    ID_TingkatSulit_III = "3_nilaisulit" + Row_III
                    Scroll_TingkatSulit_III = driver.find_element(By.ID, ID_TingkatSulit_III)
                    action.move_to_element(Scroll_TingkatSulit_III).perform()
                    Select_TingkatSulit_III = Select(Scroll_TingkatSulit_III)
                    try:
                        Select_TingkatSulit_III.select_by_visible_text(TingkatSulit_III)
                        print("- Tingkat Sulit III: " + TingkatSulit_III)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat Sulit III: NSEE")
                        Log_Error.update({"Tingkat Sulit III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat Sulit III: KeyError")
                    Log_Error.update({"Tingkat Sulit III":"KeyError"})
                    ErrorKey += 1

                try:
                    NilaiProyek_III = Isi_III["skalaProyek"]  
                    ID_NilaiProyek_III = "3_nilaiproyek" + Row_III
                    Scroll_NilaiProyek_III = driver.find_element(By.ID, ID_NilaiProyek_III)
                    action.move_to_element(Scroll_NilaiProyek_III).perform()
                    Select_NilaiProyek_III = Select(Scroll_NilaiProyek_III)
                    try:
                        Select_NilaiProyek_III.select_by_visible_text(NilaiProyek_III)
                        print("- Nilai Proyek III: " + NilaiProyek_III)
                        Elemen += 1
                    except NSEE:
                        print("- Nilai Proyek III: NSEE")
                        Log_Error.update({"Nilai Proyek III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Nilai Proyek III: KeyError")
                    Log_Error.update({"Nilai Proyek III":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_III = Isi_III["uraianSingkatNSPK"]
                    ID_Uraian_III = "3_uraian" + Row_III
                    Scroll_Uraian_III = driver.find_element(By.ID, ID_Uraian_III)
                    action.move_to_element(Scroll_Uraian_III).perform()
                    Scroll_Uraian_III.send_keys(Uraian_III)
                    print("- Uraian III: " + Uraian_III)
                    Elemen += 1
                except KeyError:
                    print("- Uraian III: KeyError")
                    Log_Error.update({"Uraian III":"KeyError"})
                    ErrorKey += 1

                #Kompetisi III 
                ID_Komp_III = "3_komp" + Row_III
                Scroll_Komp_III = driver.find_element(By.ID, ID_Komp_III)
                action.move_to_element(Scroll_Komp_III).perform()
                
                try:
                    Komp_W2_III = Isi_III["klaimKompetensiWdua"]
                    print("- Komp W2 III: " + str(len(Komp_W2_III)))
                    try:
                        for Komp_Value_W2_III in Komp_W2_III:
                            Komp_Label_W2_III = Komp_Value_W2_III[slice(5)]
                            Komp_Call_W2_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_W2_III}")]/option[@value="{Komp_Value_W2_III}."]'
                            Komp_Find_W2_III = driver.find_element(By.XPATH, Komp_Call_W2_III)
                            action.move_to_element_with_offset(Komp_Find_W2_III, 0, -15).click().perform()
                            print("-", Komp_Value_W2_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W2 III: NSEE")
                        Log_Error.update({"Komp W2 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W2 III: KeyError") 
                    Log_Error.update({"Komp W2 III":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Komp_W3_III = Isi_III["klaimKompetensiWtiga"]
                    print("- Komp W3 III: " + str(len(Komp_W3_III)))
                    try:
                        for Komp_Value_W3_III in Komp_W3_III:
                            Komp_Label_W3_III = Komp_Value_W3_III[slice(5)]
                            Komp_Call_W3_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_W3_III}")]/option[@value="{Komp_Value_W3_III}."]'
                            Komp_Find_W3_III = driver.find_element(By.XPATH, Komp_Call_W3_III)
                            action.move_to_element_with_offset(Komp_Find_W3_III, 0, -15).click().perform()
                            print("-", Komp_Value_W3_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W3 III: NSEE")
                        Log_Error.update({"Komp W3 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W3 III: KeyError") 
                    Log_Error.update({"Komp W3 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_W4_III = Isi_III["klaimKompetensiWempat"]
                    print("- Komp W4 III: " + str(len(Komp_W4_III)))
                    try:
                        for Komp_Value_W4_III in Komp_W4_III:
                            Komp_Label_W4_III = Komp_Value_W4_III[slice(5)]
                            Komp_Call_W4_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_W4_III}")]/option[@value="{Komp_Value_W4_III}."]'
                            Komp_Find_W4_III = driver.find_element(By.XPATH, Komp_Call_W4_III)
                            action.move_to_element_with_offset(Komp_Find_W4_III, 0, -15).click().perform()
                            print("-", Komp_Value_W4_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 III: NSEE")
                        Log_Error.update({"Komp W4 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 III: KeyError") 
                    Log_Error.update({"Komp W4 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P6_III = Isi_III["klaimKompetensiPenam"]
                    print("- Komp P6 III: " + str(len(Komp_P6_III)))
                    try:
                        for Komp_Value_P6_III in Komp_P6_III:
                            Komp_Label_P6_III = Komp_Value_P6_III[slice(5)]
                            Komp_Call_P6_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P6_III}")]/option[@value="{Komp_Value_P6_III}."]'
                            Komp_Find_P6_III = driver.find_element(By.XPATH, Komp_Call_P6_III)
                            action.move_to_element_with_offset(Komp_Find_P6_III, 0, -15).click().perform()
                            print("-", Komp_Value_P6_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P6 III: NSEE")
                        Log_Error.update({"Komp P6 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P6 III: KeyError") 
                    Log_Error.update({"Komp P6 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P7_III = Isi_III["klaimKompetensiPtujuh"]
                    print("- Komp P7 III: " + str(len(Komp_P7_III)))
                    try:
                        for Komp_Value_P7_III in Komp_P7_III:
                            Komp_Label_P7_III = Komp_Value_P7_III[slice(5)]
                            Komp_Call_P7_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P7_III}")]/option[@value="{Komp_Value_P7_III}."]'
                            Komp_Find_P7_III = driver.find_element(By.XPATH, Komp_Call_P7_III)
                            action.move_to_element_with_offset(Komp_Find_P7_III, 0, -15).click().perform()
                            print("-", Komp_Value_P7_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P7 III: NSEE")
                        Log_Error.update({"Komp P7 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P7 III: KeyError") 
                    Log_Error.update({"Komp P7 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P8_III = Isi_III["klaimKompetensiPdelapan"]
                    print("- Komp P8 III: " + str(len(Komp_P8_III)))
                    try:
                        for Komp_Value_P8_III in Komp_P8_III:
                            Komp_Label_P8_III = Komp_Value_P8_III[slice(5)]
                            Komp_Call_P8_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P8_III}")]/option[@value="{Komp_Value_P8_III}."]'
                            Komp_Find_P8_III = driver.find_element(By.XPATH, Komp_Call_P8_III)
                            action.move_to_element_with_offset(Komp_Find_P8_III, 0, -15).click().perform()
                            print("-", Komp_Value_P8_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P8 III: NSEE")
                        Log_Error.update({"Komp P8 III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P8 III: KeyError") 
                    Log_Error.update({"Komp P8 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P9_III = Isi_III["klaimKompetensiPsembilan"]
                    print("- Komp P9 III: " + str(len(Komp_P9_III)))
                    try:
                        for Komp_Value_P9_III in Komp_P9_III:
                            Komp_Label_P9_III = Komp_Value_P9_III[slice(5)]
                            Komp_Call_P9_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P9_III}")]/option[@value="{Komp_Value_P9_III}."]'
                            Komp_Find_P9_III = driver.find_element(By.XPATH, Komp_Call_P9_III)
                            action.move_to_element_with_offset(Komp_Find_P9_III, 0, -15).click().perform()
                            print("-", Komp_Value_P9_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P9 III: NSEE")
                        Log_Error.update({"Komp P9  III":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P9 III: KeyError") 
                    Log_Error.update({"Komp P9 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P10_III = Isi_III["klaimKompetensiPsepuluh"]
                    print("- Komp P10 III: " + str(len(Komp_P10_III)))
                    try:
                        for Komp_Value_P10_III in Komp_P10_III:
                            Komp_Label_P10_III = Komp_Value_P10_III[slice(5)]
                            Komp_Call_P10_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P10_III}")]/option[@value="{Komp_Value_P10_III}."]'
                            Komp_Find_P10_III = driver.find_element(By.XPATH, Komp_Call_P10_III)
                            action.move_to_element_with_offset(Komp_Find_P10_III, 0, -15).click().perform()
                            print("-", Komp_Value_P10_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P10 III: NSEE")  
                        Log_Error.update({"Komp P10 III":"NSEE"})  
                        NSEEn += 1
                except KeyError:
                    print("- Komp P10 III: KeyError") 
                    Log_Error.update({"Komp P10 III":"KeyError"})
                    ErrorKey += 1

                try:
                    Komp_P11_III = Isi_III["klaimKompetensiPsebelas"]
                    print("- Komp P11 III: " + str(len(Komp_P11_III)))
                    try:
                        for Komp_Value_P11_III in Komp_P11_III:
                            Komp_Label_P11_III = Komp_Value_P11_III[slice(5)]
                            Komp_Call_P11_III = f'//*[@id="{ID_Komp_III}"]//optgroup[contains(@label, "{Komp_Label_P11_III}")]/option[@value="{Komp_Value_P11_III}."]'
                            Komp_Find_P11_III = driver.find_element(By.XPATH, Komp_Call_P11_III)
                            action.move_to_element_with_offset(Komp_Find_P11_III, 0, -15).click().perform()
                            print("-", Komp_Value_P11_III)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P11 III: NSEE")
                        Log_Error.update({"Komp P11 III":"NSEEE"})
                except KeyError:
                    print("- Komp P11 III: KeyError") 
                    Log_Error.update({"Komp P11 III":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_III += 1
                ID_Count_III += 1
                print("Row " + Row_III + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN IV
        def FormIV():
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
            DB_Count_IV = 0

            #Database
            Dict_IV = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_iv':1})
            List_IV = Dict_IV["form_iv"]
            n_IV = len(List_IV)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_IV) + "\n")
            
            print("Start from Row: " + str(ID_Count_IV))
            print("Row Ditambah: " + str(n_IV) + "\n")

            while Counter_IV <= n_IV:
                #add row
                TambahIV = driver.find_element(By.XPATH, '//button[@onclick="add4(\'man\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahIV)
                action.move_to_element(TambahIV).perform()
                TambahIV.send_keys(Keys.ENTER)

                Row_IV = str(ID_Count_IV)

                #Document IV
                Isi_IV = List_IV[DB_Count_IV]
                print("Counter Row: " + str(Counter_IV))
                print("Key Document: " + Isi_IV["key"] + "\n")

                try:
                    Instansi_IV = Isi_IV["namaPerguruan"]  
                    ID_Instansi_IV = "4_instansi" + Row_IV
                    driver.find_element(By.ID, ID_Instansi_IV).send_keys(Instansi_IV)
                    print("- Instansi IV: " + Instansi_IV)
                    Elemen += 1
                except KeyError:
                    print("- Instansi IV: KeyError")
                    Log_Error.update({"Instansi IV":"KeyError"})
                    ErrorKey += 1

                try:
                    NamaProyek_IV = Isi_IV["namaMataAjaran"]  
                    ID_NamaProyek_IV = "4_namaproyek" + Row_IV
                    driver.find_element(By.ID, ID_NamaProyek_IV).send_keys(NamaProyek_IV)
                    print("- Nama Proyek IV: " + NamaProyek_IV)
                    Elemen += 1
                except KeyError:
                    print("- Nama Proyek IV: KeyError")
                    Log_Error.update({"Nama Proyek IV":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Kota_IV = Isi_IV["kota"]  
                    ID_Kota_IV = "4_location" + Row_IV
                    driver.find_element(By.ID, ID_Kota_IV).send_keys(Kota_IV)
                    print("- Kota IV: " + Kota_IV)
                    Elemen += 1
                except KeyError:
                    print("- Kota IV: KeyError")
                    Log_Error.update({"Kota IV":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_IV = Isi_IV["provinsi"]  
                    ID_Provinsi_IV = "4_provinsi" + Row_IV
                    driver.find_element(By.ID, ID_Provinsi_IV).send_keys(Provinsi_IV)
                    print("- Provinsi IV: " + Provinsi_IV)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi IV: KeyError")
                    Log_Error.update({"Provinsi IV":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_IV = Isi_IV["negara"]  
                    ID_Negara_IV = "4_negara" + Row_IV
                    driver.find_element(By.ID, ID_Negara_IV).send_keys(Negara_IV)
                    print("- Negara IV: " + Negara_IV)
                    Elemen += 1
                except KeyError:
                    print("- Negara IV: KeyError")
                    Log_Error.update({"Negara IV":"KeyError"})
                    ErrorKey += 1

                try:
                    Periode_IV = Isi_IV["perioda"]  
                    ID_Periode_IV = "4_periode" + Row_IV
                    Select_Periode_IV = Select(driver.find_element(By.ID, ID_Periode_IV))
                    try:
                        Select_Periode_IV.select_by_visible_text(Periode_IV)
                        print("- Periode IV: " + Periode_IV)
                        Elemen += 1
                    except NSEE:
                        print("- Periode IV: NSEE")
                        Log_Error.update({"Periode IV":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Periode IV: KeyError")
                    Log_Error.update({"Periode IV":"KeyError"})
                    ErrorKey += 1

                try:
                    Posisi_IV = Isi_IV["jabatandiPerguruan"]  
                    ID_Posisi_IV = "4_posisi" + Row_IV
                    Scroll_Posisi_IV = driver.find_element(By.ID, ID_Posisi_IV)
                    action.move_to_element(Scroll_Posisi_IV).perform()
                    Select_Posisi_IV = Select(Scroll_Posisi_IV)
                    try:
                        Select_Posisi_IV.select_by_visible_text(Posisi_IV)
                        print("- Posisi IV: " + Posisi_IV)
                        Elemen += 1
                    except NSEE:
                        print("- Posisi IV: NSEE")
                        Log_Error.update({"Posisi IV":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Posisi IV: KeyError")
                    Log_Error.update({"Posisi IV":"KeyError"})
                    ErrorKey += 1

                try:
                    JumlahSKS_IV = Isi_IV["jumlahWaktu"]  
                    ID_JumlahSKS_IV = "4_jumlahsks" + Row_IV
                    Scroll_JumlahSKS_IV = driver.find_element(By.ID, ID_JumlahSKS_IV)
                    action.move_to_element(Scroll_JumlahSKS_IV).perform()
                    Select_JumlahSKS_IV = Select(Scroll_JumlahSKS_IV)
                    try:
                        Select_JumlahSKS_IV.select_by_visible_text(JumlahSKS_IV)
                        print("- Jumlah SKS IV: " + JumlahSKS_IV)
                        Elemen += 1
                    except NSEE:
                        print("- Jumlah SKS IV: NSEE")
                        Log_Error.update({"Jumlah SKS IV":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jumlah SKS IV: KeyError")
                    Log_Error.update({"Jumlah SKS IV":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_IV = Isi_IV["uraianSingkatAktifitas"]  
                    ID_Uraian_IV = "4_uraian" + Row_IV
                    Scroll_Uraian_IV = driver.find_element(By.ID, ID_Uraian_IV)
                    action.move_to_element(Scroll_Uraian_IV).perform()
                    Scroll_Uraian_IV.send_keys(Uraian_IV)
                    print("- Uraian IV: " + Uraian_IV)
                    Elemen += 1
                except KeyError:
                    print("- Uraian IV: KeyError")
                    Log_Error.update({"Uraian IV":"KeyError"})
                    ErrorKey += 1

                #Kompetisi IV 
                ID_Komp_IV = "4_komp" + Row_IV
                Scroll_Komp_IV = driver.find_element(By.ID, ID_Komp_IV)
                action.move_to_element(Scroll_Komp_IV).perform()
                
                try:
                    Komp_P5_IV = Isi_IV["klaimKompetensiPlima"]
                    print("- Komp P5 IV: " + str(len(Komp_P5_IV)))
                    try:
                        for Komp_Value_P5_IV in Komp_P5_IV:
                            Komp_Label_P5_IV = Komp_Value_P5_IV[slice(5)]
                            Komp_Call_P5_IV = f'//*[@id="{ID_Komp_IV}"]//optgroup[contains(@label, "{Komp_Label_P5_IV}")]/option[@value="{Komp_Value_P5_IV}."]'
                            Komp_Find_P5_IV = driver.find_element(By.XPATH, Komp_Call_P5_IV)
                            action.move_to_element_with_offset(Komp_Find_P5_IV, 0, -15).click().perform()
                            print("-", Komp_Value_P5_IV)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P5 IV: NSEE")
                        Log_Error.update({"Komp P5 IV":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P5 IV: KeyError") 
                    Log_Error.update({"Komp P5 IV":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_IV += 1
                ID_Count_IV += 1
                print("Row " + Row_IV + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN V1
        def FormV1():
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
            DB_Count_V1 = 0

            #Database
            Dict_V1 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_v_satu':1})
            List_V1 = Dict_V1["form_v_satu"]
            n_V1 = len(List_V1)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_V1) + "\n")
            
            print("Start from Row: " + str(ID_Count_V1))
            print("Row Ditambah: " + str(n_V1) + "\n")

            while Counter_V1 <= n_V1:
                #add row
                TambahV1 = driver.find_element(By.XPATH, '//button[@onclick="add51(\'pub\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahV1)
                action.move_to_element(TambahV1).perform()
                TambahV1.send_keys(Keys.ENTER)

                Row_V1 = str(ID_Count_V1)

                #Document V1
                Isi_V1 = List_V1[DB_Count_V1]
                print("Counter Row: " + str(Counter_V1))
                print("Key Document: " + Isi_V1["key"] + "\n")

                try:
                    Judul_V1 = Isi_V1["judulKaryaTulis"]  
                    ID_Judul_V1 = "51_nama" + Row_V1
                    driver.find_element(By.ID, ID_Judul_V1).send_keys(Judul_V1)
                    print("- Judul V1: " + Judul_V1)
                    Elemen += 1
                except KeyError:
                    print("- Judul V1: KeyError")
                    Log_Error.update({"Judul V1":"KeyError"})
                    ErrorKey += 1

                try:
                    Media_V1 = Isi_V1["namaMedia"]  
                    ID_Media_V1 = "51_media" + Row_V1
                    driver.find_element(By.ID, ID_Media_V1).send_keys(Media_V1)
                    print("- Media V1: " + Media_V1)
                    Elemen += 1
                except KeyError:
                    print("- Media V1: KeyError")
                    Log_Error.update({"Media V1":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_V1 = Isi_V1["kota"]  
                    ID_Kota_V1 = "51_location" + Row_V1
                    driver.find_element(By.ID, ID_Kota_V1).send_keys(Kota_V1)
                    print("- Kota V1: " + Kota_V1)
                    Elemen += 1
                except KeyError:
                    print("- Kota V1: KeyError")
                    Log_Error.update({"Kota V1":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_V1 = Isi_V1["provinsi"]  
                    ID_Provinsi_V1 = "51_provinsi" + Row_V1
                    driver.find_element(By.ID, ID_Provinsi_V1).send_keys(Provinsi_V1)
                    print("- Provinsi V1: " + Provinsi_V1)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi V1: KeyError")
                    Log_Error.update({"Provinsi V1":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_V1 = Isi_V1["negara"]  
                    ID_Negara_V1 = "51_negara" + Row_V1
                    driver.find_element(By.ID, ID_Negara_V1).send_keys(Negara_V1)
                    print("- Negara V1: " + Negara_V1)
                    Elemen += 1
                except KeyError:
                    print("- Negara V1: KeyError")
                    Log_Error.update({"Negara V1":"KeyError"})
                    ErrorKey += 1

                try:
                    BulanPublikasi_V1 = Isi_V1["bulanTerbit"]  
                    ID_BulanPublikasi_V1 = "51_startdate" + Row_V1
                    Select_BulanPublikasi_V1 = Select(driver.find_element(By.ID, ID_BulanPublikasi_V1))
                    try:
                        Select_BulanPublikasi_V1.select_by_visible_text(BulanPublikasi_V1)
                        print("- Bulan Publikasi V1: " + BulanPublikasi_V1)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Publikasi V1: NSEE")
                        Log_Error.update({"Bulan Publikasi V1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Publikasi: KeyError")
                    Log_Error.update({"Bulan Publikasi V1":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunPublikasi_V1 = Isi_V1["tahunTerbit"]  
                    ID_TahunPublikasi_V1 = "51_startyear" + Row_V1
                    driver.find_element(By.ID, ID_TahunPublikasi_V1).send_keys(TahunPublikasi_V1)
                    print("- TahunPublikasi V1: " + TahunPublikasi_V1)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Publikasi V1: KeyError")
                    Log_Error.update({"Tahun Publikasi V1":"KeyError"})
                    ErrorKey += 1

                try:
                    TingkatMedia_V1 = Isi_V1["tingkatMediaPublikasi"]  
                    ID_TingkatMedia_V1 = "51_tingkatmedia" + Row_V1
                    Scroll_TingkatMedia_V1 = driver.find_element(By.ID, ID_TingkatMedia_V1)
                    action.move_to_element(Scroll_TingkatMedia_V1).perform()
                    Select_TingkatMedia_V1 = Select(Scroll_TingkatMedia_V1)
                    try:   
                        Select_TingkatMedia_V1.select_by_visible_text(TingkatMedia_V1)
                        print("- Tingkat Media V1: " + TingkatMedia_V1)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat Media V1: NSEE")
                        Log_Error.update({"Tingkat Media V1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat Media V1: KeyError")
                    Log_Error.update({"Tingkat Media V1":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_V1 = Isi_V1["uraianSingkatMateriPublikasi"]  
                    ID_Uraian_V1 = "51_uraian" + Row_V1
                    Scroll_Uraian_V1 = driver.find_element(By.ID, ID_Uraian_V1)
                    action.move_to_element(Scroll_Uraian_V1).perform()
                    Scroll_Uraian_V1.send_keys(Uraian_V1)
                    print("- Uraian V1: " + Uraian_V1)
                    Elemen += 1
                except KeyError:
                    print("- Uraian V1: KeyError")
                    Log_Error.update({"Uraian V1":"KeyError"})
                    ErrorKey += 1

                try:        
                    Tingkat_V1 = Isi_V1["tingkatKesulitanPublikasi"]  
                    ID_Tingkat_V1 = "51_tingkat" + Row_V1
                    Scroll_Tingkat_V1 = driver.find_element(By.ID, ID_Tingkat_V1)
                    action.move_to_element(Scroll_Tingkat_V1).perform()
                    Select_Tingkat_V1 = Select(Scroll_Tingkat_V1)
                    try:
                        Select_Tingkat_V1.select_by_visible_text(Tingkat_V1)
                        print("- Tingkat V1: " + Tingkat_V1)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat V1: NSEE")
                        Log_Error.update({"Tingkat V1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat V1: KeyError")
                    Log_Error.update({"Tingkat V1":"KeyError"})
                    ErrorKey += 1

                #Kompetisi V1 
                ID_Komp_V1 = "51_komp" + Row_V1
                Scroll_Komp_V1 = driver.find_element(By.ID, ID_Komp_V1)
                action.move_to_element(Scroll_Komp_V1).perform()
                
                try:
                    Komp_W4_V1 = Isi_V1["klaimKompetensiWempat"]
                    print("- Komp W4 V1: " + str(len(Komp_W4_V1)))
                    try:
                        for Komp_Value_W4_V1 in Komp_W4_V1:
                            Komp_Label_W4_V1 = Komp_Value_W4_V1[slice(5)]
                            Komp_Call_W4_V1 = f'//*[@id="{ID_Komp_V1}"]//optgroup[contains(@label, "{Komp_Label_W4_V1}")]/option[@value="{Komp_Value_W4_V1}."]'
                            Komp_Find_W4_V1 = driver.find_element(By.XPATH, Komp_Call_W4_V1)
                            action.move_to_element_with_offset(Komp_Find_W4_V1, 0, -15).click().perform()
                            print("-", Komp_Value_W4_V1)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 V1: NSEE")
                        Log_Error.update({"Komp W4 V1":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 V1: KeyError") 
                    Log_Error.update({"Komp W4 V1":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_V1 += 1
                ID_Count_V1 += 1
                print("Row " + Row_V1 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN V2
        def FormV2():
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
            DB_Count_V2 = 0

            #Database
            Dict_V2 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_v_dua':1})
            List_V2 = Dict_V2["form_v_dua"]
            n_V2 = len(List_V2)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_V2) + "\n")
            
            print("Start from Row: " + str(ID_Count_V2))
            print("Row Ditambah: " + str(n_V2) + "\n")

            while Counter_V2 <= n_V2:
                #add row
                TambahV2 = driver.find_element(By.XPATH, '//button[@onclick="add52(\'lok\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahV2)
                action.move_to_element(TambahV2).perform()
                TambahV2.send_keys(Keys.ENTER)

                Row_V2 = str(ID_Count_V2)

                #Document V2
                Isi_V2 = List_V2[DB_Count_V2]
                print("Counter Row: " + str(Counter_V2))
                print("Key Document: " + Isi_V2["key"] + "\n")

                try:
                    Judul_V2 = Isi_V2["judulMakalah"]  
                    ID_Judul_V2 = "52_judul" + Row_V2
                    driver.find_element(By.ID, ID_Judul_V2).send_keys(Judul_V2)
                    print("- Judul V2: " + Judul_V2)
                    Elemen += 1
                except KeyError:
                    print("- Judul V2: KeyError")
                    Log_Error.update({"Judul V2":"KeyError"})
                    ErrorKey += 1

                try:
                    Seminar_V2 = Isi_V2["namaSeminar"] 
                    ID_Seminar_V2 = "52_nama" + Row_V2
                    driver.find_element(By.ID, ID_Seminar_V2).send_keys(Seminar_V2)
                    print("- Seminar V2: " + Seminar_V2)
                    Elemen += 1
                except KeyError:
                    print("- Seminar V2: KeyError")
                    Log_Error.update({"Seminar V2":"KeyError"})
                    ErrorKey += 1

                try:
                    Penyelenggara_V2 = Isi_V2[""] 
                    ID_Penyelenggara_V2 = "52_penyelenggara" + Row_V2
                    driver.find_element(By.ID, ID_Penyelenggara_V2).send_keys(Penyelenggara_V2)
                    print("- Penyelenggara V2: " + Penyelenggara_V2)
                    Elemen += 1
                except KeyError:
                    print("- Penyelenggara: KeyError")
                    Log_Error.update({"Penyelenggara V2":"KeyError"})
                    ErrorKey += 1
                
                try:
                    Kota_V2 = Isi_V2["kota"] 
                    ID_Kota_V2 = "52_location" + Row_V2
                    driver.find_element(By.ID, ID_Kota_V2).send_keys(Kota_V2)
                    print("- Kota V2: " + Kota_V2)
                    Elemen += 1
                except KeyError:
                    print("- Kota V2: KeyError")
                    Log_Error.update({"Kota V2":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_V2 = Isi_V2["provinsi"] 
                    ID_Provinsi_V2 = "52_provinsi" + Row_V2
                    driver.find_element(By.ID, ID_Provinsi_V2).send_keys(Provinsi_V2)
                    print("- Provinsi V2: " + Provinsi_V2)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi V2: KeyError")
                    Log_Error.update({"Provinsi V2":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_V2 = Isi_V2["negara"] 
                    ID_Negara_V2 = "52_negara" + Row_V2
                    driver.find_element(By.ID, ID_Negara_V2).send_keys(Negara_V2)
                    print("- Negara V2: " + Negara_V2)
                    Elemen += 1
                except KeyError:
                    print("- Negara V2: KeyError")
                    Log_Error.update({"Negara V2":"KeyError"})
                    ErrorKey += 1

                try:        
                    BulanSeminar_V2 = Isi_V2["bulanPenyelenggaraSeminar"] 
                    ID_BulanSeminar_V2 = "52_startdate" + Row_V2
                    Select_BulanSeminar_V2 = Select(driver.find_element(By.ID, ID_BulanSeminar_V2))
                    try:
                        Select_BulanSeminar_V2.select_by_visible_text(BulanSeminar_V2)
                        print("- Bulan Seminar V2: " + BulanSeminar_V2)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Seminar V2: NSEE")
                        Log_Error.update({"Bulan Seminar V2":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Seminar V2: KeyError")
                    Log_Error.update({"Bulan Seminar V2":"KeyError"})
                    ErrorKey += 1

                try:
                    TahunSeminar_V2 = Isi_V2["tahunPenyelenggaraSeminar"] 
                    ID_TahunSeminar_V2 = "52_startyear" + Row_V2
                    driver.find_element(By.ID, ID_TahunSeminar_V2).send_keys(TahunSeminar_V2)
                    print("- Tahun Seminar V2: " + TahunSeminar_V2)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Seminar V2: KeyError")
                    Log_Error.update({"Tahun Seminar V2":"KeyError"})
                    ErrorKey += 1
                
                try:
                    TingkatSeminar_V2 = Isi_V2["tingkatSeminar"] 
                    ID_TingkatSeminar_V2 = "52_tingkatseminar" + Row_V2
                    Scroll_TingkatSeminar_V2 = driver.find_element(By.ID, ID_TingkatSeminar_V2)
                    action.move_to_element(Scroll_TingkatSeminar_V2).perform()
                    Select_TingkatSeminar_V2 = Select(Scroll_TingkatSeminar_V2)
                    try:
                        Select_TingkatSeminar_V2.select_by_visible_text(TingkatSeminar_V2)
                        print("- TingkatSeminar V2: " + TingkatSeminar_V2)
                        Elemen += 1
                    except NSEE:
                        print("- TingkatSeminar V2: NSEE")
                        Log_Error.update({"Tingkat Seminar V2":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat Seminar V2: KeyError")
                    Log_Error.update({"Tingkat Seminar V2":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_V2 = Isi_V2["uraianSingkatMateriSeminar"] 
                    ID_Uraian_V2 = "52_uraian" + Row_V2
                    Scroll_Uraian_V2 = driver.find_element(By.ID, ID_Uraian_V2)
                    action.move_to_element(Scroll_Uraian_V2).perform()
                    Scroll_Uraian_V2.send_keys(Uraian_V2)
                    print("- Uraian V2: " + Uraian_V2)
                    Elemen += 1
                except KeyError:
                    print("- Uraian V2: KeyError")
                    Log_Error.update({"Uraian V2":"KeyError"})
                    ErrorKey += 1

                try:        
                    Tingkat_V2 = Isi_V2["tingkatKesulitan"] 
                    ID_Tingkat_V2 = "52_tingkat" + Row_V2
                    Scroll_Tingkat_V2 = driver.find_element(By.ID, ID_Tingkat_V2)
                    action.move_to_element(Scroll_Tingkat_V2).perform()
                    Select_Tingkat_V2 = Select(Scroll_Tingkat_V2)
                    try:
                        Select_Tingkat_V2.select_by_visible_text(Tingkat_V2)
                        print("- Tingkat V2: " + Tingkat_V2)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat V2: NSEE")
                        Log_Error.update({"Tingkat V2":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat V2: KeyError")
                    Log_Error.update({"Tingkat V2":"KeyError"})
                    ErrorKey += 1

                #Kompetisi V2 
                ID_Komp_V2 = "52_komp" + Row_V2
                Scroll_Komp_V2 = driver.find_element(By.ID, ID_Komp_V2)
                action.move_to_element(Scroll_Komp_V2).perform()

                try:
                    Komp_W4_V2 = Isi_V2["klaimKompetensiWempat"]        
                    print("- Komp W4 V2: " + str(len(Komp_W4_V2)))
                    try:
                        for Komp_Value_W4_V2 in Komp_W4_V2:
                            Komp_Label_W4_V2 = Komp_Value_W4_V2[slice(5)]
                            Komp_Call_W4_V2 = f'//*[@id="{ID_Komp_V2}"]//optgroup[contains(@label, "{Komp_Label_W4_V2}")]/option[@value="{Komp_Value_W4_V2}."]'
                            Komp_Find_W4_V2 = driver.find_element(By.XPATH, Komp_Call_W4_V2)
                            action.move_to_element_with_offset(Komp_Find_W4_V2, 0, -15).click().perform()
                            print("-", Komp_Value_W4_V2)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 V2: NSEE")
                        Log_Error.update({"Komp W4 V2":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 V2: KeyError")
                    Log_Error.update({"Komp W4 V2":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_V2 += 1
                ID_Count_V2 += 1
                print("Row " + Row_V2 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN V3
        def FormV3():
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
            DB_Count_V3 = 0

            #Database
            Dict_V3 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_v_tiga':1})
            List_V3 = Dict_V3["form_v_tiga"]
            n_V3 = len(List_V3)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_V3) + "\n")
            
            print("Start from Row: " + str(ID_Count_V3))
            print("Row Ditambah: " + str(n_V3) + "\n")

            while Counter_V3 <= n_V3:
                #add row
                TambahV3 = driver.find_element(By.XPATH, '//button[@onclick="add53(\'sem\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahV3)
                action.move_to_element(TambahV3).perform()
                TambahV3.send_keys(Keys.ENTER)

                Row_V3 = str(ID_Count_V3)

                #Document V3
                Isi_V3 = List_V3[DB_Count_V3]
                print("Counter Row: " + str(Counter_V3))
                print("Key Document: " + Isi_V3["key"] + "\n")

                try:
                    NamaSeminar_V3 = Isi_V3["namaSeminar"] 
                    ID_NamaSeminar_V3 = "53_nama" + Row_V3
                    driver.find_element(By.ID, ID_NamaSeminar_V3).send_keys(NamaSeminar_V3)
                    print("- Nama Seminar V3: " + NamaSeminar_V3)
                    Elemen += 1
                except KeyError:
                    print("- Nama Seminar V3: KeyError")
                    Log_Error.update({"Nama Seminar V3":"KeyError"})
                    ErrorKey += 1

                try:        
                    Penyelenggara_V3 = Isi_V3["namaPenyelenggara"] 
                    ID_Penyelenggara_V3 = "53_penyelenggara" + Row_V3
                    driver.find_element(By.ID, ID_Penyelenggara_V3).send_keys(Penyelenggara_V3)
                    print("- Penyelenggara V3: " + Penyelenggara_V3)
                    Elemen += 1
                except KeyError:
                    print("- Penyelenggara V3: KeyError")
                    Log_Error.update({"Penyelenggara V3":"KeyError"})
                    ErrorKey += 1

                try:
                    Kota_V3 = Isi_V3["kota"] 
                    ID_Kota_V3 = "53_location" + Row_V3
                    driver.find_element(By.ID, ID_Kota_V3).send_keys(Kota_V3)
                    print("- Kota V3: " + Kota_V3)
                    Elemen += 1
                except KeyError:
                    print("- Kota V3: KeyError")
                    Log_Error.update({"Kota V3":"KeyError"})
                    ErrorKey += 1

                try:
                    Provinsi_V3 = Isi_V3["provinsi"] 
                    ID_Provinsi_V3 = "53_provinsi" + Row_V3
                    driver.find_element(By.ID, ID_Provinsi_V3).send_keys(Provinsi_V3)
                    print("- Provinsi V3: " + Provinsi_V3)
                    Elemen += 1
                except KeyError:
                    print("- Provinsi V3: KeyError")
                    Log_Error.update({"Provinsi V3":"KeyError"})
                    ErrorKey += 1

                try:
                    Negara_V3 = Isi_V3["negara"] 
                    ID_Negara_V3 = "53_negara" + Row_V3
                    driver.find_element(By.ID, ID_Negara_V3).send_keys(Negara_V3)
                    print("- Negara V3: " + Negara_V3)
                    Elemen += 1
                except KeyError:
                    print("- Negara V3: KeyError")
                    Log_Error.update({"Negara V3":"KeyError"})
                    ErrorKey += 1

                try:        
                    BulanSeminar_V3 = Isi_V3["bulanPenyelenggaraSeminar"] 
                    ID_BulanSeminar_V3 = "53_startdate" + Row_V3
                    Select_BulanSeminar_V3 = Select(driver.find_element(By.ID, ID_BulanSeminar_V3))
                    try:
                        Select_BulanSeminar_V3.select_by_visible_text(BulanSeminar_V3)
                        print("- Bulan Seminar V3: " + BulanSeminar_V3)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan Seminar V3: NSEE")
                        Log_Error.update({"Bulan Seminar V3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan Seminar V3: KeyError")
                    Log_Error.update({"Bulan Seminar V3":"KeyError"})
                    ErrorKey += 1

                try:        
                    TahunSeminar_V3 = Isi_V3["tahunPenyelenggaraSeminar"] 
                    ID_TahunSeminar_V3 = "53_startyear" + Row_V3
                    driver.find_element(By.ID, ID_TahunSeminar_V3).send_keys(TahunSeminar_V3)
                    print("- Tahun Seminar V3: " + TahunSeminar_V3)
                    Elemen += 1
                except KeyError:
                    print("- Tahun Seminar V3: KeyError")
                    Log_Error.update({"Tahun Seminar V3":"KeyError"})
                    ErrorKey += 1

                try:        
                    TingkatSeminar_V3 = Isi_V3["tingkatSeminar"] 
                    ID_TingkatSeminar_V3 = "53_tingkatseminar" + Row_V3
                    Scroll_TingkatSeminar_V3 = driver.find_element(By.ID, ID_TingkatSeminar_V3)
                    action.move_to_element(Scroll_TingkatSeminar_V3).perform()
                    Select_TingkatSeminar_V3 = Select(Scroll_TingkatSeminar_V3)
                    try:
                        Select_TingkatSeminar_V3.select_by_visible_text(TingkatSeminar_V3)
                        print("- Tingkat Seminar V3: " + TingkatSeminar_V3)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat Seminar V3: NSEE")
                        Log_Error.update({"Tingkat Seminar V3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat Seminar V3: KeyError")
                    Log_Error.update({"Tingkat Seminar V3":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_V3 = Isi_V3["uraianSingkatMateriSeminar"] 
                    ID_Uraian_V3 = "53_uraian" + Row_V3
                    Scroll_Uraian_V3 = driver.find_element(By.ID, ID_Uraian_V3)
                    action.move_to_element(Scroll_Uraian_V3)
                    Scroll_Uraian_V3.send_keys(Uraian_V3)
                    print("- Uraian V3: " + Uraian_V3)
                    Elemen += 1
                except KeyError:
                    print("- Uraian V3: KeyError")
                    Log_Error.update({"Uraian V3":"KeyError"})
                    ErrorKey += 1

                try:        
                    Tingkat_V3 = Isi_V3["tingkatKesulitan"] 
                    ID_Tingkat_V3 = "53_tingkat" + Row_V3
                    Scroll_Tingkat_V3 = driver.find_element(By.ID, ID_Tingkat_V3)
                    action.move_to_element(Scroll_Tingkat_V3)
                    Select_Tingkat_V3 = Select(Scroll_Tingkat_V3)
                    try:
                        Select_Tingkat_V3.select_by_visible_text(Tingkat_V3)
                        print("- Tingkat V3: " + Tingkat_V3)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat V3: NSEE")
                        Log_Error.update({"Tingkat V3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat V3: KeyError")
                    Log_Error.update({"Tingkat V3":"KeyError"})
                    ErrorKey += 1

                #Kompetisi V3 
                
                ID_Komp_V3 = "53_komp" + Row_V3
                Scroll_Komp_V3 = driver.find_element(By.ID, ID_Komp_V3)
                action.move_to_element(Scroll_Komp_V3).perform()
                
                try:
                    Komp_W2_V3 = Isi_V3["klaimKompetensiWdua"]
                    print("- Komp W2 V3: " + str(len(Komp_W2_V3)))
                    try:
                        for Komp_Value_W2_V3 in Komp_W2_V3:
                            Komp_Label_W2_V3 = Komp_Value_W2_V3[slice(5)]
                            Komp_Call_W2_V3 = f'//*[@id="{ID_Komp_V3}"]//optgroup[contains(@label, "{Komp_Label_W2_V3}")]/option[@value="{Komp_Value_W2_V3}."]'
                            Komp_Find_W2_V3 = driver.find_element(By.XPATH, Komp_Call_W2_V3)
                            action.move_to_element_with_offset(Komp_Find_W2_V3, 0, -15).click().perform()
                            print("-", Komp_Value_W2_V3)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W2 V3: NSEE")  
                        Log_Error.update({"Komp W2 V3":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W2 V3: KeyError")
                    Log_Error.update({"Komp W2 V3":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_V3 += 1
                ID_Count_V3 += 1
                print("Row " + Row_V3 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN V4
        def FormV4():
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
            DB_Count_V4 = 0

            #Database
            Dict_V4 = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_v_empat':1})
            List_V4 = Dict_V4["form_v_empat"]
            n_V4 = len(List_V4)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_V4) + "\n")
            
            print("Start from Row: " + str(ID_Count_V4))
            print("Row Ditambah: " + str(n_V4) + "\n")

            while Counter_V4 <= n_V4:
                #add row
                TambahV4 = driver.find_element(By.XPATH, '//button[@onclick="add54(\'ino\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahV4)
                action.move_to_element(TambahV4).perform()
                TambahV4.send_keys(Keys.ENTER)

                Row_V4 = str(ID_Count_V4)

                #Document V4
                Isi_V4 = List_V4[DB_Count_V4]
                print("Counter Row: " + str(Counter_V4))
                print("Key Document: " + Isi_V4["key"] + "\n")

                try:
                    Judul_V4 = Isi_V4["namaInovasi"] 
                    ID_Judul_V4 = "54_nama" + Row_V4
                    driver.find_element(By.ID, ID_Judul_V4).send_keys(Judul_V4)
                    print("- Judul V4: " + Judul_V4)
                    Elemen += 1
                except KeyError:
                    print("- Judul V4: KeyError")
                    Log_Error.update({"Judul V4":"KeyError"})
                    ErrorKey += 1
        
                try:        
                    Bulan_V4 = Isi_V4["bulan"] 
                    ID_Bulan_V4 = "54_startdate" + Row_V4
                    Select_Bulan_V4 = Select(driver.find_element(By.ID, ID_Bulan_V4))
                    try:
                        Select_Bulan_V4.select_by_visible_text(Bulan_V4)
                        print("- Bulan V4: " + Bulan_V4)
                        Elemen += 1
                    except NSEE:
                        print("- Bulan V4: NSEE")
                        Log_Error.update({"Bulan V4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Bulan V4: KeyError")
                    Log_Error.update({"Bulan V4":"KeyError"})
                    ErrorKey += 1

                try:
                    Tahun_V4 = Isi_V4["tahun"] 
                    ID_Tahun_V4 = "54_startyear" + Row_V4
                    driver.find_element(By.ID, ID_Tahun_V4).send_keys(Tahun_V4)
                    print("- Tahun V4: " + Tahun_V4)
                    Elemen += 1
                except KeyError:
                    print("- Tahun V4: KeyError")
                    Log_Error.update({"Tahun V4":"KeyError"})
                    ErrorKey += 1

                try:
                    MediaPublikasi_V4 = Isi_V4["mediaPublikasi"]
                    ID_MediaPublikasi_V4 = "54_media_publikasi" + Row_V4
                    driver.find_element(By.ID, ID_MediaPublikasi_V4).send_keys(MediaPublikasi_V4)
                    print("- Media Publikasi V4: " + MediaPublikasi_V4)
                    Elemen += 1
                except KeyError:
                    print("- Media Publikasi V4: KeyError")
                    Log_Error.update({"Media Publikasi V4":"KeyError"})
                    ErrorKey += 1

                try:        
                    TingkatMedia_V4 = Isi_V4["tingkatPublikasi"] 
                    ID_TingkatMedia_V4 = "54_tingkatseminar" + Row_V4
                    Select_TingkatMedia_V4 = Select(driver.find_element(By.ID, ID_TingkatMedia_V4))
                    try:    
                        Select_TingkatMedia_V4.select_by_visible_text(TingkatMedia_V4)
                        print("- Tingkat Media V4: " + TingkatMedia_V4)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat Media V4: NSEE")
                        Log_Error.update({"Tingkat Media V4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat Media V4: KeyError")
                    Log_Error.update({"Tingkat Media V4":"KeyError"})
                    ErrorKey += 1

                try:
                    Uraian_V4 = Isi_V4["uraianSingkatInovasi"] 
                    ID_Uraian_V4 = "54_uraian" + Row_V4
                    Scroll_Uraian_V4 = driver.find_element(By.ID, ID_Uraian_V4)
                    action.move_to_element(Scroll_Uraian_V4)
                    Scroll_Uraian_V4.send_keys(Uraian_V4)
                    print("- Uraian V4: " + Uraian_V4)
                    Elemen += 1
                except KeyError:
                    print("- Uraian V4: KeyError")
                    Log_Error.update({"Uraian V4":"KeyError"})
                    ErrorKey += 1

                try:        
                    Tingkat_V4 = Isi_V4["tingkatKesulitanInovasi"] 
                    ID_Tingkat_V4 = "54_tingkat" + Row_V4
                    Scroll_Tingkat_V4 = driver.find_element(By.ID, ID_Tingkat_V4)
                    action.move_to_element(Scroll_Tingkat_V4).perform()
                    Select_Tingkat_V4 = Select(Scroll_Tingkat_V4)
                    try:
                        Select_Tingkat_V4.select_by_visible_text(Tingkat_V4)
                        print("- Tingkat V4: " + Tingkat_V4)
                        Elemen += 1
                    except NSEE:
                        print("- Tingkat V4: NSEE")
                        Log_Error.update({"Tingkat V4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Tingkat V4: KeyError")
                    Log_Error.update({"Tingkat V4":"KeyError"})
                    ErrorKey += 1

                #Kompetisi V4 
                ID_Komp_V4 = "54_komp" + Row_V4
                Scroll_Komp_V4 = driver.find_element(By.ID, ID_Komp_V4)
                action.move_to_element(Scroll_Komp_V4).perform()
                
                try:
                    Komp_P6_V4 = Isi_V4["klaimKompetensiPenam"]
                    print("- Komp P6 V4: " + str(len(Komp_P6_V4)))
                    try:
                        for Komp_Value_P6_V4 in Komp_P6_V4:
                            Komp_Label_P6_V4 = Komp_Value_P6_V4[slice(5)]
                            Komp_Call_P6_V4 = f'//*[@id="{ID_Komp_V4}"]//optgroup[contains(@label, "{Komp_Label_P6_V4}")]/option[@value="{Komp_Value_P6_V4}."]'
                            Komp_Find_P6_V4 = driver.find_element(By.XPATH, Komp_Call_P6_V4)
                            action.move_to_element_with_offset(Komp_Find_P6_V4, 0, -15).click().perform()
                            print("-", Komp_Value_P6_V4)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp P6 V4: NSEE")
                        Log_Error.update({"Komp P6 V4":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp P6 V4: KeyError")
                    Log_Error.update({"Komp P6 V4":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_V4 += 1
                ID_Count_V4 += 1
                print("Row " + Row_V4 + " telah diisi\n")

            driver.refresh() 

        #PENGISIAN VI
        def FormVI():
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
            DB_Count_VI = 0

            #Database
            Dict_VI = col.find_one({'pid':PID, 'student_id':Student_ID},{'_id': 0, 'form_vi':1})
            List_VI = Dict_VI["form_vi"]
            n_VI = len(List_VI)
            
            #Variabel return
            nonlocal Elemen
            nonlocal ErrorKey
            nonlocal NSEEn
            nonlocal Labelkomp

            print("Jumlah Document: " + str(n_VI) + "\n")
            
            print("Start from Row: " + str(ID_Count_VI))
            print("Row Ditambah: " + str(n_VI) + "\n")

            while Counter_VI <= n_VI:
                #add row
                TambahVI = driver.find_element(By.XPATH, '//button[@onclick="add6(\'bah\')"]')
                driver.execute_script("arguments[0].scrollIntoView();",TambahVI)
                action.move_to_element(TambahVI).perform()
                TambahVI.send_keys(Keys.ENTER)

                Row_VI = str(ID_Count_VI)

                #Document VI
                Isi_VI = List_VI[DB_Count_VI]
                print("Counter Row: " + str(Counter_VI))
                print("Key Document: " + Isi_VI["key"] + "\n")

                try:
                    Bahasa_VI = Isi_VI["namaBahasa"] 
                    ID_Bahasa_VI = "6_nama" + Row_VI
                    driver.find_element(By.ID, ID_Bahasa_VI).send_keys(Bahasa_VI)
                    print("- Bahasa VI: " + Bahasa_VI)
                    Elemen += 1
                except KeyError:
                    print("- Bahasa VI: KeyError")
                    Log_Error.update({"Bahasa VI":"KeyError"})
                    ErrorKey += 1
                try:        
                    JenisBahasa_VI = Isi_VI["jenisBahasa"] 
                    ID_JenisBahasa_VI = "6_jenisbahasa" + Row_VI
                    Select_JenisBahasa_VI = Select(driver.find_element(By.ID, ID_JenisBahasa_VI))
                    try:
                        Select_JenisBahasa_VI.select_by_visible_text(JenisBahasa_VI)
                        print("- Jenis Bahasa VI: " + JenisBahasa_VI)
                        Elemen += 1
                    except NSEE:
                        print("- Jenis Bahasa VI: NSEE")
                        Log_Error.update({"Jenis Bahasa VI":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jenis Bahasa VI: KeyError")
                    Log_Error.update({"Jenis Bahasa VI":"KeyError"})
                    ErrorKey += 1

                try:        
                    Verbal_VI = Isi_VI["kemampuanVerbalBahasa"] 
                    ID_Verbal_VI = "6_verbal" + Row_VI
                    Select_Verbal_VI = Select(driver.find_element(By.ID, ID_Verbal_VI))
                    try:
                        Select_Verbal_VI.select_by_visible_text(Verbal_VI)
                        print("- Verbal VI: " + Verbal_VI)
                        Elemen += 1
                    except NSEE:
                        print("- Verbal VI: NSEE")
                        Log_Error.update({"Verbal VI":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Verbal VI: KeyError")
                    Log_Error.update({"Verbal VI":"KeyError"})
                    ErrorKey += 1

                try:
                    JenisTulisan_VI = Isi_VI["jenisTulisan"] 
                    ID_JenisTulisan_VI = "6_jenistulisan" + Row_VI
                    Select_JenisTulisan_VI = Select(driver.find_element(By.ID, ID_JenisTulisan_VI))
                    try:
                        Select_JenisTulisan_VI.select_by_visible_text(JenisTulisan_VI)
                        print("- Jenis Tulisan VI: " + JenisTulisan_VI)
                        Elemen += 1
                    except NSEE:
                        print("- Jenis Tulisan VI: NSEE")
                        Log_Error.update({"Jenis Tulisan VI":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Jenis Tulisan VI: KeyError")
                    Log_Error.update({"Jenis Tulisan VI":"KeyError"})
                    ErrorKey += 1
                

                #Kompetisi VI 
                ID_Komp_VI = "6_komp" + Row_VI
                Scroll_Komp_VI = driver.find_element(By.ID, ID_Komp_VI)
                action.move_to_element(Scroll_Komp_VI).perform()

                try:      
                    Komp_W4_VI = Isi_VI["klaimKompetensiWempat"]  
                    print("- Komp W4 VI: " + str(len(Komp_W4_VI)))
                    try:
                        for Komp_Value_W4_VI in Komp_W4_VI:
                            Komp_Label_W4_VI = Komp_Value_W4_VI[slice(5)]
                            Komp_Call_W4_VI = f'//*[@id="{ID_Komp_VI}"]//optgroup[contains(@label, "{Komp_Label_W4_VI}")]/option[@value="{Komp_Value_W4_VI}."]'
                            Komp_Find_W4_VI = driver.find_element(By.XPATH, Komp_Call_W4_VI)
                            action.move_to_element_with_offset(Komp_Find_W4_VI, 0, -15).click().perform()
                            print("-", Komp_Value_W4_VI)
                            Labelkomp += 1
                    except NSEE:
                        print("- Komp W4 VI: NSEE")
                        Log_Error.update({"Komp W4 VI":"NSEE"})
                        NSEEn += 1
                except KeyError:
                    print("- Komp W4 VI: KeyError")
                    Log_Error.update({"Komp W4 VI":"KeyError"})
                    ErrorKey += 1

                #End/retry point of loop
                Counter_VI += 1
                ID_Count_VI += 1
                print("Row " + Row_VI + " telah diisi\n")

            driver.refresh() 

        def AllForm():
            FormI1()
            FormI2()
            FormI3()
            FormI4()
            FormI5()
            FormI6()
            FormII1()
            FormII2()
            FormIII()
            FormIV()
            FormV1()
            FormV2()
            FormV3()
            FormV4()
            FormVI()
            time.sleep(1)
            driver.quit()
            print("All Form Selesai")

        AllForm()
        
        # driver.find_element(By.LINK_TEXT, "Save & Continue").click()
        # WebDriverWait(driver, 10).until(EC.alert_is_present())
        # driver.switch_to.alert.accept()

        Log_Run = {"Elemen":Elemen, "KeyError":ErrorKey, "NSEE":NSEEn}

        # return {"Log Error":Log_Error}
        return {"Log Run":Log_Run}

    #Error Form
    except Exception as e:
        print("TypeError:",str(e))
        error_message = "Error Occured = " + str(e)
        raise HTTPException(status_code=400, detail=error_message)
    
#uvicorn Selen-Isian-UPD-API:app --port 8000 --reload

#uvicorn Selen-Isian-UPD-API:app --host 0.0.0.0 --port 8000 --reload

#uvicorn Selen-Isian-UPD-API:app --host 192.168.195.83 --port 8000 --reload

#{"process_id":"formM-VW2qhqD3JfkcQn_2SnAEU", "url":"https://updmember.pii.or.id/", "student_id":"21060124130129"}

