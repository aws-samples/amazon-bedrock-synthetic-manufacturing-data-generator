# Generative AI Synthetic Data Generator

## Table of Contents

- [Why Synthetic Data Generation](#why)
- [Solution Overview](#solution-overview)
- [Deploying the Solution](#installation)
- [Contributing](#contributing)
- [License](#license)

## Why Synthetic Data Generation <a name="why"></a>

Manufacturing processes generate large amounts of sensor data that can be used for analytics and machine learning models. However, this data may contain sensitive or proprietary information that cannot be shared openly. Synthetic data allows the distribution of realistic example datasets that preserve the statistical properties and relationships in the real data, without exposing confidential information. This enables more open research and benchmarking on representative data. Additionally, synthetic data can augment real datasets to provide more training examples for machine learning algorithms to generalize better. Data augmentation with synthetic manufacturing data can help improve model accuracy and robustness. Overall, synthetic data enables sharing, research, and expanded applications of AI in manufacturing while protecting data privacy and security.

This code repository delves into the specific challenges faced by the semiconductor industry regarding data collection. The semiconductor industry, known for its intricate manufacturing processes, generates a vast amount of sensor data crucial for analytics and machine learning. However, due to legacy systems and complex data infrastructure, collecting this data in real-time and at scale can be a challenging task. The adoption of synthetic data generation, as exemplified by our solution with Amazon Bedrock, provides a distinct advantage in building machine learning models. By rapidly generating synthetic datasets that mirror the statistical properties of real data, businesses in the semiconductor industry can accelerate their machine learning initiatives while overcoming the challenges posed by their legacy systems. It's a strategic approach that not only addresses industry-specific hurdles but can be seamlessly applied to revolutionize data practices across various other sectors.


## Solution Overview <a name="solution-overview"></a>

![product_image](./docs/architecture.jpg)

1. **User-Initiated [AWS Lambda](https://aws.amazon.com/lambda/) Function:**
	* Parameters:
		* `industry`: Specifies the industry for data generation (e.g., semiconductor).
		* `number`: Defines the quantity of shopfloor machines to be generated (recommended at 10).
		* `user_id`: Represents either an authentic user or a pseudonymous ID (e.g., michael-wallner).

2. **AWS Lambda Leveraging Amazon Bedrock:**
	* Utilizes Amazon Bedrock to generate a list of machines, prompted by:

```
Generate a NUMBERED list of at least {number} different {industry} manufacturing machines.
IMPORTANT: Fence the list with '```'. DO NOT add any explanations, only the machine name.
```

3. **AWS Lambda Writing to [Amazon DynamoDB](https://aws.amazon.com/dynamodb/):**
	* Stores the generated machine list and `user_id` in an Amazon DynamoDB table.
	* Sets an `active` flag, signalling [AWS CodeBuild](https://aws.amazon.com/codebuild/) to process the specific request.
4. AWS Lambda Triggering [AWS CodePipeline](https://aws.amazon.com/codepipeline/):
	* Initiates an AWS CodePipeline with two key steps:
		1. *Source Code Retrieval*: Accesses solution code through [AWS CodeCommit](https://aws.amazon.com/codecommit/).
		2. *Build Process Execution*: Utilizes AWS CodeBuild to:
			* Extract active machine signals from DynamoDB.
			* Employ Amazon Bedrock to generate Python code for synthetic data creation.
			* Execute the Python code for data generation.
			* Store the generated data in an [Amazon Simple Storage Service (S3)](https://aws.amazon.com/s3/) bucket.
5. **Prompt Example for [Amazon Bedrock](https://aws.amazon.com/bedrock):**
	* Draws inspiration from Amazon Bedrock console examples, guiding users to write high-quality scripts tailored to specific tasks.
	* The specific prompt we used is listed below:

```
Write a high-quality {language} script for the following task, something a {context} {language} expert would write. You are writing code for an experienced developer so only add comments for things that are non-obvious. Make sure to include any imports required.
```

```
NEVER write anything before the ```{language}``` block. After you are done generating the code and after the ```{language}``` block, check your work VERY CAREFULLY to make sure there are no mistakes, errors, or inconsistencies. It's IMPORTANT that if there are ERRORS, LIST THOSE ERRORS in <error> tags, then GENERATE a new version with those ERRORS FIXED. If there are no errors, write "CHECKED: NO ERRORS" in <error> tags.
```

```
Here is the task:
<task>
	* Write code to generate synthetic {question} data using ACTUAL and REALISTIC physical signal names and values
	* Add some occasional anomalies to the signals that are created
	* The first column is `Timestamp` in the format `yyyy-MM-dd HH:mm:ss`
	* The `Timestamp` is collected every minute and the dataset should span an entire year
	* Write a `main` function that executes the data generation and saves the entire data to local disk. Make sure the file contains the headers!
	* Use object-oriented programming for all code and add docstrings
</task>
```

Where `language` is the programming language to use, context is set to `skilled` developer and the `question` is the machine name used for synthetic data generation.

6. **Amazon S3 Bucket for Data Storage:**
	* Tailored for each `user_id`, this bucket serves as a repository for machine-generated data.
	* Offers utility in machine learning endeavors, including applications like [Amazon Lookout for Equipment](https://aws.amazon.com/lookout-for-equipment/) for automated anomaly detection.


## Deploying the Solution <a name="installation"></a>

**Supported Python Versions**

This [AWS CDK](https://aws.amazon.com/cdk/) stack was developed using `Python 3.10`

[Download](https://www.python.org/downloads/) it here and install it.

Once you cloned the repository create a virtual environment using

```
python3 -m venv .venv
```

Activate the environment:

```
source .venv/bin/activate
```

*Optional: Windows users*

```
.venv\Scripts\activate.bat
```

Next install the required libraries using:

```
pip install -r requirements.txt
```

Finally, initialize pre-commit using

```
pre-commit install
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

And of course deploy the stack:

```
cdk deploy --all --require-approval never
```

The `-—all` flag ensures that all components are installed at once. By specifying `-—require-approval` never you won’t need to approve each component to be deployed.

## Tips
* `cdk deploy` requires `docker`. If you are using docker alternatives like [finch]([runfinch/finch: The Finch CLI an open source client for container development](https://github.com/runfinch/finch)). you need to export this environment variable before running `cdk` commands:

	```
	export CDK_DOCKER=finch
	```
* You can override the default deployment region by setting
	```
	export AWS_REGION=eu-west-1
	```



## Contributing
If you wish to contribute to the project, please see the [Contribution Guidelines](./CONTRIBUTING.md).

## License

This repository is licensed under the MIT-0 License. It is copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved. The license is available at: http://aws.amazon.com/mit-0
