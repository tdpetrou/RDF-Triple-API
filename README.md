# RDF-Triple-API

A simple API for extracting the RDF triple (subject, predicate, object) of any sentence.

The algorithm implemented is taken from [this paper] (echo "# RDF-Triple-API" >> README.md) by Delia Rusu.

The endpoint for the api is http://www.newventify.com/rdf and has url parameter `sentence`

A complete request would look like the following: `http://www.newventify.com/rdf?sentence=The man stood next to the refrigerator` and will return

`
{
  "rdf_triple": {
    "object": "refrigerator", 
    "predicate": "stood", 
    "subject": "man"
  }
}
`
