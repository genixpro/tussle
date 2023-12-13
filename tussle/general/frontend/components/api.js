import axios from "axios";
import {ensureMinimumPromiseResolveTime} from "../utils/utils";
import {createContext} from "react";
import { axiosETAGCache } from 'axios-etag-cache';
export const apiAccessTokenContext = createContext(null);

// Apply the axios ETAG interceptor
const axiosWithETAGCache = axiosETAGCache(axios);

let localGCPArticleCachePromise = null;
let localGCPArticleCache = null;

export const api = {
    async getCompletion(prompt) {
        const postParam = {
            prompt: prompt
        }

        const response = await ensureMinimumPromiseResolveTime(axios.post(`/completion`, postParam), 500);

        return response.data;
    },
    async getArticles() {
        const queryParams = {
        }

        const response = await axiosWithETAGCache.get(`/article`, {
            params: queryParams
        });

        return response.data;
    },
    async getArticlesFromGCPStorageCache() {
        if (localGCPArticleCache) {
            return localGCPArticleCache;
        } else if (localGCPArticleCachePromise) {
            return (await localGCPArticleCachePromise).data;
        }

        localGCPArticleCachePromise = axiosWithETAGCache.get(`https://tussle-frontend.storage.googleapis.com/articles.json`);

        localGCPArticleCache = (await localGCPArticleCachePromise).data;

        return localGCPArticleCache;
    },
    async getArticle(articleId) {
        const queryParams = {
        }

        const response = await axiosWithETAGCache.get(`/article/${articleId}`, {
            params: queryParams
        });

        return response.data;
    },
    async getArticleFromGCPStorageCache(articleId) {
        if (!localGCPArticleCache) {
            await api.getArticlesFromGCPStorageCache();
        }

        // Now found the article with the matching _id
        const article = localGCPArticleCache.find((article) => article._id === articleId || article.slug === articleId);
        return article;
    },
    async saveArticle(article) {
        const response = await axios.put(`/article/${article._id}`, article);

        return response.data;
    },
    async createNewArticle() {
        const queryParams = {
        }

        const response = await axios.post(`/article`, {
            params: queryParams
        });

        return response.data;
    },
}

axios.defaults.baseURL = process.env.REACT_APP_BACKEND_API_URL;
axios.interceptors.response.use(function (response) {
    // Do something with response data
    return response;
}, function (error)
{
    if (error.response && error.response.status === 401)
    {
        // Auth0.logout();
        return (Promise.reject(error));
    }

    if (process.env.REACT_APP_DEBUG === "true")
    {
        alert(error.toString());
    } else {
        // Force reload the page. maybe this will help.
        // window.location.reload();
    }
    // Do something with response error
    return (Promise.reject(error));
});


