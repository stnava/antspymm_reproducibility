
import antspymm
import pandas as pd
import glob as glob
import os
rdir = "/mnt/cluster/data/Hawco_M3RI_Travel/" 
bd = rdir + "traveling_m3ri_antspymm/"
dffns=glob.glob( rdir + "studycsvs/*csv" )
mydf = pd.DataFrame()
for f in dffns:
    mydf = pd.concat( [ mydf, pd.read_csv( f ) ] )

# fix for an issue with type
mydf['imageID']='000'
print( mydf.shape )
zz=antspymm.aggregate_antspymm_results_sdf( mydf, subject_col='subjectID', date_col='date', image_col='imageID',  base_path=bd,
splitsep='_', idsep='_', wild_card_modality_id=True, verbose=True)
print( zz.shape )

# add brain age to each row 
for index, row in zz.iterrows():
  print( zz.loc[index, 'subjectID'] )
  bagefn=bd+'M3RITravel/'+zz.loc[index, 'subjectID']+'/'+zz.loc[index, 'date']+'/T1w/brain_age.csv'
  if os.path.exists( bagefn ):
    bage=pd.read_csv(bagefn)['brainage'].iloc[0]
    zz.loc[index,'T1w_brainage']=bage

zz.to_csv( "m3ri_travel_antspymm.csv" )
