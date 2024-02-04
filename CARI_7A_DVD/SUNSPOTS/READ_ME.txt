The file SN_m_tot_V20.csv is an exact replica of SN_m_tot_V2.0.csv from SIDC. 
To update just download, rename, and replace with the new version from SIDC.
Format is 
YYYY;MM;DATE_in_decimal; SSN; SD; other stuff not immediately related to the ISO model.
FORTRAN CODING to read this line is A4,A1,I2,A1,F8.3,A1,F6.1,A1,F5.1,A1,A8
IF SIDC changes the format this will have to fixed in the source code (UTILITY.for).

This SIDC file is used by the ISO model only. The BO'11 and 'BO'14 models have their own 
databases which also should be kept up to date

BO'11 data files are
        ISSFILE = 'GCR_MODELS\MONTHLY.TXT '   ! WOLF number file from SWPC
                                              ! They no longer update 
                                              ! so now add sidc #s *0.6 
        ISSVT   = 'GCR_MODELS\ISSVST.DAT  '
        ISSDELAY= 'GCR_MODELS\ISSDELAY.DAT'
        TMNXFIL = 'GCR_MODELS\ISSTMNX.DAT '   
        WMNXFIL = 'GCR_MODELS\ISSWMNX.DAT '
        ZONEFIL = 'GCR_MODELS\ISSZONE.DAT '
        HELIO   = 'GCR_MODELS\FRBEHELI.DAT'
        DSSFILE = 'GCR_MODELS\DSSDTISS.DAT'

BO'14 data files are to update are 
        iss-sidc.dat
	solar_cycle_date.dat
        ssn_minmax.dat

For the ISO-HP model either SOLARMOD\MV-DATES.L99 or MORDATES can be updated, 
but MV-dates is searched much faster and updated monthly. 


KC 20180629 

