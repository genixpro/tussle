/**
 * Takes a promise, and returns a new promise that won't
 * resolve until atleast the minimum time has passed.
 * This can help ensure that UI's don't update too quickly for users to notice.
 *
 *
 * @param promise
 * @param minimumTime
 * @returns {*}
 */
export function ensureMinimumPromiseResolveTime(promise, minimumTime) {
    let startTime = new Date();
    return promise.then((result) => {
        const endTime = new Date();
        const timeTaken = endTime.getTime() - startTime.getTime();
        const timeToDelay = Math.max(0, minimumTime - timeTaken)

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(result);
            }, timeToDelay)
        });
    });
}

