#!/bin/bash
set -e
pegasus_lite_version_major="5"
pegasus_lite_version_minor="0"
pegasus_lite_version_patch="1"
pegasus_lite_enforce_strict_wp_check="true"
pegasus_lite_version_allow_wp_auto_download="true"


. pegasus-lite-common.sh

pegasus_lite_init

# cleanup in case of failures
trap pegasus_lite_signal_int INT
trap pegasus_lite_signal_term TERM
trap pegasus_lite_unexpected_exit EXIT

printf "\n########################[Pegasus Lite] Setting up workdir ########################\n"  1>&2
# work dir
pegasus_lite_setup_work_dir

printf "\n##############[Pegasus Lite] Figuring out the worker package to use ##############\n"  1>&2
# figure out the worker package to use
pegasus_lite_worker_package

pegasus_lite_section_start stage_in
printf "\n###################### Staging in input data and executables ######################\n"  1>&2
# stage in data and executables
pegasus-transfer --threads 1  --symlink  1>&2 << 'eof'
[
 { "type": "transfer",
   "linkage": "input",
   "lfn": "inj_5194.ini",
   "id": 1,
   "src_urls": [
     { "site_label": "condorpool_symlink", "url": "file:///work/shashwat.singh/3gsky/prod/ET/300/output/inj_5194.ini", "priority": 0, "checkpoint": "false" }
   ],
   "dest_urls": [
     { "site_label": "condorpool_symlink", "url": "symlink://$PWD/inj_5194.ini" }
   ] }
 ,
 { "type": "transfer",
   "linkage": "input",
   "lfn": "prior.ini",
   "id": 2,
   "src_urls": [
     { "site_label": "condorpool_symlink", "url": "file:///work/shashwat.singh/3gsky/config/prior.ini", "priority": 0, "checkpoint": "false" }
   ],
   "dest_urls": [
     { "site_label": "condorpool_symlink", "url": "symlink://$PWD/prior.ini" }
   ] }
]
eof

printf "\n##################### Checking file integrity for input files #####################\n"  1>&2
# do file integrity checks

pegasus_lite_section_end stage_in
set +e
job_ec=0
pegasus_lite_section_start task_execute
printf "\n######################[Pegasus Lite] Executing the user task ######################\n"  1>&2
pegasus-kickstart  -n inference_ID0 -N ID0002027 -R condorpool_symlink  -s H1-INFERENCE_5194-0-10.hdf=H1-INFERENCE_5194-0-10.hdf -L gw.dax -T 2022-05-06T18:56:50+00:00 /work/shashwat.singh/cbc-hm/bin/pycbc_inference --nprocesses 1 --force  --seed 0 --config-file prior.ini inj_5194.ini --output-file H1-INFERENCE_5194-0-10.hdf
job_ec=$?
pegasus_lite_section_end task_execute
set -e
pegasus_lite_section_start stage_out
printf "\n############################ Staging out output files ############################\n"  1>&2
# stage out
pegasus-transfer --threads 1  1>&2 << 'eof'
[
 { "type": "transfer",
   "linkage": "output",
   "lfn": "H1-INFERENCE_5194-0-10.hdf",
   "id": 1,
   "src_urls": [
     { "site_label": "condorpool_symlink", "url": "file://$PWD/H1-INFERENCE_5194-0-10.hdf", "checkpoint": "false" }
   ],
   "dest_urls": [
     { "site_label": "local", "url": "file:///work/shashwat.singh/3gsky/prod/ET/300/output/local-site-scratch/work/./H1-INFERENCE_5194-0-10.hdf" }
   ] }
]
eof

pegasus_lite_section_end stage_out

set -e


# clear the trap, and exit cleanly
trap - EXIT
pegasus_lite_final_exit

