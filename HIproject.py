import datetime
import ftplib
import os
import zipfile
from pathlib import Path
import subprocess
import calendar
import re


def FTPlogin():
    ftp = ftplib.FTP()
    ftp.connect('160.153.56.40')
    ftp.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
    return ftp

def dateTime():
    #dTime = datetime.datetime.today()
    dTime = datetime.datetime(2020, 12, 21)
    return dTime

class dateObj():
    def __init__(self, date):
        self.YYYY = self.yearCreate(date.month, date.day, date.year)
        self.DD = date.day
        self.MM = self.monthCreate(date.month, date.day)
        self.dateObjStr = DateOBJSTR(self.YYYY, self.MM, self.DD)

    def monthCreate(self, month, day):
        M = month
        D = day
        if(D >= 20):
            M = M + 1
        if(M == 13):
            M = 1
        return M
    def yearCreate(self, month, day, year):
        M = month
        D = day
        Y = year
        if (D >= 20 and M == 12):
            return Y + 1
        return Y



class DateOBJSTR():
    def __init__(self, year, month, day):
        # self.strY = str(year)
        # self.strM = str(month)
        self.monthName = calendar.month_name[month]
        # self.strD = str(day)
        #self.nextYear = date.today().year + 1
        #self.strMPrior = str(month-1)
        self.updateFolderName = self.folderToStr(year, month)
        self.updateFolderNamePrior = self.folderToStr(year, month-1)
        self.updateFolderName2 = self.folderToStr2(year, month)

    def folderToStr(self, Y, M):
        if(M == 0):
            return "{}-{}album".format(Y-1,12)
        return "{}-{}album".format(Y,M)
    def folderToStr2(self, Y, M):
        if(M == 0):
            return "{}-{}album".format(Y-1,12)
        return "{}_{}_images".format(Y, M)

today = dateTime()
dateOBJ = dateObj(today)

#def timeFunc():


#    dTime = datetime.datetime.today()

#    dateObject = dateObj(dTime)
    # dateObjectString = DateOBJSTR()
    # d = datetime.datetime.today()
    # YYYY = d.year
    # MM = d.month
    # DD = d.day
    #
    # if DD >= 20:
    #     MM = MM + 1
    #
    # strY = str(YYYY)
    # strM = str(MM)
    # dash = '-'
    # underScr = '_'
    # albumStr = "album"
    # imagesStr = "images"
    #
    # folderName1 = strY + dash + strM + albumStr
    # folderName2 = strY + underScr + strM + underScr + imagesStr

    ##this code block was meant to test locally
    #print(YYYY, '-', MM)
    #createFolder(folderName1)
    #createFolder(folderName2)

    #FTPLoginFolderCreation(folderName1, folderName2)
#    return folderName1


#this function was meant to test locally
#def createFolder(directory):

    #try:
    #    os.makedirs(directory)
    #except OSError:
    #    print("Error: Creating" + directory)
    #else:
        #print("Directory created sucessfully %s" % directory)


def FTPLoginFolderCreation():


    dir2 = dateOBJ.dateObjStr.updateFolderName
    dir1 = dateOBJ.dateObjStr.updateFolderName2
    ftp = FTPlogin()
    ftp.dir('T1')
    ftp.mkd('T1/images/' + dir1)
    dirSaver = ftp.mkd('T1/monthly_albums/' + dir2)
#zip_file = 'C:\temp\images.zip'
#Unzip, then send it to the FTP server (send files?)
    #1st set of parenthesis will hold the path
    #in the final version this should be temp's path
    #with ZipFile(zip_file, 'r') as zip_ref:
        #zip_ref.extractall(directory)



def FTPUpload(path, ftp):

    os.chdir(path)
    files = os.listdir(path)
    for i in files:
        if os.path.isfile(path + r'\{}'.format(i)):
            fh = open(i, 'rb')
            ftp.storbinary('STOR %s' % i, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(i)):
           ftp.mkd(i)
           ftp.cwd(i)
           FTPUpload(path + r'\{}'.format(i), ftp)
    ftp.cwd('..')
    os.chdir('..')


def unzip():

    temp_dir = 'C:\\temp'
    file_name = "images.zip"
    os.chdir(temp_dir)

    zip_ref = zipfile.ZipFile('images.zip')
    zip_ref.extractall(temp_dir)
    zip_ref.close()

def AlbumCreation():

    subprocess.call(['runas','/user:Administrator'])
    os.chdir("C:\\Program Files\\jAlbum")
    subprocess.run("java -jar JAlbum.jar -directory C:\\temp -outputDirectory C:\\temp\\album")

def textUpdateFuncHTML():

    #download the file from ftp
    #edit it with new data
    #upload it back
    #
    #

    print ("Entering textupdatefunction...")
    # d = datetime.datetime.today()
    # YYYY = d.year
    # MM = d.month
    # DD = d.day
    #
    # if DD >= 20:
    #     MM = MM + 1
    #
    # strY = str(YYYY)
    # strM = str(MM)
    # dash = '-'
    # albumStr = "album"
    #
    # updatedFolderName = strY + dash + strM + albumStr
    FTPfileName = "index1.html"
    updatedFolderName = dateOBJ.dateObjStr.updateFolderName


    ftp = FTPlogin()
    ftp.cwd('/')

    lineToReplace = '<!-- Insert new line-->'
    replacementLine = '<td align="left" valign="top"><a href="http://www.site.com/Albums/monthly_albums/' + updatedFolderName + '/"><img src="newsbanner.png" width="296" height="36" border="0" align="left" valign="top"></a>\n'


    with open(FTPfileName, "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open(FTPfileName, 'r+') as file:
        HTMLfilelines = file.readlines()
        for i in range(0, len(HTMLfilelines)):
            line = HTMLfilelines[i].strip()
            if line == lineToReplace:
                HTMLfilelines[i+1] = replacementLine
                with open(FTPfileName , 'w') as file:
                    file.writelines(HTMLfilelines)


        #readFile = open(FTPfileName).read()
        #readFile = readFile.replace(lineToReplace, replacementLine + '\n')

#    HTMLfile = open("index1.html", "r+")
#    line_list = HTMLfile.readlines()
#    HTMLfile.truncate(0)

#    line_list[165] = '<td align="left" valign="top"><a href="http://www.site.com/Albums/monthly_albums/' + updatedFolderName + '/"><img src="newsbanner.png" width="296" height="36" border="0" align="left" valign="top"></a>'
#    HTMLfile.writelines(line_list)
#    HTMLfile.close()

    with open('index1.html', 'rb') as f:
        ftp.storlines('STOR %s' % 'index1.html', f)




def textUpdateJS():

    #
    # d = datetime.datetime.today()
    # YYYY = d.year
    # MM = d.month
    # DD = d.day
    #
    # if DD >= 20:
    #     MM = MM + 1
    #
    # strY = str(YYYY)
    # strM = str(MM)
    # dash = '-'
    # albumStr = "album"
    # strMPrior = str(MM-1)
    #
    # updatedFolderName = strY + dash + strM + albumStr
    # updatedFolderNamePrior = strY + dash + strMPrior + albumStr

    updatedFolderName = dateOBJ.dateObjStr.updateFolderName
    updatedFolderNamePrior = dateOBJ.dateObjStr.updateFolderNamePrior


    ftp = FTPlogin()
    ftp.cwd('javascript')
    FTPfileName = 'navigation1.js'

    with open('navigation1.js', "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open('navigation1.js', 'r') as file:
        JSfilelines = file.readlines()

    JSfilelines[141] = '    document.write(\'										<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href = "http://www.site.com/Albums/monthly_albums/" '  + updatedFolderName + '/ onMouseOver="glow(\\\'sub13\\\', \\\'sub13on\\\')" onMouseOut="glow(\\\'sub13\\\', \\\'sub13off\\\')"><img src="images/buttonsV2/inactive.CurrentMonth.png" name = "sub13"></a>\');\n'

    JSfilelines[142] = '    document.write(\'										<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href = "http://www.site.com/Albums/monthly_albums/' + updatedFolderNamePrior + '/" onMouseOver="glow(\\\'sub14\\\', \\\'sub14on\\\')" onMouseOut="glow(\\\'sub14\\\', \\\'sub14off\\\')"><img src="images/buttonsV2/inactive.PreviousMonth.png" name = "sub14"></a>\');\n'



    with open('navigation1.js' , 'w') as file:
        file.writelines(JSfilelines)

    with open('navigation1.js' , 'rb') as f:
        ftp.storlines('STOR %s' % 'navigation1.js', f)

    ftp.quit()


def textUpdateArchive():


    # d = datetime.datetime.today()
    # YYYY = d.year
    # MM = d.month
    # DD = d.day
    #
    #
    # if DD >= 20:
    #     MM = MM + 1
    #     MN = calendar.month_name[MM]
    #
    # strY = str(YYYY)
    # strM = str(MM)
    # dash = '-'
    # underScr = '_'
    # albumStr = "album"
    # imagesStr = "images"
    #
    # updatedAlbumName = strY + dash + strM + albumStr
    updatedAlbumName = dateOBJ.dateObjStr.updateFolderName
    MN = dateOBJ.dateObjStr.monthName
    strY = str(dateOBJ.YYYY)
    strM = str(dateOBJ.MM)



    ftp = FTPlogin()
    ftp.cwd('/')
    FTPfileName = 'archive.html'

    with open('archive.html', "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open('archive.html', 'r') as file:
        HTMLfilelines = file.readlines()


    addLocation_1 = '<!-- Insert new current month -->'
    addLocation_2 = '<!-- Insert new year -->'
    addLocation_3 = '<!-- Insert new month -->'
    lineToAdd_1 = '\t\t <p class="style1"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html" class="style2">'+ MN + ' ' + strY + '</a>&nbsp;&nbsp;\n'
    lineToAdd_2 = addLocation_3 + '\n <tr> <td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">' + MN + ' ' + strY + '</a>&nbsp;&nbsp; </tr>\n'

    if MN == "January":
        lineToAdd_3 = addLocation_2 + '\n<tr>\n<td colspan="2" class="subtitle">'+strY+'</td>\n\t</tr><tr><td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">January' + strY + '</a><br/><br/></tr><tr>\n  '
    else:
        lineToAdd_3 = ''


    with open(FTPfileName, 'r+') as file:
         HTMLfilelines = file.readlines()
         for i in range(0, len(HTMLfilelines)):
             line = HTMLfilelines[i].strip()
             if line == addLocation_1:
                 HTMLfilelines[i+1] = lineToAdd_1
                 with open(FTPfileName , 'w') as file:
                     file.writelines(HTMLfilelines)
             if line == addLocation_2 and lineToAdd_3 != '':
                 HTMLfilelines[i] = lineToAdd_3
                 with open(FTPfileName , 'w') as file:
                     file.writelines(HTMLfilelines)
             if line == addLocation_3:
               HTMLfilelines[i] = lineToAdd_2
               with open(FTPfileName , 'w') as file:
                     file.writelines(HTMLfilelines)



    #HTMLfilelines[158] = '\t\t  <p class="style1"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html" class="style2">'+ MN + ' ' + strY + '</a>&nbsp;&nbsp;\n'
    #HTMLfilelines[174] = '\n <tr> <td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">' + MN + ' ' + strY + '</a>&nbsp;&nbsp; </tr>\n'

    #if MN == "January":
        #HTMLfilelines[170] = '<tr> <td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/2021-01album/index.html">January 2020</a>\n<br/><br/>\n</tr>\n<tr> '

    with open('archive.html', 'rb') as file:
        ftp.storlines('STOR %s' % 'archive.html', file)


#def addLineOperations(lineToAdd, FTPfileName):
#    with open(FTPfileName, 'w') as file:
#        file.writelines(HTMLfilelines)
#    return lineToAdd



def main():

    updatedFolderName = dateOBJ.dateObjStr.updateFolderName
    FTPLoginFolderCreation()
    unzip()
    AlbumCreation()
    textUpdateFuncHTML()
    textUpdateJS()
    textUpdateArchive()
    ftp = FTPlogin()
    ftp.cwd('T1/monthly_albums/' + updatedFolderName)
    FTPUpload('C:\\temp\\album', ftp)
    ftp.quit()



if __name__ == "__main__":
    main()
