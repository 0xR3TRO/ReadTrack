import api from "./api";

export const getAuthors = async (params = {}) => {
    const response = await api.get("/authors", { params });
    return response.data;
};

export const getAuthor = async (id) => {
    const response = await api.get(`/authors/${id}`);
    return response.data;
};

export const createAuthor = async (data) => {
    const response = await api.post("/authors", data);
    return response.data;
};

export const updateAuthor = async (id, data) => {
    const response = await api.put(`/authors/${id}`, data);
    return response.data;
};

export const deleteAuthor = async (id) => {
    const response = await api.delete(`/authors/${id}`);
    return response.data;
};
