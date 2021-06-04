#! /bin/bash
git lfs install
project_dir=$(pwd)

function submodules_updater {
  parent_dir=$(pwd)
  for i in "./.gitmodules"; do
    while read line; do
      if [[ $line =~ "path = " ]]; then
        submodule_path=$(echo $line | cut -d '=' -f 2 | sed -e 's/^[[:space:]]*//')
        submodule_path_presents=true
        lower_submodule_cheker=$submodule_path"/.gitmodules"
      fi
      if [[ $line =~ "url = " ]]; then
        submodule_url=$(echo $line | cut -d '=' -f 2 | sed -e 's/^[[:space:]]*//' | sed -e 's%https://<gitlab>.<domain>/<some-groups-or-else>%..%g')
        submodule_url_presents=true
        if [[ $parent_url_dir_present == true ]]; then
          submodule_url="../"${submodule_url##.*/}
        fi
        parent_url_dir_present=true
      fi
      if [[ $submodule_url_presents == true && $submodule_path_presents == true ]]; then
        git submodule sync --recursive $submodule_path
        git submodule set-url $submodule_path $submodule_url
        git submodule update --init --remote --rebase $submodule_path
        submodule_url_presents=false
        submodule_path_presents=false
        if [[ -s $lower_submodule_cheker ]]; then
          cd $submodule_path
          submodules_updater
          cd $parent_dir
        fi
        parent_url_dir_present=false
      fi
    done < "./.gitmodules"
  done
  parent_dir=$project_dir
}

submodules_updater
