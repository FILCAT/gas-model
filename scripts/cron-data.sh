#!/bin/bash

# Use a trailing slash in directory if not provided
[[ "$2" != */ ]] && dir="$2"/ || dir="$2"

./lotus state --tipset=@$1 compute-state  --json | jq --argjson height "$1" '. + {Height: $height}'  >  "${dir}"gas-trace-"$1".json

cat "${dir}"gas-trace-$1.json  | jq -c '.Trace | .[]  | select( .Msg | .To== "f03") | .ExecutionTrace | .Subcalls | .[] | select( .Msg | .To == "f04") | .Subcalls | .[] | select( .Msg | .Method == 12) | {"To":( .Msg | .To) , "Gas": (reduce (.. | .GasCharges? | select(.) | .[])  as $gas ({tg: 0}; {tg: ($gas.tg + .tg)}))} ' | jq --argjson height "$1" -s '[.[] | . + {Height: $height}]'  > "${dir}"crongas-"$1".json

cat "${dir}"gas-trace-$1.json  | jq -c '.Trace | .[]  | select( .Msg | .To== "f03") | .ExecutionTrace | .Subcalls | .[] | select( .Msg | .To == "f04") | .Subcalls | .[] | select( .Msg | .Method == 12) | {"To":( .Msg | .To) , "Gas": (reduce (.. | .GasCharges? | select(.) | .[] | select(.Name == "wasm_exec") ) as $gas ({tt: 0}; {tt: ($gas.tt + .tt)}))} ' | jq --argjson height "$1" -s '[.[] | . + {Height: $height}]'  > "${dir}"crontime-"$1".json

jq -s '
  (.[0] + .[1]) |
  group_by(.To) |
  map(reduce .[] as $item ({}; .To = $item.To | .Height = $item.Height | .Gas += $item.Gas))
' "${dir}"crongas-"$1".json  "${dir}"crontime-"$1".json > "${dir}"cronsummary-"$1".json

(cat "${dir}"cronsummary-"$1".json | ./lotus-shed cron-wc deadline-summary; cat "${dir}"cronsummary-"$1".json) | jq -s '.' | jq 'transpose | .[] | .[0] + .[1]' | jq -s '.' > "${dir}"output-"$1".json

# remove intermediates
rm "${dir}"/crongas-"$1".json
rm "${dir}"/crontime-"$1".json
