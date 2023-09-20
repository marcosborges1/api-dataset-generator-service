type_defs = """
        type Query {
                generateDataset(generatedExtractedFile: String!): DatasetOutput!
        }

        type DatasetOutput @key(fields: "generatedDatasetFile") {
                generatedDatasetFile: String!
                information: String!
        }
"""
