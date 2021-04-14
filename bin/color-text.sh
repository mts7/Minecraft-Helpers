#!/bin/bash

function show_text() {
  echo -e "\e[${2}m${1}\e[0m"
}

if [[ "${1}" -gt "${2}" ]]; then
  show_text "${1}" '92'
elif [[ "${1}" -gt "${3}" ]]; then
  show_text "${1}" '93'
else
  show_text "${1}" '91'
fi
