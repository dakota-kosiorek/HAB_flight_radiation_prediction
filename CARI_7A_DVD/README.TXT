INFORMATION ABOUT CARI-7A (19 Oct 2021, version 4.2.0)

NOTICE
This program and documentation is disseminated under the sponsorship of 
the U.S. Department of Transportation in the interest of information 
exchange. The United States Government assumes no liability for the 
contents thereof.

-----------------------------------------------------------------------

TABLE OF CONTENTS
1. INTRODUCTION 

2. SYSTEM REQUIREMENTS   

3. USING THE PROGRAM
  A. FLIGHT PROFILES AND CALCULATING FLIGHT DOSES
    i. FLIGHTS FOLLOWING GEODESIC ROUTES 
    ii. FLIGHTS FOLLOWING A USER-SPECIFIED PATH
  B. AIRPORT DATA
    i. SEARCHING AIRPORT DATA
    ii. ADDING/EDITING AIRPORTS
  C. DOSE RATES AT SPECIFIC LOCATIONS
  D. PRIMARY SPECTRA
  E. MODULATION OF GALACTIC COSMIC RADIATION
    i. ISO 2004 GCR MODEL
        a. WOLF NUMBERS
        b. HELIOCENTRIC POTENTIAL
    ii. BADHWAR-O'NEILL 2011 (BO11) and 2014 GCR MODELS
    iii. FORBUSH EFFECTS
    iv. GEOMAGNETIC EFFECTS
  F. CHANGING DEFAULT SETTINGS AND REVIEW OF OLD OUTPUT
    i. CHANGING DEFAULT SETTINGS
    ii. REVIEW OF OLD OUTPUT

4. UNCERTAINTIES

5. DEVELOPERS OF CARI  

-----------------------------------------------------------------------
   
1. INTRODUCTION 

CARI-7A calculates the dose of galactic cosmic radiation received 
by an adult on a nonstop aircraft flight on any date from January 1958 
to the present. It can also calculate the effective dose rate from 
galactic cosmic radiation (GCR) at any specific location in the 
atmosphere at altitudes up to 100 km for these dates.
  
The program takes into account the effects of solar activity, as well
as the geomagnetic field on galactic cosmic radiation levels for the 
date selected by the user. Simultaneous irradiation from solar 
particle events is not taken into account by the program, but Forbush 
Decreases are taken into account if data indicate no Ground Level 
Event is ongoing, and geomagnetic cutoffs are adjusted for Kp index 
if data are available.

Doses and dose rates are integrated from databases of cosmic 
ray showers calculated by MCNPX 2.7.0. The shower intensities are 
derived from the primary cosmic ray (GCR) input spectrum. CARI-7A
allows the user to select from multiple preinstalled GCR models and 
Solar Proton Event models, to use a user defined spectrum. 

A description of the development and validation of the program 
as of October 2016 is in: 

CARI-7A: DEVELOPMENT AND VALIDATION  
Kyle Copeland. 
Radiation Protection Dosimetry 2017;
doi: 10.1093/rpd/ncw369

http://rpd.oxfordjournals.org/cgi/reprint/ncw369?
ijkey=8shPItUzeM8L8Hp&keytype=ref 

The program is an extension and update of CARI-7, which is originally 
described in a doctoral thesis at the Royal Military College of Canada
(RMCC).
"Cosmic Ray Particle Fluences in the Atmosphere Resulting from Primary 
Cosmic Ray Heavy Ions and Their Resulting Effects on Dose Rates to 
Aircraft Occupants as Calculated with MCNPX 2.7.0." by K. A. Copeland, 
Accepted July 2014. The thesis is available from the author on request,
in electronic format from the Massey Library collection at RMCC, 
and from the Canadian National Archives in Ottawa, Canada. 


2. SYSTEM REQUIREMENTS/INSTALLATION

Compiled versions are provided for Intel processsors running 64-bit
Windows and Linux. The program and associated files use about 120 MB 
of disk space and about 80 MB of RAM. This will not increase much 
with use unless debugging output is turned on in the INI file. 

No special installation is needed beyond unpacking the ZIP archive.

To use the Linux version, adjust the VIEWER and OS variables in the 
CARI.INI file and call the Linux executable instead of the Win64 
executable in the main directory (CARI-7A.exe). Linux users will 
also have to write their own shell scripts to call the BO'14 GCR
model.


3. USING THE PROGRAM

The program is CPU intensive, so when multitasking on older,
single core systems, limiting cpu access to something less 
than 100 percent may significantly improve performance of other 
running programs.  

The program can be run via scripts or by using internal menus. To
run using internal menus set the CARI.INI variable MENUS to 'YES'. 
To avoid the menus set the variable MENUS to 'NO!'   

If Menus are requested the program will preloading some data files,  
and will then start at the MAIN MENU. 

To see this HELP file select item 1. 
To enter flight profiles and calculate flight doses select item 2.
To find, change, or add airport information select item 3.
To execute calculations of dose rates at locations select item 4.
To add or lookup heliocentric potential data select item 5.
To see past calculation results or change settings select item 6.
To exit select item 7.    

3.A. FLIGHT PROFILES AND CALCULATING FLIGHT DOSES

There are 2 kinds of flight profiles the program can analyze. 
Flights that follow approximately geodesic (great circle) routes
between airports are stored collectively in archives called *.BIG 
files. Flights that follow waypoint defined flight paths are stored 
individually in *.DEG files.

Selecting item 2 on the MAIN MENU brings up the option of analyzing 
a BIG or DEG file. 

Both BIG files from CARI-6 and DEG files from -6M are compatible
with CARI-7A.

Flights can also be analyzed from the command line by designating 
the name of the flight data file in DEFAULT.INP. If the file name is
not specific but uses the asterisk, "*.DEG" or "*.BIG", then all files 
of that kind in CARI-7A folder/directory will be used. This DOES NOT WORK
for files in subfolders/subdirectories. If you wish to use files from 
other folders/directories, bulding a script to do this is 
probably the easiest way to use the program if you have many files 
to analyse, or often re-analyse a set of updated flight or location 
databases. 

3.A.i. FLIGHTS FOLLOWING GEODESIC ROUTES 

Selecting option <1> will list of all of the available BIG files in the
current directory. BIG files are just ordinary text files containing 
flight information needed by CARI to do an analysis. The file 
EXAMPLE.BIG is provided as an example for you to use as a template. The
program expects the filename to follow the traditional 8.3 format, so 
give it name with 8 characters or less, e.g. EXAMPLE1.BIG. Dozens of 
*.BIG files are allowed, and there is no limit to the size of a BIG 
file. CARI-6 users have run files with thousands of flights.  

Up to 16 BIG files can be listed on a single page at any one time. 
They will be listed in alphabetical order. Unused BIG files 
should be removed from the directory to reduce clutter and make it
easier to find the one you want to use. 

FORMAT OF A FLIGHT PROFILE IN A BIG FILE

New York-Seattle  Flight ID of 1 to 20 characters
07/1995           Flight date (MM/YYYY)  
KJFK              ICAO code of origin airport  
KSEA              ICAO code of destination airport 
2                Number of en route altitudes
29               Minutes climbing to 1st en route altitude
35000    99      1st en route altitude:  feet   minutes
39000   147      2nd en route altitude:  feet   minutes
17               Minutes descending to destination airport


After the first en route altitude, time at an en route altitude
is expected to include minutes climbing or descending from the 
previous en route altitude.

Optionally, a flight date and take-off time can specified instead of 
the year and month. This will slow the calculations down and may not 
worth the trouble for long-term dose monitoring, but can be useful 
for comparisons with instruments, as it will invoke the Kp and 
Forbush effect related corrections to the galactic cosmic radiation
dose rates for each hour during the flight. To use this feature 
specify the date and time as YYYY/MM/DD, HHMM e.g. as 
1995/07/12, 1345 

Flight doses can be calculated for the dates entered with the
flight profiles or for other dates. 

The option to calculate a dose for different time, can be selected
at runtime when using menus or specified in the file DEFAULT.INP 
if menus are avoided. 

3.A.ii. FLIGHTS FOLLOWING A USER-SPECIFIED PATH

Selecting option <2> will list of all of the available DEG files 
in the current directory. DEG files are text files containing the
user-specified waypoints that define the flight. CARI uses a 
geodesic route, constant speed, and a constant rate of climb or 
descent between each waypoint pair. The file EXAMPLE.DEG is provided 
as an example for you to use as a template.  

01/2002, FL-27                           
DEG MIN N/S DEG MIN E/W FEET TIME(MIN)   
4, 58.76, N, 97, 0.27, W, 667, 0                
3, 30.29, N, 85, 32.60, W, 33000, 6
2, 17.01, N, 84, 15.59, W, 33000, 15
1, 17.01, S, 84, 15.59, W, 37000, 18
2, 24.25, S, 3, 28.7, W, 37000, 21
3, 28.30, S, 0, 27.2, W, 80, 25

(Optionally, start time can be specified in the first line)
2002/01/01, 1357, FL-27                           

The first line is the flight date (optional time) and name, the second line is 
headers to aid the reader, and all folowing lines are waypoints.
In each waypoint data line the data are is comma separated:
Column 1 is integer degrees latitude
Column 2 is real minutes latitude
Column 3 is N or S designator (equator can be either)
Column 4 is integer degrees longitude
Column 5 is real minutes longitude
Column 6 is E or W designator (prime meridian can be either)
Column 7 is integer altitude in feet 
Column 8 is integer time in minutes from start of flight

Flight doses can be calculated for the dates (and times) entered with 
the flight profiles or for other dates. The option to calculate a dose
for a different time can be selected at runtime when using menus or 
specified in the file DEFAULT.INP if menus are avoided. 

3.B. AIRPORT DATA

3.B.i. SEARCHING AIRPORT DATA
The program databases already contain information on over 5000
airports worldwide. The International Civil Aviation Organization 
(ICAO) airport codes are used by the program to access this data.
The code for an airport may be found by choosing item <3> on the 
MAIN MENU.  This will bring up the AIRPORT MENU. You can search by city
name (1), airport name (2), or ICAO code (3).  

When searching by name use the first few characters and try alternate 
spellings. To find codes for airports in Washington, DC, for example, 
examine all city entries beginning with Washington. Note that for 
cities with several airports, not all entries may appear on the first 
screen.  

3.B.ii. ADDING/EDITING AIRPORTS
For airports not in the databases or to make corrections, the 
geographic coordinates (degrees and minutes), elevation (feet), and 
airport code for the new entry may be entered into the file 
NEWPORTS.DAT either with a text editor or by choosing item <4> on the 
AIRPORT MENU (item <3> on the MAIN MENU). If the new airport will  
become a permanent change, copy the new data line from NEWPORTS.DAT 
to AIRPORTS.DAT.

The format is an 89 character string containing:
CITY NAME(30 Characters), ICAO CODE (4-6 characters), 
AIRPORT NAME(30 Characters), 
LATITUDE (6 Characters +0) DDMMSS0, N?S character (0 for North), 
LONGITUDE (7 Characters +0) DDDMMSS0, E?W character (0 for West), 
AIRPORT RUNWAY ALTITUDE IN FEET (5 Characters +0), e.g.,

ADELAIDE, AUSTRALIA           YPAD  ADELAIDE INTL                 
3456420}13831540}000200

Airports may also be imported from older versions of CARI, since this
is the legacy data format. Copy the lines from the older files to 
either AIRPORTS.DAT (recommended) or NEWPORTS.DAT.  

If multiple airports have the same ICAO code but different location 
data, CARI will use the data for the first airport found in PORT.NDX.
PORT.NDX is a combination of the airport databases sorted on the 
airport name.  

The sorted files are rebuilt when the program is started and whenever 
a new airport might have been added through the internal menus.  

3.C. DOSE RATES AT SPECIFIC LOCATIONS

Users can calculate the dose rate at a specific location or from a list 
of pre-defined locations by selecting item (4) from the MAIN MENU. To 
calculate for a single location, choose item (1) from the LOCATION MENU
and make selections as requested by CARI.

Selecting item <1> to calculate the dose rate for a single location 
and set of conditions does not alter any files and the results are 
only printed to screen, not saved. If you want to keep it, make a note
or do a screen dump to file.

Selecting item <2> starts analysis of location data file (*.LOC). 
Results of dose rate calculations are stored in files ending with the
.ANS extension (e.g., results for MY.LOC will be placed in MY.ANS). 

LOC files can be edited by selecting item <3> from the LOCATION MENU. 
Lines are comma delimited and each line is limited to 66 characters. 
Adding more characters will introduce junk lines to the output file 
and may result in unread data at the end of the line. The sample file 
PLACES.LOC has many notes to guide customization of this kind of file.

The format is 
START----------
data line 1
data line 2
etc.
STOP-----------

Everything above the first line begining with "START-" is considered 
a comment, as is everything below the first line begining with 
"STOP--". COmments within the active data can be designated by starting
the line with a C. See the SAMPLE.LOC for more details.

To view results select item <4>. The ANS is rewritten each time when 
using item <2>, so to keep the results it is best to rename the LOC 
file or copy the ANS file elswhere before re-running an analysis of the
same file (e.g., with different shielding in VEHICLE.DAT). 

Choosing item <5> opens this help file.

Collections of locations can also be analyzed from the command line
by designating the name of the location data file in DEFAULT.INP.

3.D. PRIMARY SPECTRA

The spectral choices currently available are:
1=ISO 2004
2=BO'11
3=BO'14*
4=ISO 2004 LIS modulated by heliocentric potential
5=LaRCFeb56SPE
6=LaRCSep89SPE
7=MY_MODEL.OUT, a user-supplied spectrum 

If an SPE spectrum (5 OR 6) is selected, note that results are 
normalized for total event fluence. 

To input a custom spectrum using option 7, the custom spectrum must be 
in the file \GCR_MODELS\MY_MODEL.OUT and have the same format as 
BO11_GCR.OUT. Expected units are: nuclei/(m2-sr-s-GeV) 
for Z=1 to Z=26 (H - Fe) ions.

*The BO'14 GCR entry, #3, is integrated only for Windows. The 
executable I was supplied would not run with my Linux distribution. 
To try to use it write a script equivalent to runbon14.bat that can
be called from the CARI-7A folder with './runBON2014'     

3.E. MODULATION OF GALACTIC COSMIC RADIATION

The GCR data are modified based on up to 3 factors: long-term solar 
activity (accounted for using model-specific methods), short-term 
variations in solar activity from the monthly average such as Forbush 
decreases accounted for using hourly neutron monitor count rate data, 
and geomagnetic storm effects accounted for using the Kp index. 

Ionizing radiation increases from solar proton events are not included
but can be calculated using MY_MODEL.OUT. Be careful since this file 
is assumed to have GCR flux units.
  
In most cases, the effects of transport through the heliosphere to 
Earth’s magnetosphere on the GCR spectra are handled within the 
respective GCR models. No further modulations based on long-term 
solar activity are performed within CARI. 

The effects of geomagnetic storms and Forbush decreases on primary 
GCR flux are usually ignored. However, for comparison with instrument 
measurements, using the specific day and hour of the measurement is 
best practice. This invokes the Forbush and geomagnetic storm based 
adjustment subroutines, which are not needed for monthly average 
calculations. Using these routines significantly increases run times.
Forbush effects and geomagnetic storm effects on primary GCR flux are 
handled independently of GCR model chosen. 

3.E.i. ISO GCR MODEL

3.E.i.a. WOLF SUNSPOT NUMBER
The dynamics of the large-scale GCR modulation by the solar wind in 
the ISO GCR model is characterized by the effective modulation 
potential of the heliosphere calculated from the Wolf sunspot number 
and solar magnetic field orientation. The latest sunspot numbers are 
in the SIDC-team, World Data Center for the Sunspot Index, Royal 
Observatory of Belgium, Monthly Report on the International Sunspot 
Number, online catalogue of the sunspot index at:

 www.sidc.be

The file SN_m_tot_V20.csv is an exact replica of SN_m_tot_V2.0.csv 
from SIDC. It contains all the needed data. To update just download 
'SN_m_tot_V2.0.csv' and rename it to 'SN_m_tot_V20.csv', replacing 
the older version.

Format is:
YYYY;MM;DATE_in_decimal; SSN; SD; other stuff not used in the ISO model.
FORTRAN CODING to read this line is: 
A4,A1,I2,A1,F8.3,A1,F6.1,A1,F5.1,A1,A8
IF SIDC changes the format this will have to fixed in the source code.

This SIDC file is used by the ISO model only.

3.E.i.b. HELIOCENTRIC POTENTIAL
CARI-7A can also use the ISO model local interstellar spectrum (LIS) 
modulated by the heliocentric potential method, instead of the Wolf 
sunspot and magnetic field orientation driven method described in the 
ISO report. While still producing a slowly varying GCR spectrum at 
Earth orbit, this type of modulation is more dynamic than the original
ISO Wolf number driven modulation. For continuity with previous 
versions of CARI, heliocentric potentials for CARI-6 are used by 
CARI-7A, despite differences in primary GCR LIS.  

Recent heliocentric potentials are available on our Web site. 
Search for "FAA Radiobiology heliocentric" and follow the links. 
The current address as of May 2019 is:

http://www.faa.gov/data_research/research/med_humanfacs/aeromedical/
radiobiology/heliocentric/

There is a lag of about one month in availability of heliocentric 
potential data on our Web site. To estimate flight doses during the 
current month or a future month, use the most recent heliocentric 
potential available (The program will default to this choice if a 
potential does not exist for the entered date. NOTE: This 
approximation is increasingly less accurate for dates more than 2 
months removed from the month of interest, particularly during solar 
maximum.).   

CARI-7A looks for these data in the folder \SOLARMOD  

Heliocentric potentials with corresponding dates are stored in a 
permanent database (MV-DATES.L99) and in a user-modifiable database 
(MORDATES.2K). 

For the ISO-HP model either SOLARMOD\MV-DATES.L99 or MORDATES can be 
updated, but MV-DATES.L99 is searched much faster and updated monthly. 

Data in MOREDATES.2K takes precedence over data in MV-DATES.L99, so be
cautious and keep it clean if you use it to override the permanent 
database.

3.E.ii. BADHWAR-O'NEILL 2011 (BO'11) AND 2014 (BO'14) GCR MODELS 
For CARI-7A, the stand alone BO11 GCR model source code provided by 
Patrick O’Neill was minimally modified to allow its incorporation.

The 2011 revised version of the 2010 GCR model of Badhwar and O’Neill
was developed to provide an accurate galactic cosmic ray (GCR) energy 
spectrum that can be used by engineers in single-event effect (SEE) 
rate prediction codes and by radiation health physicists for astronaut 
exposures on deep space missions. The GCR model is designed for free 
space, i.e., beyond the Earth’s magnetosphere. The model uses the 
spherically symmetric Fokker–Planck equation that accounts for cosmic
ray propagation in the heliosphere due to diffusion, convection, and 
adiabatic deceleration. The boundary condition is the constant energy 
spectrum [called the Local Interstellar Spectrum (LIS)] for each GCR 
element at the outer edge of the heliosphere (100 AU). The 
Fokker–Planck equation modulates the LIS to a given radius from the 
Sun, assuming steady-state heliosphere conditions.

Like the ISO model, the BO11 model uses the correlation with sunspot 
number (International Sunspot Number or ISS in this case) to determine 
the level of solar modulation to a monthly level, to allow users to 
take advantage of the predictive capability in the correlation. To 
enable increased accuracy (and finer time resolution), spacecraft 
data are used to calibrate the sunspot number for periods where they 
overlap, IMP-8 from 1974 to 1997 and ACE from 1997 to the present.

The file that most needs to be kept up-to-date is MONTHLY.TXT

CARI-7A looks for model data in various files in the \GCR_MODELS 
directory. The BO'11 and 'BO'14 models have their own databases which 
should be kept up to date for best results.

BO'11 data files are
 ISSFILE = 'GCR_MODELS\MONTHLY.TXT '! WOLF number file from NOAA-SWPC
                                    ! They no longer update this file
                                    ! so now add SIDC numbers*0.6 
 GCR_MODELS\ISSVST.DAT
 GCR_MODELS\ISSDELAY.DAT
 GCR_MODELS\ISSTMNX.DAT   
 GCR_MODELS\ISSWMNX.DAT 
 GCR_MODELS\ISSZONE.DAT 
 GCR_MODELS\FRBEHELI.DAT
 GCR_MODELS\DSSDTISS.DAT

BO'14 data files are to update are in the /IN folder for the OS 
specific call of the executable.
        iss-sidc.dat
	solar_cycle_date.dat
        ssn_minmax.dat

More information on upkeep of these models can be found in their 
specific documentation.

3.E.iii. FORBUSH EFFECTS

Hourly deviations in GCR from the monthly average such as Forbush 
decreases are kept in the file \FORBUSH\FORBUSH.DAT. The format is 
based on the IZMIRAN neutron monitor data format, with the last column 
added as the hourly count rate relative to the monthly average. If no 
day or day and hour is specified, there will be no effect on results. 
Also, if data are not found for the user entered specific day or day 
and hour there is no affect. This level of specificity will add 
calculation time. A specfic effect can be forced via FROMUSER.DAT 
(See below).

3.E.iv. GEOMAGNETIC STORMS 

Short term variations in geomagnetic shielding are accounted for 
using the Kp index. The data are stored in \KP_INDEX\KP_INDEX.TXT
and current data are available from NOAA's Space Weather Prediction 
Center. As with the Forbush data, if data are not present, 
geomagnetically quiet conditions are used. 

3.F. CHANGING DEFAULT SETTINGS AND REVIEW OF OLD OUTPUT

Item (5) on the MAIN MENU brings up the OUTPUT MENU.

3.F.i. CHANGING DEFAULT SETTINGS/RUNNING USING A SHELL SCRIPT 

From the OUTPUT MENU you can change the model settings in 
CARI.INI (item 1) and change the default input data for batch 
mode/shell scripting stored in DEFAULT.INP (item 2). The notes  
in CARI.INI and DEFAULT.INP explain how to change the files 
appropriately. I suggest backing them up somewhere so you can 
always restore the default settings if needed.

FROMUSER.DAT is a file for direct entry of data usually looked 
up from historical databases by the program. Use can considerably 
reduce run time by eliminating searches. A negative value indicates 
searching the databases, positive indicates user decided value.
FOR THIS VERSION, CARI-7A v4.0.2, ONLY THE FIRST 3 LINES ARE USED. 

Expected line formats are:
Real, A8 
Real, A24 
Real, A20 
A space is recommended before the number on each line to assure 
proper reading across platforms.

VEHICLE.DAT allows the user to define structural shielding for 
the vehicle. The model is based on effective dose equivalent
results from OLTARIS. For other dose endpoints the results are 
more approximate. File content is:

1st line is Al alloy thickness in units of g/cm**2
2nd line is HDPE (polyethylene, i.e., CH2) thickness in units of
g/cm**2.
3rd line is dry air in units of g/cm**2.

The net effect is the thickness-weighted average of the shields.  
To use this file there must be a line in the variable list in 
CARI.INI that reads 'VEHICLE   = YES'. Reading this file must be 
indicated in CARI.INI or it will be ignored ('VEHICLE   = NO!' is 
the default).

3.F.ii. REVIEW OF OLD OUTPUT

Using the OUTPUT MENU item (3) you can also review/edit 
previously calculated flight dose results. 

Selecting item (4) loads the current contents of PLACES.ANS 
into the default editor.


4. UNCERTAINTIES

Uncertainties in the component models were combined using the 
assumptions of complete independence of variables, a normal 
distribution of values, and that individual element uncertainties 
were expressed in terms of standard uncertainties, equivalent to 
standard deviations with respect to combining uncertainties. These
should be considered only an indicator of statistical precision.

After including a safety factor of 2, and using more conservative
assumptions about indepence, the estimated uncertainty from all 
sources is about 30% for commercial altitudes.   


5. DEVELOPERS OF CARI  

CARI-7 and 7A (all versions)
Kyle Copeland
Mail route AAM-631 (Numerical Sciences Research)
Civil Aerospace Medical Institute, Federal Aviation Administration
Oklahoma City, Oklahoma  73125-5066 USA
FAX (405) 954-1010
E-Mail  kyle.copeland@faa.gov

CARRIER (CARI-1) through CARI-6 
Wallace Friedberg, Frances E. Duke, Lorrenza Snyder, Kyle Copeland
Mail route AAM-610 (Radiobiology Research)
Civil Aerospace Medical Institute, Federal Aviation Administration
Oklahoma City, Oklahoma  73125-5066 USA
FAX (405) 954-1010
E-Mail  kyle.copeland@faa.gov

Keran O'Brien, III
Department of Physics and Astronomy, Northern Arizona University
Flagstaff, Arizona  86011

Donald E. Parker 
Department of Biostatistics and Epidemiology 
University of Oklahoma Health Sciences Center
Oklahoma City, Oklahoma  73190

Margaret A. Shea, Donald F. Smart
Air Force Geophysics Laboratory, Hanscom AFB (emeritus)
Bedford, Massachusetts  01731-5000

Many thanks to Dr. Copeland's thesis committee for their very useful 
comments and questions during the development of CARI-7: Brent Lewis, 
Emily Corcoran, Hughes Bonin, Andy Belyea and Kristine Spekkens at 
the Royal Military College of Canada, and Francios Lemay of i-s-r.ca. 
Thanks also to Tyler Dumouchel of i-s-r.ca (Canada) and Tatsuhito Sato 
of JAERI (Japan) for their data and comments. Also, special thanks to 
Paul Goldhagen, U.S. Dept. of Homeland Security, for his data and
many hours of discussion about GCR modeling with MCNPX and MCNP.   

We are grateful to Margaret D. Wilson (Ottawa, Canada), working
under the auspices of the Bartol Research Institute of the
University of Delaware, USA, and Eduard Vashenyuk of the Apatity
Cosmic Ray Station, Polar Geophysical Institute, Russia, for
providing neutron monitor counting rate data used to calculate
the heliocentric potential and Forbush adjustments.

Finally, thanks to the many other colleagues who contributed to the 
development of CARI through its long history, particularly:  
Edgar B. Darden, Jr., Oak Ridge, Tennessee, USA
Ernst Feldsberger of the University of Graz, Austria
Alfredo Ferrari, INFN, Sezione di Milano, Italy 
Wolfgang Heinrich, University of Siegen, Germany
Maurizio Pelliccioni, INFN, Laboratori Nazionali di Frascati, Italy
M. Pillon, Associazione EURATOM-ENEA sulla Fusione Centro Ricerche, 
     Frascati, Italy 
Stefan Roesler, CERN, Switzerland 
Timothy C. Lamey and Donald N. Faulkner of the Civil Aerospace
Medical Institute, FAA, USA.

Our thanks as well to all those who and have given us feedback over 
the many years, aiding the development and debugging of CARI.

