# Recipe Service - Main Description

## Overview

In this task, I have built a backend service called the **Recipe Service**, which provides a **REST API** for managing user ingredient preferences and generating personalized recipes based on those preferences. The service leverages **Large Language Models (LLMs)** to process user inputs, generate recipe suggestions, and output the results in a structured **JSON** format.

### Key Features:
- **User Ingredient Preferences**: The service allows users to input their available ingredients and preferences.
- **Recipe Generation**: Based on the available ingredients and preferences, the service generates personalized recipe suggestions.
- **REST API**: The service exposes several endpoints that enable users to interact with the system programmatically, including:
  - **Store Preferences**: An endpoint to submit and store user ingredient preferences.
  - **Retrieve Preferences**: An endpoint to retrieve stored user preferences from the database (MongoDB).
  - **Generate Recipes**: An endpoint to generate personalized recipes based on available ingredients and preferences.

### Project Goals:
- Integrating LLMs into a Pipeline
- Building Clean, Maintainable Code

## Challenges and Solutions

### 1. **Storing Ingredients and Preferences**

In our recipe generation app, users must enter two things:
- **Ingredient Preferences:** What ingredients they like or dislike.
- **Available Ingredients:** A list of the ingredients they have, including amounts and units.

The challenge is that this kind of data can vary a lot. Different users may enter different ingredients and quantities, which makes the data unstructured.

#### Key design solution:
In order to avoid a rigid database structure, given the wide variety of ingredient names, and different quantities and units, I opted to use MongoDB. Reasons to use MongoDB:

- Flexible Storage: MongoDB doesn't require a fixed structure. This means I can store different types of data, like ingredient names, like/dislike preferences, quantities, and units, without needing to adjust the database every time.
- Easy to Update: If I need to add new information later, MongoDB lets me do it without making major changes to the database.
- Handles Different Data: Since users might enter a variety of ingredients, MongoDB works well for storing all the different kinds of data they might input.

#### Areas for future improvement:
- User inputs can vary widely, leading to potential inconsistencies or invalid data. Validation rules can be implemented to ensure the data is in the expected format, or alternatively, a machine learning model could be used for validation, as they are effective at understanding human language.
- There is no tracking of when user preferences are created or updated.
- The system does not track additional user information that could be useful for generating better recipes, such as cooking skill level, preferred meal types (e.g., breakfast, dinner), and time constraints. Collecting this information would allow the system to generate even more tailored recipes based on a broader range of factors.
- Ingredient units are stored as simple strings without validation. I assumed that the LLM would generate ingredients using consistent units, but adding unit validation would improve accuracy and consistency.
- Currently, the app interacts directly with MongoDB for data storage and retrieval. Implementing an abstraction layer, would decouple the business logic from database operations, making the code cleaner and easier to maintain.
- Implement security and user permits. 
- The user should be able to update their preferences. 

### 2. **Integrating LLMs for Recipe Generation**

The goal was to integrate Large Language Models (LLMs) to generate coherent and relevant recipe suggestions based on the user's available ingredients and preferences, particularly focusing on liked ingredients and excluding disliked ones.

#### Solution:
To achieve this, I prompt the model to generate five recipe suggestions. The model ensures that disliked ingredients are avoided, and only liked ingredients are used, all while considering the available ingredients that the user has on hand. This approach allows the system to generate personalized and relevant recipe suggestions tailored to the user’s preferences and inventory.

#### Areas for future improvement:
- While OpenAI's language model is great for demos, it's expensive, especially for high-traffic apps or complex tasks. In production, it would be useful to explore cheaper models that can achieve similar results with lower costs.
- The model could be fine-tuned to reflect a specific tone that aligns with the company’s branding (e.g., friendly, professional, casual). This would make the recipe suggestions more consistent and personalized to the company's style.
- The model could be improved to take into account additional user preferences, such as dietary restrictions (e.g., gluten-free, vegan) or preferred meal types (e.g., breakfast, dinner), to generate more relevant recipes.
- The model could be fine-tuned to better handle complex recipes with multiple steps and cooking techniques, ensuring the instructions are clear and easy to follow.


#### 3. Other areas for futher improvement/future work:
- Implement full unit testing and design integration tests, including async test cases for asynchronous functions.
- Address Flake8 E501 errors.
- Integrate the pipeline and dataset for LLM testing, optimizing async data fetching and processing.
- Improve API key configuration and move model-related variables to the config file.
- Integrate the pipeline and dataset for LLM testing.
