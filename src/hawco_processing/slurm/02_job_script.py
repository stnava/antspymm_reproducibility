####################################################################################

import os
from os.path import exists
import glob

####################################################################################
base_directory = "/mnt/cluster/data/Hawco_M3RI_Travel/"
rootdir = base_directory + "data/M3RITravel/"
######################################################
t1fns = glob.glob( rootdir + "*/*/anat/*T1w.nii.gz" )
t1fns.sort()
import sys
fileindex = 3
if len( sys.argv ) > 1:
    fileindex = int(sys.argv[1])

if fileindex > len( t1fns ):
    sys.exit(0)

t1fn = t1fns[ fileindex ]
import re
newoutdir = base_directory + 'traveling_m3ri_antspymm/'
os.makedirs( newoutdir, exist_ok=True  )
os.makedirs( base_directory + 'studycsvs', exist_ok=True  )

subject_id = os.path.basename( t1fn )
splitit = subject_id.split( "_" )
subject_id = splitit[0]
subdate=splitit[1]
print( "RUN " + subject_id + " --- " + newoutdir + " " )
import antspymm

import os
nth='24'
os.environ["TF_NUM_INTEROP_THREADS"] = nth
os.environ["TF_NUM_INTRAOP_THREADS"] = nth
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = nth
import sys
import pandas as pd
import glob
import ants
import antspymm


template = ants.image_read("~/.antspymm/PPMI_template0.nii.gz")
bxt = ants.image_read("~/.antspymm/PPMI_template0_brainmask.nii.gz")
template = template * bxt
template = ants.crop_image( template, ants.iMath( bxt, "MD", 12 ) )

anatfn = t1fn + '/anat/' + subject_id + "_T1w.nii.gz"
anatfn = t1fn 
dtfn = glob.glob( rootdir + subject_id + "/" + subdate + '/dwi/' + '*dwi.nii.gz' )[0] 
rsfn = glob.glob( rootdir + subject_id + "/" + subdate + '/func/' + '*bold.nii.gz' )[0]

if not os.path.exists( anatfn ) or not os.path.exists( dtfn ) or not os.path.exists( rsfn ):
    print( anatfn + " does not exist : exiting ")
    sys.exit(0)

# generate_mm_dataframe(projectID, subjectID, date, imageUniqueID, modality, source_image_directory, output_image_directory, t1_filename, flair_filename=[], rsf_filenames=[], dti_filenames=[], nm_filenames=[], perf_filename=[])

studycsv = antspymm.generate_mm_dataframe(
        'M3RITravel',
        subject_id,
        subdate,
        '000',
        'T1w',
        rootdir,
        newoutdir,
        t1_filename = anatfn,
        dti_filenames = [dtfn],
        rsf_filenames = [rsfn]
    )
studycsv.to_csv(base_directory + "studycsvs/" + subject_id + "_" + subdate + ".csv")
studycsv2 = studycsv.dropna(axis=1)
mmrun = antspymm.mm_csv(studycsv2,
                        dti_motion_correct='SyN',
                        dti_denoise=True,
                        normalization_template=template,
                        normalization_template_output='ppmi',
                        normalization_template_transform_type='antsRegistrationSyNQuickRepro[s]',
                        normalization_template_spacing=[1,1,1],
                        mysep='_')  # should be this





