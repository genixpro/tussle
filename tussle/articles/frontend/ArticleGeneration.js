
export function generateArticlePrompt(paragraph_generating_prompt, existingSections, questionAnswer, nextSection) {
    let existing = "";
    if (existingSections.length > 0) {
        for (let section of existingSections) {
            existing += `${section}\n\n`;
        }
    } else {
        existing = " ";
    }

    // Now we substitute in the data to the paragraph generating prompt
    let prompt = paragraph_generating_prompt.replace(/\$existing/g, existing);
    prompt = prompt.replace(/\$answer/g, questionAnswer);
    prompt = prompt.replace(/\$next/g, nextSection);

    return prompt;
}