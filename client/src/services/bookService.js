import api from "./api";

export const getBooks = async (params = {}) => {
    const response = await api.get("/books", { params });
    return response.data;
};

export const getBook = async (id) => {
    const response = await api.get(`/books/${id}`);
    return response.data;
};

export const createBook = async (data) => {
    const response = await api.post("/books", data);
    return response.data;
};

export const updateBook = async (id, data) => {
    const response = await api.put(`/books/${id}`, data);
    return response.data;
};

export const updateProgress = async (id, data) => {
    const response = await api.patch(`/books/${id}/progress`, data);
    return response.data;
};

export const deleteBook = async (id) => {
    const response = await api.delete(`/books/${id}`);
    return response.data;
};
