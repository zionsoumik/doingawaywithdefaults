#!/bin/bash
trap 'trap - SIGTERM && kill 0' SIGINT SIGTERM EXIT
while IFS='' read -r line || [[ -n "$line" ]]
do
read -r line2
read -r line3
read -r line4
read -r line5
read -r line6
read -r line7
read -r line8
read -r line9
read -r line10
read -r line11
read -r line12
read -r line13
read -r line14
read -r line15
read -r line16
read -r line17
read -r line18
read -r line19
read -r line20
read -r line21
read -r line22
read -r line23
read -r line24
read -r line25
python main1.py 1 5 $line2 &
python main1.py 1 5 $line3 &
python main1.py 1 5 $line4 &
python main1.py 1 5 $line5 &
python main1.py 1 5 $line6 &
python main1.py 1 5 $line7 &
python main1.py 1 5 $line8 &
python main1.py 1 5 $line9 &
python main1.py 1 5 $line10 &
python main1.py 1 5 $line11 &
python main1.py 1 5 $line12 &
python main1.py 1 5 $line13 &
python main1.py 1 5 $line14 &
python main1.py 1 5 $line15 &
python main1.py 1 5 $line16 &
python main1.py 1 5 $line17 &
python main1.py 1 5 $line18 &
python main1.py 1 5 $line19 &
python main1.py 1 5 $line20 &
python main1.py 1 5 $line21 &
python main1.py 1 5 $line22 &
python main1.py 1 5 $line23 &
python main1.py 1 5 $line24 &
python main1.py 1 5 $line25 &
done< "$1"
