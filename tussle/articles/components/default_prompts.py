


default_paragraph_generating_prompt = """Adopt the persona of a professional artificial intelligence engineer, who is responsible for explaining how AI works to regular, non-technical people. You are writing an article about AI. You have a partial article already completed, and you need to write the next section of that article, based on the given instructions.

The client has given you a specific working example of an AI product that they want to build. Take their AI product into account when writing the article. The AI product they want to build is $answer.

Here is the current partial article. If it is empty, that means this is the very first section of the article.

\"\"\"$existing\"\"\"

Now to write the next section, please take the following template paragraph, and modify it following the instructions in the square brackets, so that it takes into account the AI product description the user provided, which is $answer.

\"\"\"$next\"\"\"

Again, please modify the above template paragraph, following the instructions in the square brackets, so that it takes into account the AI product description the user provided, which is $answer."""
