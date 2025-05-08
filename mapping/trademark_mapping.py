trade_mappings = {
        "settings": {
            "analysis": {
                "analyzer": {
                "korean_ngram": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase"]
                }
                }
            }
        },
        "mappings": {
            "properties": {
            "all_text_fields": {
                "type": "text",
                "analyzer": "korean_ngram",
            },
            "all_keyword_fields": {
                "type": "keyword",
            },
            "productName": {
                "type": "text",
                "copy_to": ["all_text_fields","all_keyword_fields"],
                "fields": {
                "keyword": { "type": "keyword", "ignore_above": 256 }
                }
            },
            "productNameEng": {
                "type": "text",
                "copy_to": ["all_text_fields","all_keyword_fields"],
                "fields": {
                "keyword": { "type": "keyword", "ignore_above": 256 }
                }
            },
            "applicationNumber": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "applicationDate": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "registerStatus": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "publicationNumber": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "publicationDate": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "registrationNumber": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "registrationDate": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "registrationPubNumber": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "registrationPubDate": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "internationalRegDate": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "internationalRegNumbers": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "priorityClaimNumList": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "priorityClaimDateList": {
                "type": "date",
                "null_value": "99990101",
                "format": "yyyyMMdd"
            },
            "asignProductMainCodeList": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "asignProductSubCodeList": {
                "type": "keyword",
                "null_value": "NULL",
            },
            "viennaCodeList": {
                "type": "keyword",
                "null_value": "NULL",
            }
        }
    }
}