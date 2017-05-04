grep -o "\('''\||\).*" symphony_parser.py | sed "s/|/\ \ \ \ |/g" | sed "s/'''//g" > clean_grammar
echo "Grammar saved in clean_grammar"
