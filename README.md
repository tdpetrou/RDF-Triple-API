# RDF-Triple-API

A simple API for extracting the RDF triple (subject, predicate, object) of any sentence.

The algorithm implemented is taken from [this paper] (echo "# RDF-Triple-API" >> README.md) by Delia Rusu.

The sentence is parsed using the [stanford parser] (http://nlp.stanford.edu/software/lex-parser.shtml)

The endpoint for the api is http://www.newventify.com/rdf and has url parameter `sentence`

A complete request would look like the following: `http://www.newventify.com/rdf?sentence=The man stood next to the refrigerator` and will return

`
{
  "object": {
    "POS": "NN", 
    "Tree Attributes": [], 
    "Word Attributes": [
      [
        "the", 
        "DT"
      ]
    ], 
    "word": "refrigerator"
  }, 
  "parse_tree": "Tree('ROOT', [Tree('S', [Tree('NP', [Tree('DT', ['The']), Tree('NN', ['man'])]), Tree('VP', [Tree('VBD', ['stood']), Tree('ADVP', [Tree('JJ', ['next'])]), Tree('PP', [Tree('TO', ['to']), Tree('NP', [Tree('DT', ['the']), Tree('NN', ['refrigerator'])])])])])])", 
  "predicate": {
    "POS": "VB", 
    "Tree Attributes": [
      "Tree('ADVP', [Tree('JJ', ['next'])])"
    ], 
    "Word Attributes": [], 
    "word": "stood"
  }, 
  "rdf": [
    "man", 
    "stood", 
    "refrigerator"
  ], 
  "sentence": "The man stood next to the refrigerator", 
  "subject": {
    "POS": "NN", 
    "Tree Attributes": [], 
    "Word Attributes": [
      [
        "The", 
        "DT"
      ]
    ], 
    "word": "man"
  }
}
`
