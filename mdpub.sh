gitUrl='ssh://git@github.com/akhsiM/akhsiM.github.io.git'
gitpostdir='/Random/_posts/'
gitimgdir='/static/img/'

gitRoot=$(basename "$gitUrl" .git)
filename=$(basename "$1")
title=$(echo "$filename" | cut -d '.' -f 1)
gitImgpostdir=$gitRoot$gitimgdir$title
filedir=$(dirname "$1")

echo "Title = $title"
echo "Git Dir = $gitUrl"

# Set temp folder
temp='mdpub-tmp'

# Python script mdmod.py needs to be in the same dir as this script
# Setting env variable for mdmod.py script
mdmod=$(dirname "$(readlink -f "$0")")"/mdmod.py"

# Set filename for markdown with timestamp appended at the beginning
stamp=$(date -r "$1" '+%Y-%m-%d-')
newfilename=$stamp$filename

if [ $# -eq 0 ]
    then
        echo "No argument supplied."
        exit 1
fi

# Confirm if you want to delete tmp folder
cd "$filedir"
if [ -d "$temp" ]
    then 
        echo "$temp folder already exists at $filedir"
        read -p "Delete existing $temp folder? " -n 1 -r answer
        echo
        if [[ $answer =~ ^[Yy]$ ]];
            then
                trash -r $temp
            else
                echo 'Exiting..'
                exit 1
            fi
    fi 
mkdir $temp

# Execute Python script
if python "$mdmod" "$1"
    then
        echo "Execution of Python script succeeded."
    else
        echo "Execution of Python script failed.."
        exit 1
fi

mv "./$temp/$filename" "./$temp/$newfilename"
git clone $gitUrl && echo "Git has been cloned." &&
echo "Moving Markdown file to local git.." && mv "./$temp/$newfilename" "./$gitRoot$gitpostdir" &&
echo "Moving Image files to local git.." && mkdir "$gitImgpostdir" && cd "$temp" && mv * "../$gitImgpostdir/" && cd ..
echo "committing.." && cd $gitRoot && git add -A && git commit -m "Commit - $newfilename"
echo "pushing.." && git push origin master && cd ..
echo "Cleaning up.." && rm -rf "$gitRoot" "$temp"