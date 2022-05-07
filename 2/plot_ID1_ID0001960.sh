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
   "lfn": "H1-INFERENCE_5017-0-10.hdf",
   "id": 1,
   "src_urls": [
     { "site_label": "local", "url": "file:///work/shashwat.singh/3gsky/prod/ET/300/output/local-site-scratch/work/./H1-INFERENCE_5017-0-10.hdf", "checkpoint": "false" }
   ],
   "dest_urls": [
     { "site_label": "condorpool_symlink", "url": "symlink://$PWD/H1-INFERENCE_5017-0-10.hdf" }
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
pegasus-kickstart  -n plot_ID1 -N ID0001960 -R condorpool_symlink  -s H1-PLOT_5017-0-10.png=H1-PLOT_5017-0-10.png -L gw.dax -T 2022-05-06T18:56:50+00:00 /work/shashwat.singh/cbc-hm/bin/pycbc_inference_plot_posterior --z-arg snr --plot-injection-parameters  --pick-injection-by-time  --input-file H1-INFERENCE_5017-0-10.hdf --output-file H1-PLOT_5017-0-10.png
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
   "lfn": "H1-PLOT_5017-0-10.png",
   "id": 1,
   "src_urls": [
     { "site_label": "condorpool_symlink", "url": "file://$PWD/H1-PLOT_5017-0-10.png", "checkpoint": "false" }
   ],
   "dest_urls": [
     { "site_label": "local", "url": "file:///work/shashwat.singh/3gsky/prod/ET/300/output/local-site-scratch/work/./H1-PLOT_5017-0-10.png" }
   ] }
]
eof

pegasus_lite_section_end stage_out

set -e


# clear the trap, and exit cleanly
trap - EXIT
pegasus_lite_final_exit

