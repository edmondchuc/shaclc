const examples = [
  {
    name: 'array-in.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/array-in.shaclc'
  },
  {
    name: 'basic-shape-iri.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/basic-shape-iri.shaclc'
  },
  {
    name: 'basic-shape-with-target.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/basic-shape-with-target.shaclc'
  },
  {
    name: 'basic-shape-with-targets.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/basic-shape-with-targets.shaclc'
  },
  {
    name: 'basic-shape.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/basic-shape.shaclc'
  },
  {
    name: 'class.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/class.shaclc'
  },
  {
    name: 'comment.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/comment.shaclc'
  },
  {
    name: 'complex1.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/complex1.shaclc'
  },
  {
    name: 'complex2.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/complex2.shaclc'
  },
  {
    name: 'count-0-1.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/count-0-1.shaclc'
  },
  {
    name: 'count-0-unlimited.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/count-0-unlimited.shaclc'
  },
  {
    name: 'count-1-2.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/count-1-2.shaclc'
  },
  {
    name: 'count-1-unlimited.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/count-1-unlimited.shaclc'
  },
  {
    name: 'datatype.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/datatype.shaclc'
  },
  {
    name: 'directives.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/directives.shaclc'
  },
  {
    name: 'empty.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/empty.shaclc'
  },
  {
    name: 'escaped_chars.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/escaped_chars.shaclc'
  },
  {
    name: 'nestedShape.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/nestedShape.shaclc'
  },
  {
    name: 'node-or-2.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/node-or-2.shaclc'
  },
  {
    name: 'node-or-3-not.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/node-or-3-not.shaclc'
  },
  {
    name: 'nodeKind.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/nodeKind.shaclc'
  },
  {
    name: 'path-alternative.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-alternative.shaclc'
  },
  {
    name: 'path-complex.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-complex.shaclc'
  },
  {
    name: 'path-inverse.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-inverse.shaclc'
  },
  {
    name: 'path-oneOrMore.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-oneOrMore.shaclc'
  },
  {
    name: 'path-sequence.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-sequence.shaclc'
  },
  {
    name: 'path-zeroOrMore.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-zeroOrMore.shaclc'
  },
  {
    name: 'path-zeroOrOne.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/path-zeroOrOne.shaclc'
  },
  {
    name: 'property-empty.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/property-empty.shaclc'
  },
  {
    name: 'property-not.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/property-not.shaclc'
  },
  {
    name: 'property-or-2.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/property-or-2.shaclc'
  },
  {
    name: 'property-or-3.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/property-or-3.shaclc'
  },
  {
    name: 'shapeRef.shaclc',
    code: 'https://cdn.jsdelivr.net/gh/edmondchuc/shaclc@latest/tests/data/valid/shapeRef.shaclc'
  }
]

export { examples }
