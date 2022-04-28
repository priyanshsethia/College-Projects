import mysql.connector as sqltor
import matplotlib.pyplot as pl
import pandas as pd
import numpy as np

mycon=sqltor.connect(host='localhost', user='root', passwd='')
if mycon.is_connected:
    print('Connected Successfully...')
    
cursor=mycon.cursor()

cursor.execute('Create database if not exists Parkdb')
cursor.execute('Use Parkdb')

cursor.execute('Create table if not exists Parking_Details(PID int primary key, PLevel char(30), Charges int, Vacancy char(10))')

cursor.execute('Create table if not exists Vehicle_Details(Vehicle_No char(15) primary key, VType char(20), Company char(20), Model char(30),\
                                                           Reg_State char(20), Owner_Name char(20), Mobile bigint)')

cursor.execute('Create table if not exists Booking_Details(BID int primary key, PID int, Vehicle_No char(15), Check_in_Date date)')

cursor.execute('Create table if not exists Previous_Booking_Details(BID int primary key, PID int, Vehicle_No char(15), Check_in_Date date, Check_out_Date date,\
                                                            NOD int, Charges int, Net_Amount int)')

cursor.execute('Alter table Booking_Details add foreign key(PID) references Parking_Details(PID), add foreign key(Vehicle_No) references Vehicle_Details(Vehicle_No)')
cursor.execute('Alter table Previous_Booking_Details add foreign key(PID) references Parking_Details(PID), add foreign key(Vehicle_No) references Vehicle_Details(Vehicle_No)')

#Some pre-inserted parking areas
while True:
    cursor.execute('Select * from Parking_Details')
    cursor.fetchall()
    cnt=cursor.rowcount
    if cnt==0:
        cursor.execute('Insert into Parking_Details values(101, "Level 1", 100, "Vacant"),\
                                                          (102, "Level 1", 100, "Vacant"),\
                                                          (103, "Level 1", 100, "Vacant"),\
                                                          (104, "Level 1", 100, "Vacant"),\
                                                          (105, "Level 1", 100, "Vacant"),\
                                                          (201, "Level 2", 50, "Vacant"),\
                                                          (202, "Level 2", 50, "Vacant"),\
                                                          (203, "Level 2", 50, "Vacant"),\
                                                          (204, "Level 2", 50, "Vacant"),\
                                                          (205, "Level 2", 50, "Vacant"),\
                                                          (301, "Level 3", 30, "Vacant"),\
                                                          (302, "Level 3", 30, "Vacant"),\
                                                          (303, "Level 3", 30, "Vacant"),\
                                                          (304, "Level 3", 30, "Vacant"),\
                                                          (305, "Level 3", 30, "Vacant")')
        mycon.commit()
    else:
        break


""" FUNCTIONS """

## FUNCTIONS OF PARKING MENU

    #Function - 1 : Show Details
def ShowParkings():
    print()
    print('Parking Details are :-')
    print()
    cursor.execute('Select * from Parking_Details order by PLevel')
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Parking ID', 'Parking Level', 'Charges', 'Vacancy'])
    print(df.to_string(index=False))
    print()
    
    #Function - 2 : Add Parking Details
def AddParkings():
    print()
    PID=int(input('Parking ID > '))
    while True:
        cursor.execute('Select * from Parking_Details where PID={}'.format(PID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt>=1:
            print('Parking ID ',PID, ' already exist...')
            PID=int(input('Again Enter Parking ID >'))
        else:
            break
    print('Select Parking Level :-')
    print('     1. Level 1(Charges - 100)')
    print('     2. Level 2(Charges - 50)')
    print('     3. Level 3(Charges - 30)')
    PLevel=int(input('Select any type > '))
    while True:
        ptype=''
        Charges=0
        if PLevel<=0 or PLevel>=4:
            print('Parking level does not exist')
            PLevel=int(input('Again select any type > '))
        else:
            if PLevel==1:
                ptype='Level 1(Charges - 100)'
                Charges=100
            elif PLevel==2:
                ptype='Level 2(Charges - 50)'
                Charges=50
            elif PLevel==3:
                ptype='Level 3(Charges - 30)'
                Charges=30
            break
    Vacancy='Vacant'
    
    cursor.execute('Insert into Parking_Details values({}, "{}", {}, "{}")'.format(PID, ptype, Charges, Vacancy))
    mycon.commit()
    print()
    print('Parking added successfully...')
    
    #Function - 3 : Delete Parking Details
def DeleteParking():
    print()
    PID=int(input('Parking ID > '))
    while True:
        cursor.execute('Select * from Parking_Details where PID={}'.format(PID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Parking ID ',PID, ' not exist...')
            PID=int(input('Again Enter Parking ID >'))
        else:
            break
    
    cursor.execute('Delete from Parking_Details where PID={}'.format(PID))
    mycon.commit()
    print()
    print('Parking Under Maintenance , Sorry for the inconvinience...')

    #Function - 4 : Search for Parking
def SearchParking():
    print()
    PID=int(input('Parking ID > '))
    while True:
        cursor.execute('Select * from Parking_Details where PID={}'.format(PID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Parking ID ',PID, ' not exist...')
            PID=int(input('Again Enter Parking ID >'))
        else:
            break
    
    cursor.execute('Select * from Parking_Details where PID={}'.format(PID))
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Parking ID', 'Parking Level', 'Charges', 'Vacancy'])
    print()
    print('Result is :- ')
    print()
    print(df.to_string(index=False))
    
    #Function - 5 : Summary of the Parking
def SummaryOfParking():
    print()
    print('Summary of the Parking')
    print()

    cursor.execute('Select * from Parking_Details')
    cursor.fetchall()
    cntparkings=cursor.rowcount
    print('     Total No. of Parking Areas     :     ', cntparkings)
    print()
    
    print('     No. of Parkings on Different Levels :-')
    print()
    cursor.execute('Select * from Parking_Details where PLevel like "%Level 1%"')
    cursor.fetchall()
    carparkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Vacant%" and PLevel like "%Level 1%"')
    cursor.fetchall()
    v1parkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Booked%" and PLevel like "%Level 1%"')
    cursor.fetchall()
    b1parkings=cursor.rowcount

    
    print('          Level 1      :     ', carparkings)
    print()
    print('                   Vacant     :     ', v1parkings)
    print('                   Booked     :     ', b1parkings)
    print()

    cursor.execute('Select * from Parking_Details where PLevel like "%Level 2%"')
    cursor.fetchall()
    bikeparkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Vacant%" and PLevel like "%Level 2%"')
    cursor.fetchall()
    v2parkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Booked%" and PLevel like "%Level 2%"')
    cursor.fetchall()
    b2parkings=cursor.rowcount
    
    print('          Level 2      :     ', bikeparkings)
    print()
    print('                   Vacant     :     ', v2parkings)
    print('                   Booked     :     ', b2parkings)
    print()
    
    cursor.execute('Select * from Parking_Details where PLevel like "%Level 3%"')
    cursor.fetchall()
    scootyparkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Vacant%" and PLevel like "%Level 3%"')
    cursor.fetchall()
    v3parkings=cursor.rowcount
    
    cursor.execute('Select * from Parking_Details where Vacancy like "%Booked%" and PLevel like "%Level 3%"')
    cursor.fetchall()
    b3parkings=cursor.rowcount
    
    print('          Level 3      :     ', scootyparkings)
    print()
    print('                   Vacant     :     ', v3parkings)
    print('                   Booked     :     ', b3parkings)


## FUNCTIONS OF VEHICLE MENU

    #Function - 1 : Show Details
def ShowVehicle():
    print()
    print('Vehicles Details are :-')
    print()
    cursor.execute('Select * from Vehicle_Details')
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Vehicle No', 'Vehicle Type', 'Company', 'Model', 'Reg. State', 'Owner Name', 'Mobile No.'])
    print(df.to_string(index=False))
    print()
    
    #Function - 2 : Add Vehicle
def AddVehicle():
    print()
    VehicleNo=input('Vehicle No. > ')
    while True:
        cursor.execute('Select * from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
        data=cursor.fetchall()
        cnt=cursor.rowcount
        if cnt>=1:
            print('Vehicle No. ',VehicleNo, ' already exist...')
            df=pd.DataFrame(data, columns=['Vehicle No', 'Vehicle Type', 'Company', 'Model', 'Reg. State', 'Owner Name', 'Mobile No.'])
            print(df.to_string(index=False))
            print()
            VehicleNo=int(input('Again Vehicle No. > '))
        else:
            break
    print('Select Vehicle Type :-')
    print('     1. Car')
    print('     2. Bike')
    print('     3. Scooty')
    VType=int(input('Select any type > '))
    while True:
        vtype=''
        if VType<=0 or VType>=4:
            print('Vehicle Type does not exist')
            VType=int(input('Again select any type > '))
        else:
            if VType==1:
                vtype='Car'
            elif VType==2:
                vtype='Bike'
            elif VType==3:
                vtype='Scooty'
            break
    Company=input('Company of Vehicle > ')
    Model=input('Model Name of Vehicle > ')
    Reg_State=input('Registered State > ')
    Owner=input('Owner Name > ')
    Mobile=int(input('Mobile No. > '))
    
    cursor.execute('Insert into Vehicle_Details values("{}", "{}", "{}", "{}", "{}", "{}",{})'.format(VehicleNo, vtype, Company, Model, Reg_State, Owner, Mobile))
    mycon.commit()
    print()
    print('Vehicle added successfully...')

    #Function - 3 : Update Vehicle Details
def UpdateVehicle():
    print()
    print('Select Update Type :-')
    print('     1. By Vehicle No.')
    print('     2. By Owner Name')
    print()
    UpdateCmd=int(input('Choose any Update Type > '))
    while True:
        if UpdateCmd<=0 or UpdateCmd>=3:
            print('Invalid Input...')
            print('Select Update Type :-')
            print('     1. By Vehicle No.')
            print('     2. By Owner Name')
            print()
            UpdateCmd=int(input('Again choose any Update Type > '))
        else:
            if UpdateCmd==1:
                print()
                VehicleNo=input('Enter Vehicle No. to Update > ')
                while True:
                    cursor.execute('Select * from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
                    cursor.fetchall()
                    cnt=cursor.rowcount
                    if cnt==0:
                        print('Vehicle No. ',VehicleNo, ' not exist...')
                        VehicleNo=input('Again Enter Vehicle No. > ')
                    else:
                        break
                print('Select Vehicle Type :-')
                print('     1. Car')
                print('     2. Bike')
                print('     3. Scooty')
                VType=int(input('Select any type > '))
                while True:
                    vtype=''
                    if VType<=0 or VType>=4:
                        print('Vehicle Type does not exist')
                        VType=int(input('Again select any type > '))
                    else:
                        if VType==1:
                            vtype='Car'
                        elif VType==2:
                            vtype='Bike'
                        elif VType==3:
                            vtype='Scooty'
                        break
                Company=input('Company of Vehicle > ')
                Model=input('Model Name of Vehicle > ')
                Reg_State=input('Registered State > ')
                Owner=input('Owner Name > ')
                Mobile=int(input('Mobile No. > '))
                
                cursor.execute('Update Vehicle_Details set VType="{}", Company="{}", Model="{}", Reg_State="{}", Owner_Name="{}", Mobile={} where Vehicle_No="{}"'.format(vtype, Company, Model, Reg_State, Owner, Mobile, VehicleNo))
                mycon.commit()
                print()
                print('Vehicle updated successfully...')
        
            elif UpdateCmd==2:
                print()
                Owner=input('Enter Owner Name to Update > ')
                while True:
                    cursor.execute('Select * from Vehicle_Details where Owner_Name="{}"'.format(Owner))
                    cursor.fetchall()
                    cnt=cursor.rowcount
                    if cnt==0:
                        print('Owner Name ',Owner, ' not exist...')
                        Owner=input('Again Enter Owner Name > ')
                    else:
                        break
                VehicleNo=input('Enter Vehicle No. > ')
                print('Select Vehicle Type :-')
                print('     1. Car')
                print('     2. Bike')
                print('     3. Scooty')
                VType=int(input('Select any type > '))
                while True:
                    vtype=''
                    if VType<=0 or VType>=4:
                        print('Vehicle Type does not exist')
                        VType=int(input('Again select any type > '))
                    else:
                        if VType==1:
                            vtype='Car'
                        elif VType==2:
                            vtype='Bike'
                        elif VType==3:
                            vtype='Scooty'
                        break
                Company=input('Company of Vehicle > ')
                Model=input('Model Name of Vehicle > ')
                Reg_State=input('Registered State > ')
                Mobile=int(input('Mobile No. > '))
                
                cursor.execute('Update Vehicle_Details set Vehicle_No="{}", VType="{}", Company="{}", Model="{}", Reg_State="{}", Mobile={} where Owner_Name="{}"'.format(VehicleNo, vtype, Company, Model, Reg_State, Mobile, Owner))
                mycon.commit()
                print()
                print('Vehicle updated successfully...')
            break
    
    #Function - 4 : Delete Vehicle Details
def DeleteVehicle():
    print()
    Vehicleno=int(input('Vehicle number > '))
    while True:
        cursor.execute('Select * from Vehicle_details where Vehicle_No={}'.format(Vehicleno))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Vehicle Number ',Vehicleno, ' not exist...')
            Vehicleno=int(input('Again Enter Vehicle Number >'))
        else:
            break
    
    cursor.execute('Delete from Vehicle_Details where Vehicle_No={}'.format(Vehicleno))
    mycon.commit()
    print()

    #Function - 5 : Search for Vehicle
def Searchvehicle():
    print()
    Vehicleno=int(input('Vehicle numbner > '))
    while True:
        cursor.execute('Select * from Vehicle_Details where Vehicle_No like "%{}%"'.format(Vehicleno))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Vehicle number ',Vehicleno, ' not exist...')
            Vehicleno=int(input('Again Enter Vehicle number >'))
        else:
            break
    
    cursor.execute('Select * from Vehicle_Details where Vehicle_No={}'.format(Vehicleno))
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Vehicle Number', 'Vehicle Type', 'Company', 'Model', 'Reg. State', 'Owner Name','Mobile Number'])
    print()
    print('Result is :- ')
    print()
    print(df.to_string(index=False))
    
    #Function - 6 : Summary of the Vehicle
def SummaryOfVehicle():
    print()
    print('Summary of the Vehicle')
    print()

    cursor.execute('Select * from Vehicle_Details')
    cursor.fetchall()
    cntvehicles=cursor.rowcount
    print('     Total No. of Vehicles     :     ', cntvehicles)
    print()
    print('     No. of Vehicles Type :-')
    print()
    cursor.execute('Select VType, Count(VType) from Vehicle_Details group by VType')
    com=cursor.fetchall()
    df=pd.DataFrame(com, columns=['Vehicle Type', 'No. of Vehicles'])
    print(df.to_string(index=False))
    print()    
    
    print('     No. of Vehicles of Different Companies :-')
    print()
    cursor.execute('Select Company, Count(Company) from Vehicle_Details group by Company')
    com=cursor.fetchall()
    df=pd.DataFrame(com, columns=['Companies', 'No. of Vehicles'])
    print(df.to_string(index=False))
    print()    
    
    print('     No. of Vehicles from Different States :-')
    print()
    cursor.execute('Select Reg_State, Count(Reg_State) from Vehicle_Details group by Company')
    com=cursor.fetchall()
    df=pd.DataFrame(com, columns=['States', 'No. of Vehicles'])
    print(df.to_string(index=False))
    print()
    
    
## FUNCTIONS OF BOOKING MENU

    #Function - 1 : Show Current Booking Details
def ShowCurrentBooking():
    print()
    print('Current Booking Details are :-')
    print()
    cursor.execute('Select * from Booking_Details')
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Booking ID','Parking ID', 'Vehicle No.', 'Check in Date'])
    print(df.to_string(index=False))
    print()
    
    #Function - 2 : Show Previous Booking Details
def ShowPreviousBooking():
    print()
    print('Previous Booking Details are :-')
    print()
    cursor.execute('Select * from Previous_Booking_Details')
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Booking ID','Parking ID', 'Vehicle No.', 'Check in Date', 'Check out Date', 'NOD', 'Charges', 'Net Amount'])
    print(df.to_string(index=False))
    print()
    
    #Function - 3 : Issue of Parking Area
def IssueOfParkingArea():
    print()
    BID=int(input('Booking ID > '))
    while True:
        cursor.execute('Select * from Booking_Details where BID={}'.format(BID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt>=1:
            print('Booking ID ',BID, ' already exist...')
            BID=int(input('Again Enter Booking ID >'))
        else:
            break   
    print()
    print('**************************************************')
    print('Available Parkings are :-')
    print('**************************************************')
    print()
    cursor.execute('Select PID, PLevel from Parking_Details where Vacancy like "%Vacant%" order by PLevel')
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Parking ID', 'Parking Level'])
    print(df.to_string(index=False))
    print()
    
    PID=int(input('Enter Parking ID > '))
    while True:
        cursor.execute('Select * from Parking_Details where PID={}'.format(PID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Parking Area ',str(PID), ' not exist...')
            PID=int(input('Again enter Parking ID > '))
        elif cnt>=1:           
            cursor.execute('Select * from Parking_Details where Vacancy like "%Booked%" and PID={}'.format(PID))
            cursor.fetchall()
            cnt=cursor.rowcount
            if cnt>=1:
                print('Parking Area ', str(PID), ' is already Booked.')
                PID=int(input('Again enter Parking ID > '))
            else:
                break
            break
    
    VehicleNo=input('Vehicle numbner > ')
    while True:
        cursor.execute('Select * from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Vehicle number ',VehicleNo, ' not exist...')
            VehicleNo=input('Again Enter Vehicle number >')
        else:
            break
    Check_in_Date=input('Check_in_Date (YYYY-MM-DD) > ')
    
    cursor.execute('Insert into Booking_Details(BID, PID, Vehicle_No, Check_in_Date) values({}, {}, "{}", "{}")'.format(BID, PID, VehicleNo, Check_in_Date))
    mycon.commit()
    cursor.execute('Insert into Previous_Booking_Details(BID, PID, Vehicle_No, Check_in_Date) values({}, {}, "{}", "{}")'.format(BID, PID, VehicleNo, Check_in_Date))
    mycon.commit()
    
    cursor.execute('Update Parking_Details set Vacancy="Booked" where PID={}'.format(PID))
    mycon.commit()
    print('Parking area ',PID, ' booked successfully for vehicle no. ', VehicleNo, '...')
    
    #Function - 4 : Generate Bill
def GenerateBill():
    print()
    BID=int(input('Booking ID > '))
    while True:
        cursor.execute('Select * from Booking_Details where BID={}'.format(BID))
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt==0:
            print('Booking ID ',BID, ' not exist...')
            BID=int(input('Again Enter Booking ID >'))
        else:
            break   
    
    print()
    print('***********************************************')
    cursor.execute('Select BID, PID, Vehicle_No, Check_in_Date from Booking_Details where BID={}'.format(BID))
    data=cursor.fetchall()
    df=pd.DataFrame(data, columns=['Booking ID', 'Parking ID', 'Vehicle No.', 'Check_in_Date'])
    print(df.to_string(index=False))
    print('***********************************************')
    
    Check_out_Date=input('Check_out_Date (YYYY-MM-DD) > ')
    cursor.execute('Update Previous_Booking_Details set Check_out_Date="{}" where BID={}'.format(Check_out_Date, BID))
    mycon.commit()
    while True:
        cursor.execute('Select DateDiff(Check_out_Date, Check_in_Date) from Previous_Booking_Details where BID={}'.format(BID))
        data=cursor.fetchone()
        for a in data:
            NOD=a
        if NOD<0:
            print("Invalid Check out date, it can't be less than check in date...")
            Check_out_Date=input('Again check_out_Date (YYYY-MM-DD) > ')
            cursor.execute('Update Previous_Booking_Details set Check_out_Date="{}" where BID={}'.format(Check_out_Date, BID))
            mycon.commit()
        if NOD==0:
            NOD=NOD+1
        else:
            break
    
    cursor.execute('Select pd.Charges from Parking_Details pd, Booking_Details bd where pd.PID=bd.PID and BID={}'.format(BID))
    data=cursor.fetchone()
    for a in data:
        Charges=a
    Net_Amount=NOD*Charges
    
    cursor.execute('Update Previous_Booking_Details set NOD={}, Charges={}, Net_Amount={} where BID={}'.format(NOD, Charges, Net_Amount, BID))
    mycon.commit()
    cursor.execute('Update Parking_Details set Vacancy="Vacant" where (Select PID from Booking_Details where BID={})'.format(BID))
    mycon.commit()
    cursor.execute('Delete from Booking_Details where BID={}'.format(BID))
    mycon.commit()
    
    cursor.execute('Select PID from Previous_Booking_Details where BID={}'.format(BID))
    data=cursor.fetchone()
    for a in data:
        PID=a
    
    cursor.execute('Select PLevel from Parking_Details where PID={}'.format(PID))
    data=cursor.fetchone()
    for a in data:
        PLevel=a
    
    cursor.execute('Select Vehicle_No from Previous_Booking_Details where BID={}'.format(BID))
    data=cursor.fetchone()
    for a in data:
        VehicleNo=a
    
    cursor.execute('Select Owner_Name from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        Owner=a
        
    cursor.execute('Select Mobile from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        Mobile=a
    
    cursor.execute('Select Company from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        Company=a
    
    cursor.execute('Select Model from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        Model=a
    
    cursor.execute('Select VType from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        VType=a
    
    cursor.execute('Select Reg_State from Vehicle_Details where Vehicle_No="{}"'.format(VehicleNo))
    data=cursor.fetchone()
    for a in data:
        Reg_State=a

    cursor.execute('Select Check_in_Date from Previous_Booking_Details where BID={}'.format(BID))
    data=cursor.fetchone()
    for a in data:
        Check_in_Date=a

    cursor.execute('Select Check_out_Date from Previous_Booking_Details where BID={}'.format(BID))
    data=cursor.fetchone()
    for a in data:
        Check_Out_Date=a
        
    print('*'*60)
    print(' '*14, 'City Parking Management System')
    print(' '*12 ,'-'*34)
    print('_'*60)
    print()
    print(' '*23, 'Parking Bill')
    print()
    print('     1.  Booking ID           :        ', BID)
    print('     2.  Parking Area & Level :        ', PID, '&', PLevel)
    print('     3.  Vehicle No.          :        ', VehicleNo)
    print('     4.  Owner Name           :        ', Owner)
    print('     5.  Vehicle Type         :        ', VType)
    print('     6.  Company & Model      :        ', Company, '&', Model)
    print('     7.  Registered State     :        ', Reg_State)
    print('     8.  Mobile No.           :        ', Mobile)
    print('     9.  Charges(per day)     :        ', Charges)
    print('     10. Check in Date        :        ', Check_in_Date)
    print('     11. Check out Date       :        ', Check_Out_Date)
    print('     12. No. of Days          :        ', NOD)
    print()
    print('                          Net Amount     =       Rs.', Net_Amount)
    print()
    print('_'*60)
    print()
    print(' '*19, 'Thank you, Visit Again')
    print('_'*60)
    print()
    print('*'*60)    
    

## FUNCTIONS OF REPORT MENU

    #Function - 1 : On the basis of vacancy
def VacancyBasis():
    cursor.execute('Select Vacancy from Parking_Details where Vacancy like "%Booked%"')
    cursor.fetchall()
    BookedCnt=cursor.rowcount
    cursor.execute('Select Vacancy from Parking_Details where Vacancy like "%vacant%"')
    cursor.fetchall()
    VacantCnt=cursor.rowcount
    
    x=[BookedCnt, VacantCnt]
    y=np.arange(2)
    pl.bar(y,x, color=['blue', 'orange'], width=0.5)
    pl.xticks(y, ['Booked', 'Vacant'])
    pl.title('Report on the Basis of Vacancy')
    pl.xlabel('Types of Vacancy')
    pl.ylabel('No. of Parkings')
    pl.show()
    
    #Function - 2 : On the basis of frequency of booking
def FrequencyBasis():
    Year=int(input('Enter Year to fetch report > '))
    while True:
        cursor.execute('Select Count(Check_in_Date) from Previous_Booking_Details where Year(Check_in_Date)={}'.format(Year))    
        cursor.fetchall()
        cnt=cursor.rowcount
        if cnt<=0:
            print('Data of Year ', str(Year), ' not found.')
            Year=int(input('Again enter year > '))
        else:
            for a in range(1,13):
                cursor.execute('Select Count(Check_in_Date) from Previous_Booking_Details where Month(Check_in_Date)={} and Year(Check_in_Date)={}'.format(a, Year))
                
            
    #Function - 3 : On the basis of Income from booking
def IncomeBasis():
    print()
    
    #Function - 4 : All the basis together
def AllBasis():
    print()
    
    
    
""" MENUS """

    ## Menu - 1 : PARKING MENU
def ParkingMenu():
    while True:
        print()  
        print('Parking Details :-')
        print()
        print('          1. Show Parking Details')
        print('          2. Add Parking Area')
        print('          3. Remove Parking')
        print('          4. Search for Parking')
        print('          5. Summary of the Parking')
        print('          6. Back to Main Menu(<<)')
        print()
        pmenu=int(input('    Enter any option from above -->'))
        
        if pmenu==1:
            ShowParkings()
        elif pmenu==2:
            AddParkings()
        elif pmenu==3:
            DeleteParking()
        elif pmenu==4:
            SearchParking()
        elif pmenu==5:
            SummaryOfParking()
        elif pmenu==6:
            break
        else:
            print('Invalid input, Please select valid input...')
            
    ## Menu - 2 : VEHICLE MENU
def VehicleMenu():
    while True:
        print()  
        print('Vehicle Details :-')
        print()
        print('          1. Show Vehicle Details')
        print('          2. Add Vehicle')
        print('          3. Update Vehicle Details')
        print('          4. Remove Vehicle')
        print('          5. Search for Vehicle')
        print('          6. Summary of the Vehicle')
        print('          7. Back to Main Menu(<<)')
        print()
        vmenu=int(input('    Enter any option from above -->'))
        
        if vmenu==1:
            ShowVehicle()
        elif vmenu==2:
            AddVehicle()
        elif vmenu==3:
            UpdateVehicle()
        elif vmenu==4:
            DeleteVehicle()
        elif vmenu==5:
            Searchvehicle()
        elif vmenu==6:
            SummaryOfVehicle()
        elif vmenu==7:
            break
        else:
            print('Invalid input, Please select valid input...')

    ## Menu - 2 : Booking MENU
def BookingMenu():
    while True:
        print()  
        print('Booking Details :-')
        print()
        print('          1. Show Current Booking Details')
        print('          2. Show Previous Booking Details')
        print('          3. Issue Of Parking Area')
        print('          4. Generate Bill')
        print('          5. Back to Main Menu(<<)')
        print()
        bmenu=int(input('    Enter any option from above -->'))
        
        if bmenu==1:
            ShowCurrentBooking()
        elif bmenu==2:
            ShowPreviousBooking()
        elif bmenu==3:
            IssueOfParkingArea()
        elif bmenu==4:
            GenerateBill()
        elif bmenu==5:
            break
        else:
            print('Invalid input, Please select valid input...')

    ## Menu - 4 : REPORT OF THE PARKING MANAGEMENT SYSTEM
def ReportMenu():
    while True:
        print()  
        print('Report Of The City Parking :-')
        print()
        print('          1. On the basis of vacancy')
        print('          2. On the basis of frequency of booking')
        print('          3. On the basis of Income from booking')  
        print('          4. All the basis together')
        print('          5. Back to Main Menu(<<)')
        print()
        reportmenu=int(input('    Enter any option from above -->'))
        
        if reportmenu==1:
            VacancyBasis()
        elif reportmenu==2:
            FrequencyBasis()
        elif reportmenu==3:
            IncomeBasis()
        elif reportmenu==4:
            AllBasis()
        elif reportmenu==5:
            break
        else:
            print('Invalid input, Please select valid input...')  


""" Main Menu of The Parking Management System"""

def MainMenu():
    while True:
        print()  
        print('Welcome To The City Parking :-')
        print()
        print('          1. Parking Details')
        print('          2. Vehicle Details')
        print('          3. Booking Details')
        print('          4. Report of the City Parking')
        print('          5. Exit')
        print()
        mainmenu=int(input('    Enter any option from above -->'))
        
        if mainmenu==1:
            ParkingMenu()
        elif mainmenu==2:
            VehicleMenu()
        elif mainmenu==3:
            BookingMenu()
        elif mainmenu==4:
            ReportMenu()
        elif mainmenu==5:
            print('Exiting...')
            break
        else:
            print('Invalid input, Please select valid input...')
MainMenu()
