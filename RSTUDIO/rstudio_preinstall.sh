# Kill app process
appName="$4"
running_proc=$(ps -eaf | grep "$appName" | grep -v "grep" |  awk '{print $2}' 2>/dev/null)
for proc in $running_proc
do
  echo "Killed Process ID: $proc"
  kill $proc
done