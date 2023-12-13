/**
 * Implements a weighted random choice on an array of objects.
 *
 * @param {Array} choices - An array of objects to be selected
 * @param {Array} weights - An array of weights for each object
 * @returns {Object} - A random object from the array.
 */

export function weightedRandom(choices, weights) {
    let totalWeight = 0;
    for (let i = 0; i < weights.length; i++) {
        totalWeight += weights[i];
    }

    let sum = 0;
    let rand = Math.random() * totalWeight;
    for (let i = 0; i < choices.length; i++) {
        sum += weights[i];
        if (rand <= sum) {
            return choices[i];
        }
    }

    return choices[choices.length - 1]
}


/**
 * Generates a random string of the given length
 */
export function randomString(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;

    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }

    return result;
}