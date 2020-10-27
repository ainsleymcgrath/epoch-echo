# did the changelog change? for enforcing documentation on deployed branches
branch=$(git branch --show-current)

if [[ $branch == 'master' || $branch == 'dev' ]]; then
  git diff origin/$branch --name-only \
    | grep 'CHANGELOG' \
    | wc -l \
    | awk '{
      if ($0 == 1) {
        print "Ok"; exit 0
      } else {
        print ">:( Changelog"; exit 1
      }
    }'
  exit  # awk's exit doesn't exit the whole script
fi

echo "Didn't check changelog fyi."
