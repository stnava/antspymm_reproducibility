#!/bin/bash
echo TASK ID is $SLURM_ARRAY_TASK_ID
python3 /mnt/cluster/data/Hawco_M3RI_Travel/src/slurm/02_job_script.py $SLURM_ARRAY_TASK_ID
