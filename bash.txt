while IFS='' read -r line || [[ -n "$line" ]]; do
        read -r line2
        python main1.py 3 6 $line &
        python main1.py 3 6 $line2 &
        wait
done < "$1"