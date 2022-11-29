import MeCab
from flask import Flask, request, jsonify
import flask

tagger = MeCab.Tagger("-Ochasen")
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['JSON_AS_ASCII'] = False

# routing
@app.route('/split', methods={"POST"})
def index():
    req = request.json['text']
    print(req)
    noun = categolizeNoun(req)
    print(noun)
    return jsonify({"result": noun})

# 名詞のみ抽出
def categolizeNoun (text):
  node = tagger.parseToNode(text)
  word_list=[]
  while node:
    word_type = node.feature.split(',')[0]
    #名詞の他にも動詞や形容詞なども追加できる
    if word_type in ["名詞"]:
        word_list.append(node.surface)
    node=node.next
  word_chain=' '.join(word_list)
  print(word_list)
  return word_list


app.run(port=8000, debug=True)