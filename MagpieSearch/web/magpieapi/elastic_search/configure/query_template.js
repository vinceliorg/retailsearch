{
 "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "must": [
              {
                "bool": {
                  "filter": [
                    {
                      "simple_query_string": {
                        "fields": [
                          "title",
                          "productdetails"
                        ],
                        "query": "{{query}}",
                        "default_operator": "{{retrieval_boolean_operator}}"
                      }
                    }
                  ]
                }
              }
            ],
            "should": [
              {
                "multi_match": {
                  "type": "most_fields",
                  "query": "{{query}}",
                  "fields": [
                    "title^100",
                    "productdetails^10"
                  ]
                }
              }
            ]
          }
        }
      ],
      "should": [
        {
          "multi_match": {
            "type": "phrase",
            "query": "{{query}}",
            "slop": 20,
            "fields": [
              "tiltle^100",
              "productdetails^1"
            ]
          }
        }
      ]
    }
  }
}