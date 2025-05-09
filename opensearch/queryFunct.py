from create_client import create_client



def query_OpenSearch(search_term):

    client = create_client()

    index_name = "comments"

    query = {
        "size": 0,  # No need to fetch individual documents
        "aggs": {
            "docketId_stats": {
                "terms": {
                    "field": "docketId.keyword",  # Use .keyword for exact match on text fields
                    "size": 1000000  # Adjust size for expected number of unique docketIds
                },
                "aggs": {
                    "matching_comments": {
                        "filter": {
                            "match_phrase": {
                                "commentText": search_term
                            }
                        }
                    }
                }
            }
        }
    }

    # Execute the query
    response = client.search(index=index_name, body=query)

    # Extract the aggregation results
    dockets = response["aggregations"]["docketId_stats"]["buckets"]

    # Create a list of dockets in json format that contains the docketId, docketTitle, the number of total comments, and the number of matching comments out of total comments
    dockets_list = [
        {
            "docketID": docket["key"],
            "doc_count": docket["doc_count"],
            "matching_comments": docket["matching_comments"]["doc_count"]
        }

        for docket in dockets
        ]
    
    return dockets_list

