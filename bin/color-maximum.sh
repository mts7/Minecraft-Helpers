#!/bin/bash

function show_text() {
  echo -e "\e[${2}m ${1} \e[0m"
}

if [[ "${1}" < "${2}" ]]; then
  show_text "${1}" '42'
elif [[ "${1}" < "${3}" ]]; then
  show_text "${1}" '43'
else
  show_text "${1}" '41'
fi
