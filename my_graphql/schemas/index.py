type_defs = """
        type Query {
        generateDataset(input_file_path: String!): DatasetOutput!
        }

        type DatasetOutput {
        fileGenerated: String!
        information: String!
        }
"""
