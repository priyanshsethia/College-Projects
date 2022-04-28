'''Welcome To the Source Code of 'Hotel Management System'''
#   This application is developed by Kunal Jain, Priyansh Sethia & Riya Mahatma 
#   under the guidance of 'Mr. Sumit Sir' in 'Shri Jain Public School, Bikaner'. 

'''Source Code'''

##Some imported library which is used during coding
import mysql.connector as mtor
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

#Connect MySQL with Python, and show that it connect successfully or not
mycon=mtor.connect(host='localhost', user='root', passwd='')
if mycon.is_connected():
    print('Connected Successfully')

#Some Commands that helps in Run this Program in every PC that have Python & MySQL    
command=mycon.cursor()
command.execute('Create database if not exists Hotel_db')
command.execute('Use Hotel_db')

command.execute('Create table if not exists Guest_Info(GID int primary key,\
               GName char(30), Mobile_No bigint, ID_Proof char(20), ID_No bigint,\
               Nationality char(30), City char(20), Status char(20))')

command.execute('Create table if not exists Room_Info(Room_No int primary key,\
               Room_Type char(40), Charges int, IsVacant char(8))')

command.execute('Create table if not exists Room_Booking(BID char(8) primary key,\
               GID int, Room_No int , Check_in_Date date)')
command.execute('Alter table Room_Booking add foreign key(GID) references Guest_Info(GID),\
                add foreign key(Room_No) references Room_Info(Room_No)')

command.execute('Create table if not exists Previous_Booking(BID int primary key,\
               GID int, Room_No int, Check_in_Date date, Check_out_Date date, Stay int,\
               Amount int, GST int, Discount int, Net_Amount int)')
command.execute('Alter table Previous_Booking add foreign key(GID) references Guest_Info(GID),\
                add foreign key(Room_No) references Room_Info(Room_No)')

#Some pre-inserted rooms in the Table : Room_Info
while True:
    command.execute('Select * from Room_Info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        command.execute('Insert into Room_Info values(101, "Single Room", 1500, "Vacant"),\
                                                     (102, "Single Room", 1500, "Vacant"),\
                                                     (103, "Single Room", 1500, "Vacant"),\
                                                     (201, "Double Room", 2500, "Vacant"),\
                                                     (202, "Double Room", 2500, "Vacant"),\
                                                     (203, "Double Room", 2500, "Vacant"),\
                                                     (301, "Family Room", 3000, "Vacant"),\
                                                     (302, "Family Room", 3000, "Vacant"),\
                                                     (303, "Family Room", 3000, "Vacant"),\
                                                     (401, "Duplex Room", 5500, "Vacant"),\
                                                     (402, "Duplex Room", 5500, "Vacant"),\
                                                     (403, "Duplex Room", 5500, "Vacant"),\
                                                     (501, "Conference Room", 8500, "Vacant"),\
                                                     (502, "Conference Room", 8500, "Vacant"),\
                                                     (503, "Conference Room", 8500, "Vacant"),\
                                                     (601, "Inter-Connecting Room", 6000, "Vacant"),\
                                                     (602, "Inter-Connecting Room", 6000, "Vacant"),\
                                                     (603, "Inter-Connecting Room", 6000, "Vacant")')
        mycon.commit()
    else:
        break


'''FUNCTIONS USED IN DIFFERENT MENUS'''

##Functions of Guest Menu

    #Function : 1 - Show Guests
def ShowGuest():
    print()
    print('**********************************************************')
    print('Guest details are : ')
    print('__________________________________________________________')
    print()
    command.execute('select * from Guest_Info')
    gdetails=command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print('No Guest Records Available.')
    else:
        dfgdetails=pd.DataFrame(gdetails, columns=['Guest ID', 'Guest Name', 'Mobile No', 'ID Proof', 'ID No', 'Nationality', 'City', 'Status'])
        print(dfgdetails.to_string(index=False))
    print('**********************************************************')

    #Function : 2 - Adding Guest    
def AddGuest():
    print()
    print('**********************************************************')
    print('Adding Guests...')
    print('__________________________________________________________')
    print()
    GID=int(input('Guest ID -->'))
    while True:
        command.execute('Select * from Guest_Info where GID={}'.format(GID,))
        command.fetchall()
        cnt=command.rowcount
        if cnt>=1:
            print('Guest ID '+str(GID)+' is already exist...')
            GID=int(input('Again Enter Guest ID -->'))
        else:
            break
    GName=input('Guest Name-->')
    Mobile_No=int(input('Mobile No. -->'))
    print()
    print('Identification type are :')
    print('     1. Aadhar Card')
    print('     2. Passport')
    print('     3. PAN Card')
    print('     4. Driving Licence')
    ID_Proof=int(input('Choose any Identification type :'))
    while True:
        idtype=''
        if ID_Proof<=0 or ID_Proof>=5:            
            print('Invalid input, Please select valid input...')
            ID_Proof=int(input('Again choose any Identification type :'))
        else:       
            if ID_Proof==1:
                idtype='Aadhar Card'
            elif ID_Proof==2:
                idtype='Passport'
            elif ID_Proof==3:
                idtype='PAN Card'
            elif ID_Proof==4:
                idtype='Driving Licence'
            break
    ID_No=int(input('ID Number -->'))    
    print()
    print('Which type of nationality do you have :')
    print('     1. Indian')
    print('     2. Foreigner')
    Nationality=int(input('Choose nationality type -->'))
    while True:
        ntype=''
        if Nationality<=0 or Nationality>=3:
            print('Invalid input, Please select valid input...')
            Nationality=int(input('Again choose nationality type -->'))
        else:
            if Nationality==1:
                ntype='Indian'
            elif Nationality==2:
                ntype='Foreigner'
            break
    City=input('City Name -->') 
    print()
    print('Which type of Marital Status do you have :')
    print('     1. Married')
    print('     2. Unmarried')
    Status=int(input('Choose Marital Status type -->'))
    while True:
        stype=''
        if Status<=0 or Status>=3:
            print('Invalid input, Please select valid input...')
            Status=int(input('Again choose Marital Status type -->'))
        else:
            if Status==1:
                stype='Married'
            elif Status==2:
                stype='Unmarried'
            break

    command.execute('Insert into Guest_Info values({}, "{}", {}, "{}", {}, "{}", "{}", "{}")'.format(GID, GName, Mobile_No, idtype, ID_No, ntype, City, stype))
    mycon.commit()
    print()
    print('__________________________________________________________')
    print()
    print('Guest Add Successfully...')
    print()
    print('**********************************************************')
    
    #Function : 3 - Update Guest Details
def UpdateGuestDetails():
    command.execute('Select * from Guest_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Guest is Available to Update.')
        print()
        print('**********************************************************')
    else:
        print()
        print('**********************************************************')
        ShowGuest()
        print('__________________________________________________________')
        print()
        print('Updating Guest Details...')
        print('__________________________________________________________')
        print()   
        print('Enter Update Field Type : ')
        print('     1. By Guest ID')
        print('     2. By Guest Name')
        UpdateGuestCmd=int(input('Select type to update Guest Details -->'))
        while True:
            if UpdateGuestCmd<=0 or UpdateGuestCmd>=3:
                print('Invalid input, Please select valid input...')
                UpdateGuestCmd=int(input('Again select type to update Guest Details -->'))
            
            else:
                if UpdateGuestCmd==1:
                    GID=int(input('Enter Guest ID of the Guest for update -->'))
                    while True:
                        command.execute('Select * from Guest_Info where GID={}'.format(GID,))
                        command.fetchall()
                        cnt=command.rowcount
                        if cnt==0:
                            print('Guest ID '+str(GID)+' is not found...')
                            GID=int(input('Again Enter Guest ID -->'))
                        else:
                            break
                    GName=input('Guest Name-->')
                    Mobile_No=int(input('Mobile No. -->'))
                    print()
                    print('Identification type are :')
                    print('     1. Aadhar Card')
                    print('     2. Passport')
                    print('     3. PAN Card')
                    print('     4. Driving Licence')
                    ID_Proof=int(input('Choose any Identification type :'))
                    while True:
                        idtype=''
                        if ID_Proof<=0 or ID_Proof>=5:            
                            print('Invalid input, Please select valid input...')
                            ID_Proof=int(input('Again choose any Identification type :'))
                        else:       
                            if ID_Proof==1:
                                idtype='Aadhar Card'
                            elif ID_Proof==2:
                                idtype='Passport'
                            elif ID_Proof==3:
                                idtype='PAN Card'
                            elif ID_Proof==4:
                                idtype='Driving Licence'
                            break
                    ID_No=int(input('ID Number -->'))    
                    print()
                    print('Which type of nationality do you have :')
                    print('     1. Indian')
                    print('     2. Foreigner')
                    Nationality=int(input('Choose nationality type -->'))
                    while True:
                        ntype=''
                        if Nationality<=0 or Nationality>=3:
                            print('Invalid input, Please select valid input...')
                            Nationality=int(input('Again choose nationality type -->'))
                        else:
                            if Nationality==1:
                                ntype='Indian'
                            elif Nationality==2:
                                ntype='Foreigner'
                            break
                    City=input('City Name -->') 
                    print()
                    print('Which type of Marital Status do you have :')
                    print('     1. Married')
                    print('     2. Unmarried')
                    Status=int(input('Choose Marital Status type -->'))
                    while True:
                        stype=''
                        if Status<=0 or Status>=3:
                            print('Invalid input, Please select valid input...')
                            Status=int(input('Again choose Marital Status type -->'))
                        else:
                            if Status==1:
                                stype='Married'
                            elif Status==2:
                                stype='Unmarried'
                            break
                        
                    command.execute('Update Guest_Info set GName="{}", Mobile_No={}, ID_Proof="{}", ID_No={}, Nationality="{}", City="{}", Status="{}" where GID={}'.format(GName, Mobile_No, idtype, ID_No, ntype, City, stype, GID))
                    mycon.commit()
                    print()
                    print('__________________________________________________________')
                    print()
                    print('Guest Details Update Successfully...')
                    print()
                    print('**********************************************************')
                    
                elif UpdateGuestCmd==2:
                    GName=input('Enter Guest Name for update -->')
                    while True:
                        command.execute('Select * from Guest_Info where GName="{}"'.format(GName,))
                        command.fetchall()
                        cnt=command.rowcount
                        if cnt==0:
                            print('Guest Name '+GName+' is not found...')
                            GName=input('Again Enter Guest Name -->')
                        else:
                            break
                    Name=input('Enter old or new name of Guest -->')
                    Mobile_No=int(input('Mobile No. -->'))
                    print()
                    print('Identification type are :')
                    print('     1. Aadhar Card')
                    print('     2. Passport')
                    print('     3. PAN Card')
                    print('     4. Driving Licence')
                    ID_Proof=int(input('Choose any Identification type :'))
                    while True:
                        idtype=''
                        if ID_Proof<=0 or ID_Proof>=5:            
                            print('Invalid input, Please select valid input...')
                            ID_Proof=int(input('Again choose any Identification type :'))
                        else:       
                            if ID_Proof==1:
                                idtype='Aadhar Card'
                            elif ID_Proof==2:
                                idtype='Passport'
                            elif ID_Proof==3:
                                idtype='PAN Card'
                            elif ID_Proof==4:
                                idtype='Driving Licence'
                            break
                    ID_No=int(input('ID Number -->'))    
                    print()
                    print('Which type of nationality do you have :')
                    print('     1. Indian')
                    print('     2. Foreigner')
                    Nationality=int(input('Choose nationality type -->'))
                    while True:
                        ntype=''
                        if Nationality<=0 or Nationality>=3:
                            print('Invalid input, Please select valid input...')
                            Nationality=int(input('Again choose nationality type -->'))
                        else:
                            if Nationality==1:
                                ntype='Indian'
                            elif Nationality==2:
                                ntype='Foreigner'
                            break
                    City=input('City Name -->') 
                    print()
                    print('Which type of Marital Status do you have :')
                    print('     1. Married')
                    print('     2. Unmarried')
                    Status=int(input('Choose Marital Status type -->'))
                    while True:
                        stype=''
                        if Status<=0 or Status>=3:
                            print('Invalid input, Please select valid input...')
                            Status=int(input('Again choose Marital Status type -->'))
                        else:
                            if Status==1:
                                stype='Married'
                            elif Status==2:
                                stype='Unmarried'
                            break
                        
                    command.execute('Update Guest_Info set GName="{}", Mobile_No={}, ID_Proof="{}", ID_No={}, Nationality="{}", City="{}", Status="{}" where GName="{}"'.format(Name, Mobile_No, idtype, ID_No, ntype, City, stype, GName))
                    mycon.commit()
                    print()
                    print('__________________________________________________________')
                    print()
                    print('Guest Details Update Successfully...')
                    print()
                    print('**********************************************************')
                break
            
    #Function : 4 - Removing Guest
def RemoveGuest():
    command.execute('Select * from Guest_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Guest is Available to Delete.')
        print()
        print('**********************************************************')
    else:
        print()
        print('**********************************************************')
        ShowGuest()
        print('__________________________________________________________')
        print()
        print('Deleting Guest Details...')
        print('__________________________________________________________')
        print()   
        print('Enter Delete Field Type : ')
        print('     1. By Guest ID')
        print('     2. By Guest Name')
        DeleteGuestCmd=int(input('Select type to delete Guest deatils -->'))
        while True:
            if DeleteGuestCmd<=0 or DeleteGuestCmd>=3:
                print('Invalid input, Please select valid input...')
                DeleteGuestCmd=int(input('Again select type to delete Guest Details -->'))
            
            else:
                if DeleteGuestCmd==1:
                    GID=int(input('Enter Guest ID of the Guest for delete -->'))
                    while True:
                        command.execute('Select * from Guest_Info where GID={}'.format(GID,))
                        command.fetchall()
                        cnt=command.rowcount
                        if cnt==0:
                            print('Guest ID '+str(GID)+' is not found...')
                            GID=int(input('Again Enter Guest ID -->'))
                        else:
                            command.execute('Delete from Guest_Info where GID={}'.format(GID,))
                            mycon.commit()
                            print()
                            print('__________________________________________________________')
                            print()
                            print('Guest Details Deleted Successfully...')
                            print()
                            print('**********************************************************') 
                            break
                                                   
                elif DeleteGuestCmd==2:
                    GName=input('Enter Guest Name for delete -->')
                    while True:
                        command.execute('Select * from Guest_Info where GName="{}"'.format(GName,))
                        command.fetchall()
                        cnt=command.rowcount
                        if cnt==0:
                            print('Guest Name '+GName+' is not found...')
                            GName=input('Again Enter Guest Name -->')
                        else:
                            command.execute('Delete from Guest_Info where GName="{}"'.format(GName,))
                            mycon.commit()
                            print()
                            print('__________________________________________________________')
                            print()
                            print('Guest Details Deleted Successfully...')
                            print()
                            print('**********************************************************')
                            break
                break
                
    #Function : 5 - Search for Guest
def SearchGuest():
    command.execute('Select * from Guest_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Guest is Available to Search.')
        print()
        print('**********************************************************')
    else:
        print()
        print('**********************************************************')
        print('Searching for Guest...')
        print('__________________________________________________________')
        print()   
        print('Enter Search Field Type : ')
        print('     1. By Guest ID')
        print('     2. By Guest Name')
        SearchGuestCmd=int(input('Select type to search Guest deatils -->'))
        while True:
            if SearchGuestCmd<=0 or SearchGuestCmd>=3:
                print('Invalid input, Please select valid input...')
                SearchGuestCmd=int(input('Again select type to Guest Details -->'))
            
            else:
                if SearchGuestCmd==1:
                    GID=int(input('Enter Guest ID to search the Guest -->'))
                    command.execute('Select * from Guest_Info where GID={}'.format(GID,))
                    command.fetchall()
                    cnt=command.rowcount
                    if cnt>=1:
                        print()
                        print('Guest Detail is : ')
                        print()
                        print('__________________________________________________________')
                        print()
                        command.execute('Select * from Guest_Info where GID={}'.format(GID,))
                        gdetail=command.fetchall()
                        dfgdetail=pd.DataFrame(gdetail, columns=['Guest ID', 'Guest Name', 'Mobile No', 'ID Proof', 'ID No', 'Nationality', 'City', 'Status'])
                        print(dfgdetail.to_string(index=False))
                        print()
                        print('**********************************************************')
                    else:
                        print()
                        print('__________________________________________________________')
                        print()
                        print('Guest No. ',str(GID), ' is not found...' )
                        print()
                        print('**********************************************************')        
                        
                elif SearchGuestCmd==2:
                    GName=input('Enter Guest Name to search the Guest -->')
                    command.execute('Select * from Guest_Info where GName like "%{}%"'.format(GName,))
                    command.fetchall()
                    cnt=command.rowcount
                    if cnt>=1:
                        print()
                        print('Guest Detail is : ')
                        print()
                        print('__________________________________________________________')
                        print()
                        command.execute('Select * from Guest_Info where Gname like "%{}%"'.format(GName,))
                        gdetail=command.fetchall()
                        dfgdetail=pd.DataFrame(gdetail, columns=['Guest ID', 'Guest Name', 'Mobile No', 'ID Proof', 'ID No', 'Nationality', 'City', 'Status'])
                        print(dfgdetail.to_string(index=False))
                        print()    
                        print('**********************************************************')
                    else:
                        print()
                        print('__________________________________________________________')
                        print()
                        print('Guest Name ',GName, ' is not found...' )
                        print() 
                        print('**********************************************************')
                break
                    
    #Function : 6 - Summary of Guest
def SummaryOfGuest():
    print()
    print('**********************************************************')
    print('Summary of Guests...')
    print('__________________________________________________________')
    print()
    command.execute('Select * from Guest_Info')
    command.fetchall()
    noofguest=command.rowcount
    print(' >>> Total No. of Guest in our Hotel  :  ', noofguest)
    print()
    print(' >>> No. of Guest Nationality wise :- ')
    command.execute('Select * from Guest_Info where Nationality="Indian"')
    command.fetchall()
    noofindian=command.rowcount
    print('          Indian  :  ', noofindian)
    command.execute('Select * from Guest_Info where Nationality="Foreigner"')
    command.fetchall()
    noofforeigner=command.rowcount
    print('          Foreigner  :  ', noofforeigner)
    print()
    print(' >>> No. of Guest Marital Status wise :- ')
    command.execute('Select * from Guest_Info where Status="Married"')
    command.fetchall()
    noofmarried=command.rowcount
    print('          Married  :  ', noofmarried)
    command.execute('Select * from Guest_Info where Status="Unmarried"')
    command.fetchall()
    noofunmarried=command.rowcount
    print('          Unmarried  :  ', noofunmarried)
    print()
    print(' >>> No. of Guest City wise :- ')
    command.execute('Select City, count(*) as "No. of Guest" from Guest_Info group by City')
    noofguestbyciities=command.fetchall()
    dfnoofcities=pd.DataFrame(noofguestbyciities, columns=['City', 'No. of Guest'])
    print(dfnoofcities.to_string(index=False))
    print()
    print('**********************************************************')


##Functions of Room Menu

    #Function : 1 - Show Rooms
def ShowRoom():
    print()
    print('**********************************************************')
    print('Room Details are : ')
    print('__________________________________________________________')
    print()
    command.execute('select * from Room_Info')
    rdetails=command.fetchall()
    if cnt==0:
        print('No Guest Records Available.')
    else:
        dfrdetails=pd.DataFrame(rdetails, columns=['Room No', 'Room Type', 'Charges', 'IsVacant'])
        print(dfrdetails.to_string(index=False))
    print('**********************************************************')

    #Function : 2 - Adding New Room
def AddRoom():
    print()
    print('**********************************************************')
    print('Adding Room...')
    print('__________________________________________________________')
    print()
    Room_No=int(input('Room No -->'))
    while True:
        command.execute('Select * from Room_Info where Room_No={}'.format(Room_No,))
        command.fetchall()
        cnt=command.rowcount
        if cnt>=1:
            print('Room No. '+str(Room_No)+' is already exist...')
            Room_No=int(input('Again Enter Room No. -->'))
        else:
            break
    print()
    print('Room types are :')
    print('     1. Single Room (Charges(per day) = Rs. 1500)')
    print('     2. Double Room (Charges(per day) = Rs. 2500)')
    print('     3. Family Room (Charges(per day) = Rs. 3000)')
    print('     4. Duplex Room (Charges(per day) = Rs. 5500)')
    print('     5. Conference Room (Charges(per day) = Rs. 8500)')
    print('     6. Inter-Connecting Room (Charges(per day) = Rs. 6000)')
    print()
    Room_Type=int(input('Choose any Room type :'))
    while True:
        if Room_Type<=0 and Room_Type>=7:
            print('Invalid input, Please select valid input...')
            Room_Type=int(input('Again choose any Room type :'))
        else:
            rtype=''
            Charges=0
            if Room_Type==1:
                rtype='Single Room'
                Charges=1500
            elif Room_Type==2:
                rtype='Double Room'
                Charges=2500
            elif Room_Type==3:
                rtype='Family Room'
                Charges=3000
            elif Room_Type==4:
                rtype='Duplex Room'
                Charges=5500
            elif Room_Type==5:
                rtype='Conference Room'
                Charges=8500
            elif Room_Type==6:
                rtype='Inter-Connecting Room'
                Charges=6000
            break
                
    command.execute('Insert into Room_Info values({}, "{}", {}, "Vacant")'.format(Room_No, rtype, Charges))
    mycon.commit()
    print()
    print('__________________________________________________________')
    print()
    print('Room Add Successfully...')
    print()
    print('**********************************************************')

    #Function : 3 - Update Room Details
def UpdateRoomDetails():
    command.execute('Select * from Room_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Room is Available to Update.')
        print()
        print('**********************************************************')
    else:
        print()
        print('**********************************************************')
        print('Updating Room Details...')
        print('__________________________________________________________')
        print()
        Room_No=int(input('Enter Room No to Update Room Details -->'))
        while True:
            command.execute('Select * from Room_Info where Room_No={}'.format(Room_No,))
            command.fetchall()
            cnt=command.rowcount
            if cnt==0:
                print('Room No. '+str(Room_No)+' is not exist...')
                Room_No=int(input('Again Enter Room No. -->'))
            else:
                break
        print()
        print('Room types are :')
        print('     1. Single Room (Charges(per day) = Rs. 1500)')
        print('     2. Double Room (Charges(per day) = Rs. 2500)')
        print('     3. Family Room (Charges(per day) = Rs. 3000)')
        print('     4. Duplex Room (Charges(per day) = Rs. 5500)')
        print('     5. Conference Room (Charges(per day) = Rs. 8500)')
        print('     6. Inter-Connecting Room (Charges(per day) = Rs. 6000)')
        print()
        Room_Type=int(input('Choose any Room type :'))
        while True:
            if Room_Type<=0 and Room_Type>=7:
                print('Invalid input, Please select valid input...')
                Room_Type=int(input('Again choose any Room type :'))
            else:
                rtype=''
                Charges=0
                if Room_Type==1:
                    rtype='Single Room'
                    Charges=1500
                elif Room_Type==2:
                    rtype='Double Room'
                    Charges=2500
                elif Room_Type==3:
                    rtype='Family Room'
                    Charges=3000
                elif Room_Type==4:
                    rtype='Duplex Room'
                    Charges=5500
                elif Room_Type==5:
                    rtype='Conference Room'
                    Charges=8500
                elif Room_Type==6:
                    rtype='Inter-Connecting Room'
                    Charges=6000
                break
                    
        command.execute('Update Room_Info set Room_type="{}", Charges={} where Room_No={}'.format(rtype, Charges, Room_No))
        mycon.commit()
        print()
        print('__________________________________________________________')
        print()
        print('Room Details Updating Successfully...')
        print()
        print('**********************************************************')

    #Function : 4 - Removing Room
def RemoveRoom():
    command.execute('Select * from Room_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Room is Available to Delete.')
        print()
        print('**********************************************************')
    else:
        print()
        print('**********************************************************')
        ShowRoom()
        print('__________________________________________________________')
        print()
        print('Deleting Room Details...')
        print('__________________________________________________________')
        print()   
        Room_No=int(input('Enter Room No for delete the room -->'))
        while True:
            command.execute('Select * from Room_Info where Room_No={}'.format(Room_No,))
            command.fetchall()
            cnt=command.rowcount
            if cnt==0:
                print('Room No. '+str(Room_No)+' is not found...')
                Room_No=int(input('Again Enter Room No -->'))
            else:
                command.execute('Delete from Room_Info where Room_No={}'.format(Room_No,))
                mycon.commit()
                print()
                print('__________________________________________________________')
                print()
                print('Room Details Deleted Successfully...')
                print()
                print('**********************************************************') 
                break
                
    #Function : 5 - Search for Room
def SearchRoom():
    command.execute('Select * from Room_info')
    command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print()
        print('No Room is Available to Delete.')
        print()
        print('**********************************************************')
    else:
        print()
        Room_No=int(input('Enter Room No for search the room -->'))
        command.execute('Select * from Room_Info where Room_No={}'.format(Room_No,))
        command.fetchall()
        cnt=command.rowcount
        if cnt>=1:
            print()
            print('Room Detail is : ')
            print()
            print('__________________________________________________________')
            print()
            command.execute('Select * from Room_Info where Room_No={}'.format(Room_No,))
            rdetail=command.fetchall()
            dfrdetail=pd.DataFrame(rdetail, columns=['Room No', 'Room Type', 'Charges', 'IsVacant'])
            print(dfrdetail.to_string(index=False))
            print()
            print('**********************************************************')
        else:
            print()
            print('__________________________________________________________')
            print()
            print('Room No. ',str(Room_No), ' is not found...' )
            print()
            print('**********************************************************') 
        
    #Function : 6 - Summary of Guest
def SummaryOfRoom():
    print()
    print('**********************************************************')
    print('Summary of Rooms...')
    print('__________________________________________________________')
    print()
    command.execute('Select * from Room_Info')
    command.fetchall()
    noofguest=command.rowcount
    print(' >>> Total No. of Room in our Hotel  :  ', noofguest)
    print()
    
    print(' >>> No. of Room type wise :- ')
    command.execute('Select * from Room_Info where Room_Type="Single Room"')
    command.fetchall()
    noofsingle=command.rowcount
    print('          Single Room            :  ', noofsingle)
    command.execute('Select * from Room_Info where Room_Type="Double Room"')
    command.fetchall()
    noofdouble=command.rowcount
    print('          Double Room            :  ', noofdouble)
    command.execute('Select * from Room_Info where Room_Type="Family Room"')
    command.fetchall()
    nooffamily=command.rowcount
    print('          Family Room            :  ', nooffamily)
    command.execute('Select * from Room_Info where Room_Type="Duplex Room"')
    command.fetchall()
    noofduplex=command.rowcount
    print('          Duplex Room            :  ', noofduplex)
    command.execute('Select * from Room_Info where Room_Type="Conference Room"')
    command.fetchall()
    noofconference=command.rowcount
    print('          Conference Room        :  ', noofconference)
    command.execute('Select * from Room_Info where Room_Type="Inter-Connecting Room"')
    command.fetchall()
    noofintcon=command.rowcount
    print('          Inter-Connecting Room  :  ', noofintcon)
    print()
    
    print(' >>> No. of Room Vacancy wise :- ')
    command.execute('Select * from Room_Info where IsVacant="Vacant"')
    command.fetchall()
    noofvacant=command.rowcount
    print('          Vacant Room  :  ', noofvacant)
    command.execute('Select * from Room_Info where IsVacant="Booked"')
    command.fetchall()
    noofbook=command.rowcount
    print('          Booked Room  :  ', noofbook)
    print()
    print('**********************************************************')


##Functions of Booking Menu

    #Function : 1 - Show Current Booking Details
def ShowCurrentBooking():
    print()
    print('**********************************************************')
    print('Current Booking Details are : ')
    print('__________________________________________________________')
    print()
    command.execute('select * from Room_Booking')
    bdetails=command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print('No Bookings are Available.')
    else:
        dfbdetails=pd.DataFrame(bdetails, columns=['Booking ID', 'Guest ID', 'Room No', 'Check in Date'])
        print(dfbdetails.to_string(index=False))
    print('**********************************************************')

    #Function : 2 - Show Previous Booking Details
def ShowPreviousBooking():
    print()
    print('**********************************************************')
    print('Previous Booking Details are : ')
    print('__________________________________________________________')
    print()
    command.execute('select * from Previous_Booking')
    bdetails=command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print('No Previous Bookings are Available.')
    else:
        dfbdetails=pd.DataFrame(bdetails, columns=['Booking ID', 'Guest ID', 'Room No', 'Check in Date', 'Check out Date', 'Stay', 'Amount', 'GST', 'Discount', 'NetAmount'])
        print(dfbdetails.to_string(index=False))
    print('**********************************************************')
    
    #Function : 3 - Booking of a Room
def BookingRoom():
    print()
    print('**********************************************************')
    print('Booking of Room...')
    print('__________________________________________________________')
    print()
    BID=int(input('Booking ID > '))
    while True:
        command.execute('Select * from Room_Booking where BID={}'.format(BID))
        command.fetchall()
        cnt=command.rowcount
        if cnt>=1:
            print('Booking ID ',BID, ' already exist...')
            BID=int(input('Again Enter Booking ID >'))
        else:
            break   
    print()
    print('**********************************************************')
    print('Availability of Rooms...')
    print('__________________________________________________________')
    print()
    command.execute('Select Room_No, Room_Type from Room_info where IsVacant like "%Vacant%" order by Room_No')
    data=command.fetchall()
    cnt=command.rowcount
    if cnt==0:
        print()
        print('**********************************************************')
        print('No Rooms are Available... ')
        print('__________________________________________________________')
        print()
    else:
        print()
        print('**************************************************')
        print('Available Rooms are :-')
        print('**************************************************')
        print()
        df=pd.DataFrame(data, columns=['Room No.', 'Room Type'])
        print(df.to_string(index=False))
        print()
    
    Room_No=int(input('Enter Room_No > '))
    while True:
        command.execute('Select * from Room_Info where Room_No={}'.format(Room_No))
        command.fetchall()
        cnt=command.rowcount
        if cnt==0:
            print('Room No. ',str(Room_No), ' not exist...')
            Room_No=int(input('Again enter Room No > '))
        if cnt>=1:           
            while True:
                command.execute('Select * from Room_Info where IsVacant like "%Booked%" and Room_No={}'.format(Room_No))
                command.fetchall()
                cnt=command.rowcount
                if cnt>=1:
                    print('Room No. ', str(Room_No), ' is already Booked.')
                    Room_No=int(input('Again enter Room No > '))
                else:
                    break
        else:
            break
        
    GID=int(input('Guest ID > '))
    while True:
        command.execute('Select * from Guest_Info where GID={}'.format(GID))
        command.fetchall()
        cnt=command.rowcount
        if cnt==0:
            print('Guest ID ',GID, ' not exist...')
            GID=int(input('Again Enter Guest ID >'))
        else:
            break
    Check_in_Date=input('Check in Date (YYYY-MM-DD) > ')
    
    command.execute('Insert into Room_Booking(BID, GID, Room_No, Check_in_Date) values({}, {}, "{}", "{}")'.format(BID, GID, Room_No, Check_in_Date))
    mycon.commit()
    command.execute('Insert into Previous_Booking(BID, GID, Room_No, Check_in_Date) values({}, {}, "{}", "{}")'.format(BID, GID, Room_No, Check_in_Date))
    mycon.commit()
    
    command.execute('Update Room_Info set IsVacant="Booked" where Room_No={}'.format(Room_No))
    mycon.commit()
    
    command.execute('Select GName from Guest_Info where GID={}'.format(GID))
    data=command.fetchone()
    for Name in data:
        GName=Name
    print('Room No. ',Room_No, ' booked successfully for Guest ', GName, '...')
    print()
    print('**********************************************************')
        
    #Function : 4 - Generate Bill
def BillGenerate():
    print()
    print('**********************************************************')
    print('Gebaerating Bill...')
    print('__________________________________________________________')
    print()
    BID=int(input('Booking ID > '))
    while True:
        command.execute('Select * from Room_Booking where BID={}'.format(BID))
        command.fetchall()
        cnt=command.rowcount
        if cnt==0:
            print('Booking ID ',BID, ' not exist...')
            BID=int(input('Again Enter Booking ID >'))
        else:
            break   
        
    print()
    print('__________________________________________________________')
    command.execute('Select BID, GID, Room_No, Check_in_Date from Room_Booking where BID={}'.format(BID))
    data=command.fetchall()
    df=pd.DataFrame(data, columns=['Booking ID', 'Guest ID', 'Room No.', 'Check in Date'])
    print(df.to_string(index=False))
    print('__________________________________________________________')
    
    Check_out_Date=input('Check out Date (YYYY-MM-DD) > ')
    command.execute('Update Previous_Booking set Check_out_Date="{}" where BID={}'.format(Check_out_Date, BID))
    mycon.commit()
    while True:
        command.execute('Select DateDiff(Check_out_Date, Check_in_Date) from Previous_Booking where BID={}'.format(BID))
        data=command.fetchone()
        for a in data:
            Stay=a
        if Stay<0:
            print("Invalid Check out date, it can't be less than check in date...")
            Check_out_Date=input('Again Check out Date (YYYY-MM-DD) > ')
            command.execute('Update Previous_Booking set Check_out_Date="{}" where BID={}'.format(Check_out_Date, BID))
            mycon.commit()
        if Stay>=0:
            Stay=Stay+1
            break
    
    command.execute('Select ri.Charges from Room_Info ri, Room_Booking rb where ri.Room_No=rb.Room_No and BID={}'.format(BID))
    data=command.fetchone()
    for ch in data:
        Charges=ch
    
    Amount=Stay*Charges
    GST=Amount*(12/100)
    Discount=(Amount+GST)*(5/100)
    Net_Amount=Amount+GST-Discount
    
    command.execute('Update Previous_Booking set Stay={}, Amount={}, GST={}, Discount={}, Net_Amount={} where BID={}'.format(Stay, Amount, GST, Discount, Net_Amount, BID))
    mycon.commit()
    command.execute('Update Room_Info set IsVacant="Vacant" where (Select Room_No from Room_Booking where BID={})'.format(BID))
    mycon.commit()
    command.execute('Delete from Room_Booking where BID={}'.format(BID))
    mycon.commit()
    
    command.execute('Select Room_No from Previous_Booking where BID={}'.format(BID))
    data=command.fetchone()
    for a in data:
        Room_No=a
    
    command.execute('Select Room_Type from Room_Info where Room_No={}'.format(Room_No))
    data=command.fetchone()
    for a in data:
        Room_Type=a
    
    command.execute('Select GID from Previous_Booking where BID={}'.format(BID))
    data=command.fetchone()
    for a in data:
        GID=a
    
    command.execute('Select GName from Guest_Info  where GID="{}"'.format(GID))
    data=command.fetchone()
    for a in data:
        GName=a

    command.execute('Select Check_in_Date from Previous_Booking where BID={}'.format(BID))
    data=command.fetchone()
    for a in data:
        Check_In_Date=a

    command.execute('Select Check_out_Date from Previous_Booking where BID={}'.format(BID))
    data=command.fetchone()
    for a in data:
        Check_Out_Date=a
    
    print()
    print()
    print('*'*50)
    print('                   HOTEL MAHARAJA')
    print('            (Opp. Bikaner Railway Station)')
    print('_'*50)
    print('_'*50)
    print()
    print()
    print('                 Billing Receipt :-')
    print('              _______________________')
    print()
    print('          Booking ID           :           ', BID)
    print('          Room No              :           ', Room_No)
    print('          Room Type            :           ', Room_Type)
    print('          Guest ID             :           ', GID)
    print('          Guest Name           :           ', GName)
    print('    From    ', Check_In_Date, '    To    ', Check_Out_Date)
    print('          No. of Stay          :           ', Stay)
    print('          Charges (per Room)   :           ', Charges)
    print('          Amount               :           ', Amount)
    print('          GST (@ 12 %)         :           ', GST)
    print('          Discount (@ 5 %)     :           ', Discount)
    print()
    print('                                 Net Amount          :           ', Net_Amount)
    print()
    print('          ___________________________________________')
    print()
    print('                Thanks for Stay in our Hotel &')
    print('              Enjoy the Feeling of "MAHARAJAS" !')
    print('          ___________________________________________')    
    print()
    print()
    print('**********************************************************')
    print()
    
## FUNCTIONS OF REPORT MENU

    #Function - 1 : On the basis of vacancy
def Report_VacancyBasis():
    print()
    print('**********************************************************')
    print('Report of the Hotel Maharaja')
    print('__________________________________________________________')
    print()
    command.execute('Select IsVacant from Room_Info where IsVacant like "%Booked%"')
    command.fetchall()
    BookedRoom=command.rowcount
    command.execute('Select IsVacant from Room_Info where IsVacant like "%vacant%"')
    command.fetchall()
    VacantRoom=command.rowcount
    
    x=[BookedRoom, VacantRoom]
    y=np.arange(2)
    pl.bar(y,x, color=['g', 'orange'], width=0.5)
    pl.xticks(y, ['Booked', 'Vacant'])
    pl.title('Report of Hotel on the Basis of Vacancies of Room')
    pl.xlabel('Types of Vacancy')
    pl.ylabel('No. of Rooms')
    pl.show()
    
    print('Total No. of Room ',BookedRoom+VacantRoom, 'out of which : ' )
    print(' >>> Booked     :     ', BookedRoom)
    print(' >>> Vacant     :     ', VacantRoom)
    print('**********************************************************')
    
    #Function - 2 : On the basis of frequency of booking
def Report_FrequencyOfBooking():
    print()
    print('**********************************************************')
    print('Report of the Hotel Maharaja')
    print('__________________________________________________________')
    print()
    Year=int(input('Enter Year --> '))
    while True:
        command.execute('Select * from Previous_Booking where Year(Check_in_Date)={}'.format(Year,))
        command.fetchall()
        cnt=command.rowcount
        if cnt<=0:
            print('Bookings of Year ', str(Year), ' not available...')
            Year=int(input('Again enter Year --> '))
        else:
            li=[]
            clrs=['m', 'olive', 'r', 'tan', 'g', 'burlywood', 'b', 'gold', 'y', 'c', 'k', 'b']
            month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            count=0
            for a in range(1, 13):
                command.execute('Select count(Check_in_Date) from Previous_Booking where Month(Check_in_Date)={} and Year(Check_in_Date)={}'.format(a, Year))
                data=command.fetchone()[0]
                if data==None:
                    count=0
                    li.append(count)
                else:
                    count=int(data)
                    li.append(count)
            df=pd.DataFrame(li, index=month, columns=['No. of Bookings'])
            print()
            pl.bar(month, df['No. of Bookings'], color=clrs)
            pl.xlabel('Months')
            pl.ylabel('Total No. of Room Bookings (acc. to months) ')
            pl.title('Report of Hotel on the Basis of Frequency of Room Bookings')
            pl.show()
            
            command.execute('Select count(Check_in_Date) from Previous_Booking where Year(Check_in_Date)={}'.format(Year,))
            data=command.fetchone()[0]
            TBooking=int(data)
            print('Total Booking in Year ', Year, ' is : ', TBooking)
            break
            print('**********************************************************')    
        
    #Function - 3 : On the basis of Income from booking
def Report_IncomeFromBooking():
    print()
    print('**********************************************************')
    print('Report of the Hotel Maharaja')
    print('__________________________________________________________')
    print()
    Year=int(input('Enter Year --> '))
    while True:
        command.execute('Select * from Previous_Booking where Year(Check_in_Date)={}'.format(Year,))
        command.fetchall()
        cnt=command.rowcount
        if cnt<=0:
            print('Bookings of Year ', str(Year), ' not available...')
            Year=int(input('Again enter Year --> '))
        else:
            li=[]
            clrs=['m', 'olive', 'r', 'tan', 'g', 'burlywood', 'b', 'gold', 'y', 'c', 'k', 'b']
            month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            count=0
            for a in range(1, 13):
                command.execute('Select sum(Net_Amount) from Previous_Booking where Month(Check_in_Date)={} and Year(Check_in_Date)={}'.format(a, Year))
                data=command.fetchone()[0]
                if data==None:
                    count=0
                    li.append(count)
                else:
                    count=int(data)
                    li.append(count)
            df=pd.DataFrame(li, index=month, columns=['Total Income'])
            print()
            pl.bar(month, df['Total Income'], color=clrs)
            pl.xlabel('Months')
            pl.ylabel('Total Income (acc. to months) ')
            pl.title('Report of Hotel on the Basis of Income from Bookings')
            pl.show()
            
            command.execute('Select sum(Net_Amount) from Previous_Booking where Year(Check_in_Date)={}'.format(Year,))
            data=command.fetchone()[0]
            TIncome=int(data)
            print('Total Income in Year ', Year, ' is : Rs. ', TIncome)
            break
            print('**********************************************************')
                    
    
'''DIFFERENT SUB-MENUS OF THE HOTEL MANAGEMENT SYSTEM'''

## Menu : 1 - Guest Details
def GuestMenu():
    while True:
            print('Guest Details :-')
            print()
            print('          1. Show Guests')
            print('          2. Add Guest')
            print('          3. Update Guest Details')
            print('          4. Remove Guest')
            print('          5. Search for Guest')
            print('          6. Summary of the Guest')
            print('          7. Back to Main Menu(<<)')
            print()
            gwant=int(input('    Enter any option from above -->'))
            
            if gwant==1:
                ShowGuest()
            elif gwant==2:
                AddGuest()
            elif gwant==3:
                UpdateGuestDetails()
            elif gwant==4:
                RemoveGuest()
            elif gwant==5:
                SearchGuest()
            elif gwant==6:
                SummaryOfGuest()
            elif gwant==7:
                break
            else:
                print()
                print('Invalid input, Please select valid input...')
                print()

## Menu : 2 - Room Details
def RoomMenu():
    while True:
            print('Room Details :-')
            print()
            print('          1. Show Rooms')
            print('          2. Add Room')
            print('          3. Update Room Details')
            print('          4. Remove Room')
            print('          5. Search for Room')
            print('          6. Summary of the Rooms')
            print('          7. Back to Main Menu(<<)')
            print()
            rwant=int(input('    Enter any option from above -->'))
            
            if rwant==1:
                ShowRoom()
            elif rwant==2:
                AddRoom()
            elif rwant==3:
                UpdateRoomDetails()
            elif rwant==4:
                RemoveRoom()
            elif rwant==5:
                SearchRoom()
            elif rwant==6:
                SummaryOfRoom()
            elif rwant==7:
                break
            else:
                print()
                print('Invalid input, Please select valid input...')
                print()

## Menu : 3 - Booking of Rooms
def BookingMenu():
    while True:
            print('Booking Details :-')
            print()
            print('          1. Show Current Booking Details')
            print('          2. Show Previous Booking Details')
            print('          3. Booking of a Room')
            print('          4. Generate Bill')
            print('          5. Back to Main Menu(<<)')
            print()
            bwant=int(input('    Enter any option from above -->'))
            
            if bwant==1:
                ShowCurrentBooking()
            elif bwant==2:
                ShowPreviousBooking()
            elif bwant==3:
                BookingRoom()
            elif bwant==4:
                BillGenerate()
            elif bwant==5:
                break
            else:
                print()
                print('Invalid input, Please select valid input...')
                print()
    
    
    
## Menu : 4 - Report Menu
def Reports():
    while True:
        print()  
        print('Report Of The City Parking :-')
        print()
        print('          1. On the Basis of Vacancies of Rooms')
        print('          2. On the Basis of Frequency of Booking')
        print('          3. On the Basis of Income from Booking')
        print('          4. Back to Main Menu(<<)')
        print()
        reportmenu=int(input('    Enter any option from above -->'))
        
        if reportmenu==1:
            Report_VacancyBasis()
        elif reportmenu==2:
            Report_FrequencyOfBooking()
        elif reportmenu==3:
            Report_IncomeFromBooking()
        elif reportmenu==4:
            break
        else:
            print('Invalid input, Please select valid input...')

    
'''MAIN MENU OF THE HOTEL'''

#Here, we are creating main menu or front page of our hotel management software
def MainMenu():
    while True:
        print()
        print()
        print()
        print('*'*50)
        print('                   HOTEL MAHARAJA')
        print('            (Opp. Bikaner Railway Station)')
        print('*'*50)
        print()
        print()
        print('     Welcome To Our Room Reservation System:-')
        print()
        print('          1. Guest Details')
        print('          2. Room Details')
        print('          3. Booking of Rooms')
        print('          4. Reports of Hotel')
        print('          5. Exit')
        MenuCmd=int(input('    Enter What you want -->'))
        
        if MenuCmd==1:
            GuestMenu()
        elif MenuCmd==2:
            RoomMenu()
        elif MenuCmd==3:
            BookingMenu()
        elif MenuCmd==4:
            Reports()
        elif MenuCmd==5:
            print('Exiting...')
            break
        else:
            print()
            print('Invalid input, Please select valid input...')
            print()
          
MainMenu()
