# API Dataset Generator (ADG)

## Overview

The API Dataset Generator (ADG) is a dedicated component within the Agape approach, tasked with the generation of datasets that encompass all 12 general information data required for similarity analyses. This dataset is crafted using a Cartesian Product, which juxtaposes all response attributes present in each endpoint of an API with every input attribute in all other APIs. The primary intention is to create a comprehensive dataset facilitating in-depth similarity analyses.

The essence of ADG's functionality is rooted in the [Algorithm section](#Algorithm). This algorithm harnesses the information extracted from the APIs by the [API Syntactic Extractor (ASE)](https://github.com/marcosborges1/api-syntactic-extractor-service). It then returns a dataset formulated through the Cartesian Product of the 12 general information data points.

## Implementation Details

The core of ADG is defined by the intricate Algorithm \ref{alg:dataset}. This algorithm, designed to seamlessly integrate with the data provided by the API Syntactic Extractor, facilitates the creation of a robust and comprehensive dataset vital for similarity analysis tasks.

## Algorithm

The ADG's core is based on the algorithm described below.

<img src="/images/adg_algorithm.png" height="300"/>

## Setup

Before running the application, make sure to install the required dependencies. You can install them using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

Before you start registering the microservices below, be sure to start them.

```bash
python server.py
```

**Note**:

- The default PORT is _4002_, but can be change for your convenience.
- This project heavily relies on GraphQL, a powerful query language for APIs, and a server-side runtime for executing those queries with your existing data. If you're unfamiliar with GraphQL or wish to dive deeper, you can [learn more about GraphQL here](https://graphql.org/).

## Project Status

The ADG, currently in the evolutionary phase, functions as a proof of concept. It is actively undergoing improvements and changes to refine its capabilities and more effectively meet new requirements.

## Author

**Marcos Borges**  
PhD Student at Federal University of Ceará, Brazil  
Email: [marcos.borges@alu.ufc.br](mailto:marcos.borges@alu.ufc.br)

## References

- **Agape Approach**: As the Agape approach is being validated through conferences and journals, updates will be periodically provided here. Once the validation process concludes and findings are published, a direct link to the paper will be shared in this section for easy accessibility.

## Contributing

Community-driven improvements are always welcome. If you're looking to contribute, feel free to raise pull requests. For more significant changes or additions, it's recommended to open an issue first for discussions.

## License

[Your License Information Here, e.g., MIT]
