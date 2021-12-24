 in gr.query:
        if query.getRelation() == 'YN':
            print(query.getRelation())
        else:
            print(query.getLeft().getValue() + ' ' +
                  query.getRelation() + ' ' + query.getRight().getValue())
