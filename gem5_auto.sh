 #!/bin/bash

echo "Hello!"
echo -e "'take_checkpoint' to execute the 'take_checkpoint.py' \n'resuming_checkpoint' to execute the 'resuming_checkpoint.py' \n'statistics' to execute the 'statistics.py' \n'no' to do nothing \n[bbv/simpoint/take_checkpoint/resuming_checkpoint/statistics/no] : "
read get_cmd 
echo "$get_cmd"
if [ $get_cmd == "take_checkpoint" ]; then
    python3 take_checkpoint.py
elif [ $get_cmd == "resuming_checkpoint" ]; then
    python3 resuming_checkpoint.py
elif [ $get_cmd == "statistics" ]; then
    python3 statistics.py
elif [ $get_cmd == "no" ]; then
    echo "bye bye!"

else
    echo "Wrong input!"
fi

