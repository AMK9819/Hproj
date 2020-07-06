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
    dTime = datetime.datetime(2022, 5, 12)
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

def FTPLoginFolderCreation():

    dir2 = dateOBJ.dateObjStr.updateFolderName
    dir1 = dateOBJ.dateObjStr.updateFolderName2
    ftp = FTPlogin()
    ftp.dir('T1')
    ftp.mkd('T1/images/' + dir1)
    dirSaver = ftp.mkd('T1/monthly_albums/' + dir2)


def FTPUpload(path, ftp):

    #recursively uploads all the files to the FTP server
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

    #C:\\temp directory given from Trello
    #unzips the images.zip file.
    temp_dir = 'C:\\temp'
    file_name = "images.zip"
    os.chdir(temp_dir)

    zip_ref = zipfile.ZipFile('images.zip')
    zip_ref.extractall(temp_dir)
    zip_ref.close()

def AlbumCreation():

    #this changes the directory to where jAlbum was installed on my
    #machine, which was the Program Files folder
    subprocess.call(['runas','/user:Administrator'])
    os.chdir("C:\\Program Files\\jAlbum")
    #this is run on command line
    subprocess.run("java -jar JAlbum.jar -directory C:\\temp -outputDirectory C:\\temp\\album")

def textUpdateFuncHTML():

    FTPfileName = "index1.html"
    updatedFolderName = dateOBJ.dateObjStr.updateFolderName


    ftp = FTPlogin()
    ftp.cwd('/')

    #Note: this string below must be in the index1.html file
    #on like 166 for this to work, this is a HTML comment used
    #to direct where the line needed to be replaced.
    lineToReplace = '<!-- Insert new line-->'
    replacementLine = '<td align="left" valign="top"><a href="http://www.site.com/Albums/monthly_albums/' + updatedFolderName + '/"><img src="newsbanner.png" width="296" height="36" border="0" align="left" valign="top"></a>\n'


    with open(FTPfileName, "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    #this chunk of code looks for the comment and replaces the line after
    #that comment as needed.
    with open(FTPfileName, 'r+') as file:
        HTMLfilelines = file.readlines()
        for i in range(0, len(HTMLfilelines)):
            line = HTMLfilelines[i].strip()
            if line == lineToReplace:
                HTMLfilelines[i+1] = replacementLine
                with open(FTPfileName , 'w') as file:
                    file.writelines(HTMLfilelines)

    with open('index1.html', 'rb') as f:
        ftp.storlines('STOR %s' % 'index1.html', f)




def textUpdateJS():

    updatedFolderName = dateOBJ.dateObjStr.updateFolderName
    updatedFolderNamePrior = dateOBJ.dateObjStr.updateFolderNamePrior


    ftp = FTPlogin()
    ftp.cwd('javascript')
    FTPfileName = 'navigation1.js'

    with open('navigation1.js', "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open('navigation1.js', 'r') as file:
        JSfilelines = file.readlines()

    #calling the lines that need to be replaced directly.
    JSfilelines[141] = '    document.write(\'										<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href = "http://www.site.com/Albums/monthly_albums/'  + updatedFolderName + '/" onMouseOver="glow(\\\'sub13\\\', \\\'sub13on\\\')" onMouseOut="glow(\\\'sub13\\\', \\\'sub13off\\\')"><img src="images/buttonsV2/inactive.CurrentMonth.png" name = "sub13"></a>\');\n'

    JSfilelines[142] = '    document.write(\'										<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href = "http://www.site.com/Albums/monthly_albums/' + updatedFolderNamePrior + '/" onMouseOver="glow(\\\'sub14\\\', \\\'sub14on\\\')" onMouseOut="glow(\\\'sub14\\\', \\\'sub14off\\\')"><img src="images/buttonsV2/inactive.PreviousMonth.png" name = "sub14"></a>\');\n'



    with open('navigation1.js' , 'w') as file:
        file.writelines(JSfilelines)

    with open('navigation1.js' , 'rb') as f:
        ftp.storlines('STOR %s' % 'navigation1.js', f)

    ftp.quit()


def textUpdateArchive():

    updatedAlbumName = dateOBJ.dateObjStr.updateFolderName
    MN = dateOBJ.dateObjStr.monthName
    strY = str(dateOBJ.YYYY)
    strM = str(dateOBJ.MM)
    strD = str(dateOBJ.DD)


    ftp = FTPlogin()
    ftp.cwd('/')
    FTPfileName = 'archive.html'

    with open('archive.html', "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open('archive.html', 'r') as file:
        HTMLfilelines = file.readlines()

    #Note: addLocation_1, addLocation_2, and addLocation_3
    # are HTML comments that need to be inserted into archive.html.
    #<!-- Insert new current month --> has to be placed on line 159
    #<!-- Insert new year --> has to be placed on line 172
    #<!-- Insert new month --> has to be placed on line 178

    addLocation_1 = '<!-- Insert new current month -->'
    addLocation_2 = '<!-- Insert new year -->'
    addLocation_3 = '<!-- Insert new month -->'
    lineToAdd_1 = '\t\t <p class="style1"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html" class="style2">'+ MN + ' ' + strY + '</a>&nbsp;&nbsp;\n'
    lineToAdd_2 = addLocation_3 + '\n <tr> \n\t\t<td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">' + MN + ' ' + strY + '</a>&nbsp;&nbsp; \n\n</tr>\n'

    #handles the case of a new year
    if MN == "January":
        lineToAdd_3 = addLocation_2 + '\n<tr>\n\t\t<td colspan="2" class="subtitle">'+strY+'</td>\n\t</tr>\n\n <!-- Insert new month -->\n <tr><td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">January' + ' ' + strY + '</a><br/><br/>\n\n</tr><tr>\n  '
        lineToAdd_2 = ''
    else:
        lineToAdd_3 = ''

    #Giant chunk  of code that checks for lines to match
    #and insert the lines that needs to be added and replaced.
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


    with open('archive.html', 'rb') as file:
        ftp.storlines('STOR %s' % 'archive.html', file)


def main():

    #runs everything together.
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
