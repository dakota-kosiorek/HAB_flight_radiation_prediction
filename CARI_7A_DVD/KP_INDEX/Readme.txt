I originally wrote CARI-7 to read the NGDC files, which NOAA stopped updating in 2018.
The batch scripts in this folder use global Kp index data files in SWPC format to create similar files in old NGDC format. 

To use the scripts: 
1. Download data from SWPC. The URL is ftp://ftp.swpc.noaa.gov/pub/indices/old_indices/ The files with Kp data are *_DGD.txt files. 
2. Convert the file to DOS format using unix2dos.exe.
3. Run CONVERT at the command prompt with the filnename with new data and output sent to the destination file. For example:

	C:\users\me\my_new_Kp_data>CONVERT 2019Q1_DGD.txt > my_destination_file.txt

The reformatted data can be appended to the file KP_INDEX\KP_INDEX.TXT, Do not worry about the lack of Ap data for recent dates. 
The CONVERT program creates dummy data to fill the fields present in the old format.

As of this writing, the data are updated quarterly by SWPC.

Best regards,
Kyle Copeland