import subprocess
import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame
from geopy.geocoders import Nominatim
import geopy.distance
import rasterio.plot
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib import cm
import re

def get_data(year, month, day, hour, minute, 
             launch_latitude, launch_longitude, launch_altitude, 
             burst_altitude, ascent_rate, descent_rate,
             file_path) -> pd.DataFrame:
    launch_datetime = f'{year}-{month.rjust(2, '0')}-{day.rjust(2, '0')}T{hour.rjust(2, '0')}%3A{minute.rjust(2, '0')}%3A00Z'
    
    # get csv data for HAB flight path uisng initial values
    api = (
        f'https://api.v2.sondehub.org/tawhiri?profile=standard_profile&pred_type=single&launch_datetime={launch_datetime}&'
        f'launch_latitude={launch_latitude}&'
        f'launch_longitude={launch_longitude}&'
        f'launch_altitude={launch_altitude}&'
        f'ascent_rate={ascent_rate}&'
        f'burst_altitude={burst_altitude}&'
        f'descent_rate={descent_rate}&'
        f'format=csv'
    )
    
    data = open(file_path, 'w')
    subprocess.run(['curl', api], stdout=data)
    data.close()
    
    return pd.read_csv(file_path)

def m_to_km(x) -> float:
    return x / 1000

def write_to_loc(loc_lines):
    loc = open('CARI_7A_DVD/HAB.LOC', 'w')
    
    # write *.LOC file info into file
    loc.write('C FORMATS (66 character limit)\n')                                               
    loc.write('C 1. BY EXPLICIT LOCATION\n')                             
    loc.write('C N/S, LATITUDE, E/E, LONGITUDE, G/F/K, DEPTH, DATE, HR, D, P, GCR, SP\n')
    loc.write('C N, XX.XXXXX, E, XXX.XXXX, F, XXXX.XXXX YYYY/MM/DD, HXX, DX, PXX, CX, SX\n')
    loc.write('C------------------- OR ---------------------------------\n')
    loc.write('C 2. USE AN AIRPORT ICAO CODE\n')                               
    loc.write('C A, CODE, G/F, ALTITUDE, DATE, HOUR, DOSE, PARTICLE, GCR, SP\n')                 
    loc.write('C A, AAAAAA, F, XXXX.XXXX, YYYY/MM/DD, H0 to H24, DX, PXX, CX, SX\n')       
    loc.write('C------------------- OR ---------------------------------\n')
    loc.write('C 3. ADD A COMMENT\n')
    loc.write('C EVERY LINE ABOVE THE FIRST INSTANCE OF START OR BELOW THE FIRST STOP IS A COMMENT\n')
    loc.write('C BETWEEN START AND STOP, BEGIN A COMMENT LINE WITH A \'C \'\n')
    loc.write('C LIMIT DATA LINES TO 66 CHARACTERS\n')
    loc.write('C\n')
    loc.write('C                           G/F/K\n')
    loc.write('C Input altitude units: atmospheric depth \'G\' (g/sq.cm),\n')
    loc.write('C                       feet \'F\', or\n') 
    loc.write('C                       kilometers, K\n')
    loc.write('C\n')
    loc.write('C                            H##\n')
    loc.write('C      <0> average\n')
    loc.write('C      <1-24> hour of the day in UT+1\n')
    loc.write('C\n')
    loc.write('C                            DOSE (D#)\n') 
    loc.write('C      <1> Particle Flux (Any rad but TOTAL, i.e., no P0)\n')
    loc.write('C          (TOTAL for P0 is total ion flux)\n')
    loc.write('C      <2> ICRP PUB 103 EFFECTIVE DOSE\n')
    loc.write('C      <3> ICRP PUB 60 EFFECTIVE DOSE\n')
    loc.write('C      <4> ICRU H*(10) AMBIENT DOSE EQUIVALENT\n')
    loc.write('C      <5> WHOLE BODY ABSORBED DOSE\n')
    loc.write('C\n')
    loc.write('C                          RADIATION (P#)\n')
    loc.write('C      <0> TOTAL       <10> DEUTERONS   <20>F    <30>K\n')
    loc.write('C      <1> NEUTRONS    <11> TRITONS     <21>Ne   <31>Ca\n')
    loc.write('C      <2> PHOTONS     <12> HELIONS     <22>Na   <32>Sc\n')
    loc.write('C      <3> ELECTRONS   <13> ALPHAS      <23>Mg   <33>Ti\n')
    loc.write('C      <4> POSITRONS   <14> Li          <24>Al   <34>V\n')
    loc.write('C      <5> NEG. MUONS  <15> Be          <25>Si   <35>Cr\n')
    loc.write('C      <6> POS. MUONS  <16> B           <26>P    <36>Mn\n')
    loc.write('C      <7> PROTONS     <17> C           <27>S    <37>Fe\n')
    loc.write('C      <8> POS. PIONS  <18> N           <28>Cl\n')
    loc.write('C      <9> NEG. PIONS  <19> O           <29>Ar\n')     
    loc.write('C\n')
    loc.write('C                         GCR SPECTRUM (C#)\n')
    loc.write('C      <4> 2004 ISO/Nymmik GCR Local Interstellar Spectrum\n')
    loc.write('C               modulated using adjusted CARI-6 heliocentric\n')
    loc.write('C               potential (Other models available in CARI-7A.)\n')
    loc.write('C\n')
    loc.write('C                         SUPERPOSITION (S#)\n')
    loc.write('C      <0> Off (Transport nuclei using LAQGSM and CEM nuclei-nuclei\n')
    loc.write('C              collision models in MCNPX 2.7.0)(SUPERPOSITION is\n')
    loc.write('C              always \'off\' for CARI-7)\n')
    loc.write('C\n')
    loc.write('START-------------------------------------------------\n')
    
    for line in loc_lines:
        loc.write(line)
    
    loc.write('STOP--------------------------------------------------------\n')
    
    loc.close()

def pipe_cari():
    print("Predicting estimated radiation values along path...")
    
    # CARI_7A_DVD/CARI-7A.exe
    #   4 Radiation level at user specified position
    #   2 At a *.LOC file
    #   2 HAB.LOC
    #   7 Quit
    # Output found in CARI-7A_DVD/HAB.ANS
    
    command = ['CARI_7A_DVD/CARI-7A.exe']
    cwd = 'CARI_7A_DVD'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    
    input_text = "4\n2\n2\n7\n"
    output, error = p.communicate(input_text)

    if p.returncode == 0:
        print("Command executed successfully.")
    else:
        print(f"Command exited with an error code: {p.returncode}")
        
    p.kill()  
     
    print("Prediction saved in CARI_7A_DVD/HAB.ANS")

def get_rad_pred(df):
    pred = pd.read_csv('CARI_7A_DVD/HAB.ANS')
    pred.columns = [x.strip() for x in pred.columns]
    
    pred.columns.values[0:3] = ['LON', 'ALTITUDE', 'ALTITUDE TYPE']
    pred['LAT'] = pred.index
    pred.index = range(0, len(pred))
    
    quantity = list()
    for i in pred['QUANTITY']:
        quantity.append(i.strip())
    pred['QUANTITY'] = quantity
    
    cols = pred.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    pred = pred[cols]
    
    pred.columns.values[::] = ['latitude', 'longitude', 'altitude', 'altitude type', 'date', 'hr', 'VCR(GV)',
       'particle', 'dose rate', 'sigma', 'unit', 'quantity']
    
    result = pd.merge(df, pred, left_index=True, right_index=True)
    result.rename(columns={
        'latitude_x': 'latitude', 
        'longitude_x': 'longitude',
        'altitude_y': 'altitude (km)'
    }, inplace=True)
    
    drop_columns = [
        'date', 'hr', 
        'latitude_y', 'longitude_y', 
        'altitude_x', 'altitude type', 
        'particle', 'unit', 'quantity'
    ]
    
    result.drop(drop_columns, axis=1, inplace=True)
    
    return result

def graph(df):
    # creating variable for latitude and longitude to list
    lat = df['latitude'].tolist()
    lon = df['longitude'].tolist()
    
    # coverting csv to geopandas dataframe
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = GeoDataFrame(df, geometry = geometry)
    
    lakes = gpd.read_file('maps/lakes and rivers/ne_50m_lakes.shp')
    coastline = gpd.read_file('maps/coastline/ne_50m_coastline.shp')
    states = gpd.read_file('maps/admin 1 states and provinces lines/ne_50m_admin_1_states_provinces_lines.shp')
    countries = gpd.read_file('maps/admin 0 boundary lines/ne_50m_admin_0_boundary_lines_land.shp')
    oceans = gpd.read_file('maps/ocean/ne_50m_ocean.shp')
    #citites = gpd.read_file('maps/population centers/ne_50m_populated_places.shp')
    
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle('HAB PREDICTIONS')
    
    ax1 = plt.subplot2grid((3,2), (0,0), rowspan=2)
    ax2 = plt.subplot2grid((3,1), (2,0))
    ax3 = plt.subplot2grid((3,2), (0,1), rowspan=2, projection='3d')
    
    #rasterio.plot.show(world, ax=ax)
    lakes.plot(ax=ax1)
    coastline.plot(ax=ax1)
    states.plot(ax=ax1, edgecolor='blue')
    countries.plot(ax=ax1, facecolor='none', edgecolor='red')
    oceans.plot(ax=ax1)
    #citites.plot(ax=ax)
    gdf.plot(ax=ax1, c=df['altitude (km)'], marker='o', linewidths=1)
    
    ax1.set_ylim(min(lat)-2, max(lat)+2)
    ax1.set_xlim(min(lon)-2, max(lon)+2)
    ax1.set_xlabel('latitude')
    ax1.set_ylabel('longitude')
    ax1.set_title('Flight Path')
    
    ax2.plot(df['dose rate'])
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Dose Rate')
    ax2.set_title('Dose Rate Along Flight Path')
    
    X = lat
    Y = lon
    Z = df['altitude (km)']
    ax3.scatter(Y, X, Z, c=Z, cmap=cm.coolwarm, marker='o')
    ax3.set_xlabel('latitude')
    ax3.set_ylabel('longitude')
    ax3.set_zlabel('Altitude')
    ax3.set_title('Altitude Rate Along Flight Path')
    #ax3.set_zlim(-1.01, 1.01)

    fig.tight_layout(pad=5.0)
    plt.show()

def main(year, month, day, hour, minute, launch_latitude, launch_longitude, launch_altitude, burst_altitude, ascent_rate, descent_rate):
    file_path = 'data.csv'
    
    # datetime, latitude, longitude, altitude
    df = pd.DataFrame()
    
    question_one = input("Get new HAB path (y/n)? ")
        
    if (question_one.upper() == 'Y' or question_one.upper() == 'YES'):
        df = get_data(year=year, month=month, day=day, hour=hour, minute=minute, 
                    launch_latitude=launch_latitude, launch_longitude=launch_longitude, launch_altitude=launch_altitude, 
                    burst_altitude=burst_altitude, ascent_rate=ascent_rate, descent_rate=descent_rate,
                    file_path=file_path)
    else:
        df = pd.read_csv(file_path)
    
    if len(df) < 10:
        print("Error: Invalid input data")
        return

    loc_lines = list()
    
    # reformat data to 'N/S, LATITUDE, E/E, LONGITUDE, G/F/K, DEPTH, DATE, HR, D, P, GCR, SP'
    for index, row in df.iterrows():
        n_s = 'N'    # NEED TO GET
        curr_lat = row['latitude']
        e_e = 'E'   # NEED TO GET
        curr_long = row['longitude']
        g_f_k = 'K'
        curr_depth = m_to_km(row['altitude'])
        curr_date = f'{row["datetime"][0:4]}/{row["datetime"][5:7]}/{row["datetime"][8:10]}'
        curr_hr = f'H{row["datetime"][11:13]}'
        dose = 'D1' # MAKE SURE IS CORRECT
        p = 'P7'
        gcr = 'C4'
        sp = 'S0'
        
        new_line = (
            f'{n_s},{curr_lat:.5f},{e_e},{curr_long:.4f},{g_f_k},{curr_depth:.4f},'
            f'{curr_date},{curr_hr},{dose},{p},{gcr},{sp}\n'
        )
        
        loc_lines.append(new_line)
    
    write_to_loc(loc_lines)
           
    if (question_one.upper() != 'Y' and question_one.upper() != 'YES'):
        question_two = input("Predict new radiation values for path (y/n)?")
        if (question_two.upper() == 'Y' or question_two.upper() == 'YES'):
                pipe_cari()
    else:
        pipe_cari()

    result = get_rad_pred(df)

    geolocator = Nominatim(user_agent="RIT SPEX Predicted HAB Landing")
    final_lat = result.iloc[-1]['latitude']
    final_long = result.iloc[-1]['longitude']
    final_coords = f'{final_lat}, {final_long}'
    location = geolocator.reverse(final_coords)
    
    print(f'\tFight Time: {len(result.index)} minutes')
    print(f'\tFinal coords: ({final_coords})')
    print(f'\tAddress: {location.address}')

    graph(result)
    '''
    days = [f'{x:0>2}' for x in range(int(day)+1, int(day)+8)]
    hours = [f'{x:0>2}' for x in range(1, 24)]
    
    # Distances from launch site
    dfls = list()
    
    for d in days:
        for h in hours:
            print(f'{d} {h}')
            temp = get_data(year=year, month=month, day=d, hour=h, minute='00', 
                    launch_latitude=launch_latitude, launch_longitude=launch_longitude, launch_altitude=launch_altitude, 
                    burst_altitude=burst_altitude, ascent_rate=ascent_rate, descent_rate=descent_rate,
                    file_path="temp.csv")
            
            final_lat = temp.iloc[-1]['latitude']
            final_long = temp.iloc[-1]['longitude']
            final_coords = f'{final_lat}, {final_long}'
    
            distance = geopy.distance.geodesic((launch_latitude, launch_longitude), (final_lat, final_long)).km
            dfls.append((d, h, distance, final_coords))
            
    for loc in dfls:
        #print("Day:", dfls[0], "Hour:", dfls[1], dfls[2], "km", geolocator.reverse(dfls[3]))
        print(f"Day: {loc[0]} Hour: {loc[1]} | {loc[2]:0.5} km\tLocation: {geolocator.reverse(loc[3])}")
    '''
    # Particle is always proton
    # units is always particles/sq.cm/sec
    # quantity is always secondary flux
    
if __name__ == "__main__":
    year = '2024'
    month = '2'
    day = '5'
    hour = '17'
    minute = '00'

    launch_latitude = 42.9977
    launch_longitude = 282.4951
    
    launch_altitude = 171       # m
    burst_altitude = 30240      # m
    ascent_rate = 5             # m/s
    descent_rate = 5            # m/s

    main(year, month, day, hour, minute, launch_latitude, launch_longitude, launch_altitude, burst_altitude, ascent_rate, descent_rate)
    
# get regression of flux
# integrate twice to get particle count