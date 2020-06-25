import datetime
import ftplib
import os
import zipfile
from pathlib import Path
import subprocess
import calendar
import re

def timeFunc():

    d = datetime.datetime.today()
    YYYY = d.year
    MM = d.month
    DD = d.day

    if DD >= 20:
        MM = MM + 1

    strY = str(YYYY)
    strM = str(MM)
    dash = '-'
    underScr = '_'
    albumStr = "album"
    imagesStr = "images"

    folderName1 = strY + dash + strM + albumStr
    folderName2 = strY + underScr + strM + underScr + imagesStr

    ##this code block was meant to test locally
    #print(YYYY, '-', MM)
    #createFolder(folderName1)
    #createFolder(folderName2)

    FTPLoginFolderCreation(folderName1, folderName2)
    return folderName1


#this function was meant to test locally
#def createFolder(directory):

    #try:
    #    os.makedirs(directory)
    #except OSError:
    #    print("Error: Creating" + directory)
    #else:
        #print("Directory created sucessfully %s" % directory)


def FTPLoginFolderCreation(directory1, directory2):

    loginServer = ftplib.FTP()
    loginServer.connect('160.153.56.40')
    loginServer.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
    loginServer.dir('T1')
    loginServer.mkd('T1/images/' + directory2)
    dirSaver = loginServer.mkd('T1/monthly_albums/' + directory1)
    loginServer.quit()
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
    d = datetime.datetime.today()
    YYYY = d.year
    MM = d.month
    DD = d.day

    if DD >= 20:
        MM = MM + 1

    strY = str(YYYY)
    strM = str(MM)
    dash = '-'
    albumStr = "album"

    updatedFolderName = strY + dash + strM + albumStr
    FTPfileName = "index1.html"

    ftp = ftplib.FTP()
    ftp.connect('160.153.56.40')
    ftp.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
    ftp.cwd('/')
    allFTPfiles = ftp.nlst()


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

    ftp.quit()



def textUpdateJS():


    d = datetime.datetime.today()
    YYYY = d.year
    MM = d.month
    DD = d.day

    if DD >= 20:
        MM = MM + 1

    strY = str(YYYY)
    strM = str(MM)
    dash = '-'
    albumStr = "album"
    strMPrior = str(MM-1)

    updatedFolderName = strY + dash + strM + albumStr
    updatedFolderNamePrior = strY + dash + strMPrior + albumStr

    ftp = ftplib.FTP()
    ftp.connect('160.153.56.40')
    ftp.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
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


    d = datetime.datetime.today()
    YYYY = d.year
    MM = d.month
    DD = d.day


    if DD >= 20:
        MM = MM + 1
        MN = calendar.month_name[MM]

    strY = str(YYYY)
    strM = str(MM)
    dash = '-'
    underScr = '_'
    albumStr = "album"
    imagesStr = "images"

    updatedAlbumName = strY + dash + strM + albumStr



    ftp = ftplib.FTP()
    ftp.connect('160.153.56.40')
    ftp.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
    ftp.cwd('/')
    FTPfileName = 'archive.html'

    with open('archive.html', "wb") as file:
        ftp.retrbinary(f"RETR {FTPfileName}", file.write)

    with open('archive.html', 'r') as file:
        HTMLfilelines = file.readlines()


    #HTMLfilelines[158] = '\t\t  <p class="style1"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html" class="style2">'+ MN + ' ' + strY + '</a>&nbsp;&nbsp;\n'
    #HTMLfilelines[174] = '\n <tr> <td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/' + updatedAlbumName + '/index.html">' + MN + ' ' + strY + '</a>&nbsp;&nbsp; </tr>\n'

    #if MN == "January":
        #HTMLfilelines[170] = '<tr> <td width="124" align="left" valign="top" class="bltext"><a href="http://www.site.com/Albums/monthly_albums/2021-01album/index.html">January 2020</a>\n<br/><br/>\n</tr>\n<tr> '


    with open('archive.html', 'w') as file:
        file.writelines(HTMLfilelines)

    with open('archive.html', 'rb') as file:
        ftp.storlines('STOR %s' % 'archive.html', file)




def main():

#    albumname = timeFunc()
    #unzip()
    #AlbumCreation()
    textUpdateFuncHTML()
    textUpdateJS()
    textUpdateArchive()
    ftp = ftplib.FTP()
    ftp.connect('160.153.56.40')
    ftp.login('test@placeholderabcdef.com', '7eEkH4E7A7zics5')
#    ftp.cwd('T1/monthly_albums/' + albumname)
    #FTPUpload('C:\\temp\\album', ftp)
    ftp.quit()



if __name__ == "__main__":
    main()
