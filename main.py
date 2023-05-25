import MeCab
from flask import Flask, request, jsonify
from flask_cors import CORS

tagger = MeCab.Tagger("-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
app.config['JSON_AS_ASCII'] = False

# routing
@app.route('/split', methods={"POST"})
def index():
    req = request.json['text']
    print(req)
    splitType = request.json['splitType']
    print(splitType)
    result = categolizeNoun(req, splitType)
    print(result)
    return jsonify({"result": result})

# 名詞のみ抽出
def categolizeNoun (text, splitType):
  node = tagger.parseToNode(text)
  word_list=[]
  while node:
    word_type = node.feature.split(',')[0]
    #名詞の他にも動詞や形容詞なども追加できる
    if word_type in [splitType]:
        word_list.append(node.surface)
    node=node.next
  word_chain=' '.join(word_list)
  print(word_list)
  return word_list

app.run(port=8000, debug=True)